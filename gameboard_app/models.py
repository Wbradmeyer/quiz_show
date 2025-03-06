from django.db import models
from user_app.models import User
# from . forms import UploadFileForm

# GAMES
class GameManager(models.Manager):
    def game_validator(self, postData):
        errors = {}

        if len(postData['title']) < 2:
            errors['title'] = 'Title should be at least 2 characters.'
        return errors

class Game(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    creator = models.ForeignKey(User, related_name='gameboards', on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = GameManager()

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
        user = User.get_by_id(data['user_id'])
        return cls.objects.create(title=data['title'], creator=user)
    
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
    def destroy(cls, id):
        cls.objects.get(id=id).delete()

# CATEGORIES
class CategoryManager(models.Manager):
    def category_validator(self, postData):
        errors = {}

        if len(postData['name']) < 2:
            errors['name'] = 'Name should be at least 2 characters.'
        return errors
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    game_assigned = models.ForeignKey(Game, related_name="categories_avail", on_delete = models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CategoryManager()

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
    def destroy(cls, id):
        cls.objects.get(id=id).delete()

# QUESTIONS
class QuestionManager(models.Manager):
    def question_validator(self, postData):
        errors = {}

        if len(postData['question']) < 2:
            errors['question'] = 'Question should be at least 2 characters.'
        if len(postData['answer']) < 2:
            errors['answer'] = 'Answer should be at least 2 characters.'
        
        points = postData.get('points', '').strip()
        if not points.isdigit():
            errors['points'] = 'Points should be a valid number.'
        elif int(postData['points']) <= 0:
            errors['points'] = 'Points should be more than 0.'
        return errors
    
class Question(models.Model):
    question = models.TextField()
    # file = models.FileField(upload_to='question_files/', null=True, blank=True, default='')
    pic = models.ImageField(upload_to='question_images/', null=True, blank=True, default='')
    answer = models.CharField(max_length=255)
    points = models.IntegerField(default=100)
    played = models.BooleanField(default=False)
    category_assigned = models.ForeignKey(Category, related_name="question_list", on_delete = models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuestionManager()

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
        # file_form = data['file']
        pic_form = data['pic']
        question =  cls.objects.create(question=data['question'],
                                    answer=data['answer'], 
                                    points=data['points'], 
                                    category_assigned=data['category_assigned'])
        if pic_form:
            if pic_form.is_valid():
                # question.file = file_form.cleaned_data['file']
                question.pic = pic_form.cleaned_data['pic']
                question.save()
            else:
                print('*************NOT VALID********8')
        return question
    
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
    def reset_all_questions(cls):
        questions = cls.get_all()
        for question in questions:
            question.played = False
            question.save()
        return

    @classmethod
    def destroy(cls, id):
        cls.objects.get(id=id).delete()