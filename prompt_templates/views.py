from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import PromptTemplate
from .forms import PromptFillForm
from .utils import generate_prompt


def template_list_view(request):
    templates = PromptTemplate.objects.all().order_by("-created_at")
    saved_template_slugs = set()

    if request.user.is_authenticated:
        saved_template_slugs = set(
            request.user.profile.saved_templates.values_list("slug", flat=True)
        )

    return render(
        request,
        "prompt_templates/prompt_templates_list.html",
        {
            "templates": templates,
            "saved_template_slugs": saved_template_slugs,
        },
    )


@login_required
def prompt_fill_view(request, slug):
    template = get_object_or_404(PromptTemplate, slug=slug)
    form = PromptFillForm(request.POST or None)
    generated = None
    profile = request.user.profile  # <-- add this

    # Fill placeholders in template text with profile info
    base_text = template.template_text
    replacements = {
        "[business_name]": profile.business_name or "[business_name]",
        "[business_type]": profile.business_type or "[business_type]",
        "[business_location]": profile.business_location or "[business_location]",
        "[target_audience]": profile.target_audience or "[target_audience]",
        "[bio]": profile.bio or "[bio]",
    }
    for placeholder, value in replacements.items():
        base_text = base_text.replace(placeholder, value)

    if request.method == "POST" and form.is_valid():
        # Use the filled base_text rather than the raw template text
        generated = generate_prompt(base_text, request.user, form.cleaned_data)
        if "download" in request.POST:
            response = HttpResponse(generated, content_type="text/plain")
            filename = f"{template.slug}.txt"
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response

    saved_template_slugs = set()
    if request.user.is_authenticated:
        saved_template_slugs = set(
            request.user.profile.saved_templates.values_list("slug", flat=True)
        )

    return render(
        request,
        "prompt_templates/prompt_fill.html",
        {
            "template": template,
            "form": form,
            "generated": generated,
            "saved_template_slugs": saved_template_slugs,
            "filled_text": base_text,
        },
    )


@login_required
def save_template(request, slug):
    template = get_object_or_404(PromptTemplate, slug=slug)
    profile = request.user.profile

    if template in profile.saved_templates.all():
        profile.saved_templates.remove(template)
        status = "removed"
    else:
        profile.saved_templates.add(template)
        status = "saved"

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"status": status})
    return redirect(request.META.get("HTTP_REFERER", "prompt_templates:template_list"))


@login_required
def dashboard_saved_templates(request):
    saved_templates = request.user.profile.saved_templates.all()
    saved_template_slugs = set(
        request.user.profile.saved_templates.values_list("slug", flat=True)
    )
    return render(
        request,
        "dashboard_saved_templates.html",
        {
            "saved_templates": saved_templates,
            "saved_template_slugs": saved_template_slugs,
        },
    )
