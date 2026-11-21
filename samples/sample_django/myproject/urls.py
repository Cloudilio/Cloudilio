from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, JsonResponse

def home(request):
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Django - Live on Cloudilio</title>
        <style>
            body { font-family: sans-serif; background: #f8fafc; color: #1e293b; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
            .card { background: white; padding: 2.5rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); text-align: center; max-width: 480px; }
            .badge { background: #dcfce7; color: #15803d; padding: 4px 12px; border-radius: 9999px; font-weight: bold; font-size: 0.85rem; }
        </style>
    </head>
    <body>
        <div class="card">
            <span class="badge">&bull; RUNNING</span>
            <h1>Django is Live!</h1>
            <p>Your Django web application is serving production requests via Gunicorn WSGI.</p>
        </div>
    </body>
    </html>
    """)

def health(request):
    return JsonResponse({"status": "healthy", "service": "django-app"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('health', health),
]
