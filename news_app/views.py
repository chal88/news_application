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
from .forms import NewsletterForm, Newsletter
from .models import CustomUser, PublishingHouse

# -------------------------
# REGISTRATION VIEW
# -------------------------


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegisterForm
from .models import CustomUser, PublishingHouse


# -------------------------------------------
# REGISTER VIEW
# -------------------------------------------
def register(request):
    """Register a new user (Reader or Journalist)."""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Hash password correctly
            user.set_password(form.cleaned_data["password1"])
            user.is_active = True
            user.is_staff = False  # Readers & Journalists only

            # Handle Publishing House
            new_ph_name = form.cleaned_data.get("new_publishing_house")
            if new_ph_name:
                publishing_house, _ = PublishingHouse.objects.get_or_create(name=new_ph_name)
                user.publishing_house = publishing_house
            else:
                user.publishing_house = form.cleaned_data.get("publishing_house")

            user.save()

            # Auto-login immediately
            login(request, user)
            messages.success(request, "Account created successfully. You are now logged in.")

            # Redirect based on role (do NOT redirect to login!)
            if user.role == "journalist":
                return redirect("journalist_dashboard")
            elif user.role == "editor":
                return redirect("editor_dashboard")
            else:
                return redirect("article_list")

    else:
        form = UserRegisterForm()

    return render(request, "news_app/register.html", {"form": form})


# -------------------------------------------
# LOGIN VIEW
# -------------------------------------------
def user_login(request):
    """Login view with proper message handling."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")

            # Redirect based on role
            if user.role == "journalist":
                return redirect("journalist_dashboard")
            elif user.role == "editor":
                return redirect("editor_dashboard")
            else:
                return redirect("article_list")

        else:
            messages.error(request, "Invalid username or password")

    # GET requests or failed login
    return render(request, "news_app/login.html")


# -------------------------------------------
# LOGOUT VIEW
# -------------------------------------------
def user_logout(request):
    """Logout the user and redirect to login."""
    logout(request)
    # Only show logout message here
    messages.success(request, "You have successfully logged out.")
    return redirect("login")


# -------------------------------------------
# HOME VIEW
# -------------------------------------------
def home(request):
    """Home page view."""
    return render(request, 'news_app/home.html')

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

    # Allow ONLY journalists
    if request.user.role != "journalist":
        messages.error(request, "You are not allowed to create newsletters.")
        return redirect("article_list")

    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)

            # CORRECT field assignment
            newsletter.author = request.user

            # Optional publishing house
            if request.user.publishing_house:
                newsletter.publishing_house = request.user.publishing_house

            newsletter.save()

            messages.success(request, "Newsletter created successfully.")
            return redirect("journalist_dashboard")
    else:
        form = NewsletterForm()

    return render(
        request,
        "news_app/create_newsletter.html",
        {"form": form}
    )


@login_required
def edit_newsletter(request, newsletter_id):
    newsletter = get_object_or_404(
        Newsletter,
        id=newsletter_id,
        author=request.user
    )

    if request.method == "POST":
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.approved = False
            newsletter.save()
            return redirect("journalist_dashboard")
    else:
        form = NewsletterForm(instance=newsletter)

    return render(request, "news_app/edit_newsletter.html", {"form": form})


@login_required
def delete_newsletter(request, newsletter_id):
    newsletter = get_object_or_404(
        Newsletter,
        id=newsletter_id,
        author=request.user
    )

    if request.method == "POST":
        newsletter.delete()
        return redirect("journalist_dashboard")

    return render(
        request,
        "news_app/delete_newsletter.html",
        {"newsletter": newsletter}
    )

# -------------------------
# JOURNALIST VIEWS
# -------------------------


@login_required
def journalist_dashboard(request):
    if request.user.role != "journalist":
        return redirect("article_list")

    articles = Article.objects.filter(author=request.user).order_by("-created_at")
    newsletters = Newsletter.objects.filter(author=request.user).order_by("-created_at")

    context = {
        "articles": articles,
        "newsletters": newsletters,
    }

    return render(request, "news_app/journalist_dashboard.html", context)


@login_required
def submit_article(request):
    """Submit a new article."""
    if request.user.role != "journalist":
        raise PermissionDenied

    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
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


@login_required
def edit_article(request, article_id):
    article = get_object_or_404(
        Article,
        id=article_id,
        author=request.user
    )

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.approved = False  # re-approval required
            article.save()
            return redirect("journalist_dashboard")
    else:
        form = ArticleForm(instance=article)

    return render(request, "news_app/edit_article.html", {"form": form})


@login_required
def delete_article(request, article_id):
    article = get_object_or_404(
        Article,
        id=article_id,
        author=request.user
    )

    if request.method == "POST":
        article.delete()
        return redirect("journalist_dashboard")

    return render(
        request,
        "news_app/delete_article.html",
        {"article": article}
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
