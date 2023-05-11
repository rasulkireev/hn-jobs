import logging
from typing import List

from ninja import NinjaAPI

from jobs.models import Company

from .schemas import ReadCompany

logger = logging.getLogger(__file__)

api = NinjaAPI()


@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}


@api.get("/companies", response=List[ReadCompany])
def companies(request):
    logger.info(f"request: {request}")

    companies = Company.objects.all()
    logger.info(f"companies: {companies}")
    return companies
