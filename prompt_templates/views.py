from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import PromptTemplate
from .forms import PromptFillForm
from .utils import generate_prompt


def template_list_view(request):
    templates = PromptTemplate.objects.all().order_by("-created_at")
    return render(
        request, "prompt_templates/prompt_templates_list.html", {"templates": templates}
    )


def prompt_fill_view(request, pk):
    template = get_object_or_404(PromptTemplate, pk=pk)
    form = PromptFillForm(request.POST or None)
    generated = None

    if request.method == "POST" and form.is_valid():
        generated = generate_prompt(
            template.template_text, request.user, form.cleaned_data
        )

        # If "download" button pressed, return text file
        if "download" in request.POST:
            response = HttpResponse(generated, content_type="text/plain")
            filename = f"{template.title.replace(' ', '_')}.txt"
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
