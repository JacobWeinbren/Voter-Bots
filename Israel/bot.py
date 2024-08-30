import pyreadstat
import os
import random
import pandas as pd


def read_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "data", "2022.sav")
    return pyreadstat.read_sav(file_path)[0]


def get_mapped_value(value, mapping, default=""):
    return mapping.get(value, default)


def get_education_group(edu_level):
    education_map = {
        1: "no formal",
        2: "abasic",
        3: "a secondary",
        4: "a secondary",
        5: "a secondary",
        6: "a further",
        7: "a partial university",
        8: "a bachelor's",
        9: "a postgraduate",
    }
    return get_mapped_value(edu_level, education_map, "postgraduate degree")


def get_religiosity(religiosity_level):
    religiosity_map = {
        1: "very religious",
        2: "religious",
        3: "traditional religious",
        4: "traditional, not-so-religious",
        5: "non-religious, secular",
    }
    return get_mapped_value(religiosity_level, religiosity_map)


def get_random_policies(row):
    policy_maps = {
        "palestinian_state": {
            1: "strongly support",
            2: "support",
            3: "oppose",
            4: "strongly oppose",
        },
        "economic_approach": {
            1: "strongly support free market",
            2: "support free market",
            3: "support socialist",
            4: "strongly support socialist",
        },
        "religious_tradition": {
            1: "strongly support",
            2: "support",
            3: "oppose",
            4: "strongly oppose",
        },
        "civil_marriage": {
            1: "strongly oppose",
            2: "oppose",
            3: "support",
            4: "strongly support",
        },
        "strong_leader": {
            1: "strongly support",
            2: "support",
            3: "oppose",
            4: "strongly oppose",
        },
        "freedom_of_speech": {
            1: "strongly agree with",
            2: "agree with",
            3: "disagree with",
            4: "strongly disagree with",
        },
    }

    policies = [
        f"{get_mapped_value(row['v19'], policy_maps['palestinian_state'])} a Palestinian state",
        f"{get_mapped_value(row['v20'], policy_maps['economic_approach'])} economics",
        f"{get_mapped_value(row['v21'], policy_maps['religious_tradition'])} Jewish religious traditions in public life",
        f"{get_mapped_value(row['v36'], policy_maps['civil_marriage'])} civil marriage",
        f"{get_mapped_value(row['v120'], policy_maps['strong_leader'])} a strong leader who doesn't consider the Knesset or elections",
        f"{get_mapped_value(row['v123'], policy_maps['freedom_of_speech'])} protecting freedom of speech for those criticising the state",
    ]
    return random.sample([p for p in policies if p], 2)


def get_top_issue(issue_code):
    if issue_code in {100, 101, 102, 103}:
        return None

    script_dir = os.path.dirname(os.path.abspath(__file__))
    issues_file = os.path.join(script_dir, "issues.txt")

    with open(issues_file, "r", encoding="utf-8") as f:
        issues = f.readlines()

    for issue in issues:
        code, description = issue.split("-", 1)
        if int(code) == issue_code:
            return description.strip().lower()

    return None


def generate_tweet(row):
    religion_map = {1: "Jewish", 2: "Muslim", 3: "Christian", 4: "Druze"}
    religion = get_mapped_value(row["v143_code"], religion_map)
    religiosity = get_religiosity(row["v144"])
    gender = "man" if row["sex"] == 1 else "woman"
    education = get_education_group(row["educ"])

    vote_map = {
        1: "Likud (Benjamin Netanyahu)",
        2: "Yesh Atid (Yair Lapid)",
        3: "National Unity (Benny Gantz)",
        4: "Hatzionut Hadatit (Bezalel Smotrich & Itamar Ben-Gvir)",
        5: "Shas (Aryeh Deri)",
        6: "Yahadut HaTorah (Moshe Gafni)",
        7: "Yisrael Beitenu (Avigdor Lieberman)",
        8: "HaAvoda (Merav Michaeli)",
        9: "Meretz (Zehava Gal-On)",
        10: "HaBayit HaYehudi (Ayelet Shaked)",
        11: "Hadash-Ta'al (Ayman Odeh)",
        12: "Ra'am (Mansour Abbas)",
        13: "Balad (Sami Abu Shehadeh)",
        30: "Other",
        94: "Doesn't intend to vote",
        96: "Blank Ballot",
    }

    vote = get_mapped_value(row["v104"], vote_map)
    if not vote or row["v104"] in [97, 98, 99] or pd.isna(row["age"]):
        return None

    tweet = f"I'm a"
    if religiosity:
        tweet += f" {religiosity}"
    if religion:
        tweet += f" {religion}"
    tweet += f" {gender} with {education} education, aged {round(row['age'])}.\n\n"

    top_issue = get_top_issue(row["v8_code1"])
    if top_issue:
        tweet += f"My top issue is {top_issue}.\n\n"

    policies = get_random_policies(row)
    tweet += f"I {' and '.join(policies)}.\n\n"

    tweet += f"I voted for {vote} in 2022."

    return tweet


def generate_and_save_tweets(df):
    with open("tweets.txt", "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            tweet = generate_tweet(row)
            if tweet:
                f.write(tweet + "\n\n")


if __name__ == "__main__":
    df = read_data()
    generate_and_save_tweets(df)
    print("Tweets have been generated and saved to tweets.txt")
