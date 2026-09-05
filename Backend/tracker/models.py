from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    ROLE_CHOICES = (
        ("STUDENT", "Student"),
        ("TEACHER", "Teacher"),
    )

    SUBJECT_CHOICES = (
        ("JAVA", "Java"),
        ("PYTHON", "Python"),
        ("JAVASCRIPT", "JavaScript"),
        ("WEB_DEVELOPMENT", "Web Development"),
        ("DATABASE", "Database / SQL"),
        ("DATA_SCIENCE", "Data Science"),
        ("MACHINE_LEARNING", "Machine Learning"),
        ("SOFTWARE_ENGINEERING", "Software Engineering"),
    )

    COURSE_CHOICES = (
        ("BSC_IT", "B.Sc. IT"),
        ("BCA", "BCA"),
        ("BSC_CS", "B.Sc. Computer Science"),
        ("BTECH_CSE", "B.Tech CSE"),
        ("BCOM", "B.Com"),
        ("MCA", "MCA"),
    )

    BATCH_CHOICES = (
        ("2023-2026", "2023 - 2026"),
        ("2024-2027", "2024 - 2027"),
        ("2025-2028", "2025 - 2028"),
        ("2026-2029", "2026 - 2029"),
        ("2027-2030", "2027 - 2030"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    subject = models.CharField(max_length=40, choices=SUBJECT_CHOICES, blank=True)
    course = models.CharField(max_length=30, choices=COURSE_CHOICES, blank=True)
    batch = models.CharField(max_length=20, choices=BATCH_CHOICES, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Assignment(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.CharField(max_length=40, choices=Profile.SUBJECT_CHOICES)
    target_course = models.CharField(max_length=30, choices=Profile.COURSE_CHOICES)
    target_batch = models.CharField(max_length=20, choices=Profile.BATCH_CHOICES)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def target_course_display(self):
        return dict(Profile.COURSE_CHOICES).get(self.target_course, self.target_course)

    @property
    def target_batch_display(self):
        return dict(Profile.BATCH_CHOICES).get(self.target_batch, self.target_batch)

    @property
    def subject_display(self):
        return dict(Profile.SUBJECT_CHOICES).get(self.subject, self.subject)


class Submission(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("GRADED", "Graded"),
    )
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    file = models.FileField(upload_to="submissions/", blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    marks = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["assignment", "student"],
                name="unique_assignment_student_submission"
            )
        ]
        ordering = ["student__username"]

    def __str__(self):
        return f"{self.assignment.title} - {self.student.username}"
