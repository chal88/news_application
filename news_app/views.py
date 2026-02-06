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
from .models import PublishingHouse


# -------------------------------------------
# REGISTER VIEW
# -------------------------------------------
def register(request):
    """Register a new user (Reader or Journalist)
    with optional publishing house association.
        - Journalists can create articles and newsletters.
        - Readers can only view approved articles.
        - Editors are created by admins and cannot register here.
        - Users can optionally create or join a publishing house
        during registration.
        - After registration, users are auto-logged in and
        redirected based on their role.
        - Proper password hashing and form validation are implemented.
        - Success messages are shown upon successful registration and login.
        - No redirection to login page after registration; users go directly
        to their dashboard or article list.
        - Editors must be created by admins; they cannot register through
        this form.
        - The form handles both creating a new publishing house or selecting
        an existing one.
        - User roles are determined by the form input, and appropriate
        permissions are set.
        - The view ensures that only valid data is processed and saved to
        the database.
        - Error handling is in place for invalid form submissions, with
        feedback to the user.
    """
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
                publishing_house, _ = PublishingHouse.objects.get_or_create(
                    name=new_ph_name)
                user.publishing_house = publishing_house
            else:
                user.publishing_house = form.cleaned_data.get(
                    "publishing_house")

            user.save()

            # Auto-login immediately
            login(request, user)
            messages.success(request,
                             "Account created successfully. "
                             "You are now logged in.")

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
    """Handles user authentication and login session creation
    with role-based redirection.
    Authenticates users based on username and password.
    On successful authentication, initiates a login session
    and redirects users to their respective dashboards:
        - Journalists to the journalist dashboard.
        - Editors to the editor dashboard.
        - Readers to the article list page.
    Displays error messages for invalid login attempts.
    """
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
    """Logs out the user and redirect to login page,
    displaying a logout success message.
    """
    logout(request)
    # Only show logout message here
    messages.success(request, "You have successfully logged out.")
    return redirect("article_list")


# -------------------------------------------
# HOME VIEW
# -------------------------------------------
def home(request):
    """Renders the Home page (landing page) for the news application."""
    return render(request, 'news_app/article_list.html')

# -------------------------
# PUBLIC VIEWS
# -------------------------


def article_list(request):
    """Renders a list of published articles for readers.
    Fetches articles marked as approved from the database,
    and displays them in the article list template.
    """
    # type: ignore[attr-defined]  # pylint: disable=no-member
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
def editor_dashboard(request):
    """
    Editor dashboard view:
    - Lists all pending articles for the editor's publishing house
    - Allows approving or deleting articles via POST
    - Ensures only editors can access this view and only act on their
        publishing house's articles.
    """
    # Ensure only editors access this view
    if request.user.role != "editor":
        return redirect("journalist_dashboard")

    # Get pending articles for the editor's publishing house
    pending_articles = Article.objects.filter(
        approved=False,
        publishing_house=request.user.publishing_house
    )

    if request.method == "POST":
        article_id = request.POST.get("article_id")
        action = request.POST.get("action")
        article = get_object_or_404(Article, id=article_id)

        # Ensure the editor only acts on articles
        # from their own publishing house
        if article.publishing_house != request.user.publishing_house:
            return redirect("editor_dashboard")

        if action == "approve":
            article.approved = True
            article.save()
        elif action == "delete":
            article.delete()

        return redirect("editor_dashboard")

    context = {
        "articles": pending_articles
    }
    return render(request, "news_app/editor_dashboard.html", context)


@login_required
def approve_article(request, article_id):
    """Only authorized editors can approve an article.
    Updates the article's approved status to True, allowing it to be visible
    to readers. Ensures that only articles from the editor's publishing house
    can be approved, and that the user has the appropriate permissions.
    """
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
    """Handles the creation of a newsletter by a journalist.
    Only users with the 'journalist' role are permitted to create newsletters.
    The view processes the submitted form data, assigns the current user
    as the author, and associates the newsletter with the user's publishing
    house if applicable. Upon successful creation, the user is redirected
    to the journalist dashboard with a success message.
    Messages are displayed for unauthorized access attempts and successful
    newsletter creation.
    """

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
    """
    Allows journalists to edit their own newsletters.
    Only the author of the newsletter can edit it, and the newsletter must
    belong to the logged-in journalist. The view handles both GET and POST
    requests, displaying the edit form with existing data for GET requests and
    processing form submissions for POST requests. Upon successful editing, the
    newsletter's approved status is reset to False, requiring re-approval by an
    editor. Unauthorized access attempts are handled with appropriate error
    messages and redirections.
    """
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
    """
    Deletes a newsletter created by the logged-in journalist.
    Only the author of the newsletter can delete it. The view handles both
    GET and POST requests, displaying a confirmation page for GET requests
    and processing the deletion for POST requests. Upon successful deletion,
    the user is redirected to the journalist dashboard. Unauthorized access
    attempts are handled with appropriate error messages and redirections.
    """

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
    """
    Renders the main dashboard for journalists.
    Allows journalists to view and manage their own articles
    and newsletters. Displays a list of articles and newsletters
    created by the logged-in journalist, ordered by creation date.
    """

    if request.user.role != "journalist":
        return redirect("article_list")

    articles = Article.objects.filter(
        author=request.user).order_by("-created_at")
    newsletters = Newsletter.objects.filter(
        author=request.user).order_by("-created_at")

    context = {
        "articles": articles,
        "newsletters": newsletters,
    }

    return render(request, "news_app/journalist_dashboard.html", context)


@login_required
def submit_article(request):
    """Handles submission of a new article.
    Only users with the 'journalist' role are permitted to submit articles.
    The view processes the submitted form data, assigns the current user
    as the author, and sets the article's approved status to False.
    Upon successful submission, the user is redirected to the journalist
    dashboard with a success message and the article awaits editor approval.
    if messages are not successful, appropriate error handling is in place.
    """
    if request.user.role != "journalist":
        raise PermissionDenied

    if request.method == "POST":
        form = ArticleForm(request.POST, request=request)
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
    """
Allows journalists to edit their own articles.
Only the author of the article can edit it, and the article must belong to
the logged-in journalist. The view handles both GET and POST requests,
displaying a form for editing the article on GET requests and processing
the form submission on POST requests. Upon successful editing, the article's
approved status is reset to False, requiring re-approval by an editor.
Unauthorized access attempts are handled with appropriate error
messages and redirections.
    """

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
    """
    Deletes an article created by the logged-in journalist.
    Only the author of the article can delete it. The view handles both
    GET and POST requests, displaying a confirmation page for GET requests
    and processing the deletion for POST requests. Upon successful deletion,
    the user is redirected to the journalist dashboard. Unauthorized access
    attempts are handled with appropriate error messages and redirections.
    """

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
    """Renders the detail view for an approved article
    Fetches the article by ID, ensuring it is approved before rendering.
    If the article is not approved or does not exist, a 404 error is raised.
    Displays the article's title, content, author, and publication date in the
    detail template."""
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
