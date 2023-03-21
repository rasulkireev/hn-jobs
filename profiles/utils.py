from datetime import datetime

def clean_profile_json_object(original_comment: dict, nlp_data: dict) -> dict:
  nlp_data["years_of_experience"] = correct_years_of_experience_value(nlp_data['years_of_experience'], original_comment['text'])
  nlp_data["level"] = check_that_level_is_one_the_allowed_values(nlp_data['level'])

  for key, value in nlp_data.items():
      nlp_data[key] = if_value_is_unknown_return_empty_string(value)

  return nlp_data


def correct_years_of_experience_value(years: int, text: str) -> bool:
  """Python function to check that the estimated years of experience appears in the text."""
  if str(years) in text:
      return years
  else:
      return 0

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

"""
options for willing to relocate + mapping
- Yes
  - Open for relocation
  - Anywhere really
  - Sure!
  - Yes, only if sponsored
  - open to discussing it
  - Can discuss
- Yes (ceratin places)
  - Within Texas
- No
  - Not in the next year
- Maybe
  - In exceptional cases
  - It depends on the position.
  - Possibly
  - Possibly
"""


def sort_dates(dates):
    """
      Sorts a list of dates in ascending order.
    """
    date_format = "%B %Y"
    sorted_dates = sorted(dates, key=lambda x: datetime.strptime(x, date_format))
    return sorted_dates