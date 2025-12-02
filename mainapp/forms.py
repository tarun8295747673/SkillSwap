# forms.py
from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class EditUserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))  # ✅

    class Meta:
        model = UserProfile
        fields = ['full_name', 'phone_number', 'time_balance']  # ✅ only UserProfile fields

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'time_balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EditUserProfileForm, self).__init__(*args, **kwargs)
        if self.user:
            # ✅ show current email in form field
            self.fields['email'].initial = self.instance.email or self.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)

        # ✅ Update both User and UserProfile email
        new_email = self.cleaned_data.get('email')
        if self.user:
            self.user.email = new_email
            if commit:
                self.user.save()

        profile.email = new_email  # ✅ update UserProfile also
        if commit:
            profile.save()

        return profile
