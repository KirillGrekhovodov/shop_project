from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView

from webapp.forms import CartForm
from webapp.models import Cart, Product


class CartAddView(CreateView):
    model = Cart
    form_class = CartForm

    def form_invalid(self, form):
        return HttpResponseBadRequest(f"некорректное количество товара")

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get("pk"))
        qty = form.cleaned_data.get("qty")

        try:
            cart = Cart.objects.get(product=product)
            full_qty = qty + cart.qty
        except Cart.DoesNotExist:
            full_qty = qty

        if full_qty > product.amount:
            return HttpResponseBadRequest(f"Количество товара {product.title} всего {product.amount} штук")
        else:
            cart_product, is_created = Cart.objects.get_or_create(product=product)
            if is_created:
                cart_product.qty = qty
            else:
                cart_product.qty += qty
            cart_product.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next = self.request.GET.get("next")
        if next:
            return next
        return reverse("webapp:index")


class CartView(ListView):
    model = Cart
    context_object_name = "cart_list"
    template_name = "cart/cart_view.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['total'] = Cart.get_full_total()
        return context
