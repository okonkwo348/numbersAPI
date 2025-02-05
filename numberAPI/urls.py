from django.urls import path
from .views import classify_number

urlpatterns=[
    path('number/', classify_number, name="classify_number"),
]
