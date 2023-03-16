import logging

from django.views.generic import DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from django.urls import reverse_lazy
from django_q.tasks import async_task, result
from django_filters.views import FilterView

from .models import Profile
from .tasks import analyze_hn_page
from .filters import ProfileFilter

from hackernews_developers.utils import floor_to_tens, add_users_context


logger = logging.getLogger(__file__)

class ProfileListView(FilterView):
    model = Profile
    template_name = "profiles/all_profiles.html"
    queryset = Profile.objects.all()
    filterset_class = ProfileFilter
    paginate_by = 11

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_of_profiles"] = floor_to_tens(len(Profile.objects.all()))

        user = self.request.user
        if user.is_authenticated:
            add_users_context(context, user)

        return context

class ProfileDetailView(DetailView):
    model = Profile
    template_name = "profiles/profile_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if user.is_authenticated:
            add_users_context(context, user)

        if self.object:
            context["profile_capacity"] = self.object.capacity.split(",")

        return context


class GenericForm(forms.Form):
    who_wants_to_be_hired_post_id = forms.CharField()

class TriggerAsyncTask(LoginRequiredMixin, UserPassesTestMixin, FormView):
    login_url = "account_login"
    success_url = reverse_lazy("home")
    template_name = "profiles/trigger_task.html"
    form_class = GenericForm

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        who_wants_to_be_hired_post_id = form.cleaned_data.get('who_wants_to_be_hired_post_id')
        async_task(analyze_hn_page, who_wants_to_be_hired_post_id, hook='hooks.print_result')
        return super(TriggerAsyncTask, self).form_valid(form)