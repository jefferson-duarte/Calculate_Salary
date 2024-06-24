from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    def add_attr(self, field, attr_name, attr_new_val):
        existing_attr = field.widget.attrs.get(attr_name, '')
        field.widget.attrs[attr_name] = f'{
            existing_attr} {attr_new_val}'.strip()

    def add_placeholder(self, field, placeholder_val):
        self.add_attr(field, 'placeholder', placeholder_val)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.add_placeholder(self.fields['username'], 'Your username')
        self.add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        self.add_placeholder(self.fields['first_name'], 'Ex.: John')
        self.add_placeholder(self.fields['password1'], 'Type your password')
        self.add_placeholder(self.fields['password2'], 'Repeat your password')

        self.fields['username'].help_text = 'Please enter a unique username.'
        self.fields['password1'].help_text = (
            'Your password must contain at least 8 characters.'
        )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username)

        if len(username) < 4:
            raise ValidationError(
                'Username do not contain less than 4 chars.'
            )

        if user.exists():
            raise ValidationError('Username is already taken', code='invalid')

        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise ValidationError("Passwords do not match.")

        return cleaned_data
