# prompt_generator/views.py
from django.shortcuts import render, get_object_or_404
from prompts.models import Prompt


def generator_list(request):
    category = request.GET.get("category")
    prompts = (
        Prompt.objects.filter(category=category) if category else Prompt.objects.all()
    )
    return render(request, "prompt_generator/generator_list.html", {"prompts": prompts})


def generator_detail(request, pk):
    prompt = get_object_or_404(Prompt, pk=pk)
    return render(request, "prompt_generator/generator_detail.html", {"prompt": prompt})
