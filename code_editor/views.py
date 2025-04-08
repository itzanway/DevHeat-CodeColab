import os
import json
import random
import string
import requests

from dotenv import load_dotenv
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import CodeRoom, Profile
from .utils import *

# Load environment variables
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# ----------------- Home & Auth Views -----------------

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "code_editor/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user.profile

        profiles = Profile.objects.exclude(interests="").exclude(user=self.request.user)
        
        recommended_rooms = []
        if profiles:
            similar_profiles = find_similar_profiles(user_profile, list(profiles), max_clusters=5)
            
            recommended_rooms = CodeRoom.objects.filter(creator__profile__in=similar_profiles).distinct()[:5]

        context['recommended_rooms'] = recommended_rooms
        return context

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = UserCreationForm()
        for field in form.fields.values():
            field.widget.attrs['class'] = 'form-control'
        return render(request, 'authentication/register.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = UserCreationForm(request.POST)
        for field in form.fields.values():
            field.widget.attrs['class'] = 'form-control'
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
        return render(request, 'authentication/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    success_url = reverse_lazy('home')
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        messages.success(self.request, 'Login successful!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You have been logged out.')
        return super().dispatch(request, *args, **kwargs)

# ----------------- Room Collaboration Views -----------------

@method_decorator(login_required(login_url=reverse_lazy('login')), name='dispatch')
class CreateRoomView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        room_code = self.generate_room_code()
        room = CodeRoom.objects.create(name=room_code, creator=self.request.user)
        return reverse_lazy('code_room', kwargs={'room_name': room_code})

    @staticmethod
    def generate_room_code(length=6):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@method_decorator(login_required(login_url=reverse_lazy('login')), name='dispatch')
class JoinRoomView(View):
    def get(self, request):
        return render(request, 'code_editor/join_room.html')

    def post(self, request):
        room_code = request.POST.get('room_code')
        try:
            room = CodeRoom.objects.get(name=room_code)
            return redirect('code_room', room_name=room.name)
        except CodeRoom.DoesNotExist:
            return render(request, 'code_editor/join_room.html', {'error': 'Room not found'})

@method_decorator(login_required(login_url=reverse_lazy('login')), name='dispatch')
class CodeRoomView(TemplateView):
    template_name = 'code_editor/room.html'

    def get_context_data(self, **kwargs):
        room_name = kwargs['room_name']
        room = get_object_or_404(CodeRoom, name=room_name)
        context = super().get_context_data(**kwargs)
        context['room_name'] = room_name
        context['languages'] = ['python', 'java', 'cpp']
        return context

# ----------------- Interests -----------------

INTERESTS_CHOICES = {
    "Programming Languages": [
        "Python", "C++", "C", "Java", "JavaScript", "TypeScript", "Go", "Rust", "Ruby", "Swift", "Kotlin", "PHP", "R", "Scala"
    ],
    "Frameworks & Libraries": [
        "Django", "Flask", "FastAPI", "React", "Angular", "Vue", "Next.js", "Svelte", "Spring Boot", 
        "Express.js", "NestJS", "Bootstrap", "Tailwind CSS", "jQuery"
    ],
    "Tech Fields": [
        "Machine Learning", "Deep Learning", "Data Science", "Web Development", "App Development",
        "Blockchain", "Cybersecurity", "DevOps", "Cloud Computing", "Game Development", 
        "Embedded Systems", "AR/VR", "IoT", "AI/ML Ops"
    ],
    "Databases & Tools": [
        "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Firebase", "Docker", "Kubernetes", 
        "Git", "GitHub", "CI/CD", "AWS", "Azure", "GCP"
    ]
}

@login_required
def update_interests(request):
    profile = request.user.profile
    if request.method == "POST":
        interests = request.POST.get("interests", "")
        profile.interests = interests
        profile.save()
        return redirect("home")
    return render(request, "interests.html", {"interests_choices": INTERESTS_CHOICES})

# ----------------- Hugging Face AI Code Assistant -----------------

@method_decorator(csrf_exempt, name='dispatch')
class HuggingFaceAutocompleteView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Ensure request body exists
            if not request.body:
                return JsonResponse({"error": "Empty request body"}, status=400)

            # Attempt to parse JSON
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)

            # Extract code and language
            code = data.get("code", "").strip()
            language = data.get("language", "code").strip()

            if not code:
                return JsonResponse({"error": "Code field is required"}, status=400)

            # Construct the prompt using language
            prompt = f"Complete the following {language} code:\n{code}"

            headers = {
                "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 64,
                    "return_full_text": False
                }
            }

            response = requests.post(
                "https://api-inference.huggingface.co/models/Salesforce/codegen-350M-mono",
                headers=headers,
                json=payload
            )

            try:
                result = response.json()
            except ValueError:
                return JsonResponse({"error": "Invalid response from Hugging Face API"}, status=500)

            # Handle response errors
            if response.status_code != 200:
                return JsonResponse({
                    "error": "Hugging Face API returned an error",
                    "status_code": response.status_code,
                    "details": result
                }, status=500)

            # Extract generated text
            if isinstance(result, list) and result:
                generated_text = result[0].get("generated_text", "")
                return JsonResponse({"suggestion": generated_text}, status=200)
            else:
                return JsonResponse({"error": "Unexpected response format", "details": result}, status=500)

        except Exception as e:
            return JsonResponse({"error": "Internal server error", "details": str(e)}, status=500)
