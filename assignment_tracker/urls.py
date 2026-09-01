from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from tracker import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("student/assignment/<int:assignment_id>/", views.assignment_detail, name="assignment_detail"),
    path("student/assignment/<int:assignment_id>/submit/", views.submit_assignment, name="submit_assignment"),

    path("teacher/dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("teacher/assignment/create/", views.create_assignment, name="create_assignment"),
    path("teacher/assignment/<int:assignment_id>/", views.teacher_assignment_detail, name="teacher_assignment_detail"),
    path("teacher/submission/<int:submission_id>/grade/", views.grade_submission, name="grade_submission"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
