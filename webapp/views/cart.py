from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView

from webapp.forms import CartForm, OrderForm
from webapp.models import Cart, Product, Order, OrderProduct


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
        context['form'] = OrderForm()
        return context


class CartDeleteView(DeleteView):
    model = Cart
    success_url = reverse_lazy('webapp:cart')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class CartDeleteOneView(DeleteView):
    model = Cart
    success_url = reverse_lazy('webapp:cart')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        self.object.qty -= 1
        if self.object.qty < 1:
            self.object.delete()
        else:
            self.object.save()
        return HttpResponseRedirect(success_url)


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("webapp:index")

    # def form_valid(self, form):
    #     order = form.save()
    #     print(order)
    #
    #     for item in Cart.objects.all():
    #         OrderProduct.objects.create(order=order, product=item.product, qty=item.qty)
    #         item.product.amount -= item.qty
    #         item.product.save()
    #         item.delete()
    #
    #     return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        return HttpResponseBadRequest(form.errors['__all__'])

    def form_valid(self, form):
        order = form.save()

        products = []
        order_products = []

        for item in Cart.objects.all():
            order_products.append(OrderProduct(order=order, product=item.product, qty=item.qty))
            item.product.amount -= item.qty
            products.append(item.product)

        OrderProduct.objects.bulk_create(order_products)
        Product.objects.bulk_update(products, ('amount',))
        Cart.objects.all().delete()

        return HttpResponseRedirect(self.success_url)

