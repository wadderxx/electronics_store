from django.db import models


class Product(models.Model):
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
