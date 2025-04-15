import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_models.models import (
    ServiceCategory,
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
    ServiceCategorySerializer,
    ServiceProposalSerializer,
    ServiceProposalSkillSerializer,
    ServiceRequestSerializer,
    UpdateServiceProposalSerializer,
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
            logging.exception(serializer.errors)
            return Response(
                {"error": "Error while trying to create service request"},
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

        # Check if the category exists
        if validated_data.get("category_uuid", None):
            try:
                existing_category = ServiceCategory.objects.get(
                    uuid=validated_data["category_uuid"],
                )
            except ServiceCategory.DoesNotExist:
                return Response(
                    {"error": "Category not found !"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        else:
            existing_category, _ = ServiceCategory.objects.get_or_create(
                **{
                    "fr_name": "Autres",
                    "fr_description": "Autres services non classés ailleurs",
                    "en_name": "Others",
                    "en_description": "Other unclassified services",
                }
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
            category=existing_category,
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
        operation_description="""
        # Endpoint for getting paginated services requests.
        
        ## To retrieve paginated services requests, you can use the following query parameters:
        - **page**: The page number to retrieve (default is 1).
        - **size**: The number of items per page (default is 10).
        **Exemple**: /services/requests/list/?page=2&size=5
        
        ## To apply filters, you can use the following query parameters:
        - **town**: The town of the service request.
        - **category_uuid**: The uuid of the service category.
        - **min_amount**: The minimum fixed amount of the service request.
        - **max_amount**: The maximum fixed amount of the service request.
        **Exemple**: /services/requests/list/?town=Douala&category_uuid=32fcc008b5ef4d84b0390bdcca229b9a&min_amount=1000&max_amount=5000
        
        ## If you want to sort the results, you can use the following query parameter:
        - **sort**: The sorting order (default is "desc"). Use "asc" for ascending order.
        **Exemple**: /services/requests/list/?sort=asc
        """,
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
        
        filters = {}
        if "town" in request.GET and request.GET["town"].strip() != "":
            filters["town"] = request.GET["town"]
        
        if "category_uuid" in request.GET and request.GET["category_uuid"].strip() != "":
            filters["category__uuid"] = request.GET["category_uuid"]
        
        if "min_amount" in request.GET and request.GET["min_amount"].strip() != "":
            filters["fixed_amount__gte"] = request.GET["min_amount"]
        
        if "max_amount" in request.GET and request.GET["max_amount"].strip() != "":
            filters["fixed_amount__lte"] = request.GET["max_amount"]

        sort = "desc"
        if "sort" in request.GET and request.GET["sort"].strip() != "":
            sort = request.GET["sort"]

        start = (page - 1) * size
        end = page * size

        # Retrieve services requests
        services_requests = ServiceRequest.objects.filter(
            **filters, status=ServiceRequestStatus.ACTIVE,
        ).order_by("-updated_at" if sort == "desc" else "updated_at")
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
        responses={200: ServiceCategorySerializer(many=True)},
        tags=["Services"],
        security=[],
    )
    def get(self, request):
        categories = ServiceCategory.objects.all()
        return Response(
            ServiceCategorySerializer(categories, many=True).data,
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
            logging.exception(serializer.errors)
            return Response(
                {"error": "Error while trying to create service proposal"},
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
        for skill_name in validated_data.get("skills", []):
            formatted_skill_name = skill_name.strip().lower()
            skill, _ = ServiceProposalSkill.objects.get_or_create(
                name=formatted_skill_name
            )
            skills.append(skill)

        # Check if the category exists
        if validated_data.get("category_uuid", None):
            try:
                existing_category = ServiceCategory.objects.get(
                    uuid=validated_data["category_uuid"],
                )
            except ServiceCategory.DoesNotExist:
                return Response(
                    {"error": "Category not found !"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        else:
            existing_category, _ = ServiceCategory.objects.get_or_create(
                **{
                    "fr_name": "Autres",
                    "fr_description": "Autres services non classés ailleurs",
                    "en_name": "Others",
                    "en_description": "Other unclassified services",
                }
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
        operation_description="""
        # Endpoint for getting paginated service proposals with optional filters.
        
        ## To retrieve paginated services proposals, you can use the following query parameters:
        - **page**: The page number to retrieve (default is 1).
        - **size**: The number of items per page (default is 10).
        **Exemple**: /services/proposals/list/?page=2&size=5
        """,
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
            logging.exception(serializer.errors)
            return Response(
                {"error": "Error while trying to update service request"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(
            ServiceRequestSerializer(service_request).data, status=status.HTTP_200_OK
        )


class UpdateServiceProposalAPIView(APIView):
    serializer_class = UpdateServiceProposalSerializer

    @swagger_auto_schema(
        operation_id="update_service_proposal",
        operation_description="Endpoint for updating a service proposal",
        operation_summary="Update a service proposal",
        request_body=UpdateServiceProposalSerializer,
        responses={200: ServiceProposalSerializer()},
        tags=["Services"],
        security=[{"Bearer": []}],
    )
    @check_is_connected
    def put(self, request, proposal_uuid: str, *args, **kwargs):
        connected_user = get_connected_user(request)
        if not connected_user:
            return Response(
                {"error": "Connected user not found !"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            service_proposal = ServiceProposal.objects.get(
                uuid=proposal_uuid, user=connected_user
            )
        except ServiceProposal.DoesNotExist:
            return Response(
                {
                    "error": "Service proposal not found or you do not have permission to edit this proposal!"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(
            service_proposal, data=request.data, partial=True
        )
        if not serializer.is_valid():
            logging.exception(serializer.errors)
            return Response(
                {"error": "Error while trying to update service proposal"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_data = serializer.validated_data
        if "category_uuid" in validated_data:
            try:
                existing_category = ServiceCategory.objects.get(
                    uuid=validated_data["category_uuid"],
                )
            except ServiceCategory.DoesNotExist:
                return Response(
                    {"error": "Category not found !"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            service_proposal.category = existing_category

        # Create or get skills
        if "skills" in validated_data:
            skills = []
            for skill_name in validated_data["skills"]:
                formatted_skill_name = skill_name.strip().lower()
                skill, created = ServiceProposalSkill.objects.get_or_create(
                    name=formatted_skill_name
                )
                skills.append(skill)

            service_proposal.skills.set(skills)

        serializer.save()
        return Response(
            ServiceProposalSerializer(service_proposal).data, status=status.HTTP_200_OK
        )
