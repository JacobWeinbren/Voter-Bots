import pandas as pd
import os


def read_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, "data", "BES.sav")
    return pd.read_spss(data_file_path, convert_categoricals=False)


def get_mapped_value(value, mapping, default=None):
    return mapping.get(value, default)


def get_gender(gender_code):
    gender_map = {1: "man", 2: "woman"}
    return get_mapped_value(gender_code, gender_map)


script_dir = os.path.dirname(os.path.abspath(__file__))
cons_file_path = os.path.join(script_dir, "data", "cons.csv")
cons_df = pd.read_csv(cons_file_path)


def get_constituency_name(constituency_code):
    if constituency_code and not pd.isna(constituency_code):
        matching_rows = cons_df[cons_df["PCON24CD"] == constituency_code]
        if not matching_rows.empty:
            constituency = matching_rows["PCON24NM"].iloc[0]
            return constituency if pd.notna(constituency) else None
    return None


def get_education_group(code):
    education_levels = {
        1: "no formal qualifications",
        2: "a vocational training certificate",
        3: "a trade apprenticeship",
        4: "a clerical or commercial qualification",
        5: "a basic technical certificate",
        6: "an advanced technical certificate",
        7: "a technical diploma",
        8: "lower secondary education (CSE grades 2-5)",
        9: "secondary education (GCSE/O Level)",
        10: "Scottish Ordinary Certificate",
        11: "higher secondary education (A Level)",
        12: "Scottish Higher Certificate",
        13: "a nursing qualification",
        14: "a teaching qualification (non-degree)",
        15: "a university diploma",
        16: "a bachelor's degree",
        17: "a postgraduate degree (Master's or PhD)",
        18: "a professional qualification",
        19: None,
        20: None,
    }
    if pd.isna(code):
        return None
    try:
        return education_levels.get(int(code), None)
    except ValueError:
        return None


def get_economic_lean(lr_scale):
    if pd.isna(lr_scale):
        return None

    try:
        lr_scale = float(lr_scale)
    except ValueError:
        return None

    if 0 <= lr_scale <= 2:
        return "strongly economically left-wing ⬅️"
    elif 2 < lr_scale <= 4:
        return "moderately economically left-wing ⬅️"
    elif 4 < lr_scale <= 6:
        return "economically centrist ⚖️"
    elif 6 < lr_scale <= 8:
        return "moderately economically right-wing ➡️"
    elif 8 < lr_scale <= 10:
        return "strongly economically right-wing ➡️"
    else:
        return None


def get_social_lean(al_scale):
    if pd.isna(al_scale):
        return None

    try:
        al_scale = float(al_scale)
    except ValueError:
        return None

    if 0 <= al_scale <= 2:
        return "strongly socially liberal 🕊️"
    elif 2 < al_scale <= 4:
        return "moderately socially liberal 🕊️"
    elif 4 < al_scale <= 6:
        return "socially centrist ⚖️"
    elif 6 < al_scale <= 8:
        return "moderately socially authoritarian 🔒"
    elif 8 < al_scale <= 10:
        return "strongly socially authoritarian 🔒"
    else:
        return None


def get_ethnicity(ethnicity_code):
    ethnicity_map = {
        1: "white British",
        2: "white",
        3: "mixed white and Black Caribbean",
        4: "mixed white and Black African",
        5: "mixed white and Asian",
        6: "mixed ethnicity",
        7: "Indian",
        8: "Pakistani",
        9: "Bangladeshi",
        10: "Asian",
        11: "Black Caribbean",
        12: "Black African",
        13: "Black",
        14: "Chinese",
        15: "",
        16: "",
    }
    ethnicity = ethnicity_map.get(ethnicity_code, "")
    if ethnicity == "prefer not to say":
        return ""
    return ethnicity


def get_religion(religion_code):
    religion_map = {
        1: "Atheist/Agnostic",
        2: "Anglican ✝️",
        3: "Catholic ✝️",
        4: "Presbyterian ✝️",
        5: "Methodist ✝️",
        6: "Baptist ✝️",
        7: "United Reformed ✝️",
        8: "Free Presbyterian ✝️",
        9: "Brethren ✝️",
        10: "Jewish ✡️",
        11: "Hindu 🕉️",
        12: "Muslim ☪️",
        13: "Sikh 🪯",
        14: "Buddhist ☸️",
        15: "",
        16: "",
        17: "Orthodox Christian ✝️",
        18: "Pentecostal ✝️",
        19: "Evangelical ✝️",
    }
    return religion_map.get(religion_code, "")


