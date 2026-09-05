from django.contrib import admin
from .models import Assignment, Profile, Submission


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "subject", "course", "batch")
    list_filter = ("role", "subject", "course", "batch")
    search_fields = ("user__username", "user__email")


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher", "subject", "target_course", "target_batch", "due_date", "created_at")
    list_filter = ("subject", "target_course", "target_batch")
    search_fields = ("title", "description", "teacher__username")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("assignment", "student", "status", "marks", "submitted_at")
    list_filter = ("status",)
    search_fields = ("assignment__title", "student__username")
