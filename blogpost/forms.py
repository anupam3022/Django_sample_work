from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserCreateForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

	# def __init__(self, *args, **kwargs):
	# 	super(UserCreateForm, self).__init__(*args, **kwargs)

	# 	for fieldname in ['username', 'password1', 'password2','first_name', 'last_name', 'email']:
	# 		self.fields[fieldname].help_text = None
		

	def clean_username(self):
		user = self.cleaned_data.get('username')
		try:
			match = User.objects.get(username =user)
		except:
			return user
		raise forms.ValidationError("Username alredy exists!!!")
		if not '@' in user or '#' in user or '!' in user:
			raise forms.ValidationError("Usernames should have special characters.")
		return user


# class PostCreateForm(forms):
# 	title = forms.CharField(max_length=30, required=True)
# 	content = forms.TextField()

# 	class Meta:
# 		model = User
# 		fields = ('title','content')