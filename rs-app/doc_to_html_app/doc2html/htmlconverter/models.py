from django.db import models

class ConvertedHtml(models.Model):
    content_file= models.ImageField(upload_to='')
    contentid= models.IntegerField(default=0)
    content_type = models.IntegerField(default=0)
    html_str = models.TextField(blank=True,null=True)
