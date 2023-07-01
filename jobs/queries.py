from django.db.models import Max

from jobs.models import Post


def get_latest_submissions(number_of: int):
    return Post.objects.annotate(latest_datetime=Max("submitted_datetime")).order_by("-latest_datetime")[:number_of]
