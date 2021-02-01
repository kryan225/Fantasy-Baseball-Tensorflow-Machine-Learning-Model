from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import TodoItem
from .models import Batter
import DataManipulation as DataManipulation
from Team import Team
#from Batter import Batter
import DraftTool2020 as Tool 



def myView(request):
    all_todo_items = TodoItem.objects.all()
    ll = Tool.ll
    print("team:")
    
    print(ll.getTeams())
    print("------------------------")
    return render(request, 'test.html', {'all_items': all_todo_items})


def addTodo(request):
    new_item = TodoItem(content = request.POST['content'])
    new_item.save()
    return HttpResponseRedirect('/sayHello/')

def deleteTodo(request, todo_id):
    item_to_delete = TodoItem.objects.get(id=todo_id)
    item_to_delete.delete()
    return HttpResponseRedirect('/sayHello/')

def customBatter(request):
    all_batter_items = Batter.objects.all()
    return render(request, 'customBatter.html', {'all_batters': all_batter_items})


def addBatter(request):
    new_batter = Batter(name = request.POST['name'],
                        pos = request.POST['pos'],
                        ab = request.POST['ab'],
                        h = request.POST['h'],
                        r = request.POST['r'],
                        rbi = request.POST['rbi'],
                        hr = request.POST['hr'],
                        sb = request.POST['sb'],
                        salary = request.POST['salary'])
    new_batter.save()
    return HttpResponseRedirect('/customBatter/')

def deleteBatter(request, batter_id):
    batter_to_delete = Batter.objects.get(id=batter_id)
    batter_to_delete.delete()
    return HttpResponseRedirect('/customBatter/')




