# Generated by Django 2.2.9 on 2020-03-07 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MasterSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(1, 'Deleted'), (0, 'Active')], default=0)),
                ('label', models.CharField(max_length=200)),
                ('short_code', models.CharField(max_length=20)),
                ('url', models.ImageField(upload_to='subjects/')),
                ('background_code', models.CharField(default='#0000FF', max_length=10)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(1, 'Deleted'), (0, 'Active')], default=0)),
                ('label', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('code', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TOC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(1, 'Deleted'), (0, 'Active')], default=0)),
                ('label', models.CharField(max_length=200)),
                ('order', models.IntegerField(default=0)),
                ('level', models.SmallIntegerField(choices=[(0, 'Unit'), (1, 'Chapter'), (2, 'Topic'), (3, 'Subtopic')], default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]