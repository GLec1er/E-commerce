from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from shop.models import User, Product, SellerProfile, StoreName
from shop.models.product import Discount


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email address",
            "title": "Enter a valid phone number (e.g., +1234567890)"
        }),
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your phone number",
            "title": "Enter a valid phone number (e.g., +1234567890)"
        })
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'phone',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Choose a username",
            "title": "Enter a unique username"
        })
        self.fields['password1'].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter your password",
            "title": "Enter a secure password with at least 8 characters"
        })
        self.fields['password2'].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirm your password",
            "title": "Passwords must match"
        })


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class SellerProfileForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=True)
    is_active = forms.BooleanField(required=False)
    logo = forms.ImageField(required=False)

    class Meta:
        model = SellerProfile
        fields = ['description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Предзаполняем поля данными из связанной модели StoreName
        if self.instance and self.instance.store_name:
            self.fields['name'].initial = self.instance.store_name.name
            self.fields['is_active'].initial = self.instance.store_name.is_active
            self.fields['logo'].initial = self.instance.store_name.logo

    def save(self, commit=True):
        # Сохраняем SellerProfile
        instance = super().save(commit=False)

        # Сохраняем или создаем связанный StoreName
        store_name = instance.store_name or StoreName()
        store_name.name = self.cleaned_data['name']
        store_name.is_active = self.cleaned_data['is_active']
        store_name.logo = self.cleaned_data['logo']

        if commit:
            store_name.save()
            instance.store_name = store_name
            instance.save()

        return instance


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('owner',)
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'quantity_in_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-select'}),
            'material': forms.Select(attrs={'class': 'form-select'}),
            'discount': forms.Select(attrs={'class': 'form-select'}),
        }

    rating = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))


class ShopForm(forms.ModelForm):
    class Meta:
        model = StoreName
        fields = ['name', 'logo']

    def save(self, commit=True, user=None):
        if not user:
            raise ValidationError("Пользователь обязателен для создания магазина.")
        store = super().save(commit=False)

        seller_profile, created = SellerProfile.objects.get_or_create(user=user)
        store.save()
        seller_profile.store_name = store
        seller_profile.save()

        if not user.is_sealer:
            user.is_sealer = True
            user.save(update_fields=['is_sealer'])

        return store


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['name', 'description', 'discount_type', 'value', 'start_date', 'end_date']

    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea, required=False)
    discount_type = forms.ChoiceField(choices=Discount.DISCOUNT_TYPES)
    value = forms.DecimalField(max_digits=5, decimal_places=2)
    start_date = forms.DateField(widget=forms.SelectDateWidget())
    end_date = forms.DateField(widget=forms.SelectDateWidget())
