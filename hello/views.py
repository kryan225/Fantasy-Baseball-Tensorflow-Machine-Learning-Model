from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import TodoItem
import DataManipulation as DataManipulation
from Team import Team
from Batter import Batter
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
