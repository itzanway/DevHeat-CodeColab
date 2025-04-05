from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .models import CodeRoom, Profile
import random
import string
from django.contrib.auth import login
from django.utils.decorators import method_decorator

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

<<<<<<< HEAD
'''
$$$$$$$\                                                                                      $$\            $$\     $$\                     
$$  __$$\                                                                                     $$ |           $$ |    \__|                    
$$ |  $$ | $$$$$$\   $$$$$$$\  $$$$$$\  $$$$$$\$$$$\  $$$$$$\$$$$\   $$$$$$\  $$$$$$$\   $$$$$$$ | $$$$$$\ $$$$$$\   $$\  $$$$$$\  $$$$$$$\  
$$$$$$$  |$$  __$$\ $$  _____|$$  __$$\ $$  _$$  _$$\ $$  _$$  _$$\ $$  __$$\ $$  __$$\ $$  __$$ | \____$$\\_$$  _|  $$ |$$  __$$\ $$  __$$\ 
$$  __$$< $$$$$$$$ |$$ /      $$ /  $$ |$$ / $$ / $$ |$$ / $$ / $$ |$$$$$$$$ |$$ |  $$ |$$ /  $$ | $$$$$$$ | $$ |    $$ |$$ /  $$ |$$ |  $$ |
$$ |  $$ |$$   ____|$$ |      $$ |  $$ |$$ | $$ | $$ |$$ | $$ | $$ |$$   ____|$$ |  $$ |$$ |  $$ |$$  __$$ | $$ |$$\ $$ |$$ |  $$ |$$ |  $$ |
$$ |  $$ |\$$$$$$$\ \$$$$$$$\ \$$$$$$  |$$ | $$ | $$ |$$ | $$ | $$ |\$$$$$$$\ $$ |  $$ |\$$$$$$$ |\$$$$$$$ | \$$$$  |$$ |\$$$$$$  |$$ |  $$ |
\__|  \__| \_______| \_______| \______/ \__| \__| \__|\__| \__| \__| \_______|\__|  \__| \_______| \_______|  \____/ \__| \______/ \__|  \__|                                                                                                                                
'''
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "code_editor/home.html"
=======
def home_view(request):
    return render(request, "code_editor/home.html")
>>>>>>> 04beb3fb4c7a8888cbfa4d6caad876f44bde702b

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user.profile

        profiles = Profile.objects.exclude(interests="").exclude(user=self.request.user)
        interests_list = [profile.interests for profile in profiles]

        recommended_rooms = []
        if interests_list:
            vectorizer = TfidfVectorizer()
            interest_matrix = vectorizer.fit_transform([user_profile.interests] + interests_list)

            num_clusters = min(len(profiles), 5)
            kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
            clusters = kmeans.fit_predict(interest_matrix)

            user_cluster = clusters[0]

            similar_users = [
                profiles[i] for i in range(len(profiles)) if clusters[i + 1] == user_cluster
            ]

            recommended_rooms = CodeRoom.objects.filter(creator__profile__in=similar_users).distinct()[:5]

        context['recommended_rooms'] = recommended_rooms
        return context
'''
 $$$$$$\  $$\   $$\ $$$$$$$$\ $$\   $$\ 
$$  __$$\ $$ |  $$ |\__$$  __|$$ |  $$ |
$$ /  $$ |$$ |  $$ |   $$ |   $$ |  $$ |
$$$$$$$$ |$$ |  $$ |   $$ |   $$$$$$$$ |
$$  __$$ |$$ |  $$ |   $$ |   $$  __$$ |
$$ |  $$ |$$ |  $$ |   $$ |   $$ |  $$ |
$$ |  $$ |\$$$$$$  |   $$ |   $$ |  $$ |
\__|  \__| \______/    \__|   \__|  \__|
'''
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

'''
$$$$$$$\   $$$$$$\   $$$$$$\  $$\      $$\
$$  __$$\ $$  __$$\ $$  __$$\ $$$\    $$$ |
$$ |  $$ |$$ /  $$ |$$ /  $$ |$$$$\  $$$$ |
$$$$$$$  |$$ |  $$ |$$ |  $$ |$$\$$\$$ $$ |
$$  __$$< $$ |  $$ |$$ |  $$ |$$ \$$$  $$ |
$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |\$  /$$ |
$$ |  $$ | $$$$$$  | $$$$$$  |$$ | \_/ $$ |
\__|  \__| \______/  \______/ \__|     \__|
'''
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
        return redirect("home")  # Redirect to homepage or profile page

    return render(request, "interests.html", {"interests_choices": INTERESTS_CHOICES})