def get_mii_category(mii_code):
    mii_map = {
        1: ("🏥 Health", "is"),
        2: ("🎓 Education", "is"),
        3: ("🗳️ The Election", "is"),
        4: ("😠 Political negativity", "is"),
        5: ("🤬 Partisan negativity", "is"),
        6: ("🔀 Societal divides", "are"),
        7: ("🙏 Morals", "are"),
        8: ("🇬🇧 National identity", "is"),
        9: ("🚫 Discrimination", "is"),
        10: ("💰 Welfare", "is"),
        11: ("❌ Terrorism", "is"),
        12: ("🛂 Immigration", "is"),
        13: ("🆘 Asylum", "is"),
        14: ("🚓 Crime", "is"),
        15: ("🇪🇺 Europe/Brexit", "is"),
        16: ("📜 Constitutional issues", "are"),
        17: ("🌐 International trade", "is"),
        18: ("🏴󠁧󠁢󠁳󠁣󠁴󠁿 Devolution", "is"),
        19: ("🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scottish independence", "is"),
        21: ("🌍 Foreign affairs", "are"),
        22: ("⚔️ War", "is"),
        23: ("🛡️ Defence", "is"),
        24: ("🚨 Foreign emergency", "is"),
        25: ("🚨 Domestic emergency", "is"),
        26: ("💷 Economy (general)", "is"),
        27: ("💵 Personal finances", "are"),
        28: ("📉 Unemployment", "is"),
        29: ("💸 Taxation", "is"),
        30: ("📊 Public debt/deficit", "is"),
        31: ("📈 Inflation", "is"),
        32: ("💲 Living costs", "are"),
        33: ("😞 Poverty", "is"),
        34: ("✂️ Austerity", "is"),
        35: ("⚖️ Inequality", "is"),
        36: ("🏠 Housing", "is"),
        37: ("🤝 Social care", "is"),
        38: ("👴 Pensions/ageing", "are"),
        39: ("🚆 Transport/infrastructure", "is"),
        40: ("🌳 Environment", "is"),
        41: ("🔒 Authoritarian values", "are"),
        42: ("🕊️ Liberal values", "are"),
        43: ("➡️ Right-wing values", "are"),
        44: ("⬅️ Left-wing values", "are"),
        45: (None, None),
        46: (None, None),
        47: (None, None),
        48: ("🦠 Coronavirus", "is"),
        49: ("💼 Covid economy", "is"),
        50: ("👪 Gender/sexuality/family", "are"),
    }
    if pd.isna(mii_code):
        return None, None
    try:
        result = get_mapped_value(int(mii_code), mii_map, None)
        return result if result else (None, None)
    except ValueError:
        return None, None


def get_home_ownership(value):
    ownership_mapping = {
        1: "I own my home outright",
        2: "I own my home with a mortgage",
        3: "I rent from a local authority",
        4: "I rent from a private landlord",
        5: "I rent from a Housing Association",
        6: "I live rent-free in a family member or friend’s home",
        9999: None,
    }
    return ownership_mapping.get(value)


# Mapping of party codes to party names
def get_party_name(party_code, country=None):
    party_mapping = {
        0: None,
        1: "Conservative",
        2: "Labour",
        3: "Liberal Democrat",
        4: "Scottish National Party (SNP)",
        5: "Plaid Cymru",
        6: "United Kingdom Independence Party (UKIP)",
        7: "Green",
        8: "British National Party (BNP)",
        11: "Change UK",
        12: "Reform UK",
        13: "Independent",
        9: "Other",
        99: None,  # Don't know
    }
    # Handle country-specific options
    if party_code == 4 and country != 2:
        return None  # SNP only if country==2 (Scotland)
    if party_code == 5 and country != 3:
        return None  # Plaid Cymru only if country==3 (Wales)
    return party_mapping.get(party_code)


# Mapping of party names to colored square emojis
party_emojis = {
    "Conservative": "🟦",
    "Labour": "🟥",
    "Liberal Democrat": "🟧",
    "Green": "🟩",
    "Scottish National Party (SNP)": "🟨",
    "Plaid Cymru": "🟩",
    "United Kingdom Independence Party (UKIP)": "🟪",
    "Reform UK": "🟦",
    "Brexit Party": "🟦",
    "Change UK": "⬛",
    "Independent": "⬜",
    "Other": "⬜",
}


