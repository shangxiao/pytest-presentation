from django.urls import include, path

from .views import list_todo_lists

urlpatterns = [path("/todo-lists/", list_todo_lists, name='list_todo_lists')]
