# prompt_generator/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.contrib import messages
from prompts.models import Prompt


def generator_list(request):
    prompts = Prompt.objects.all().order_by("-created_at")
    saved_prompt_ids = set()

    if request.user.is_authenticated:
        saved_prompt_ids = set(
            request.user.profile.saved_prompts.values_list("id", flat=True)
        )

    return render(
        request,
        "prompt_generator/generator_list.html",
        {
            "prompts": prompts,
            "saved_prompt_ids": saved_prompt_ids,
        },
    )


def generator_detail(request, pk):
    prompt = get_object_or_404(Prompt, pk=pk)
    saved_prompt_ids = set()
    if request.user.is_authenticated:
        saved_prompt_ids = set(
            request.user.profile.saved_prompts.values_list("id", flat=True)
        )
    return render(
        request,
        "prompt_generator/generator_detail.html",
        {
            "prompt": prompt,
            "saved_prompt_ids": saved_prompt_ids,
        },
    )


@login_required
def toggle_saved_prompt(request, prompt_id):
    prompt = get_object_or_404(Prompt, id=prompt_id)
    profile = request.user.profile

    if prompt in profile.saved_prompts.all():
        profile.saved_prompts.remove(prompt)
        status = "removed"
    else:
        profile.saved_prompts.add(prompt)
        status = "saved"

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"status": status})

    messages.success(request, f"Prompt {status}!")
    return redirect(request.META.get("HTTP_REFERER", "accounts:dashboard"))
