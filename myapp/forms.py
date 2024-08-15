from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import MyUser

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('phone_number', 'name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = MyUser.objects.generate_username(self.cleaned_data['name'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    phone_number = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'time', 'num_of_people', 'special_requests']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'HH:MM'}),
            'num_of_people': forms.NumberInput(attrs={'min': 1}),
            'special_requests': forms.Textarea(attrs={'placeholder': 'Any special requests'}),
        }
        help_texts = {
            'date': 'Please enter a valid date in YYYY-MM-DD format.',
            'time': 'Please enter a valid time in HH:MM format.',
        }



from django import forms
from .models import MenuItem, Category, PopularMenuItem

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['category', 'name', 'price', 'size', 'special', 'image']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class PopularMenuItemForm(forms.ModelForm):
    class Meta:
        model = PopularMenuItem
        fields = ['name', 'description', 'image']




from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
import datetime
import pytz


class CheckoutForm(forms.Form):
    DELIVERY_CHOICES = [
        ('pickup', 'Pickup'),
        ('delivery', 'Delivery'),
    ]
    delivery_preference = forms.ChoiceField(choices=DELIVERY_CHOICES, widget=forms.RadioSelect)
    delivery_time = forms.CharField(required=False)
    street = forms.CharField(required=False, max_length=255)
    apt_number = forms.CharField(required=False, max_length=50)
    city = forms.CharField(required=False, max_length=100)
    zip_code = forms.CharField(required=False, max_length=10)
    state = forms.CharField(required=False, max_length=50)
    card_number = forms.CharField(required=True, max_length=16)
    card_expiry = forms.CharField(required=True, max_length=5)
    card_cvc = forms.CharField(required=True, max_length=3)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_time = timezone.now().astimezone(pytz.timezone('US/Pacific'))
        time_choices = [('asap', 'ASAP')]

        pickup_times = [(current_time + datetime.timedelta(minutes=i * 20)).strftime('%I:%M %p') for i in range(1, 6)]
        delivery_times = [(current_time + datetime.timedelta(minutes=i * 40)).strftime('%I:%M %p') for i in range(1, 6)]

        unique_times = list(set(pickup_times + delivery_times))
        time_choices.extend([(time, time) for time in sorted(unique_times)])

        self.fields['delivery_time'].choices = time_choices

    def clean_delivery_time(self):
        delivery_time = self.cleaned_data.get('delivery_time')
        valid_delivery_times = [choice[0] for choice in self.fields['delivery_time'].choices]

        if delivery_time and delivery_time not in valid_delivery_times:
            raise forms.ValidationError('Invalid delivery time. Please choose from available options.')

        return delivery_time





from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'review_text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

