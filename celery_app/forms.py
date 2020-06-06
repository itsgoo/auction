from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Auctions, Bids





class ChangeUserData(UserChangeForm):


    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'



class BidUpForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = (
            'bid',
            'auction',
            'buyer_id',
        )





class AuctionsForm(forms.ModelForm):

    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Auctions
        fields = ('title',
                  'description',
                  'seller',
                  'status',
                  'start_price',
                  'bid_up',
                  'start_auction',
                  'start_auction_time',
                  'sort_auction',
                  'main_img',
                  )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if field == 'start_auction':
                self.fields[field].widget.input_type = 'date'
            self.fields[field].widget.attrs['class'] = 'form-control'



class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if field == 'password':
                self.fields[field].widget.input_type = 'password'



class RegisterUserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'groups', 'password1', 'password2')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



# class RegisterUserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'password', 'email', 'groups')
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'
#             if field == 'password':
#                 self.fields[field].widget.input_type = 'password'
#             if field == 'email':
#                 self.fields[field].widget.attrs['required'] = True
#             if field == 'groups':
#                 self.fields[field].widget.attrs['required'] = True
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password"])
#         if commit:
#             user.save()
#         return user