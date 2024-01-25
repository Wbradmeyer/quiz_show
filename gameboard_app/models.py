from django.db import models
from user_app.models import User

# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    creator = models.ForeignKey(User, related_name='gameboards', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @classmethod
    def get_all(cls):
        return cls.objects.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(id=id)

    @classmethod
    def add_game(cls, data):
        return cls.objects.create(title=data['title'], creator=data['user_id'])
    
    @classmethod
    def update(cls, data):
        game = cls.objects.get(id=data['id'])
        game.title = data['title']
        game.save()
        return game
    
    @classmethod
    def update_activity(cls, data):
        game = cls.objects.get(id=data['id'])
        game.is_active = data['is_active']
        game.save()
        return game
    
    @classmethod
    def reset_categories(cls, data):
        game = cls.objects.get(id=data['id'])
        for category in game.categories_avail:
            category.reset_questions({'id': category.id})
        return

    @classmethod
    def destroy(cls, id):
        cls.objects.get(id=id).delete()


class Category(models.Model):
    name = models.CharField(max_length=255)
    game_assigned = models.ForeignKey(Game, related_name="categories_avail", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.objects.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(id=id)
    
    @classmethod
    def add_category(cls, data):
        return cls.objects.create(name=data['name'], game_assigned=data['game_assigned'])

    @classmethod
    def update(cls, data):
        category = cls.objects.get(id=data['id'])
        category.name = data['name']
        category.save()
        return category
    
    @classmethod
    def reset_questions(cls, data):
        category = cls.objects.get(id=data['id'])
        for question in category.question_list:
            question.update_played({'id': question.id, 'played': False})
        return

    @classmethod
    def destroy(cls, id):
        cls.objects.get(id=id).delete()


class Question(models.Model):
    question = models.TextField()
    answer = models.CharField(max_length=255)
    points = models.IntegerField(default=100)
    played = models.BooleanField(default=False)
    category_assigned = models.ForeignKey(Category, related_name="question_list", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question[0:30]

    @classmethod
    def get_all(cls):
        return cls.objects.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(id=id)
    
    @classmethod
    def add_question(cls, data):
        return cls.objects.create(question=data['question'], answer=data['answer'], 
                                points=data['points'], category_assigned=data['category_assigned'])
    
    @classmethod
    def update(cls, data):
        question = cls.objects.get(id=data['id'])
        question.question = data['question']
        question.answer = data['answer']
        question.points = data['points']
        question.save()
        return question
    
    @classmethod
    def update_played(cls, data):
        question = cls.objects.get(id=data['id'])
        question.played = data['played']
        question.save()
        return

    @classmethod
    def destroy(cls, id):
        cls.objects.get(id=id).delete()