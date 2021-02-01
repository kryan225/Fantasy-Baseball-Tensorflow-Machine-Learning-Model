from django.db import models

class TodoItem(models.Model):
    content = models.TextField()

class League(models.Model):
    name = models.CharField(max_length = 30)

class Team(models.Model):
    name = models.CharField(max_length=30)
    league = models.ForeignKey(League, on_delete=models.PROTECT, null=True)
    

class Batter(models.Model):
    name = models.CharField(max_length=50)
    pos = models.IntegerField()
    ab = models.IntegerField()
    h = models.IntegerField()
    r = models.IntegerField()
    hr = models.IntegerField()
    rbi = models.IntegerField()
    sb = models.IntegerField()
    salary = models.IntegerField()
    team =  models.ForeignKey(Team, on_delete=models.PROTECT, null=True)


    

