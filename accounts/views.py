# accounts/views.py
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
from .models import Prompt
from .forms import UserRegistrationForm, UserProfileForm
from .models import EmailVerificationToken
from prompt_templates.models import PromptTemplate


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create inactive user until email is verified
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password1"])
            new_user.is_active = False  # User inactive until email verified
            new_user.save()

            # Send verification email
            send_verification_email(request, new_user)

            # Redirect to verification sent page
            return redirect("accounts:verification_sent")
    else:
        form = UserRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def send_verification_email(request, user):
    """Send email verification link to newly registered user"""
    try:
        # Delete any existing tokens for this user
        EmailVerificationToken.objects.filter(user=user).delete()

        # Create new token
        token = EmailVerificationToken.objects.create(user=user)

        verification_url = request.build_absolute_uri(
            reverse("accounts:verify_email", args=[str(token.token)])
        )

        # Context for email template
        context = {
            "user": user,
            "verification_url": verification_url,
            "site_url": settings.SITE_URL,
            "email": user.email,
        }

        subject = "Verify your email for PromptSite"
        html_message = render_to_string(
            "accounts/email/email_verification_email.html", context
        )
        plain_message = strip_tags(html_message)

        # Send the email
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception:
        return False


def verification_sent(request):
    return render(request, "accounts/verification_sent.html")


def verify_email(request, token):
    try:
        verification_token = EmailVerificationToken.objects.get(token=token)

        if verification_token.is_valid():
            user = verification_token.user
            user.is_active = True
            user.save()

            # Mark the profile as verified
            user.profile.verified = True
            user.profile.save()

            # Clean up the token
            verification_token.delete()

            return render(request, "accounts/email/email_verified.html")

        else:
            return render(request, "accounts/email/email_verification_invalid.html")

    except EmailVerificationToken.DoesNotExist:
        return render(request, "accounts/email/email_verification_invalid.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")

                next_page = request.GET.get("next")
                return (
                    redirect(next_page)
                    if next_page
                    else redirect(settings.LOGIN_REDIRECT_URL)
                )
            else:
                messages.error(
                    request,
                    "Account not activated. Please check your email for verification link.",
                )
                return render(request, "accounts/login.html")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("core:home")


@login_required
def dashboard_view(request):
    saved_prompts = request.user.profile.saved_prompts.all()
    return render(request, "accounts/dashboard.html", {"saved_prompts": saved_prompts})


@login_required
def profile_view(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("accounts:profile")
    else:
        form = UserProfileForm(instance=request.user.profile)

    return render(request, "accounts/profile.html", {"form": form})


@login_required
def add_favourite_prompt(request, prompt_id):
    prompt = get_object_or_404(Prompt, id=prompt_id)
    user_profile = request.user.profile

    is_favourite = prompt in user_profile.favourite_prompts.all()

    if is_favourite:
        user_profile.favourite_prompts.remove(prompt)
        is_favourite = False
        message = "Prompt removed from your profile."
    else:
        user_profile.favourite_prompts.add(prompt)
        is_favourite = True
        message = "Prompt added to your profile!"

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(
            {"status": "success", "is_favourite": is_favourite, "message": message}
        )

    messages.success(request, message)
    return redirect(request.META.get("HTTP_REFERER", "core:home"))


@login_required
def add_favourite_template(request, slug):
    template = get_object_or_404(PromptTemplate, slug=slug)
    user_profile = request.user.profile

    if template in user_profile.saved_templates.all():
        user_profile.saved_templates.remove(template)
        status = "removed"
    else:
        user_profile.saved_templates.add(template)
        status = "saved"

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"status": status})

    return redirect(request.META.get("HTTP_REFERER", "accounts:dashboard"))
