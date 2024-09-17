from django.http import JsonResponse


def csrf_failure_view(request, reason=""):
    return JsonResponse(data={"detail": reason}, status=403)
