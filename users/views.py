from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from users.forms import UserCreateForm, ProfileForm
from users.models import Profile
from django.views.generic.detail import DetailView
from users.models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

class UserProfileView(DetailView):
    model = User
    template_name = 'profile.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return User.objects.get(username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = Profile(user=user)
            profile.save()
        context['profile'] = profile
        if self.request.user == user:
            context['form'] = ProfileForm(instance=profile)
        return context

    def post(self, request, username):
        user = self.get_object()
        if request.user != user:
            return HttpResponseForbidden()
        profile = Profile.objects.get(user=user)
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile', username=user.username)
        context = {
            'user': user,
            'profile': profile,
            'form': form
        }
        return render(request, 'profile.html', context)


@login_required
def edit_profile(request, username):
    if request.user.username != username:
        return HttpResponseForbidden()

    profile = Profile.objects.get(user__username=username)

    if request.method == 'POST':
        if request.user != profile.user:
            return HttpResponseForbidden()
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            # Handle avatar upload separately
            avatar = request.FILES.get('avatar')
            if avatar:
                # Use Django's FileSystemStorage to save the file to MEDIA_ROOT
                fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                filename = fs.save(avatar.name, avatar)
                profile.avatar = filename
            profile.save()
            return redirect('users:profile', username=username)
    else:
        form = ProfileForm(instance=profile)
    context = {
        'user': profile.user,
        'profile': profile,
        'form': form
    }
    return render(request, 'users/profile_edit.html', context)

















class CustomLoginView(LoginView):
    template_name = 'auth/sign_in.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('core:home')
    
    


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('core:home')


class UserSignUpView(CreateView):
    template_name = 'auth/sign_up.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('core:home')
