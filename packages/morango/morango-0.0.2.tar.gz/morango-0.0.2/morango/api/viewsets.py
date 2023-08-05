import json
import socket
import uuid

from django.core.exceptions import ValidationError
from django.utils import timezone
from ipware.ip import get_ip
from morango.models import Buffer, DatabaseMaxCounter, RecordMaxCounterBuffer
from morango.utils.sync_utils import _queue_into_buffer, _dequeue_into_store
from rest_framework import viewsets, response, status, mixins, pagination, decorators

from . import serializers, permissions
from .. import models, errors, certificates


class CertificateViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.CertificatePermissions,)
    serializer_class = serializers.CertificateSerializer
    authentication_classes = (permissions.BasicMultiArgumentAuthentication,)

    # @decorators.authentication_classes(permissions.BasicMultiArgumentAuthentication,)
    def create(self, request):

        serialized_cert = serializers.CertificateSerializer(data=request.data)

        if serialized_cert.is_valid():

            # inflate the provided data into an actual in-memory certificate
            certificate = models.Certificate(**serialized_cert.validated_data)

            # add a salt, ID and signature to the certificate
            certificate.salt = uuid.uuid4().hex
            certificate.id = certificate.calculate_uuid()
            certificate.parent.sign_certificate(certificate)

            # ensure that the certificate model fields validate
            try:
                certificate.full_clean()
            except ValidationError as e:
                return response.Response(
                    e,
                    status=status.HTTP_400_BAD_REQUEST
                )

            # verify the certificate (scope is a subset, profiles match, etc)
            try:
                certificate.check_certificate()
            except errors.MorangoCertificateError as e:
                return response.Response(
                    {"error_class": e.__class__.__name__,
                     "error_message": getattr(e, "message", (getattr(e, "args") or ("",))[0])},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # we got this far, and everything looks good, so we can save the certificate
            certificate.save()

            # return a serialized copy of the signed certificate to the client
            return response.Response(
                serializers.CertificateSerializer(certificate).data,
                status=status.HTTP_201_CREATED
            )

        else:
            return response.Response(serialized_cert.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):

        params = self.request.query_params

        base_queryset = models.Certificate.objects

        # filter by profile, if requested
        if "profile" in params:
            base_queryset = base_queryset.filter(profile=params["profile"])

        try:

            # if specified, filter by primary partition, and only include certs the server owns
            if "primary_partition" in params:
                target_cert = base_queryset.get(id=params["primary_partition"])
                return target_cert.get_descendants(include_self=True).exclude(_private_key=None)

            # if specified, return the certificate chain for a certificate owned by the server
            if "ancestors_of" in params:
                target_cert = base_queryset.exclude(_private_key=None).get(id=params["ancestors_of"])
                return target_cert.get_ancestors(include_self=True)

        except models.Certificate.DoesNotExist:
            # if the target_cert can't be found, just return an empty queryset
            return base_queryset.none()

        # if no filters were specified, just return all certificates owned by the server
        return base_queryset.exclude(_private_key=None)


class NonceViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.NoncePermissions,)
    serializer_class = serializers.NonceSerializer

    def create(self, request):
        nonce = models.Nonce.objects.create(ip=get_ip(request))

        return response.Response(
            serializers.NonceSerializer(nonce).data,
            status=status.HTTP_201_CREATED,
        )


class SyncSessionViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.SyncSessionPermissions,)
    serializer_class = serializers.SyncSessionSerializer

    def create(self, request):

        instance_id, _ = models.InstanceIDModel.get_or_create_current_instance()

        # attempt to extract the local IP from the request host
        local_ip = request.META.get('SERVER_NAME', '')
        try:
            local_ip = socket.gethostbyname(local_ip)
        except:
            pass

        # verify and save the certificate chain to our cert store
        try:
            models.Certificate.save_certificate_chain(
                request.data.get("certificate_chain"),
                expected_last_id=request.data.get("client_certificate_id")
            )
        except (AssertionError, errors.MorangoCertificateError):
            return response.Response(
                "Saving certificate chain has failed",
                status=status.HTTP_403_FORBIDDEN
            )

        # attempt to load the requested certificates
        try:
            local_cert = models.Certificate.objects.get(id=request.data.get("server_certificate_id"))
            remote_cert = models.Certificate.objects.get(id=request.data.get("client_certificate_id"))
        except models.Certificate.DoesNotExist:
            return response.Response(
                "Requested certificate does not exist!",
                status=status.HTTP_400_BAD_REQUEST
            )

        if local_cert.profile != remote_cert.profile:
            return response.Response(
                "Certificates must both be associated with the same profile",
                status=status.HTTP_400_BAD_REQUEST
            )

        # check that the nonce/id were properly signed
        message = "{nonce}:{id}".format(nonce=request.data.get('nonce'), id=request.data.get('id'))
        if not remote_cert.verify(message, request.data["signature"]):
            return response.Response(
                "Client certificate failed to verify signature",
                status=status.HTTP_403_FORBIDDEN
            )

        # check that the nonce is valid, and consume it so it can't be used again
        try:
            certificates.Nonce.use_nonce(request.data["nonce"])
        except errors.MorangoNonceError:
            return response.Response(
                "Nonce is not valid",
                status=status.HTTP_403_FORBIDDEN
            )

        # build the data to be used for creation the syncsession
        data = {
            "id": request.data.get("id"),
            "start_timestamp": timezone.now(),
            "last_activity_timestamp": timezone.now(),
            "active": True,
            "is_server": True,
            "local_certificate": local_cert,
            "remote_certificate": remote_cert,
            "profile": local_cert.profile,
            "connection_kind": "network",
            "connection_path": request.data.get("connection_path"),
            "local_ip": local_ip,
            "remote_ip": get_ip(request),
            "local_instance": json.dumps(serializers.InstanceIDSerializer(instance_id).data),
            "remote_instance": request.data.get("instance"),
        }

        syncsession = models.SyncSession(**data)
        syncsession.full_clean()
        syncsession.save()

        resp_data = {
            "signature": local_cert.sign(message),
            "local_instance": data["local_instance"]
        }

        return response.Response(
            # serializers.SyncSessionSerializer(syncsession).data,
            resp_data,
            status=status.HTTP_201_CREATED,
        )

    def perform_destroy(self, syncsession):
        syncsession.active = False
        syncsession.save()

    def get_queryset(self):
        return models.SyncSession.objects.filter(active=True)


class TransferSessionViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.TransferSessionPermissions,)
    serializer_class = serializers.TransferSessionSerializer

    def create(self, request):

        # attempt to load the requested syncsession
        try:
            syncsession = models.SyncSession.objects.filter(active=True).get(id=request.data.get("sync_session_id"))
        except models.SyncSession.DoesNotExist:
            return response.Response(
                "Requested syncsession does not exist or is no longer active!",
                status=status.HTTP_400_BAD_REQUEST
            )

        # a push is to transfer data from client to server; a pull is the inverse
        is_a_push = request.data.get("push")

        # check that the requested filter is within the appropriate certificate scopes
        scope_error_msg = None
        requested_filter = certificates.Filter(request.data.get("filter"))
        remote_scope = syncsession.remote_certificate.get_scope()
        local_scope = syncsession.local_certificate.get_scope()
        if is_a_push:
            if not requested_filter.is_subset_of(remote_scope.write_filter):
                scope_error_msg = "Client certificate scope does not permit pushing for the requested filter."
            if not requested_filter.is_subset_of(local_scope.read_filter):
                scope_error_msg = "Server certificate scope does not permit receiving pushes for the requested filter."
        else:
            if not requested_filter.is_subset_of(remote_scope.read_filter):
                scope_error_msg = "Client certificate scope does not permit pulling for the requested filter."
            if not requested_filter.is_subset_of(local_scope.write_filter):
                scope_error_msg = "Server certificate scope does not permit responding to pulls for the requested filter."
        if scope_error_msg:
            return response.Response(
                scope_error_msg,
                status=status.HTTP_403_FORBIDDEN
            )

        # build the data to be used for creating the transfersession
        data = {
            "id": request.data.get("id"),
            "start_timestamp": timezone.now(),
            "last_activity_timestamp": timezone.now(),
            "active": True,
            "filter": requested_filter,
            "push": is_a_push,
            "records_total": request.data.get("records_total") if is_a_push else None,
            "sync_session": syncsession,
            "local_fsic": '{}',
            "remote_fsic": request.data.get('local_fsic') or '{}',
        }

        transfersession = models.TransferSession(**data)
        transfersession.full_clean()
        transfersession.save()

        if not is_a_push:
            # queue records to get ready for pulling
            _queue_into_buffer(transfersession)

            # update records_total on transfer session object
            records_total = Buffer.objects.filter(transfer_session=transfersession).count()
            transfersession.records_total = records_total

        fsics = DatabaseMaxCounter.calculate_filter_max_counters(requested_filter)
        transfersession.local_fsic = json.dumps(fsics)
        transfersession.save()
        return response.Response(
            serializers.TransferSessionSerializer(transfersession).data,
            status=status.HTTP_201_CREATED,
        )

    def perform_destroy(self, transfersession):
        if transfersession.push:
            # dequeue into store and then delete records
            _dequeue_into_store(transfersession)
        else:
            Buffer.objects.filter(transfer_session=transfersession).delete()
            RecordMaxCounterBuffer.objects.filter(transfer_session=transfersession).delete()
        transfersession.active = False
        transfersession.save()

    def get_queryset(self):
        return models.TransferSession.objects.filter(active=True)


class BufferViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.BufferPermissions,)
    serializer_class = serializers.BufferSerializer
    pagination_class = pagination.LimitOffsetPagination

    def create(self, request):
        data = request.data if isinstance(request.data, list) else [request.data]
        serial_data = serializers.BufferSerializer(data=data, many=True)
        if serial_data.is_valid():

            # ensure the transfer session allows pushes, and is same across records
            transfer_session = serial_data.validated_data[0]["transfer_session"]
            if not transfer_session.push:
                return response.Response(
                    "Specified TransferSession does not allow pushes.",
                    status=status.HTTP_403_FORBIDDEN
                )
            if len(set(rec["transfer_session"] for rec in serial_data.data)) > 1:
                return response.Response(
                    "All pushed records must be associated with the same TransferSession.",
                    status=status.HTTP_403_FORBIDDEN
                )

            serial_data.save()
            transfer_session.records_transferred += len(data)
            transfer_session.save()
            return response.Response(status=status.HTTP_201_CREATED)

        else:

            return response.Response(serial_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):

        session_id = self.request.query_params["transfer_session_id"]

        return models.Buffer.objects.filter(transfer_session_id=session_id)
