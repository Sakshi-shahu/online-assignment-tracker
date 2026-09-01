from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("STUDENT", "Student"), ("TEACHER", "Teacher")], max_length=20)),
                ("subject", models.CharField(blank=True, choices=[("JAVA", "Java"), ("PYTHON", "Python"), ("JAVASCRIPT", "JavaScript"), ("WEB_DEVELOPMENT", "Web Development"), ("DATABASE", "Database / SQL"), ("DATA_SCIENCE", "Data Science"), ("MACHINE_LEARNING", "Machine Learning"), ("SOFTWARE_ENGINEERING", "Software Engineering")], max_length=40)),
                ("course", models.CharField(blank=True, choices=[("BSC_IT", "B.Sc. IT"), ("BCA", "BCA"), ("BSC_CS", "B.Sc. Computer Science"), ("BTECH_CSE", "B.Tech CSE"), ("BCOM", "B.Com"), ("MCA", "MCA")], max_length=30)),
                ("batch", models.CharField(blank=True, choices=[("2023-2026", "2023 - 2026"), ("2024-2027", "2024 - 2027"), ("2025-2028", "2025 - 2028"), ("2026-2029", "2026 - 2029"), ("2027-2030", "2027 - 2030")], max_length=20)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Assignment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("subject", models.CharField(choices=[("JAVA", "Java"), ("PYTHON", "Python"), ("JAVASCRIPT", "JavaScript"), ("WEB_DEVELOPMENT", "Web Development"), ("DATABASE", "Database / SQL"), ("DATA_SCIENCE", "Data Science"), ("MACHINE_LEARNING", "Machine Learning"), ("SOFTWARE_ENGINEERING", "Software Engineering")], max_length=40)),
                ("target_course", models.CharField(choices=[("BSC_IT", "B.Sc. IT"), ("BCA", "BCA"), ("BSC_CS", "B.Sc. Computer Science"), ("BTECH_CSE", "B.Tech CSE"), ("BCOM", "B.Com"), ("MCA", "MCA")], max_length=30)),
                ("target_batch", models.CharField(choices=[("2023-2026", "2023 - 2026"), ("2024-2027", "2024 - 2027"), ("2025-2028", "2025 - 2028"), ("2026-2029", "2026 - 2029"), ("2027-2030", "2027 - 2030")], max_length=20)),
                ("due_date", models.DateField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("teacher", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="assignments", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Submission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(blank=True, upload_to="submissions/")),
                ("submitted_at", models.DateTimeField(blank=True, null=True)),
                ("status", models.CharField(choices=[("PENDING", "Pending"), ("GRADED", "Graded")], default="PENDING", max_length=20)),
                ("marks", models.PositiveIntegerField(blank=True, null=True)),
                ("feedback", models.TextField(blank=True)),
                ("assignment", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="submissions", to="tracker.assignment")),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="submissions", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["student__username"],
            },
        ),
        migrations.AddConstraint(
            model_name="submission",
            constraint=models.UniqueConstraint(fields=("assignment", "student"), name="unique_assignment_student_submission"),
        ),
    ]
