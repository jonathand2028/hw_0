"""
views.py — HTTP request handlers for AttendanceChimp.

Each view corresponds to one URL endpoint.  Views receive an HTTP request,
interact with the database via models.py, and return an HTTP response.
"""

from django.shortcuts import render, redirect
from django.http import (HttpResponse, HttpResponseForbidden,
                         HttpResponseBadRequest, JsonResponse)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import datetime
import zoneinfo
import json
import io

# from .models import (InstructorProfile, StudentProfile, Course, Enrollment,
#                      Lecture, QRCodeUpload, is_instructor, is_student,
#                      getUploadsForCourse)
from .models import StudentProfile, InstructorProfile

CDT = zoneinfo.ZoneInfo("America/Chicago")


# ---------------------------------------------------------------------------
# HW2  — index, time, sum
# ---------------------------------------------------------------------------

def index(request):
    """Render the home page (index.html)."""
    current_time = datetime.now(CDT).strftime("%H:%M")
    context = {"time": current_time, "user": request.user}
    return render(request, 'app/index.html', context)

def time_view(request):
    chicago_time = datetime.now(CDT)
    formatted_chicago_time = chicago_time.strftime("%H:%M")
    return HttpResponse(formatted_chicago_time)

def sum_view(request):
    n1 = request.GET.get("n1")
    n2 = request.GET.get("n2")
    float_n1 = float(n1)
    float_n2 = float(n2)
    total = round(float_n1 + float_n2, 10)
    return HttpResponse(f"<p>{total}</p>")


# ---------------------------------------------------------------------------
# HW4  — user creation
# ---------------------------------------------------------------------------
def new(request):
    """Show the sign-up form. Only GET is allowed."""
    if request.method != "GET":
        return HttpResponseBadRequest("Only GET allowed")
    return render(request, 'app/new.html')

@csrf_exempt
def createUser(request):
    """Create a new user and student/instructor profile from POST data."""
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST allowed")

    user_name = request.POST.get("user_name")
    email = request.POST.get("email")
    password = request.POST.get("password")
    is_student = request.POST.get("is_student")

    if User.objects.filter(email=email).exists():
        return HttpResponseBadRequest("Email already in use")

    if User.objects.filter(username=user_name).exists():
        return HttpResponseBadRequest("Username already in use")

    user = User.objects.create_user(username=user_name, email=email, password=password)

    if is_student == "1":
        StudentProfile.objects.create(user=user)
    else:
        InstructorProfile.objects.create(user=user)

    login(request, user)
    return HttpResponse("User created", status=200)
# ---------------------------------------------------------------------------
# HW5  — courses, lectures, QR uploads, dump
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# HW6  — getUploads
# ---------------------------------------------------------------------------



