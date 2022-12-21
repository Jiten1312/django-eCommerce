from django.db import models
import datetime
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils import timezone
from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)

    # indicates the city where warehouses for this category of products is located
    # Add a new required field warehouse 
    warehouse = models.CharField(blank=False, default='', max_length=200)

    def __str__(self):
        return 'Category: ' + self.name + ' Warehouse: ' + self.warehouse


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    name = models.CharField(max_length=200)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.PositiveIntegerField(default=100, validators=[
        MaxValueValidator(1000),
        MinValueValidator(0)
    ])

    available = models.BooleanField(default=True)

    # This field indicates how many people are interested in this product. The default value for the field is 0.
    interested = models.PositiveIntegerField(default=0)

    # blank=True makes field optional
    description = models.TextField(blank=True)

    # This method is used to replenishments for a particular product. When refill(self) is called, it adds 50 to
    # the current value of the stock field for the specified product
    # Method for Feature3
    def refill(self):
        self.stock += 50
        self.available = True
        self.save()

    def __str__(self):
        return 'Product: ' + self.name + ' Price: ' + str(self.price) + ' Stock: ' + str(
            self.stock) + ' Available: ' + str(self.available) + ' Category: ' + self.category.name


class Client(User):
    PROVINCE_CHOICES = [
        (
            'AB', 'Alberta'
        ),
        (
            'MB', 'Manitoba'
        ),
        (
            'ON', 'Ontario'
        ),
        (
            'QC', 'Quebec'
        ), ]

    company = models.CharField(max_length=50, blank=True)

    shipping_address = models.CharField(max_length=300, null=True, blank=True)

    city = models.CharField(max_length=20, default='Windsor')

    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')

    interested_in = models.ManyToManyField(Category, blank=True)

    image = models.ImageField(null=True, blank=True, upload_to='images/')

    # method for Feature2
    def interests(self):
        return ", ".join([category.name for category in self.interested_in.all()])

    def __str__(self):
        return 'Client: ' + self.first_name + ' ' + self.last_name + ' City: ' + self.city + ' Province: ' + self.province


class Center(models.Model):
    # Update the name field of Center model to be unique.
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=100)


class Course(models.Model):
    type = models.CharField(max_length=50)
    # Make the field number the primary key for the model Course
    number = models.IntegerField(primary_key=True)
    price = models.IntegerField()
    min_age = models.IntegerField()
    # Update the Course model to indicate that description field is optional.
    description = models.CharField(max_length=200, blank=True)
    available = models.BooleanField()
    # create a new field Center in Course model that refers to an instance of Center model with
    # “many-to-one” relationship. So, a center can provide many courses and each course is provided by
    # exactly one center.
    center = models.ForeignKey(Center, related_name='center_course', on_delete=models.CASCADE)

    def __str__(self):
        return 'Type:' + self.type + 'Center Name: ' + self.center.name


class Order(models.Model):
    # indicates the product that was ordered
    product = models.ForeignKey(Product, related_name='order_product', on_delete=models.CASCADE)

    # indicates the client that ordered the product
    client = models.ForeignKey(Client, related_name='order_client', on_delete=models.CASCADE)

    # indicates how many items were ordered
    num_units = models.PositiveIntegerField()

    ORDER_STATUS_CHOICES = [
        (
            0, 'Order Cancelled'
        ),
        (
            1, 'Order Placed'
        ),
        (
            2, 'Order Shipped'
        ),
        (
            3, 'Order Delivered'
        ), ]

    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)

    # indicates the date the order_status was last updated
    status_date = models.DateTimeField(default=now)

    # For the Order model, write a method total_cost(self) that returns the total cost for all items in the order.
    def total_cost(self):
        return self.product.price * self.num_units

    def __str__(self):
        return 'Order: ' + self.product.name + ' Client: ' + self.client.username + ' Num_units: ' + str(self.num_units)


class PasswordReset(models.Model):
    username = models.CharField(max_length=200)

    def __str__(self):
        return self.username
