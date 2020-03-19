import json

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from factory.django import DjangoModelFactory

from sample.models import Author, TodoItem, TodoList


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author


class TodoListFactory(DjangoModelFactory):
    class Meta:
        model = TodoList


class TodoItemTestCase(TestCase):
    def test_create_and_get_todo_item(self):
        author = AuthorFactory()
        todo_list = TodoListFactory(name="My List", author=author)
        TodoItem.objects.create(
            todo_list=todo_list,
            description="Give a presentation on Pytest",
            is_done=False,
        )

        item = TodoItem.objects.get(description="Give a presentation on Pytest")
        self.assertEqual(item.todo_list, todo_list)
        self.assertFalse(item.is_done)

    def test_is_done_is_required(self):
        author = AuthorFactory()
        todo_list = TodoListFactory(name="My List", author=author)
        item = TodoItem(
            todo_list=todo_list, description="Give a presentation on Pytest"
        )

        with self.assertRaises(IntegrityError):
            item.save()


class TodoListTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create()
        self.client.force_login(user)

    def tearDown(self):
        pass

    def test_list_todo_items(self):
        author = AuthorFactory()
        todo_list = TodoListFactory(name="My List", author=author)

        response = self.client.get(reverse("list_todo_lists"))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.json())
        self.assertEqual(len(data), 1)
