"""
HTML views for the news app.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from news_app.models import Article
from .forms import UserRegisterForm, ArticleForm
from .forms import NewsletterForm

# -------------------------
# REGISTRATION VIEW
# -------------------------


def register(request):
    """Register a new user (reader or journalist)."""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print("User", user)

            # IMPORTANT: hash password correctly
            user.set_password(form.cleaned_data["password1"])
            user.is_active = True
            user.is_staff = False  # readers & journalists only
            print(user.is_active)

            user.save()

            messages.success(
                request,
                "Account created successfully. You can now log in."
            )
            return redirect("login")
    else:
        form = UserRegisterForm()

    return render(request, "news_app/register.html", {"form": form})


def home(request):
    """Home page view."""
    # You can redirect readers or show generic landing page
    return render(request, 'news_app/home.html')


# -------------------------
# AUTHENTICATION VIEWS
# -------------------------


def user_login(request):
    """Log in the user with role-based redirection."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

        login(request, user)

        # ROLE-BASED REDIRECT
        if user.role == "editor":
            return redirect("editor_dashboard")
        elif user.role == "journalist":
            return redirect("journalist_dashboard")
        else:
            return redirect("article_list")
    else:
        messages.error(request, "Invalid username or password.")

    return render(request, "news_app/login.html")


@login_required
def user_logout(request):
    """Log out the user."""
    logout(request)
    return redirect("login")


# -------------------------
# PUBLIC VIEWS
# -------------------------

def article_list(request):
    """List approved articles for readers."""
    articles = Article.objects.filter(approved=True)  # type: ignore[attr-defined]  # pylint: disable=no-member
    return render(
        request,
        "news_app/article_list.html",
        {"articles": articles}
    )


# -------------------------
# EDITOR VIEWS
# -------------------------

@login_required
def editor_dashboard(request):
    """Dashboard for editors."""
    if request.user.role != "editor":
        raise PermissionDenied

    publishing_house = request.user.publishing_house

    articles = Article.objects.filter(  # type: ignore[attr-defined]  # pylint: disable=no-member
        approved=False,
        publishing_house=publishing_house
    )

    return render(
        request,
        "news_app/editor_dashboard.html",
        {"articles": articles}
    )


@login_required
def approve_article(request, article_id):
    """Approve an article."""
    if request.user.role != "editor":
        raise PermissionDenied

    article = get_object_or_404(
        Article,
        id=article_id,
        publishing_house=request.user.publishing_house
    )

    article.approved = True
    article.save()

    return redirect("editor_dashboard")


@login_required
def create_newsletter(request):
    """Create a newsletter (journalist only)."""
    if request.user.role != "journalist":
        return redirect("article_list")

    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.journalist = request.user
            newsletter.publishing_house = request.user.publishing_house
            newsletter.save()
            return redirect("journalist_dashboard")
    else:
        form = NewsletterForm()

    return render(request, "news_app/create_newsletter.html", {"form": form})


# -------------------------
# JOURNALIST VIEWS
# -------------------------


@login_required
def journalist_dashboard(request):
    """Dashboard for journalists."""
    if request.user.role != "journalist":
        raise PermissionDenied

    articles = Article.objects.filter(journalist=request.user)  # type: ignore[attr-defined]  # pylint: disable=no-member
    return render(
        request,
        "news_app/journalist_dashboard.html",
        {"articles": articles}
    )


@login_required
def submit_article(request):
    """Submit a new article."""
    if request.user.role != "journalist":
        raise PermissionDenied

    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.journalist = request.user
            article.approved = False
            article.save()

            messages.success(request, "Article submitted for approval.")
            return redirect("journalist_dashboard")
    else:
        form = ArticleForm()

    return render(
        request,
        "news_app/submit_article.html",
        {"form": form}
    )


def article_detail(request, article_id):
    """View details of an approved article."""
    article = get_object_or_404(
        Article,
        id=article_id,
        approved=True
    )
    return render(
        request,
        "news_app/article_detail.html",
        {"article": article}
    )
