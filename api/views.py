import logging
from typing import List

from django.conf import settings
from django_q.tasks import async_task
from ninja import NinjaAPI, Query
from ninja.security import HttpBearer

from jobs.models import Company, Email
from jobs.tasks import create_valid_emails

from .schemas import ReadCompany, ReadEmails

logger = logging.getLogger(__file__)


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == settings.API_TOKEN:
            return token


api = NinjaAPI(auth=GlobalAuth())


@api.get("/companies", response=List[ReadCompany])
def companies(request):
    logger.info(f"request: {request}")

    companies = Company.objects.all()
    logger.info(f"companies: {companies}")
    return companies


@api.get("/create-emails")
def create_emails(request):
    async_task(create_valid_emails)  # noqa: F821
    return "Task Started"


@api.get("/emails", response=ReadEmails)
def get_emails(
    request,
    is_valid: bool = True,
    with_names_only: bool = Query(False, alias="names"),
    exclude_generic_email: bool = Query(True, alias="exclude-generic"),
    only_approved: bool = Query(False, alias="only-approved"),
):
    emails = (
        Email.objects.select_related("company")
        .filter(email_is_valid=is_valid)
        .values("email", "name", "company__name", "company__compliment")
    )

    if with_names_only:
        emails = emails.exclude(name="")

    if exclude_generic_email:
        emails = emails.exclude(email_is_generic=True)

    if only_approved:
        emails = emails.filter(is_approved=True)

    unique_emails = emails.objects.values("email").distinct()

    return {
        "count": len(unique_emails),
        "emails": list(unique_emails),
    }
