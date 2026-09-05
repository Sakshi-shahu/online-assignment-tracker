from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import AssignmentForm, GradeForm, RegisterForm, SubmissionForm
from .models import Assignment, Profile, Submission


def get_role(user):
    profile = getattr(user, "profile", None)
    return profile.role if profile else None


def home(request):
    if request.user.is_authenticated:
        role = get_role(request.user)
        return redirect("teacher_dashboard" if role == "TEACHER" else "student_dashboard")
    return render(request, "home.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
        )
        Profile.objects.create(
            user=user,
            role=form.cleaned_data["role"],
            subject=form.cleaned_data.get("subject", "") if form.cleaned_data["role"] == "TEACHER" else "",
            course=form.cleaned_data.get("course", "") if form.cleaned_data["role"] == "STUDENT" else "",
            batch=form.cleaned_data.get("batch", "") if form.cleaned_data["role"] == "STUDENT" else "",
        )
        messages.success(request, "Registration successful. Please login.")
        return redirect("login")
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def student_dashboard(request):
    if get_role(request.user) != "STUDENT":
        return redirect("home")

    profile = request.user.profile
    assignments = Assignment.objects.filter(
        target_course=profile.course,
        target_batch=profile.batch,
    ).select_related("teacher")
    submissions = {
        s.assignment_id: s for s in Submission.objects.filter(
            student=request.user,
            assignment__in=assignments,
        )
    }
    return render(request, "student_dashboard.html", {
        "assignments": assignments,
        "submissions": submissions,
        "profile": profile,
    })


@login_required
def assignment_detail(request, assignment_id):
    if get_role(request.user) != "STUDENT":
        return redirect("home")
    profile = request.user.profile
    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        target_course=profile.course,
        target_batch=profile.batch,
    )
    submission = Submission.objects.filter(assignment=assignment, student=request.user).first()
    return render(request, "assignment_detail.html", {
        "assignment": assignment,
        "submission": submission,
        "form": SubmissionForm(instance=submission),
    })


@login_required
def submit_assignment(request, assignment_id):
    if get_role(request.user) != "STUDENT":
        return redirect("home")

    profile = request.user.profile
    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        target_course=profile.course,
        target_batch=profile.batch,
    )
    existing = Submission.objects.filter(assignment=assignment, student=request.user).first()

    if timezone.localdate() > assignment.due_date and not existing:
        messages.error(request, "The submission deadline has passed.")
        return redirect("assignment_detail", assignment_id=assignment.id)

    form = SubmissionForm(request.POST or None, request.FILES or None, instance=existing)
    if request.method == "POST" and form.is_valid():
        if not request.FILES.get("file"):
            form.add_error("file", "Please select a file to submit.")
        else:
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.status = "PENDING"
            submission.submitted_at = timezone.now()
            submission.marks = None
            submission.feedback = ""
            submission.save()
            messages.success(request, "Assignment submitted successfully.")
            return redirect("student_dashboard")

    return render(request, "assignment_detail.html", {
        "assignment": assignment,
        "submission": existing,
        "form": form,
    })


@login_required
def teacher_dashboard(request):
    if get_role(request.user) != "TEACHER":
        return redirect("home")

    assignments = Assignment.objects.filter(teacher=request.user)
    total_submissions = Submission.objects.filter(assignment__teacher=request.user, file__isnull=False).count()
    graded = Submission.objects.filter(assignment__teacher=request.user, status="GRADED").count()
    profile = request.user.profile

    assignment_stats = []
    for assignment in assignments:
        assigned_count = Submission.objects.filter(assignment=assignment).count()
        submitted_count = Submission.objects.filter(assignment=assignment, submitted_at__isnull=False).count()
        assignment_stats.append((assignment, assigned_count, submitted_count))

    return render(request, "teacher_dashboard.html", {
        "assignments": assignments,
        "total_submissions": total_submissions,
        "graded": graded,
        "profile": profile,
        "assignment_stats": assignment_stats,
    })


@login_required
@transaction.atomic
def create_assignment(request):
    if get_role(request.user) != "TEACHER":
        return redirect("home")

    form = AssignmentForm(request.POST or None)
    teacher_profile = request.user.profile

    if request.method == "POST" and form.is_valid():
        assignment = form.save(commit=False)
        assignment.teacher = request.user
        assignment.subject = teacher_profile.subject
        assignment.save()

        # Automatically create one pending submission record for every student
        # belonging to the selected course + batch.
        matching_students = User.objects.filter(
            profile__role="STUDENT",
            profile__course=assignment.target_course,
            profile__batch=assignment.target_batch,
        )
        Submission.objects.bulk_create([
            Submission(assignment=assignment, student=student, status="PENDING")
            for student in matching_students
        ])

        assigned_count = matching_students.count()
        messages.success(
            request,
            f"Assignment created and assigned to {assigned_count} matching student(s)."
        )
        return redirect("teacher_dashboard")

    return render(request, "create_assignment.html", {
        "form": form,
        "teacher_profile": teacher_profile,
    })


@login_required
def teacher_assignment_detail(request, assignment_id):
    if get_role(request.user) != "TEACHER":
        return redirect("home")

    assignment = get_object_or_404(Assignment, id=assignment_id, teacher=request.user)
    submissions = assignment.submissions.select_related("student", "student__profile").all()
    return render(request, "teacher_assignment_detail.html", {
        "assignment": assignment,
        "submissions": submissions,
    })


@login_required
def grade_submission(request, submission_id):
    if get_role(request.user) != "TEACHER":
        return redirect("home")

    submission = get_object_or_404(
        Submission,
        id=submission_id,
        assignment__teacher=request.user,
    )
    if not submission.file:
        messages.error(request, "This student has not submitted a file yet.")
        return redirect("teacher_assignment_detail", assignment_id=submission.assignment_id)

    form = GradeForm(request.POST or None, instance=submission)

    if request.method == "POST" and form.is_valid():
        graded = form.save(commit=False)
        graded.status = "GRADED"
        graded.save()
        messages.success(request, "Submission graded successfully.")
        return redirect("teacher_assignment_detail", assignment_id=submission.assignment_id)

    return render(request, "grade_submission.html", {
        "submission": submission,
        "form": form,
    })
