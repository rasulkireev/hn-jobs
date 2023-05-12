import logging
from typing import List

from django_q.tasks import async_task
from ninja import NinjaAPI, Query

from jobs.models import Company, Email
from jobs.tasks import create_valid_emails

from .schemas import ReadCompany, ReadEmail

logger = logging.getLogger(__file__)

api = NinjaAPI()


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


@api.get("/emails", response=List[ReadEmail])
def get_emails(request, is_valid: bool = True, with_names_only: bool = Query(False, alias="names")):
    emails = (
        Email.objects.select_related("company")
        .filter(email_is_valid=is_valid)
        .values("email", "name", "company__name", "company__compliment")
    )

    if with_names_only:
        emails = emails.exclude(name="")

    return emails
