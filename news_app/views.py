"""
HTML views for the news app.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Article
from .forms import UserRegisterForm

# -------------------------
# REGISTRATION VIEW
# -------------------------


def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'news_app/register.html', {'form': form})


# -------------------------
# AUTHENTICATION VIEWS
# -------------------------

def user_login(request):
    """Handle login for journalist, editor, and reader."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            messages.error(request, "Invalid username or password.")
            return redirect("home")

        # Redirect by role
        if role == "journalist":
            return redirect("journalist_dashboard")
        elif role == "editor":
            return redirect("pending_articles")
        elif role == "reader":
            return redirect("article_list")

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
    articles = Article.objects.filter(approved=True)
    return render(
        request,
        "news_app/article_list.html",
        {"articles": articles}
    )


# -------------------------
# EDITOR VIEWS
# -------------------------

@login_required
@permission_required("news_app.change_article", raise_exception=True)
def pending_articles(request):
    """List articles pending approval."""
    articles = Article.objects.filter(approved=False)
    return render(
        request,
        "news_app/pending_articles.html",
        {"articles": articles}
    )


@login_required
@permission_required("news_app.change_article", raise_exception=True)
def approve_article(request, article_id):
    """Approve an article."""
    article = get_object_or_404(Article, id=article_id)
    article.approved = True
    article.save()
    return redirect("pending_articles")


# -------------------------
# JOURNALIST VIEWS
# -------------------------

@login_required
def journalist_dashboard(request):
    """Dashboard for journalists."""
    if request.user.role != "journalist":
        raise PermissionDenied

    articles = Article.objects.filter(journalist=request.user)
    return render(
        request,
        "news_app/journalist_dashboard.html",
        {"articles": articles}
    )


@login_required
def submit_article(request):
    """Allow journalists to submit articles."""
    if request.user.role != "journalist":
        raise PermissionDenied

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        Article.objects.create(
            title=title,
            content=content,
            journalist=request.user,
            approved=False
        )

        messages.success(request, "Article submitted for approval.")
        return redirect("journalist_dashboard")

    return render(request, "news_app/submit_article.html")


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
