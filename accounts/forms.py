from django import forms
from accounts.validators import allow_only_images_validator
from .models import User, UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']

    # for non_field_errors we use clean methods
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password does not match!")
        

#userprofileform
class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'start typing...', 'required':'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[allow_only_images_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[allow_only_images_validator])

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']
    

    # there are ptwo methods to make latitude and longitude read only
    # method_1:
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))

    #method_2: preffered one
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'


# customers user form
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']


