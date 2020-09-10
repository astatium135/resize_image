from django import forms
from .models import Image

class ImageAddForm(forms.Form):
	link = forms.URLField(label='Ссылка', required=False)
	file = forms.ImageField(label='Файл', required=False)

	def clean(self):
		super(ImageAddForm, self).clean()
		link = self.cleaned_data.get('link')
		file = self.cleaned_data.get('file')
		if not (link or file):
			self.add_error(None, forms.ValidationError('Ни один из вариантов не выбран'))
		elif link and file:
			self.add_error(None, forms.ValidationError('Выбраны оба варианта. Выберите только один'))

class ImageEditForm(forms.Form):
	width = forms.IntegerField(label="Ширина", required=False, min_value=0)
	height = forms.IntegerField(label="Высота", required=False, min_value=0)

	def clean(self):
		super(ImageEditForm, self).clean()
		width = self.cleaned_data.get('width')
		height = self.cleaned_data.get('height')
		if not (width or height):
			self.add_error(None, forms.ValidationError('Как минимум одно поле должно быть указано'))