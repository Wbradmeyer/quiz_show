from django.db import models

# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Category(models.Model):
    name = models.CharField(max_length=255)
    game_assigned = models.ForeignKey(Game, related_name="categories_avail", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Question(models.Model):
    question = models.TextField()
    answer = models.CharField(max_length=255)
    points = models.IntegerField(default=100)
    category_assigned = models.ForeignKey(Category, related_name="question_list", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)