
from django.urls import path,resolve
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy




class MyHackedView(auth_views.PasswordResetView):
    success_url = reverse_lazy("news_website:password_reset_done")


app_name = "news_website"
urlpatterns = [
    path('news_type/<slug:slug>/', views.detailed_news_type, name='detailed_news_type'),
    path('', views.all_news_type, name='all_news_type'),
    path('<int:y>/<int:m>/<int:d>/<slug:slug>/', views.detailed_news,
         name="detailed_news"),
    path('<int:news_id>/share/', views.share_post, name="share_post"),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password_reset/', MyHackedView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy("news_website:password_reset_complete"),
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('password-change/', auth_views.PasswordChangeView.as_view(
        success_url=reverse_lazy("news_website:password_change_done"),
    ), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)