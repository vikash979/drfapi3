from django import forms
from django.contrib.auth import (authenticate, get_user_model)

from users.models import Student

class StudentForm(forms.ModelForm):
	name = forms.CharField(max_length=150)
	email = forms.EmailField()

	class Meta:
		model = Student
		fields = [
			'name', 'email', 'father_name', 'father_email', 'father_mobile',
			'mother_name', 'mother_email', 'mother_mobile'
		]


class UserLoginForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		email = self.cleaned_data.get("email")
		password = self.cleaned_data.get("password")
		if email and password:
			if not User.objects.filter(email=email).exists():
				raise forms.ValidationError("This user doesn't exists")
			user = authenticate(email=email, password=password)
			if not user:
				raise forms.ValidationError("Incorrect password")
			if not user.is_active:
				raise forms.ValidationError("This user no longer active")
			if not user.is_staff:
				raise forms.ValidationError("You are not authorized to login")

		return super(UserLoginForm,self).clean(*args,**kwargs)
