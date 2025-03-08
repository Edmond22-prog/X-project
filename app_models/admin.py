from django.contrib import admin
from django.utils.html import format_html

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
    list_display = ("user", "verification_photo", "created_at", "updated_at", "approved")
    
    actions = ["approve_verification", "reject_verification"]
    
    def approved(self, obj) -> bool:
        "Returns a check mark if the user is verified, otherwise a cross mark"
        if obj.user.is_verified:
            return format_html('<span style="color: green;">✔️</span>')
        else:
            return format_html('<span style="color: red;">❌</span>')
    
    @admin.action(description="Approve selected verifications")
    def approve_verification(self, request, queryset):
        for verification in queryset:
            verification.user.is_verified = True
            verification.user.is_active = True
            verification.user.save()
    
    @admin.action(description="Reject selected verifications")
    def reject_verification(self, request, queryset):
        for verification in queryset:
            verification.user.is_verified = False
            verification.user.is_active = False
            verification.user.save()


admin.site.site_header = "X-Project Administration Site"
admin.site.site_title = "X-Project Admin"

admin.site.register(ServiceProposalSkill)
admin.site.register(ServiceProposalCategory)
admin.site.register(UserSocials)
admin.site.register(ServiceRequestSocials)
