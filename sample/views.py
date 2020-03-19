from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse

from sample.models import TodoList


@login_required
def list_todo_lists(request):
    todo_lists = TodoList.objects.all()
    data = serializers.serialize("json", todo_lists)
    return JsonResponse(data, safe=False)
