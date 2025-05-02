from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin_title = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Admin Profile: {self.user.username}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female")],
        blank=True,
        null=True
    )
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.parent.name} > {self.name}" if self.parent else self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    availability = models.BooleanField(default=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    best_deal = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def sub_total(self):
        return (self.product.discount_price if self.product.discount_price else self.product.price) * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.product.name} (x{self.quantity})"

    class Meta:
        unique_together = ('user', 'product')


class ShippingOption(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    note = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} - {self.price}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username}'s Wishlist: {self.product.name}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    PAYMENT_CHOICES = (
        ('Cash on Delivery', 'Cash on Delivery'),
        ('Bkash', 'Bkash'),
        ('Nagad', 'Nagad'),
        ('Card', 'Card'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_option = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='Cash on Delivery')
    shipping_address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
    @property
    def total_amount(self):
        return sum(item.total_price() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return (self.product.discount_price if self.product.discount_price else self.product.price) * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Order {self.order.id}"


class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} review of {self.product.name}"
    


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
