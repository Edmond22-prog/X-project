from rest_framework import serializers

from app_models.models import (
    ServiceProposal,
    ServiceProposalCategory,
    ServiceProposalSkill,
    ServiceRequest,
)


class ServiceRequestSerializer(serializers.ModelSerializer):
    socials = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceRequest
        fields = "__all__"
    
    def get_socials(self, service_request):
        contacts = service_request.contacts
        return {
            "email": contacts.email,
            "phone": contacts.phone,
            "whatsapp": contacts.whatsapp,
            "telegram": contacts.telegram,
        }
    
    def get_user(self, service_request):
        user = service_request.user
        return {
            "uuid": user.uuid,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_verified": user.is_verified,
        }


class ServiceProposalSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceProposal
        fields = "__all__"
    
    def get_skills(self, service_prop):
        return service_prop.skills.values_list("name", flat=True)
    
    def get_category(self, service_prop):
        if service_prop.category:
            category = service_prop.category
            return f"{category.fr_name} | {category.en_name}"
        
        return None
    
    def get_user(self, service_prop):
        user = service_prop.user
        return {
            "uuid": user.uuid,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_verified": user.is_verified,
        }


class CreateServiceRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(max_length=20, required=False)
    whatsapp = serializers.CharField(max_length=20, required=False)
    telegram = serializers.CharField(max_length=20, required=False)

    class Meta:
        model = ServiceRequest
        fields = (
            "title",
            "description",
            "city",
            "district",
            "duration",
            "fixed_amount",
            "email",
            "phone",
            "whatsapp",
            "telegram",
        )

    def validate(self, attrs):
        if not any(
            [
                attrs.get("email", None),
                attrs.get("phone", None),
                attrs.get("whatsapp", None),
                attrs.get("telegram", None),
            ]
        ):
            raise serializers.ValidationError(
                "At least one contact information is required."
            )

        return attrs


class ServiceProposalSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProposalSkill
        fields = "__all__"


class ServiceProposalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProposalCategory
        fields = "__all__"


class CreateServiceProposalSerializer(serializers.ModelSerializer):
    skills = serializers.ListField(child=serializers.CharField())
    category_uuid = serializers.CharField()

    class Meta:
        model = ServiceProposal
        fields = (
            "title",
            "description",
            "hourly_rate",
            "skills",
            "category_uuid",
        )

    def validate(self, attrs):
        if not attrs.get("skills", None):
            raise serializers.ValidationError("Skills are required.")

        if not attrs.get("category_uuid", None):
            raise serializers.ValidationError("Category is required.")

        return attrs
