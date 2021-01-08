from django.db import models


# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50, default="")
    brand = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=1000, default="")
    category = models.CharField(max_length=20, default="")
    gender = models.CharField(max_length=1, default="")
    price = models.IntegerField(default=0)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="", editable=False)
    email = models.CharField(max_length=70, default="", editable=False)
    phone = models.CharField(max_length=70, default="", editable=False)
    desc = models.CharField(max_length=500, default="", editable=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True, editable=False)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0, editable=False)
    name = models.CharField(max_length=90, editable=False)
    email = models.CharField(max_length=70, editable=False)
    address = models.CharField(max_length=500, editable=False)
    city = models.CharField(max_length=100, editable=False)
    state = models.CharField(max_length=100, editable=False)
    zip_code = models.CharField(max_length=100, editable=False)
    phone = models.CharField(max_length=100, default="", editable=False)

    def __str__(self):
        return self.name


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."