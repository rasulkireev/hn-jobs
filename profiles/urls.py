from django.urls import path

from .views import ProfileListView, ProfileDetailView, TriggerAsyncTask

urlpatterns = [
    path("", ProfileListView.as_view(), name="profiles"),
    path("<uuid:pk>", ProfileDetailView.as_view(), name="profile"),
    path('trigger-task/', TriggerAsyncTask.as_view(), name='trigger_task'),
]
