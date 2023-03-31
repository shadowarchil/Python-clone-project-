from django.urls import path
from users.views import CustomLoginView, CustomLogoutView, UserSignUpView, UserProfileView,edit_profile
from users.models import Profile
from django.conf.urls.static import static
from django.conf import settings

app_name = 'users'

urlpatterns = [
    path('sign-in/', CustomLoginView.as_view(), name='sign-in'),
    path('sign-out/', CustomLogoutView.as_view(), name='sign-out'),
    path('sign-up/', UserSignUpView.as_view(), name='sign-up'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='profile'),
    path('profile/<str:username>/edit/', edit_profile, name='edit_profile'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

