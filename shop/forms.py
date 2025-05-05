from django import forms
from .models import Profile, Product


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'date_of_birth', 'gender']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


# ✅ NEW: ProductForm for users to add/edit their own products
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['owner', 'slug']  # owner set in view, slug auto-generated

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'discount_price': forms.NumberInput(attrs={'step': '0.01'}),
        }
