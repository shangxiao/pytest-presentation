from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)


class TodoList(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class TodoItem(models.Model):
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    is_done = models.BooleanField()
