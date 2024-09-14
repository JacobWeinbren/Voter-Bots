import pandas as pd
import random
from data_utils import (
    get_gender,
    get_education_group,
    get_ethnicity,
    get_religion,
    get_mii_category,
    get_economic_lean,
    get_social_lean,
    get_voting_intention,
    get_preferred_party,
    get_home_ownership,
    get_constituency_name,
    get_country_emoji,
    generate_policies,
)


def generate_tweet(row):
    gender = get_gender(row["gender"])
    constituency = get_constituency_name(row["new_pcon_codeW29"])
    top_issue, verb = get_mii_category(row["miiW29"])
    age = int(row["ageW29"]) if not pd.isna(row["ageW29"]) else None
    religion = get_religion(row["p_religionW29"])
    ethnicity = get_ethnicity(row["p_ethnicityW29"])
    education = get_education_group(row["p_educationW29"])
    economic_lean = get_economic_lean(row["lr_scaleW27W29"])
    social_lean = get_social_lean(row["al_scaleW27W29"])
    home_ownership = get_home_ownership(row["homeOwn2W26W27"])
    country_emoji = get_country_emoji(row["countryW29"])

    voting_intention = get_voting_intention(row)
    preferred_party = get_preferred_party(row)

    if not all(
        [
            gender,
            constituency,
            top_issue,
            age,
            economic_lean,
            social_lean,
            voting_intention,
        ]
    ):
        return None

    # Handle optional fields
    ethnicity_str = f"{ethnicity} " if ethnicity else ""
    religion_str = f"{religion} " if religion else ""
    education_str = f", with {education}" if education else ""

    tweet = f"👤 I'm a {ethnicity_str}{religion_str}{gender} from {constituency} {country_emoji}, aged {age}{education_str}."
    if home_ownership:
        tweet += f" 🏠 {home_ownership}."
    tweet += f"\n\n{top_issue} {verb} my top issue.\n\n"
    tweet += f"I am economically {economic_lean} and socially {social_lean}.\n\n"

    if preferred_party and preferred_party != voting_intention:
        tweet += f"🗳️ I wanted to vote {preferred_party}, but I tactically voted {voting_intention} in 2024.\n\n"
    else:
        tweet += f"🗳️ I voted {voting_intention} in 2024.\n\n"

    policies = generate_policies(row)
    if len(policies) > 3:
        policies = random.sample(policies, 3)
    if policies:
        tweet += "Some opinions I hold:\n"
        for policy in policies:
            tweet += f"• {policy}\n"

    return tweet
