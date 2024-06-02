from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from .models import CustomUser
from core.models import Follow


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


class ProfileView(generic.DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'user_profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()
        is_following = Follow.objects.filter(follower=self.request.user, following=user_profile).exists()
        context['is_following'] = is_following
        return context
