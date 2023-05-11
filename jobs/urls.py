from django.urls import path

from .views import PostListView, TriggerAsyncTask  # , JobDetailView

urlpatterns = [
    path("", PostListView.as_view(), name="posts"),
    # path("<uuid:pk>", JobDetailView.as_view(), name="job"),
    path("trigger-task/", TriggerAsyncTask.as_view(), name="trigger_task"),
]
