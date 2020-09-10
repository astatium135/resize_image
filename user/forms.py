from django import forms
from django.contrib.auth import get_user_model

class UserForm(forms.ModelForm):
	password2 = forms.CharField(widget=forms.PasswordInput(), label="Повторите пароль")
	class Meta:
		model = get_user_model()
		fields = ['username', 'email', 'password', 'password2']
		widgets = {
			'password': forms.PasswordInput(),
		}

	def clean(self):
		super(UserForm, self).clean()
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password!=password2:
			self.add_error('password', forms.ValidationError('Пароли не совпадаёт. Проверьте правильность ввода'))

class UserAuthForm(forms.Form):
	username = forms.CharField(label="Имя пользователя")
	password = forms.CharField(label="Пароль", widget=forms.PasswordInput())
