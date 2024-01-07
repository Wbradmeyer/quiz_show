from django.contrib import admin

# Register your models here.
from .models import Game
from .models import Category
from .models import Question

admin.site.register(Game)
admin.site.register(Category)
admin.site.register(Question)