from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Image
from .forms import ImageAddForm, ImageEditForm
import urllib3
import PIL
import io
import uuid
from django.conf import settings
import os
from django.http import Http404

@login_required
def image_list(request):
    images = Image.objects.filter(user=request.user)
    return render(request, 'image_list.html', {'images': images})
@login_required
def image_add(request):
    if request.method == 'POST':
        form = ImageAddForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data.get('file'):
                print(form)
                print(form.cleaned_data['file'])
                Image.objects.create(user=request.user, name=form.cleaned_data.get('file'), base_image=form.cleaned_data.get('file'))
                return redirect('/')
            else:
                try:
                    Image.objects.add_by_link(form.cleaned_data.get('link'), request.user)
                    return redirect('/')
                except ValueError as v:
                    form.add_error('link', v)
    else:
        form = ImageAddForm()
    return render(request, 'image_add.html', {'form': form})
@login_required
def image_edit(request, id):
    try:
        image = Image.objects.get(user=request.user, pk=id)
    except:
        raise Http404("Файл не найден или доступ запрещён")
    if request.method == 'POST':
        form = ImageEditForm(request.POST)
        if form.is_valid():
            width = form.cleaned_data.get('width', '0')
            height = form.cleaned_data.get('height', '0')

            image.change_image(width, height)
            return redirect("/edit/"+str(image.pk))

    else:
        form = ImageEditForm(initial={'width': image.get_image().width, 'height': image.get_image().height})

    return render(request, 'image_edit.html', {'form': form, 'image': image.get_image().url, 'name': image.name})
