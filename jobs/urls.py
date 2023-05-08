from django.urls import path

from .views import PostListView, TriggerAsyncTask, api

urlpatterns = [
    path("", PostListView.as_view(), name="posts"),
    path("api/", api.urls),
    # path("<uuid:pk>", JobDetailView.as_view(), name="job"),
    path('trigger-task/', TriggerAsyncTask.as_view(), name='trigger_task'),
]
