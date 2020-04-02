import json

import pytest
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from factory.django import DjangoModelFactory

from sample.models import Author, TodoItem, TodoList


pytestmark = pytest.mark.django_db


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author


class TodoListFactory(DjangoModelFactory):
    class Meta:
        model = TodoList


@pytest.fixture
def author():
    return AuthorFactory()


def test_create_and_get_todo_item(author):
    todo_list = TodoListFactory(name="My List", author=author)
    TodoItem.objects.create(
        todo_list=todo_list,
        description="Give a presentation on Pytest",
        is_done=False,
    )

    item = TodoItem.objects.get(description="Give a presentation on Pytest")
    assert item.todo_list == todo_list
    assert item.is_done is False


def test_is_done_is_required(author):
    todo_list = TodoListFactory(name="My List", author=author)
    item = TodoItem(
        todo_list=todo_list, description="Give a presentation on Pytest"
    )

    with pytest.raises(IntegrityError):
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

        assert response.status_code == 200
        data = json.loads(response.json())
        assert len(data) == 1
