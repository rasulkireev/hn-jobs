
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
    if value in ["Unknown", "unknown", "empty"]:
        return ""
    else:
        return value

# options for willing to relocate
# Yes
# Yes (certain places)
# No
# Maybe
