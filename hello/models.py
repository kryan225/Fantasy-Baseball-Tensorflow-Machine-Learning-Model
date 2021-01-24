from django.db import models

class TodoItem(models.Model):
    content = models.TextField()

'''TODO: 
Team:
    name:: Sring
    currentSalary:: Int
    catcher1:: Batter_Id
    catcher2:: Batter_Id
    firstBasemen:: Batter_Id
    ...

Batter:
    name:: String
    position:: Int
    salary:: Int
    atBats:: Int
    hits:: Int
    ...


'''