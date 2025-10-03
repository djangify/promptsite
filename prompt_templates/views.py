from django.shortcuts import render, get_object_or_404
from .models import PromptTemplate
from .forms import PromptFillForm
from .utils import generate_prompt
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def template_list_view(request):
    templates = PromptTemplate.objects.all().order_by("-created_at")
    return render(
        request, "prompt_templates/prompt_templates_list.html", {"templates": templates}
    )


def prompt_fill_view(request, slug):
    template = get_object_or_404(PromptTemplate, slug=slug)
    form = PromptFillForm(request.POST or None)
    generated = None

    if request.method == "POST" and form.is_valid():
        generated = generate_prompt(
            template.template_text, request.user, form.cleaned_data
        )
        if "download" in request.POST:
            response = HttpResponse(generated, content_type="text/plain")
            filename = f"{template.slug}.txt"
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response

    return render(
        request,
        "prompt_templates/prompt_fill.html",
        {
            "template": template,
            "form": form,
            "generated": generated,
        },
    )


@login_required
def save_template(request, slug):
    template = get_object_or_404(PromptTemplate, slug=slug)
    user = request.user

    # Check if already saved
    if template in user.profile.saved_templates.all():
        user.profile.saved_templates.remove(template)
        return JsonResponse({"status": "removed"})
    else:
        user.profile.saved_templates.add(template)
        return JsonResponse({"status": "saved"})


@login_required
def dashboard_saved_templates(request):
    saved_templates = request.user.profile.saved_templates.all()
    return render(
        request,
        "dashboard_saved_templates.html",
        {
            "saved_templates": saved_templates,
        },
    )
