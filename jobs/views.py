import logging

from django.views.generic import DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from django.urls import reverse_lazy
from django_q.tasks import async_task, result
from django_filters.views import FilterView
from django.core.paginator import Paginator

from .models import Post
from .tasks import analyze_hn_page
from .filters import PostFilter

from hn_jobs.utils import floor_to_tens, add_users_context


logger = logging.getLogger(__file__)

class PostListView(FilterView):
    model = Post
    template_name = "jobs/all_jobs.html"
    queryset = Post.objects.all()
    filterset_class = PostFilter
    paginate_by = 11

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_of_jobs"] = floor_to_tens(len(Post.objects.all()))

        user = self.request.user
        if user.is_authenticated:
            add_users_context(context, user)

        return context

# class JobDetailView(DetailView):
#     model = Job
#     template_name = "jobs/Job_detail.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         user = self.request.user
#         if user.is_authenticated:
#             add_users_context(context, user)

#         if self.object:
#             context["Job_capacity"] = self.object.capacity.split(",")

#         return context


class GenericForm(forms.Form):
    who_is_hiring_post_id = forms.CharField()

class TriggerAsyncTask(LoginRequiredMixin, UserPassesTestMixin, FormView):
    login_url = "account_login"
    success_url = reverse_lazy("home")
    template_name = "jobs/trigger_task.html"
    form_class = GenericForm

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        who_is_hiring_post_id = form.cleaned_data.get('who_is_hiring_post_id')
        async_task(analyze_hn_page, who_is_hiring_post_id, hook='hooks.print_result')
        return super(TriggerAsyncTask, self).form_valid(form)