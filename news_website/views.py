from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from . import models
from . import forms
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import auth
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

SUBJECT = "{name} Хочет показать рассказать вам новость {title}."
BODY = ("{title} at {uri}. {name} отправил вам новость. "
        "Пожалуйста, посмотрите её "  ".")




@login_required()
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


def share_post(request, news_id,):
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

            send_mail(subject, body, 'admin@my.com', [cd['send_adres'], ])
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
    query = request.GET.get("q", "")
    if query:
        news_type = models.NewsType.objects.all()
        news = models.News.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))

    else:
        news_type = models.NewsType.objects.all()
        news = models.News.objects.all()

    paginator = Paginator(news, 2)
    page = request.GET.get('page', 1)

    try:
        news = paginator.get_page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)


    return render(request, "news_type/all_news_type.html",
                    {"news_type": news_type, "news": news, "page": page})


def detailed_news_type(request, slug):
    news_type = get_object_or_404(models.NewsType, slug=slug)

    news_types = models.NewsType.objects.all()

    return render(request, "news_type/detailed_news_type.html",
                  {"news_type": news_type, 'news_types': news_types})
