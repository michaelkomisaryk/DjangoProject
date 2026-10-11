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