def get_party_with_emoji(party_name):
    if not party_name:
        return None
    emoji = party_emojis.get(party_name, "")
    return f"{party_name} {emoji}"


def get_voting_intention(row):
    party_code = row.get("generalElectionVoteW29")
    country = row.get("countryW29")
    party_name = get_party_name(party_code, country)
    if party_code == 99 or not party_name:
        return None
    return get_party_with_emoji(party_name)


def get_preferred_party(row):
    party_code = row.get("partyPreferredW29")
    country = row.get("countryW29")
    party_name = get_party_name(party_code, country)
    if party_code == 99 or not party_name:
        return None
    return get_party_with_emoji(party_name)


def get_past_vote(row):
    party_code = row.get("generalElectionVoteW19")
    country = row.get("countryW19")
    party_name = get_party_name(party_code, country)

    # Special handling for Brexit Party
    if party_code == 12:
        party_name = "Brexit Party"

    if party_code == 99 or not party_name:
        return None
    return get_party_with_emoji(party_name)


def generate_policies(row):
    policies = []

    # PR Preference
    if "prPreferenceW29" in row and row["prPreferenceW29"] != 99:
        preference = row["prPreferenceW29"]
        if preference == 1:
            policies.append("🏛️ One party should have a majority to govern alone.")
        elif preference == 2:
            policies.append("🗳️ Seats in parliament should match vote percentages.")

    # EU Integration Grid
    if "EUIntegrationSelfW29" in row and row["EUIntegrationSelfW29"] != 99:
        position = row["EUIntegrationSelfW29"]
        if position >= 7:
            policies.append("🇬🇧 Britain should protect its independence from the EU.")
        elif position <= 3:
            policies.append("🇪🇺 Britain should unite more with the EU.")
        else:
            policies.append("🤝 Britain should find a middle ground with the EU.")

    # Redistribution
    if "redistSelfW29" in row and row["redistSelfW29"] != 99:
        stance = row["redistSelfW29"]
        if stance >= 7:
            policies.append(
                "🤷 Government should be less concerned about equal incomes."
            )
        elif stance <= 3:
            policies.append("🟰 Government should make incomes more equal.")
        else:
            policies.append("⚖️ Income equality requires a balanced approach.")

    # Environmental Protection vs Economic Growth
    if "enviroGrowthW28" in row and row["enviroGrowthW28"] != 99:
        value = row["enviroGrowthW28"]
        if value >= 7:
            policies.append(
                "🌳 Protecting the environment should have priority over economic growth."
            )
        elif value <= 3:
            policies.append(
                "💰 Economic growth should have priority over environmental protection."
            )
        else:
            policies.append("⚖️ We need a balance between the environment and growth.")

    # Immigration Impact (Economy and Culture)
    econ_value = row.get("immigEconW27")
    cultural_value = row.get("immigCulturalW27")

    if econ_value not in [9999, None] and cultural_value not in [9999, None]:
        avg_value = (econ_value + cultural_value) / 2
        if avg_value >= 5:
            policies.append(
                "🌍 Immigration is beneficial for Britain's economy and culture."
            )
        elif avg_value <= 3:
            policies.append(
                "🚫 Immigration has negative effects on Britain's economy and culture."
            )
        else:
            policies.append("⚖️ Immigration has mixed or neutral impacts on Britain.")
    elif econ_value not in [9999, None]:
        if econ_value >= 5:
            policies.append("💼 Immigration is good for Britain's economy.")
        elif econ_value <= 3:
            policies.append("📉 Immigration is bad for Britain's economy.")
        else:
            policies.append("⚖️ Immigration has a neutral impact on the economy.")
    elif cultural_value not in [9999, None]:
        if cultural_value >= 5:
            policies.append("🎨 Immigration enriches Britain's cultural life.")
        elif cultural_value <= 3:
            policies.append("📉 Immigration undermines Britain's cultural life.")
        else:
            policies.append("⚖️ Immigration neither enriches nor undermines culture.")

    # Equality Efforts
    equality_issues = {
        "blackEqualityW27": "Attempts to give equal opportunities to ethnic minorities",
        "femaleEqualityW27": "Attempts to give equal opportunities to women",
        "gayEqualityW27": "Attempts to give equal opportunities to gays and lesbians",
    }
    equality_emojis = {
        "blackEqualityW27": "🤝",
        "femaleEqualityW27": "♀️",
        "gayEqualityW27": "🏳️‍🌈",
    }
    for var, text in equality_issues.items():
        if var in row and row[var] != 99:
            response = row[var]
            if response <= 2:
                policies.append(
                    f"{equality_emojis[var]} {text} have not gone far enough."
                )
            elif response == 3:
                policies.append(f"{equality_emojis[var]} {text} are about right.")
            elif response >= 4:
                policies.append(f"{equality_emojis[var]} {text} have gone too far.")

    # Zero-Hour Contracts
    if "zeroHourContractW27" in row:
        value = row["zeroHourContractW27"]
        if value == 1:
            policies.append("🚫 Zero-hours contracts should definitely be illegal.")
        elif value == 2:
            policies.append("❌ Zero-hours contracts should probably be illegal.")
        elif value == 3:
            policies.append("✅ Zero-hours contracts should probably be legal.")
        elif value == 4:
            policies.append("💯 Zero-hours contracts should definitely be legal.")

    # Welfare Preference
    if "welfarePreferenceW27" in row and row["welfarePreferenceW27"] != 99:
        value = row["welfarePreferenceW27"]
        if value <= 2:
            policies.append("📈 Welfare benefits are too high.")
        elif value == 3:
            policies.append("💰 Welfare benefits are about right.")
        elif value >= 4:
            policies.append("📉 Welfare benefits are too low.")

    # Preference for Change
    if "radicalW27" in row and row["radicalW27"] != 99:
        agreement = row["radicalW27"]
        if agreement >= 4:
            policies.append("🔄 We need to fundamentally change how society works.")
        elif agreement <= 2:
            policies.append("👌 No need for fundamental changes to society.")

    if "harkBackW27" in row and row["harkBackW27"] != 99:
        agreement = row["harkBackW27"]
        if agreement >= 4:
            policies.append("🏰 Things were better in the past.")
        elif agreement <= 2:
            policies.append("🚀 The present is better than the past.")

    # Immigration Levels
    if "immigSelfW29" in row and row["immigSelfW29"] != 99:
        position = row["immigSelfW29"]
        if position >= 7:
            policies.append("🌏 The UK should allow many more immigrants.")
        elif position <= 3:
            policies.append("🚫 The UK should allow many fewer immigrants.")
        else:
            policies.append("⚖️ The UK's current immigration levels are about right.")

    # Israel-Palestine Conflict
    if "israelPalestineW28" in row and row["israelPalestineW28"] != 99:
        stance = row["israelPalestineW28"]
        if stance == 1:
            policies.append("🇮🇱 I sympathise much more with the Israeli side.")
        elif stance == 2:
            policies.append("🇮🇱 I sympathise a little more with the Israeli side.")
        elif stance == 3:
            policies.append(
                "🤝 I sympathise equally with both sides, Israeli and Palestinian."
            )
        elif stance == 4:
            policies.append("🇵🇸 I sympathise a little more with the Palestinian side.")
        elif stance == 5:
            policies.append("🇵🇸 I sympathise much more with the Palestinian side.")

    # General Trust
    if "genTrustW27" in row and row["genTrustW27"] != 99:
        trust = row["genTrustW27"]
        if trust == 1:
            policies.append("😊 Most people can be trusted.")
        elif trust == 2:
            policies.append("🤨 You can't be too careful dealing with people.")

    # Values1 ('lr1' to 'lr5')
    values1_questions = [
        "lr1W27W29",
        "lr2W27W29",
        "lr3W27W29",
        "lr4W27W29",
        "lr5W27W29",
    ]
    values1_texts = {
        "lr1W27W29": "Government should redistribute income from the better off to those who are less well off.",
        "lr2W27W29": "Big business takes advantage of ordinary people.",
        "lr3W27W29": "Ordinary working people do not get their fair share of the nation's wealth.",
        "lr4W27W29": "There is one law for the rich and one for the poor.",
        "lr5W27W29": "Management will always try to get the better of employees if it gets the chance.",
    }
    for question in values1_questions:
        if question in row and row[question] != 99:
            agreement = row[question]
            if agreement == 5:
                policies.append(f"💯 Strongly agree: {values1_texts[question]}")
            elif agreement == 4:
                policies.append(f"👍 Agree: {values1_texts[question]}")
            elif agreement == 3:
                policies.append(f"😐 Neutral on: {values1_texts[question]}")
            elif agreement == 2:
                policies.append(f"👎 Disagree: {values1_texts[question]}")
            elif agreement == 1:
                policies.append(f"🚫 Strongly disagree: {values1_texts[question]}")

    # Values2 ('al1' to 'al5')
    values2_questions = [
        "al1W27W29",
        "al2W27W29",
        "al3W27W29",
        "al4W27W29",
        "al5W27W29",
    ]
    values2_texts = {
        "al1W27W29": "Young people today don't have enough respect for traditional British values.",
        "al2W27W29": "For some crimes, the death penalty is the most appropriate sentence.",
        "al3W27W29": "Schools should teach children to obey authority.",
        "al4W27W29": "Censorship of films and magazines is necessary to uphold moral standards.",
        "al5W27W29": "People who break the law should be given stiffer sentences.",
    }
    for question in values2_questions:
        if question in row and row[question] != 99:
            agreement = row[question]
            if agreement == 5:
                policies.append(f"💯 Strongly agree: {values2_texts[question]}")
            elif agreement == 4:
                policies.append(f"👍 Agree: {values2_texts[question]}")
            elif agreement == 3:
                policies.append(f"😐 Neutral on: {values2_texts[question]}")
            elif agreement == 2:
                policies.append(f"👎 Disagree: {values2_texts[question]}")
            elif agreement == 1:
                policies.append(f"🚫 Strongly disagree: {values2_texts[question]}")

    # Culture Wars
    culture_wars_questions = [
        "cwLanguageW26W27",
        "cwStatuesW26W27",
        "cwTrainingW26W27",
        "cwAuthorsW26W27",
        "cwTransW26W27",
        "cwParentsW26W27",
    ]
    culture_wars_texts = {
        "cwLanguageW26W27": "Too many people are easily offended these days over the language that others use.",
        "cwStatuesW26W27": "Statues of historical figures shouldn't be taken down, even if they profited from the slave trade.",
        "cwTrainingW26W27": "Workplaces should end mandatory diversity training.",
        "cwAuthorsW26W27": "Curriculums should include fewer white male authors and more female and non-white authors.",
        "cwTransW26W27": "Transgender women should be allowed to compete in female sports.",
        "cwParentsW26W27": "BBC children's shows should portray more families with same-sex parents.",
    }
    for question in culture_wars_questions:
        if question in row and row[question] != 99:
            agreement = row[question]
            if agreement == 5:
                policies.append(f"💯 Strongly agree: {culture_wars_texts[question]}")
            elif agreement == 4:
                policies.append(f"👍 Agree: {culture_wars_texts[question]}")
            elif agreement == 3:
                policies.append(f"😐 Neutral on: {culture_wars_texts[question]}")
            elif agreement == 2:
                policies.append(f"👎 Disagree: {culture_wars_texts[question]}")
            elif agreement == 1:
                policies.append(f"🚫 Strongly disagree: {culture_wars_texts[question]}")

    # Scottish Referendum Intention
    if "scotReferendumIntentionW29" in row and row["scotReferendumIntentionW29"] != 99:
        vote = row["scotReferendumIntentionW29"]
        if vote == 1:
            policies.append("🏴󠁧󠁢󠁳󠁣󠁴󠁿 I'd vote Yes for Scottish independence.")
        elif vote == 0:
            policies.append("🤝 I'd vote No to stay in the UK.")
        elif vote == 2:
            policies.append("🗳️ I wouldn't vote in the Scottish referendum.")

    # British Pride
    if "britishPrideW27" in row and row["britishPrideW27"] != 99:
        agreement = row["britishPrideW27"]
        if agreement == 5:
            policies.append("🇬🇧 I strongly feel proud to be British.")
        elif agreement == 4:
            policies.append("🇬🇧 I feel proud to be British.")
        elif agreement == 3:
            policies.append(
                "🤔 I neither agree nor disagree about feeling proud to be British."
            )
        elif agreement == 2:
            policies.append("🙁 I don't feel proud to be British.")
        elif agreement == 1:
            policies.append("😞 I strongly don't feel proud to be British.")

    return policies


def get_country_emoji(country_code):
    country_emojis = {
        1: "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        2: "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
        3: "🏴󠁧󠁢󠁷󠁬󠁳󠁿",
    }
    return country_emojis.get(country_code, "")


def get_eu_referendum_intention(code):
    intention_map = {
        0: "🇪🇺 I would vote to rejoin the EU today",
        1: "🚫 I would vote to stay out of the EU today",
    }
    return intention_map.get(code, None)


def get_eu_referendum_vote(code):
    vote_map = {
        0: "🇪🇺 I voted to remain in the EU in 2016",
        1: "🚫 I voted to leave the EU in 2016",
    }
    return vote_map.get(code, None)
