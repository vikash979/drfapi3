# Generated by Django 2.2.9 on 2020-03-07 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subject', '0001_initial'),
        ('institute', '0002_auto_20200307_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='toc',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='toc',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='subject.TOC'),
        ),
        migrations.AddField(
            model_name='toc',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='toc', to='subject.Subject'),
        ),
        migrations.AddField(
            model_name='subject',
            name='classs',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subject_class', to='institute.Classs'),
        ),
        migrations.AddField(
            model_name='subject',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subject',
            name='master_subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subject.MasterSubject'),
        ),
        migrations.AddField(
            model_name='mastersubject',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
