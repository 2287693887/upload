from django.db import models


# Create your models here.

class PictureStore(models.Model):
    picture_path = models.ImageField(upload_to='photos/', blank=True, null=True)
    translate_code = models.CharField(max_length=250, verbose_name='验证码')

    class Meta:
        db_table = "photos"
