from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_models.models import (
    ServiceProposalCategory,
    ServiceProposalSkill,
    ServiceRequest,
    ServiceRequestSocials,
)
from app_models.models.constants import ServiceRequestStatus
from app_models.models.service import ServiceProposal
from middlewares.auth_middleware import check_is_connected
from serializers.service_serializer import (
    CreateServiceProposalSerializer,
    CreateServiceRequestSerializer,
    ServiceProposalCategorySerializer,
    ServiceProposalSerializer,
    ServiceProposalSkillSerializer,
    ServiceRequestSerializer,
    UpdateServiceRequestSerializer,
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


class PaginatedServiceRequestsAPIView(APIView):
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


class GetServiceRequestAPIView(APIView):
    @swagger_auto_schema(
        operation_id="get_service_request",
        operation_description="Endpoint for getting a service request by its uuid",
        operation_summary="Get a service request by its uuid",
        responses={200: ServiceRequestSerializer()},
        tags=["Services"],
        security=[],
    )
    def get(self, request, service_request_uuid: str):
        try:
            service_request = ServiceRequest.objects.get(uuid=service_request_uuid)
        except ServiceRequest.DoesNotExist:
            return Response(
                {"error": "Service request not found !"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            ServiceRequestSerializer(service_request).data, status=status.HTTP_200_OK
        )


class RetrieveSkillsAPIView(APIView):
    @swagger_auto_schema(
        operation_id="retrieve_skills",
        operation_description="Endpoint for retrieving all service proposal skills",
        operation_summary="Retrieve all service proposal skills",
        responses={200: ServiceProposalSkillSerializer(many=True)},
        tags=["Services"],
        security=[],
    )
    def get(self, request):
        skills = ServiceProposalSkill.objects.all()
        return Response(
            ServiceProposalSkillSerializer(skills, many=True).data,
            status=status.HTTP_200_OK,
        )


class RetrieveCategoriesAPIView(APIView):
    @swagger_auto_schema(
        operation_id="retrieve_categories",
        operation_description="Endpoint for retrieving all service proposal categories",
        operation_summary="Retrieve all service proposal categories",
        responses={200: ServiceProposalCategorySerializer(many=True)},
        tags=["Services"],
        security=[],
    )
    def get(self, request):
        categories = ServiceProposalCategory.objects.all()
        return Response(
            ServiceProposalCategorySerializer(categories, many=True).data,
            status=status.HTTP_200_OK,
        )


class CreateServiceProposalAPIView(APIView):
    serializer_class = CreateServiceProposalSerializer

    @swagger_auto_schema(
        operation_id="create_service_proposal",
        operation_description="Endpoint for service proposal creation",
        operation_summary="Create a service proposal",
        request_body=CreateServiceProposalSerializer,
        responses={201: ServiceProposalSerializer()},
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

        # Create or get skills
        skills = []
        for skill_name in validated_data["skills"]:
            formatted_skill_name = skill_name.strip().lower()
            skill, created = ServiceProposalSkill.objects.get_or_create(
                name=formatted_skill_name
            )
            skills.append(skill)

        # Check if the category exists
        try:
            existing_category = ServiceProposalCategory.objects.get(
                uuid=validated_data["category_uuid"],
            )
        except ServiceProposalCategory.DoesNotExist:
            return Response(
                {"error": "Category not found !"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Create the service proposal
        service_proposal = ServiceProposal.objects.create(
            user=connected_user,
            title=validated_data["title"],
            description=validated_data["description"],
            hourly_rate=validated_data["hourly_rate"],
            category=existing_category,
        )

        # Add skills to the service proposal
        service_proposal.skills.set(skills)

        return Response(
            ServiceProposalSerializer(service_proposal).data,
            status=status.HTTP_201_CREATED,
        )


class PaginatedServiceProposalsAPIView(APIView):
    @swagger_auto_schema(
        operation_id="paginated_service_proposals",
        operation_description="Endpoint for getting paginated service proposals with optional filters",
        operation_summary="Get paginated service proposals",
        responses={200: ServiceProposalSerializer(many=True)},
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

        category_uuid = None
        if "category_uuid" in request.GET and request.GET["category_uuid"].strip() != "":
            category_uuid = request.GET["category_uuid"]

        filters = {}
        if category_uuid:
            filters["category__uuid"] = category_uuid

        # Retrieve service proposals with optional filters
        service_proposals = ServiceProposal.objects.filter(**filters)

        total = service_proposals.count()
        start = (page - 1) * size
        end = page * size

        output = {
            "page": page,
            "size": size,
            "total": total,
            "more": end < total,
            "proposals": ServiceProposalSerializer(
                service_proposals[start:end], many=True
            ).data,
        }

        return Response(output, status=status.HTTP_200_OK)


class UpdateServiceRequestAPIView(APIView):
    serializer_class = UpdateServiceRequestSerializer

    @swagger_auto_schema(
        operation_id="update_service_request",
        operation_description="Endpoint for updating a service request",
        operation_summary="Update a service request",
        request_body=UpdateServiceRequestSerializer,
        responses={200: ServiceRequestSerializer()},
        tags=["Services"],
        security=[{"Bearer": []}],
    )
    @check_is_connected
    def put(self, request, request_uuid: str, *args, **kwargs):
        connected_user = get_connected_user(request)
        if not connected_user:
            return Response(
                {"error": "Connected user not found !"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            service_request = ServiceRequest.objects.get(
                uuid=request_uuid, user=connected_user
            )
        except ServiceRequest.DoesNotExist:
            return Response(
                {
                    "error": "Service request not found or you do not have permission to edit this request!"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(
            service_request, data=request.data, partial=True
        )
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors["non_field_errors"][0]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(
            ServiceRequestSerializer(service_request).data, status=status.HTTP_200_OK
        )
