from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=40, unique=True)


class Recept(models.Model):
    title = models.CharField(max_length=20)
    decription = models.CharField(max_length=250)
    hours = models.IntegerField()
    status = models.CharField(max_length=7,
                              choices=[('easy', 'Легко'), ('medium',
                                                           'Средне'), ('hard', 'Сложно')]
                              )
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    on_delete = models.BooleanField(default=False)
    # create_at = models.DateTimeField(auto_now_add=True)


class ReceptPhoto(models.Model):
    recept = models.ForeignKey(Recept, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='recept/')


class Ingredient(models.Model):
    title = models.CharField(max_length=20, unique=True)
    measure = models.CharField(
        max_length=7,
        choices=[
            ('шт', 'Штуки'),
            ('л', 'Литры'),
            ('кг', 'Килограммы'),
            ('мг', 'Миллиграммы'),
            ('ст.л.', 'Ст. ложки'),
        ],
    )


class Step(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='step/')
    recept = models.ForeignKey(
        Recept, on_delete=models.CASCADE, null=True, blank=True)


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recept = models.ForeignKey(Recept, on_delete=models.CASCADE)


class Order(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[
                              ('paid', 'оплачено'), ('unpaid', 'не оплачено'), ('error', 'ошибка оплаты'), ('timeout', 'истекло время на оплату')])


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recept = models.ForeignKey(Recept, on_delete=models.CASCADE)
    favorited_at = models.DateTimeField(auto_now_add=True)
