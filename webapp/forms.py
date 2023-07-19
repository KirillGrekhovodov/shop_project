from django import forms

from webapp.models import Product, Cart


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, required=False, label="Найти")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ["qty"]
