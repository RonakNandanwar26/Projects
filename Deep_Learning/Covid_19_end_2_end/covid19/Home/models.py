import os
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return ext

def upload_product_image_path(instance, filename):
    new_filename = instance.name
    ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "Images/{final_filename}".format(final_filename=final_filename)

class Image(models.Model):
    
    image = models.ImageField(default='default.jpg', upload_to=upload_product_image_path)
    smart = ImageSpecField(source='image1', processors=[ResizeToFill(250, 350)], format='JPEG', options={'quality': 99})

    def __str__(self):
        return self.name