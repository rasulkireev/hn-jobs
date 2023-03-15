import re
import json
import httpx
import logging
from django.conf import settings
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django_q.models import Schedule
import openai

from .models import Profile, Technology

logger = logging.getLogger(__file__)
openai.api_key = settings.OPENAI_KEY

def analyze_hn_page(who_wants_to_be_hired_post_id):
    r = httpx.get(f'https://hacker-news.firebaseio.com/v0/item/{who_wants_to_be_hired_post_id}.json').json()

    who_wants_to_be_hired_id = int(r['id'])
    who_wants_to_be_hired_title = str(re.search('\(([^)]+)', r['title']).group(1))

    list_of_comment_ids = r["kids"]

    # if working in dev don't want to go through all the comments
    if settings.DEBUG:
        list_of_comment_ids = list_of_comment_ids[:10]

    for comment_id in list_of_comment_ids:
        if not Profile.objects.filter(who_wants_to_be_hired_comment_id=comment_id).exists():
            logger.info(f"Analyzing comment {comment_id}")
            json_profile = httpx.get(f'https://hacker-news.firebaseio.com/v0/item/{comment_id}.json').json()

            try:
              if json_profile["deleted"] == True:
                  logger.info(f"Comment {comment_id} is deleted.")
                  continue
            except KeyError:
                  logger.info(f"Comment {comment_id} is not deleted.")

            logger.info(f"JSON for comment {comment_id}: {json_profile}")
            who_wants_to_be_hired_comment_id = int(json_profile['id'])
            hn_username = str(json_profile['by'])


            request = f"""Convert the following text:
                ```
                {json_profile['text']}
                ```
                into a JSON object with the following valid keys
                (feel free to give me an value of empty string if there is no info,
                also ignore the content in  brackets, it is only to explain what I need):
                - location (can't be empty)
                - city (figure out from location, can't be empty)
                - country (figure out from location, can't be empty)
                - state (if country is USA please guess the state, otherwise empty string. keep the short format, like MA, NY, etc.)
                - is_remote (boolean)
                - willing_to_relocate (choose from: Yes, No, Maybe. can't be empty)
                - technologies_used (string of comma separated values. split values like HTML/CSS into HTML, CSS)
                - resume_link (valid url or empty)
                - email (valid email or empty)
                - personal_website (valid url or empty)
                - description (can't be empty)
                - name (Full Name if mentioned)
                - title (come up with a short - 6 words max- title based on one of the technologies_used and description, can't be empty)
                - level (choose from these options: Junior, Mid-level, Senior, Principal, C-Level. figure out from description, can't be empty)
                - years_of_experience (figure out from description, make a best guess, can't be empty. make sure this is an integer, so no values like 40+, only 40)
                - capacity (string of comma separated values. options are 'Part-time Contractor', 'Full-time Contractor', 'Part-time Employee' and 'Full-time Employee', can't be empty)

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
            json_converted_comment_response = json.loads(converted_comment_response.content)

            # Create Technology Objects
            with transaction.atomic():
                technology_names = [name.strip() for name in json_converted_comment_response['technologies_used'].split(',')]

                technologies = []
                for name in technology_names:
                    try:
                        technology = Technology.objects.get(name=name)
                        logger.info(f"{name} exists")
                    except ObjectDoesNotExist:
                        technology = Technology.objects.create(name=name)
                        logger.info(f"Create entry for {name}")
                    technologies.append(technology)

            profile = Profile(
                latest_who_wants_to_be_hired_id=who_wants_to_be_hired_id,
                who_wants_to_be_hired_title=who_wants_to_be_hired_title,
                who_wants_to_be_hired_comment_id=who_wants_to_be_hired_comment_id,
                title=json_converted_comment_response['title'],
                name=json_converted_comment_response['name'],
                hn_username=hn_username,
                description=json_converted_comment_response['description'],
                location=json_converted_comment_response['location'],
                city=json_converted_comment_response['city'],
                country=json_converted_comment_response['country'],
                state=json_converted_comment_response['state'],
                level=json_converted_comment_response['level'],
                is_remote=json_converted_comment_response['is_remote'],
                willing_to_relocate=json_converted_comment_response['willing_to_relocate'],
                resume_link=json_converted_comment_response['resume_link'],
                personal_website=json_converted_comment_response['personal_website'],
                email=json_converted_comment_response['email'],
                years_of_experience=json_converted_comment_response['years_of_experience'],
                capacity=json_converted_comment_response['capacity'],
            )
            profile.save()
            logger.info(f"Adding techonologies for profile {comment_id}")
            profile.technologies_used.set(technologies)
        else:
          logger.info(f"Profile for {comment_id} already exists.")

    return f"Task Completed"


# Schedule.objects.create(
#     func=analyze_hn_page,
#     args=34983765,
#     hook="hooks.print_result",
#     schedule_type=Schedule.CRON,
#     cron = '0 0 * * *'
# )