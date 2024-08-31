import os
import random
import pandas as pd


def read_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_file_path = os.path.join(script_dir, "data", "2021.dta")
    dict_file_path = os.path.join(script_dir, "data", "dict.dta")
    main_data = pd.read_stata(main_file_path, convert_categoricals=False)
    dict_data = pd.read_stata(dict_file_path, convert_categoricals=False)
    return pd.merge(main_data, dict_data, on="cps21_ResponseId")


def get_mapped_value(value, mapping, default=None):
    return mapping.get(value, default)


def get_province(province_code):
    province_map = {
        1: "Alberta",
        2: "British Columbia",
        3: "Manitoba",
        4: "New Brunswick",
        5: "Newfoundland and Labrador",
        6: "Northwest Territories",
        7: "Nova Scotia",
        8: "Nunavut",
        9: "Ontario",
        10: "Prince Edward Island",
        11: "Quebec",
        12: "Saskatchewan",
        13: "Yukon",
    }
    return get_mapped_value(province_code, province_map)


def get_gender(gender_code):
    gender_map = {1: "man", 2: "woman", 3: "non-binary"}
    return get_mapped_value(gender_code, gender_map)


def get_education_group(edu_level):
    education_map = {
        1: "no formal",
        2: "a primary",
        3: "a primary",
        4: "some secondary",
        5: "a secondary",
        6: "a further",
        7: "a further",
        8: "some university",
        9: "a bachelor's",
        10: "a master's",
        11: "a doctorate",
    }
    return get_mapped_value(edu_level, education_map, "postgraduate degree")


def get_visible_minority(vismin_codes):
    vismin_map = {
        1: "Arab",
        2: "Asian",
        3: "Black",
        4: "Indigenous",
        5: "Hispanic",
        6: "South Asian",
        7: "Southeast Asian",
        8: "West Asian",
        9: "White",
    }
    for code in range(1, 10):
        if vismin_codes[f"cps21_vismin_{code}"] == 1:
            return get_mapped_value(code, vismin_map)
    return None


def get_religion(religion_code):
    religion_map = {
        1: "Atheist",
        2: "Agnostic",
        3: "Buddhist",
        4: "Hindu",
        5: "Jewish",
        6: "Muslim",
        7: "Sikh",
        8: "Anglican",
        9: "Baptist",
        10: "Catholic",
        11: "Orthodox",
        12: "Jehovah's Witness",
        13: "Lutheran",
        14: "Mormon",
        15: "Evangelical",
        16: "Presbyterian",
        17: "Protestant",
        18: "United Church",
        19: "Christian Reformed",
        20: "Salvation Army",
        21: "Mennonite",
    }
    return get_mapped_value(religion_code, religion_map)


def get_vote_choice(vote_code):
    vote_map = {
        1: "Liberal",
        2: "Conservative",
        3: "NDP",
        4: "Bloc Québécois",
        5: "Green",
        6: "People's Party",
    }
    return get_mapped_value(vote_code, vote_map)


def get_important_issue(row):
    issue_map = {
        "economydum": "The economy",
        "envirodum": "The environment",
        "immigrationdum": "Immigration",
        "healthcaredum": "Healthcare",
        "housingdum": "Housing",
        "seniorsdum": "Senior issues",
        "leadersdum": "Leadership",
        "ethicsdum": "Ethics",
        "educationdum": "Education",
        "crimedum": "Crime and guns",
        "indigenousdum": "Indigenous issues",
        "welfaredum": "Welfare",
        "electiondum": "Electoral reform",
        "womendum": "Women's issues and abortion",
        "securitydum": "Security, defence and IR",
        "quebecdum": "Quebec and Law 21",
        "racedum": "Race relations",
        "coviddum": "Covid-19",
    }

    important_issues = [
        issue_name for issue_var, issue_name in issue_map.items() if row[issue_var] == 1
    ]
    return random.choice(important_issues) if important_issues else None


def get_random_policies(row):
    policies = []
    policy_map = {
        "cps21_pos_fptp": (
            "support proportional representation",
            "oppose proportional representation",
        ),
        "cps21_pos_life": (
            "support doctor-assisted end-of-life",
            "oppose doctor-assisted end-of-life",
        ),
        "cps21_pos_cannabis": (
            "support criminalising cannabis",
            "oppose criminalising cannabis",
        ),
        "cps21_pos_carbon": ("support the carbon tax", "oppose the carbon tax"),
        "cps21_pos_energy": (
            "support more energy sector help",
            "oppose more energy sector help",
        ),
        "cps21_pos_envreg": (
            "support stricter environmental rules",
            "oppose stricter environmental rules",
        ),
        "cps21_pos_jobs": (
            "prioritise jobs over the environment",
            "prioritise the environment over jobs",
        ),
        "cps21_pos_subsid": (
            "support ending corporate subsidies",
            "oppose ending corporate subsidies",
        ),
        "cps21_pos_trade": ("support more free trade", "oppose more free trade"),
        "cps21_imm": (
            "support more immigration",
            "support less immigration",
            "support current immigration levels",
        ),
        "cps21_refugees": (
            "support more refugees",
            "support fewer refugees",
            "support current refugee levels",
        ),
        "cps21_quebec_sov": ("support Quebec sovereignty", "oppose Quebec sovereignty"),
    }

    for issue, options in policy_map.items():
        if (
            pd.notna(row[issue]) and row[issue] != 6
        ):  # 6 is "Don't know/ Prefer not to answer"
            value = int(row[issue])
            if issue in ["cps21_imm", "cps21_refugees"]:
                if 1 <= value <= len(options):
                    policies.append(options[value - 1])
            elif issue == "cps21_quebec_sov":
                if value <= 2:
                    policies.append(options[0])
                elif value >= 3:
                    policies.append(options[1])
            else:
                if value <= 2:
                    policies.append(options[1])
                elif value >= 4:
                    policies.append(options[0])

    return random.sample(policies, min(4, len(policies)))


def generate_tweet(row):
    gender = get_gender(row["cps21_genderid"])
    important_issue = get_important_issue(row)
    vote_choice = get_vote_choice(row["pes21_votechoice2021"])

    if not gender or not important_issue or not vote_choice:
        return None

    province = get_province(row["cps21_province"])
    age = round(row["cps21_age"]) if not pd.isna(row["cps21_age"]) else None
    education = get_education_group(row["cps21_education"])
    vismin = get_visible_minority(row)
    religion = get_religion(row["cps21_religion"])

    tweet = f"I'm a"
    if vismin:
        tweet += f" {religion} {vismin}"
    tweet += f" {gender} from {province}"
    tweet += f" with {education} education"
    if age:
        tweet += f", aged {age}"
    tweet += ".\n\n"

    tweet += f"{important_issue} is my top issue.\n\n"

    policies = get_random_policies(row)
    if policies:
        tweet += "I " + ", I ".join(policies[:-1])
        if len(policies) > 1:
            tweet += f", and I {policies[-1]}"
        else:
            tweet += policies[0]
        tweet += ".\n\n"

    tweet += f"I voted {vote_choice} in 2021."

    return tweet


def generate_and_save_tweets(df):
    with open("Canada/tweets.txt", "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            tweet = generate_tweet(row)
            if tweet and len(tweet) <= 300:
                f.write(tweet + "\n\n\n")


if __name__ == "__main__":
    df = read_data()
    generate_and_save_tweets(df)
    print("Tweets have been generated and saved to tweets.txt")
