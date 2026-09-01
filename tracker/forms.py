from django import forms
from django.contrib.auth.models import User
from .models import Assignment, Profile, Submission


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"}))
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        widget=forms.Select(attrs={"class": "form-select", "id": "id_role"}),
    )
    subject = forms.ChoiceField(
        choices=[("", "Select subject")]+list(Profile.SUBJECT_CHOICES),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    course = forms.ChoiceField(
        choices=[("", "Select course")]+list(Profile.COURSE_CHOICES),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    batch = forms.ChoiceField(
        choices=[("", "Select batch")]+list(Profile.BATCH_CHOICES),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get("role")
        if role == "TEACHER" and not cleaned.get("subject"):
            self.add_error("subject", "Please select the teacher subject.")
        if role == "STUDENT":
            if not cleaned.get("course"):
                self.add_error("course", "Please select the student course.")
            if not cleaned.get("batch"):
                self.add_error("batch", "Please select the student batch.")
        return cleaned


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["title", "description", "target_course", "target_batch", "due_date"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Assignment title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Assignment description"}),
            "target_course": forms.Select(attrs={"class": "form-select"}),
            "target_batch": forms.Select(attrs={"class": "form-select"}),
            "due_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["file"]
        widgets = {
            "file": forms.ClearableFileInput(attrs={"class": "form-control", "accept": ".pdf,.doc,.docx,.zip,.txt,.py,.java,.js,.html,.css"})
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["marks", "feedback"]
        widgets = {
            "marks": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 100}),
            "feedback": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Write feedback for the student..."})
        }
