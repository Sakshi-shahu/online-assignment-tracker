# Online Assignment Tracker - Course + Batch Version

Django + SQLite + Bootstrap web application for managing course/batch-wise assignments.

## Features
- Student and Teacher registration/login
- Teacher selects a subject during registration
- Student selects Course + Batch during registration
- Teacher creates an assignment for a selected Course + Batch
- The assignment automatically creates a pending student submission record for every matching student
- Students only see assignments belonging to their Course + Batch
- Students upload assignment files
- Teachers see all students assigned to an assignment
- Teachers grade submitted files and add feedback
- Bootstrap responsive UI
- SQLite database

## Important assignment flow
Example:

Student A -> B.Sc. IT -> 2025-2028
Student B -> B.Sc. IT -> 2025-2028
Student C -> BCA -> 2025-2028

Teacher -> Java

If the teacher creates:
`Java Assignment 1 -> B.Sc. IT -> 2025-2028`

Student A and Student B receive the assignment automatically.
Student C does not receive it.

## Run on Windows

Open terminal in this project folder:

```bash
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Open:
http://127.0.0.1:8000/

## Existing database warning
If you are replacing the old version of this project, the safest option is to use the new ZIP in a fresh folder and run migrations. If you copy the new code over an old project with an existing database, run `python manage.py makemigrations` and `python manage.py migrate` and resolve any data migration prompts if Django reports them.

## File uploads
Uploaded files are stored in `media/submissions/`.
