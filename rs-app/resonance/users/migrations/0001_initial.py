# Generated by Django 2.2.9 on 2020-03-07 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subject', '0001_initial'),
        ('institute', '0001_initial'),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions withoutexplicitly assigning them.', verbose_name='superuser status')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.PositiveSmallIntegerField(choices=[(1, 'Male'), (2, 'Female')], default=1)),
                ('profile_picture', models.ImageField(upload_to='users/profile/')),
                ('username', models.CharField(max_length=60, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('mobile', models.BigIntegerField(verbose_name='Student Mobile')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('role', models.PositiveSmallIntegerField(choices=[(1, 'Admin'), (2, 'Author'), (3, 'Faculty'), (4, 'Learner')], default=4)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_groups_set', related_query_name='resonance_user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_permissions_set', related_query_name='resonance_user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(1, 'Deleted'), (0, 'Active')], default=0)),
                ('name', models.CharField(max_length=120, verbose_name='Department')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(1, 'Deleted'), (0, 'Active')], default=0)),
                ('name', models.CharField(max_length=120, verbose_name='Designation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(1, 'Deleted'), (0, 'Active')], default=0)),
                ('name', models.CharField(max_length=120, verbose_name='Department name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmploymentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(1, 'Deleted'), (0, 'Active')], default=0)),
                ('name', models.CharField(max_length=120, verbose_name='Employment Type Name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(1, 'Deleted'), (0, 'Active')], default=0)),
                ('date_of_joining', models.DateField(blank=True, null=True)),
                ('status', models.BooleanField(blank=True, default=False, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created Date')),
                ('employee_code', models.CharField(max_length=20)),
                ('short_name', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('center', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='center', to='institute.Center')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department', to='users.Department')),
                ('designation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='designation', to='users.Designation')),
                ('division', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Division')),
                ('employment_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employee_type', to='users.EmploymentType')),
                ('reporting_manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Faculty')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(1, 'Deleted'), (0, 'Active')], default=0)),
                ('roll_no', models.CharField(blank=True, max_length=120, null=True, verbose_name='Role No')),
                ('father_name', models.CharField(blank=True, default='', max_length=120, null=True, verbose_name='Father name')),
                ('father_email', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Father Email')),
                ('father_mobile', models.BigIntegerField(blank=True, default=0, null=True, verbose_name='Father mobile')),
                ('mother_name', models.CharField(blank=True, default='', max_length=120, null=True, verbose_name='Mother name')),
                ('mother_email', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Mother email')),
                ('mother_mobile', models.BigIntegerField(blank=True, default=0, null=True, verbose_name='Mother mobile')),
                ('status', models.BooleanField(blank=True, default=False, null=True)),
                ('medium', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'English'), (1, 'Published')], default=0, null=True)),
                ('batch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='institute.Batch')),
                ('center', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institute.Center')),
                ('classs', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institute.Classs')),
                ('division', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Division')),
                ('phase', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institute.Phase')),
                ('program', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institute.Program')),
                ('session', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institute.Sessions')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StudentSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(1, 'Deleted'), (0, 'Active')], default=0)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Student')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='subject.Subject')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StudentClassPath',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(1, 'Deleted'), (0, 'Active')], default=0)),
                ('is_current', models.BooleanField(default=True)),
                ('classs', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='institute.Classs')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students_class_path', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_path', to='users.Student')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FacultySubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(1, 'Deleted'), (0, 'Active')], default=0)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject', to='users.Faculty')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='faculty_subject', to='subject.Subject')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FacultyProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(1, 'Deleted'), (0, 'Active')], default=0)),
                ('Program', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='faculty_program', to='institute.Program')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='programs', to='users.Faculty')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FacultyPhase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(1, 'Deleted'), (0, 'Active')], default=0)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phases', to='users.Faculty')),
                ('phase', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='faculty_phase', to='institute.Phase')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FacultyBatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(1, 'Deleted'), (0, 'Active')], default=0)),
                ('batch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='faculty_batch', to='institute.Batch')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batch', to='users.Faculty')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StudentBatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(1, 'Deleted'), (0, 'Active')], default=0)),
                ('batch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='institute.Batch')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Student')),
            ],
            options={
                'unique_together': {('student', 'batch')},
            },
        ),
    ]
