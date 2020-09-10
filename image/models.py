from django.db import models
from django.contrib.auth import get_user_model
import uuid
import os
import urllib3
import PIL
import io
from django.conf import settings

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return filename

class ImageManager(models.Manager):
    def add_by_link(self, link, user):
        http = urllib3.PoolManager()
        r = http.request('GET', link)
        if r.status in range(200, 300):
            image = PIL.Image.open(io.BytesIO(r.data))
            if image:
	            path = os.path.join(settings.MEDIA_ROOT, str(uuid.uuid4())+'.'+link.split('.')[-1])
	            image.save(path)
	            img = Image.objects.create(user=user, base_image=path.split('/')[-1], name=link)
	            return img
            else:
	            raise ValueError("Файл повреждён или имеет недопустимый формат")
        else:
            raise ValueError("Не удалось загрузить файл")

class Image(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.TextField(verbose_name="базовое имя изображения")
    base_image = models.ImageField(verbose_name="базовое изображение")
    resize_image = models.ImageField(verbose_name="изменённое изображение", blank=True, null=True)
    
    objects = ImageManager()
    
    class Meta:
        verbose_name = "изображение"
        verbose_name_plural = "изображения"
    def __str__(self):
        return self.name
    def get_image(self) -> str:
        if self.resize_image:
            return self.resize_image
        else:
            return self.base_image
    image = property(get_image)
    def change_image(self, width, height):
        if width and not height:
            x_rate = y_rate = width/self.base_image.width
        elif height and not width:
            x_rate = y_rate = height/self.base_image.height
        elif width and height:
            x_rate = width/self.base_image.width
            y_rate = height/self.base_image.height
        img = PIL.Image.open(self.base_image.path)
        w, h = img.size
        img = img.resize((int(w*x_rate), int(h*y_rate)))
        path = os.path.join(settings.MEDIA_ROOT, str(uuid.uuid4())+'.'+self.base_image.path.split('.')[-1]) if not self.resize_image else self.resize_image.path
        img.save(path)
        self.resize_image = path.split('/')[-1]
        self.save()
        
    '''@classmethod
    def add_image_by_link(cls, link, user):
        http = urllib3.PoolManager()
        r = http.request('GET', link)
        if r.status in range(200, 300):
            image = PIL.Image.open(io.BytesIO(r.data))
            if image:
	            path = os.path.join(settings.MEDIA_ROOT, str(uuid.uuid4())+'.'+link.split('.')[-1])
	            image.save(path)
	            img = Image.objects.create(user=user, base_image=path.split('/')[-1], name=link)
	            return img
            else:
	            raise ValueError("Файл повреждён или имеет недопустимый формат")
        else:
            raise ValueError('link', "Не удалось загрузить файл")'''
