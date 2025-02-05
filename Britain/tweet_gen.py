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
    get_eu_referendum_intention,
    get_eu_referendum_vote,
    get_past_vote,
    get_ns_sec,
    get_working_status,
)


def generate_tweet(row, selected_indices):
    if row.name not in selected_indices:
        print(f"Skipping {row.name} because it's not in the selected indices")
        return None

    gender = get_gender(row["gender"])
    constituency = get_constituency_name(row["new_pcon_codeW29"])
    top_issue, verb = get_mii_category(row["mii_cat_llmW29"])
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
    past_vote = get_past_vote(row)

    eu_referendum_vote = get_eu_referendum_vote(row.get("euRefVoteW9"))
    eu_referendum_intention = get_eu_referendum_intention(row.get("euRefVoteAfterW29"))

    occupation = get_ns_sec(row["ns_sec_analyticW26W27W29"])
    working_status = get_working_status(row["workingStatusW26W27W29"])

    if not gender or not voting_intention or not constituency:
        return None

    # Handle optional fields
    ethnicity_str = f"{ethnicity} " if ethnicity else ""
    religion_str = f"{religion} " if religion else ""
    education_str = f", with {education}" if education else ""

    # Build tweet sections
    tweet = ""

    # 1. Personal Description
    personal_desc = f"👤 I'm a {ethnicity_str}{religion_str}{gender}"
    if constituency and country_emoji:
        personal_desc += f" from {constituency} {country_emoji}"
    if age:
        personal_desc += f", aged {age}"
    if education:
        personal_desc += f", with {education}"
    # Ensure it ends with a period
    personal_desc = personal_desc.strip()
    if not personal_desc.endswith("."):
        personal_desc += "."
    tweet = add_section(tweet, personal_desc, False)

    # 2. Household/Work Status (Class)
    class_info = []
    if home_ownership:
        class_info.append(f"🏠 {home_ownership}")
    if working_status:
        class_info.append(working_status)
    elif occupation:
        class_info.append(f"💼 I am {occupation}")
    if class_info:
        tweet = add_section(tweet, ". ".join(class_info))

    # 3. Top Issue
    if top_issue:
        tweet = add_section(tweet, f"{top_issue} {verb} my top issue.")

    # 4. Political Leans
    lean_parts = []
    if economic_lean:
        lean_parts.append(f"economically {economic_lean}")
    if social_lean:
        lean_parts.append(f"socially {social_lean}")

    if lean_parts:
        lean_sentence = "🤔 I am " + " and ".join(lean_parts) + "."
        tweet = add_section(tweet, lean_sentence)

    # 5. Voting (Election)
    vote_text = f"🗳️ I voted {voting_intention} in 2024"
    if past_vote:
        vote_text += f". In 2019, I voted {past_vote}"
    if preferred_party and preferred_party != voting_intention:
        vote_text = f"🗳️ I wanted to vote {preferred_party}, but tactically voted {voting_intention} in 2024"

    # Ensure voting section ends with period
    if not vote_text.endswith("."):
        vote_text += "."
    tweet = add_section(tweet, vote_text)

    # 6. Voting (Ref)
    eu_text = " ".join(filter(None, [eu_referendum_vote, eu_referendum_intention]))
    if eu_text:
        tweet = add_section(tweet, eu_text)

    # 7. Policies
    policies = generate_policies(row)
    if policies:
        # Shuffle and select up to 3 random policies
        random.shuffle(policies)
        # Ensure each policy ends with a period
        cleaned_policies = []
        for p in policies[:3]:
            p = p.strip()
            if not p.endswith("."):
                p += "."
            cleaned_policies.append(p)
        policy_text = "Some opinions I hold:\n" + "\n".join(
            [f"• {p}" for p in cleaned_policies]
        )
        tweet = add_section(tweet, policy_text)

    return tweet


def add_section(tweet, content, section_separator=True):
    if content:
        if tweet:  # Only add separator if tweet isn't empty
            tweet += "\n\n" if section_separator else " "
        tweet += content
    return tweet
