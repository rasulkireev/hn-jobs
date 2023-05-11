from ninja import Schema
from pydantic import UUID4


class ReadCompany(Schema):
    id: UUID4
    name: str
    company_homepage_link: str
