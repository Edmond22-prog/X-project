from django.contrib import admin

from app_models.models import (
    ServiceRequest,
    ServiceRequestSocials,
    ServiceProposal,
    ServiceProposalSkill,
    ServiceProposalCategory,
    User,
    UserSocials,
    UserVerification,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("uuid", "get_full_name", "email", "phone", "is_verified")
    list_filter = ("district", "city", "is_verified")
    search_fields = ("first_name", "last_name", "email", "phone")


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status", "duration", "fixed_amount")
    list_filter = ("status", "city", "district", "user")


@admin.register(ServiceProposal)
class ServiceProposalAdmin(admin.ModelAdmin):
    list_display = ("uuid", "title", "hourly_rate", "user")
    list_filter = ("user", "category")
    search_fields = ("description",)


@admin.register(UserVerification)
class UserVerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "verification_photo", "created_at", "updated_at")


admin.site.site_header = "X-Project Administration Site"
admin.site.site_title = "X-Project Admin"

admin.site.register(ServiceProposalSkill)
admin.site.register(ServiceProposalCategory)
admin.site.register(UserSocials)
admin.site.register(ServiceRequestSocials)
