from rest_framework import serializers

from app_models.models import ServiceProposal, ServiceRequest


class ServiceRequestSerializer(serializers.ModelSerializer):
    socials = serializers.SerializerMethodField()
    
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


class ServiceProposalSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    
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
