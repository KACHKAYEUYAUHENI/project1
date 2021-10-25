from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from . import models
from . import forms
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag


# Create your views here.
SUBJECT = '{name} Wants to share material "{title}" with you.'
BODY = ("{title} at {uri}. {name} shared material with you. "
        "Please take"  "a look at it.")


def all_news(request):
    news = models.News.objects.all()
    return render(request, "news/all_news.html",
                  {"news": news})





def sport_news(request):
    sport_news = models.News.objects.filter(news_type="Спорт")
    return render(request, "news/sport_news.html",
                  {"sport_news": sport_news})


def music_news(request):
    music_news = models.News.objects.filter(news_type="Музыка")
    return render(request, "news/music_news.html",
                  {"music_news": music_news})


def events_news(request):
    events_news = models.News.objects.filter(news_type="События")
    return render(request, "news/events_news.html",
                  {"events_news": events_news})


def cinema_news(request):
    cinema_news = models.News.objects.filter(news_type="Кино")
    return render(request, "news/cinema_news.html",
                  {"cinema_news": cinema_news})


def detailed_news(request, y, m, d, slug):
    news = get_object_or_404(models.News,
                             publish__year=y,
                             publish__month=m,
                             publish__day=d,
                             slug=slug)
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.name = auth.get_user(request)
            comment.material = news
            comment.save()
            return redirect(news)

    else:
        form = forms.CommentForm()

    return render(request, "news/detailed_news.html",
                  {"news": news, 'form': form})



def share_post(request,news_id,):
    news = get_object_or_404(models.News, id=news_id)

    sent = False

    if request.method == "POST":
        form = forms.EmailMaterialForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            uri = request.build_absolute_uri(
                news.get_absolute_url(),
            )

            subject = SUBJECT.format(name=cd['name'],
                                     title=news.title)
            body = BODY.format(title=news.title,
                               uri=uri,
                               name=cd['name'],
                               )

            send_mail(subject, body, 'admin@my.com', [cd['send_adress'], ])
            sent = True
    else:
        form = forms.EmailMaterialForm()

    return render(request,
                  "news/share.html",
                  {'news': news, 'form': form, 'sent': sent})



def profile(request):
    return render(request, "profile.html", {'user': request.user})


def register(request):
    if request.method == "POST":
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_user = form.save(commit=False)
            new_user.set_password(cd['password'])
            new_user.save()
            models.Profile.objects.create(user=new_user, photo='unknown.jpg')

            return render(request, "registration_complete.html",
                          {"user": new_user})

    else:
        form = forms.UserRegistrationForm()
        return render(request, "register.html", {'form': form})


def edit_profile(request):
    if request.method == "POST":
        user_form = forms.UserEditForm(request.POST, instance=request.user)
        profile_form = forms.ProfileEditForm(request.POST,
                                             instance=request.user.profile,
                                             files=request.FILES)
        if all((user_form.is_valid(), profile_form.is_valid())):
            user_form.save()
            if not profile_form.cleaned_data['photo']:
                profile_form.cleaned_data['photo'] = request.user.profile.photo
            profile_form.save()
            return render(request, "profile.html", {'user': request.user})

    else:
        user_form = forms.UserEditForm(instance=request.user)
        profile_form = forms.ProfileEditForm(request.POST, instance=request.user.profile)

    return render(request, "edit_profile.html", {'user_form': user_form,
                                                 'profile_form': profile_form})


def all_news_type(request):
    news_type = models.NewsType.objects.all()
    news = models.News.objects.all()
    return render(request, "news_type/all_news_type.html",
                  {'news_type': news_type, 'news': news})



def detailed_news_type(request, slug):
    news_type = get_object_or_404(models.NewsType, slug=slug)

    news_types = models.NewsType.objects.all()

    return render(request, "news_type/detailed_news_type.html",
                  {"news_type": news_type, 'news_types': news_types})

