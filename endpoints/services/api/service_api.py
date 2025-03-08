from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_models.models import ServiceRequest, ServiceRequestSocials
from app_models.models.constants import ServiceRequestStatus
from middlewares.auth_middleware import check_is_connected
from serializers.service_serializer import (
    CreateServiceRequestSerializer,
    ServiceRequestSerializer,
)
from utils.user_utils import get_connected_user


class CreateServiceRequestAPIView(APIView):
    serializer_class = CreateServiceRequestSerializer

    @swagger_auto_schema(
        operation_id="create_service_request",
        operation_description="Endpoint for service request creation",
        operation_summary="Create a service request",
        request_body=CreateServiceRequestSerializer,
        responses={201: ServiceRequestSerializer()},
        tags=["Services"],
        security=[{"Bearer": []}],
    )
    @check_is_connected
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors["non_field_errors"][0]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_data = serializer.validated_data
        # Get the connected user
        connected_user = get_connected_user(request)
        if not connected_user:
            return Response(
                {"error": "Connected user not found !"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Create the service request
        service_request = ServiceRequest.objects.create(
            user=connected_user,
            title=validated_data["title"],
            description=validated_data["description"],
            city=validated_data["city"],
            district=validated_data["district"],
            duration=validated_data["duration"],
            fixed_amount=validated_data["fixed_amount"],
        )

        # Create the service request socials
        ServiceRequestSocials.objects.create(
            service_request=service_request,
            email=validated_data.get("email", None),
            phone=validated_data.get("phone", None),
            whatsapp=validated_data.get("whatsapp", None),
            telegram=validated_data.get("telegram", None),
        )

        return Response(
            ServiceRequestSerializer(service_request).data,
            status=status.HTTP_201_CREATED,
        )


class PaginatedServicesRequestsAPIView(APIView):
    @swagger_auto_schema(
        operation_id="paginated_services_requests",
        operation_description="Endpoint for getting paginated services requests",
        operation_summary="Get paginated services requests",
        responses={200: ServiceRequestSerializer(many=True)},
        tags=["Services"],
        security=[],
    )
    def get(self, request):
        page = 1
        size = 10
        if "page" in request.GET and request.GET["page"].strip() != "":
            page = int(request.GET["page"])

        if "size" in request.GET and request.GET["size"].strip() != "":
            size = int(request.GET["size"])

        start = (page - 1) * size
        end = page * size

        # Retrieve services requests
        services_requests = ServiceRequest.objects.filter(
            status=ServiceRequestStatus.ACTIVE,
        ).order_by("-updated_at")
        total = services_requests.count()
        if not services_requests:
            output = {
                "page": page,
                "size": size,
                "total": total,
                "more": False,
                "requests": [],
            }
        
        output = {
            "page": page,
            "size": size,
            "total": total,
            "more": end < total,
            "requests": ServiceRequestSerializer(
                services_requests[start:end], many=True
            ).data,
        }

        return Response(output, status=status.HTTP_200_OK)
