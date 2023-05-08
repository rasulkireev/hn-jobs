import logging
from datetime import datetime

logger = logging.getLogger(__file__)

def clean_job_json_object(original_comment: dict, nlp_data: dict) -> dict:
  nlp_data["years_of_experience"] = check_years_of_experience_value(nlp_data['years_of_experience'], original_comment['text'])
  nlp_data["level"] = check_that_level_is_one_the_allowed_values(nlp_data['level'])
  check_boolean_value(nlp_data["is_remote"])
  check_boolean_value(nlp_data["is_onsite"])

  for key, value in nlp_data.items():
      nlp_data[key] = if_value_is_unknown_return_empty_string(value)

  return nlp_data

def check_years_of_experience_value(years: int, text: str):
  """Python function to check that the estimated years of experience appears in the text."""
  if str(years) in text and isinstance(years, int):
      return years
  else:
      return None

def check_that_level_is_one_the_allowed_values(level: str) -> bool:
    if level in ["Senior", "Mid-level", "Junior", "Principal", "C-Level"]:
        return level
    else:
        return ""

def if_value_is_unknown_return_empty_string(value: str) -> str:
    if value in ["Unknown", "unknown", "empty", "not specified", "N/A"]:
        return ""
    else:
        return value


def sort_dates(dates):
    """
      Sorts a list of dates in ascending order.
    """
    date_format = "%B %Y"
    sorted_dates = sorted(dates, key=lambda x: datetime.strptime(x, date_format))
    return sorted_dates

def check_boolean_value(boolean_value: any) -> bool:
    if isinstance(boolean_value, bool) or boolean_value in ["True", "true", "Yes", "yes"]:
        return boolean_value
    else:
        return False
