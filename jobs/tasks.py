import re
import json
import httpx
import logging
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django_q.models import Schedule
import openai

from .models import Post, Technology, Company, Title
from .utils import clean_job_json_object

logger = logging.getLogger(__file__)
openai.api_key = settings.OPENAI_KEY

def analyze_hn_page(who_is_hiring_post_id):
    r = httpx.get(f'https://hacker-news.firebaseio.com/v0/item/{who_is_hiring_post_id}.json').json()

    who_is_hiring_id = int(r['id'])
    who_is_hiring_title = str(re.search('\(([^)]+)', r['title']).group(1))

    list_of_comment_ids = r["kids"]

    # if working in dev don't want to go through all the comments
    if settings.DEBUG:
        list_of_comment_ids = list_of_comment_ids[:150]

    for comment_id in list_of_comment_ids:
        if not Post.objects.filter(who_is_hiring_comment_id=comment_id).exists():
            logger.info(f"Analyzing comment {comment_id}")
            json_job = httpx.get(f'https://hacker-news.firebaseio.com/v0/item/{comment_id}.json').json()

            try:
              if json_job["deleted"] == True:
                  continue
            except KeyError:
                  pass

            who_is_hiring_comment_id = int(json_job['id'])
            hn_username = str(json_job['by'])

            request = f"""Convert the following text:
                ```
                {json_job['text']}
                ```
                into a JSON object with the following valid keys
                (feel free to give me an value of empty string if there is no info,
                also ignore the content in  brackets, it is only to explain what I need):

                company_name - (string)
                job_titles - (string of comma separated values)
                locations - (string of comma separated values)
                cities - (string of comma separated values)
                countries - (string of comma separated values)
                compensation_summary - (string)
                is_remote - (boolean)
                remote_timezones - (string of comma separated values)
                is_onsite - (boolean)
                capacity - (string of comma separated values)
                description
                technologies_used - (string of comma separated values)
                company_homepage_link - (url link)
                emails - (string of comma separated values)
                company_job_application_link - (url link)
                names_of_the_contact_person - (string of comma separated values)
                years_of_experience - (string of comma separated values)
                levels_of_experience - (string of comma separated values)

                Don't add any text and only respond with a JSON Object.
            """

            completion = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": request
                }
              ]
            )

            converted_comment_response = completion.choices[0].message

            try:
              json_converted_comment_response = json.loads(converted_comment_response.content)
            except json.decoder.JSONDecodeError:
              continue


            cleaned_data = clean_job_json_object(json_job, json_converted_comment_response)

            technology_names = [name.strip() for name in cleaned_data['technologies_used'].split(',')]
            technologies = []
            for name in technology_names:
                if name != "":
                    obj, _ = Technology.objects.get_or_create(name=name)
                    technologies.append(obj)

            job_title_names = [name.strip() for name in cleaned_data['job_titles'].split(',')]
            job_titles = []
            for job_title in job_title_names:
                if job_title != "":
                    obj, _ = Title.objects.get_or_create(name=job_title)
                    job_titles.append(obj)

            if cleaned_data["company_name"] != "":
                company_obj, _ = Company.objects.get_or_create(name = cleaned_data["company_name"])
                company_obj.company_homepage_link = cleaned_data["company_homepage_link"]
                company_obj.emails += cleaned_data["emails"]
                company_obj.save()

            post = Post(
                who_is_hiring_id=who_is_hiring_id,
                who_is_hiring_title=who_is_hiring_title,
                who_is_hiring_comment_id=who_is_hiring_comment_id,
                company=company_obj,
                hn_username=hn_username,
                description=cleaned_data['description'],
                locations=cleaned_data['locations'],
                cities=cleaned_data['cities'],
                countries=cleaned_data['countries'],
                is_remote=cleaned_data['is_remote'],
                remote_timezones = cleaned_data['remote_timezones'],
                is_onsite=cleaned_data['is_onsite'],
                years_of_experience=cleaned_data['years_of_experience'],
                capacity=cleaned_data['capacity'],
                compensation_summary=cleaned_data['compensation_summary'],
                company_job_application_link=cleaned_data['company_job_application_link'],
                names_of_the_contact_person=cleaned_data['names_of_the_contact_person'],
                levels_of_experience=cleaned_data['levels_of_experience'],
                emails=cleaned_data['emails'],
            )
            post.save()
            post.technologies_used.add(*technologies)
            post.job_titles.add(*job_titles)

            logger.info(f"{post} post was created.")
        else:
          logger.info(f"Job for {comment_id} already exists.")

    return f"Task Completed"


# Schedule.objects.create(
#     func=analyze_hn_page,
#     args=34983765,
#     hook="hooks.print_result",
#     schedule_type=Schedule.CRON,
#     cron = '0 0 * * *'
# )