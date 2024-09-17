from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users in admin panel.
    """

    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username"]

    def clean_password_confirm(self):
        data = self.cleaned_data
        pass1 = data.get("password")
        pass2 = data.get("password_confirm")
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError("Passwords don't match")
        return pass2

    def save(self, commit: True):
        user = super().save(commit=False)
        user.set_password(self.data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """
    A form for updating users in admin panel.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = "__all__"
