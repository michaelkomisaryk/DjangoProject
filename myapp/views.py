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