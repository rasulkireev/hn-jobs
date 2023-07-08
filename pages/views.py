import logging

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView, UpdateView
from django_q.tasks import async_task

from hn_jobs.utils import add_users_context
from jobs.models import Post
from jobs.queries import get_latest_submissions, get_most_popular_technologies, get_most_popular_titles
from users.models import Subscriber

from .forms import CreateAlertForm, SupportForm, UpdateAlertForm
from .tasks import email_support_request, send_confirmation_email

logger = logging.getLogger(__file__)


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["jobs"] = (
            Post.objects.exclude(description__isnull=True).exclude(description__exact="").order_by("-created")[:8]
        )
        context["latest_job_submissions"] = get_latest_submissions(9, for_homepage=True)
        context["popular_titles"] = get_most_popular_titles()
        context["popular_technologies"] = get_most_popular_technologies(min_count=2)
        context["num_of_jobs"] = len(Post.objects.all())
        context["create_alert_form"] = CreateAlertForm

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


class AlertCreateView(SuccessMessageMixin, CreateView):
    template_name = "pages/create-alert.html"
    model = Subscriber
    form_class = CreateAlertForm
    success_url = reverse_lazy("home")
    success_message = "Thanks for subscribing :) Check your emails to confirm!"

    def form_valid(self, form):
        if Subscriber.objects.filter(email=form.instance.email).exists():
            messages.add_message(self.request, messages.WARNING, "An alert already exists for this email.")
            return redirect("home")

        confirmation_url = self.request.build_absolute_uri(reverse("confirm_subscription", args=[form.instance.id]))
        async_task(send_confirmation_email, form.cleaned_data, confirmation_url)
        return super(AlertCreateView, self).form_valid(form)


class AlertUpdateView(SuccessMessageMixin, UpdateView):
    model = Subscriber
    form_class = UpdateAlertForm
    template_name = "pages/subscription-confirmation.html"
    success_url = reverse_lazy("home")
    success_message = "Thanks for confirming :) You will receive your alerts soon!"
