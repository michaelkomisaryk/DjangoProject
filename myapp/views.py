from .models import Task
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def hello(request, name):
    return JsonResponse({
        "message": f"Hello, {name}"
    })


def hello_with_age(request, name, age):
    return JsonResponse({
        "message": f"Hello, {name}",
        "age": age
    })

def greeting(request):
    name= request.GET.get("name", "Guest")
    uppercase = request.GET.get("uppercase", "false")

    message = f"Hello, {name}"

    if uppercase.lower() == "true":
        message = message.upper()

    return JsonResponse({
        "message": message
    })

def status_view(request, code):
    if code == 200:
        return JsonResponse({"message": "Request successful"}, status=200)
    if code == 400:
        return JsonResponse({"message": "Bad request"}, status=400)
    if code == 404:
        return JsonResponse({"message": "Not found"}, status=404)

@csrf_exempt
def echo(request):
    if request.method == "POST":
        data = json.loads(request.body)

        if not isinstance(data, dict):
            return JsonResponse({"error": "Invalid data"}, status=400)

        title = data.get("title")

        if not isinstance(title, str) or not title.strip():
            return JsonResponse({"error": "Title is required"}, status=400)

        if len(title) >= 100:
            return JsonResponse({"error": "Title must be shorter than 100 characters"}, status=400)

        description = data.get("description")

        if not isinstance(description, str) or not description.strip():
            return JsonResponse({"error": "Description is required"}, status=400)

        return JsonResponse(data)
    return JsonResponse({"message": "Only POST can send request"}, status=400)

tasks = []

@csrf_exempt
def task_list(request):
    if request.method == "GET":
        tasks = Task.objects.all()

        return JsonResponse({
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at
                }
                for task in tasks
            ]
        })

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        if not isinstance(data, dict):
            return JsonResponse({"error": "Invalid data"}, status=400)

        title = data.get("title")
        description = data.get("description", "")

        if not isinstance(title, str) or not title.strip():
            return JsonResponse({"error": "Title is required"}, status=400)

        if not isinstance(description, str):
            return JsonResponse({"error": "Invalid description"}, status=400)

        task = Task.objects.create(
            title=title.strip(),
            description=description.strip()
        )

        return JsonResponse({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at
        }, status=201)

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405
    )


@csrf_exempt
def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

    if request.method == "GET":
        return JsonResponse({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat()
        })

    if request.method == "PUT":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        if not isinstance(data, dict):
            return JsonResponse({"error": "Invalid data"}, status=400)

        title = data.get("title", task.title)
        description = data.get("description", task.description)
        completed = data.get("completed", task.completed)

        if not isinstance(title, str) or not title.strip():
            return JsonResponse({"error": "Title is required"}, status=400)

        if len(title.strip()) >= 100:
            return JsonResponse({"error": "Title must be shorter than 100 characters"}, status=400)

        if not isinstance(description, str):
            return JsonResponse({"error": "Invalid description"}, status=400)

        if not isinstance(completed, bool):
            return JsonResponse({"error": "Invalid completed value"}, status=400)

        task.title = title.strip()
        task.description = description.strip()
        task.completed = completed
        task.save()

        return JsonResponse({
            "message": "Task updated successfully",
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat()
        })

    if request.method == "DELETE":
        task.delete()

        return JsonResponse({
            "message": "Task deleted successfully"
        })

    return JsonResponse({"error": "Method not allowed"}, status=405)


