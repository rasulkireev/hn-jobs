import logging

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django_q.tasks import async_task

from hn_jobs.utils import add_users_context, floor_to_thousands
from jobs.models import Post

from .forms import SupportForm
from .tasks import email_support_request

logger = logging.getLogger(__file__)


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["jobs"] = (
            Post.objects.exclude(description__isnull=True).exclude(description__exact="").order_by("-created")[:8]
        )
        context["num_of_jobs"] = len(Post.objects.all())

        if user.is_authenticated:
            add_users_context(context, user)

        return context


class PricingView(TemplateView):
    template_name = "pages/pricing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            add_users_context(context, user)

        return context


class SupportView(FormView):
    template_name = "pages/support.html"
    form_class = SupportForm

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.INFO,
            "Thanks for sending your feedback. I'll get back to you ASAP.",
        )
        return reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if user.is_authenticated:
            add_users_context(context, user)

        return context

    def form_valid(self, form):
        async_task(email_support_request, form.cleaned_data, hook="hooks.email_sent")
        return super(SupportView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["current_user"] = self.request.user
        return kwargs
