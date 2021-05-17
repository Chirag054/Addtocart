from django.contrib.auth.models import User
from django.db import models
from product.models import Product


class Cart(models.Model):

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(Product, through='CartItem', related_name='products')
    created_at = models.DateTimeField(auto_now=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0}´s Cart'.format(self.owner.username)

    def get_total(self) -> float:

        total = 0
        for item in self.cartitem_set.all():
            subtotal = item.quantity * item.product.price
            total += subtotal
        return total

    @staticmethod
    def create_cart_to_new_user(user: User):
        Cart.objects.create(owner=user)


class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.title

    def update(self, instance, **data):
        instance.quantity = data.quantity
        instance.save()
