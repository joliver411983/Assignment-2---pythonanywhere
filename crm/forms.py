from django import forms
from .models import Customer, Service, Product
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(UserCreationForm):
    #    username = forms.CharField()
    #    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(label="Username", required=True, help_text="Required.")
    email = forms.EmailField(label="Email address", required=True, help_text="Required.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(username="username").exists():
            raise forms.ValidationError("Username is not unique.")
        return self.cleaned_data["email"]

    #    def clean_username(self):
    #        if User.objects.filter(email="email").exists():
    #            raise forms.ValidationError("Email is not unique.")
    #        return self.cleaned_data["username"]


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('cust_name', 'organization', 'role', 'bldgroom', 'account_number', 'address',
                  'city', 'state', 'zipcode', 'email', 'phone_number')


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = (
            'cust_name', 'service_category', 'description', 'location', 'setup_time', 'cleanup_time', 'service_charge')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('cust_name', 'product', 'p_description', 'quantity', 'charge')
