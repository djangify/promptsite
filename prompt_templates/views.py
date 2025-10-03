from django.shortcuts import render, get_object_or_404
from .models import PromptTemplate
from .forms import PromptFillForm
from .utils import generate_prompt


def prompt_fill_view(request, pk):
    template = get_object_or_404(PromptTemplate, pk=pk)
    form = PromptFillForm(request.POST or None)
    generated = None

    if request.method == "POST" and form.is_valid():
        generated = generate_prompt(
            template.template_text, request.user, form.cleaned_data
        )

    return render(
        request,
        "prompt_templates/prompt_fill.html",
        {
            "template": template,
            "form": form,
            "generated": generated,
        },
    )
