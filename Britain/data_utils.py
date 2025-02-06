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
        return "economically moderate ⚖️"
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
        return "socially moderate ⚖️"
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
        18: ("🗺️ Devolution", "is"),
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
        6: "I live rent-free in a family member or friend's home",
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

    # Democracy Satisfaction - W29
    if "satDemUKW29" in row and row["satDemUKW29"] != 99:
        satisfaction_map = {
            1: "😠 Very dissatisfied with UK democracy",
            2: "😕 Somewhat dissatisfied with UK democracy",
            3: "🙂 Fairly satisfied with UK democracy",
            4: "😊 Very satisfied with UK democracy",
        }
        policies.append(satisfaction_map.get(row["satDemUKW29"], ""))

    # Electoral System Preference - W29
    if "prPreferenceW29" in row and row["prPreferenceW29"] != 99:
        policies.append(
            "🗳️ Believe seats should match vote percentages (proportional representation)"
            if row["prPreferenceW29"] == 2
            else "🏛️ Prefer one party having majority to govern alone"
        )

    # EU Integration Position - W29
    if "EUIntegrationSelfW29" in row and row["EUIntegrationSelfW29"] != 99:
        position = row["EUIntegrationSelfW29"]
        if position >= 7:
            policies.append("🇬🇧 Strongly believe EU integration has gone too far")
        elif position <= 3:
            policies.append("🇪🇺 Strongly support European integration going further")
        else:
            policies.append("🤝 Mixed view on European integration")

    # Income Equality - W29
    if "redistSelfW29" in row and row["redistSelfW29"] != 99:
        stance = row["redistSelfW29"]
        if stance <= 3:
            policies.append(
                "🟰 Strongly support government efforts to make incomes more equal"
            )
        elif stance <= 6:
            policies.append("⚖️ Somewhat support income equality efforts")
        else:
            policies.append(
                "🤷 Believe government should be less concerned about income equality"
            )

    # Environment vs Economy - W28
    if "enviroGrowthW28" in row and row["enviroGrowthW28"] != 99:
        value = row["enviroGrowthW28"]
        if value >= 5:
            policies.append(
                "🌳 Prioritise environmental protection over economic growth"
            )
        elif value <= 3:
            policies.append("💰 Prioritise economic growth over environment protection")
        else:
            policies.append(
                "⚖️ Seek balance between environmental protection and economic growth"
            )

    # Immigration Impact - W27
    econ = row.get("immigEconW27", 9999)
    cultural = row.get("immigCulturalW27", 9999)
    if econ != 9999 and cultural != 9999:
        avg = (econ + cultural) / 2
        if avg >= 5:
            policies.append("🌍 Believe immigration benefits both economy and culture")
        elif avg <= 3:
            policies.append(
                "🚫 Think immigration negatively impacts economy and culture"
            )
        else:
            policies.append("⚖️ Neutral on immigration's economic and cultural impacts")

    # Equality Efforts - W27
    equality_issues = {
        "blackEqualityW27": (
            "🤝",
            "Attempts to give equal opportunities to ethnic minorities have",
        ),
        "femaleEqualityW27": (
            "♀️",
            "Efforts for women's equal opportunities have",
        ),
        "gayEqualityW27": (
            "🏳️‍🌈",
            "Initiatives for gay and lesbian equality have",
        ),
    }

    for var, (emoji, text) in equality_issues.items():
        val = row.get(var, 99)
        if val != 99:
            if val <= 2:
                policies.append(f"{emoji} {text} not gone far enough")
            elif val == 3:
                policies.append(f"{emoji} {text} been about right")
            elif val >= 4:
                policies.append(f"{emoji} {text} gone too far")

    # Perceptions of Poverty - W20
    poverty_perceptions = {
        "reasonForUnemploymentW20": "When someone is unemployed, it's usually through no fault of their own",
        "immigrantsWelfareStateW20": "Immigrants are a burden on the welfare state",
        "govtHandoutsW20": "Too many people rely on government handouts",
        "benefitsNotDeservedW20": "Many people who get benefits don't really deserve help",
    }

    for var, statement in poverty_perceptions.items():
        val = row.get(var, 99)
        if val != 99:
            response = {
                5: f"💯 Strongly agree: {statement}",
                4: f"👍 Agree: {statement}",
                3: f"😐 Neutral: {statement}",
                2: f"👎 Disagree: {statement}",
                1: f"🚫 Strongly disagree: {statement}",
            }.get(val, "")
            if response:
                policies.append(response)

    # Zero-hour Contracts - W27
    if "zeroHourContractW27" in row and row["zeroHourContractW27"] != 99:
        contract_map = {
            1: "🚫 Strongly believe zero-hours contracts should be illegal",
            2: "❌ Think zero-hours contracts should probably be illegal",
            3: "✅ Believe zero-hours contracts should probably remain legal",
            4: "💯 Strongly support keeping zero-hours contracts legal",
        }
        policies.append(contract_map.get(row["zeroHourContractW27"], ""))

    # Welfare Benefits - W27
    if "welfarePreferenceW27" in row and row["welfarePreferenceW27"] != 99:
        welfare_map = {
            1: "📉 Strongly believe welfare benefits are too high",
            2: "↘️ Believe welfare benefits are too high",
            3: "💰 Feel current benefit levels are about right",
            4: "↗️ Believe welfare benefits are too low",
            5: "📈 Strongly believe welfare benefits are too low",
        }
        policies.append(welfare_map.get(row["welfarePreferenceW27"], ""))

    # Nationalization Policies - W26
    nationalization_items = {
        "nationalizeTrains": "train services",
        "nationalizeHospitals": "hospitals",
        # "nationalizeUtilities": "domestic utilities (gas, electricity, water)",
        "nationalizeSchools": "schools",
    }

    for var, statement in nationalization_items.items():
        val = row.get(var, 9999)
        if val != 9999:
            response = {
                1: f"🏛️ Entirely by the public sector: {statement}",
                2: f"🏛️ Mostly by the public sector: {statement}",
                3: f"⚖️ Equally by the public and private sector: {statement}",
                4: f"🏭 Mostly by the private sector: {statement}",
                5: f"🏭 Entirely by the private sector: {statement}",
            }.get(val, "")
            if response:
                policies.append(response)

    # Welsh Devolution Preferences - W27
    if "devoPrefWalesW27" in row and row["devoPrefWalesW27"] != 99:
        devo_map = {
            1: "🇬🇧 No devolved government in Wales",
            2: "🇬🇧 Reduce Welsh Parliament powers",
            3: "⚖️ Maintain current Welsh devolution settlement",
            4: "🏴󠁧󠁢󠁷󠁬󠁳󠁿 Expand Welsh Parliament powers",
            5: "🏴󠁧󠁢󠁷󠁬󠁳󠁿 Support Welsh independence from UK",
        }
        policies.append(devo_map.get(row["devoPrefWalesW27"], ""))

    # Tax and Spending - W28
    if "taxSpendSelfW28" in row and row["taxSpendSelfW28"] != 99:
        value = row["taxSpendSelfW28"]
        if value <= 3:
            policies.append("⬇️ Favour significant tax cuts and reduced social spending")
        elif 4 <= value <= 6:
            policies.append("⚖️ Support no major changes to tax and spending levels")
        else:
            policies.append("⬆️ Favour higher taxes for expanded social spending")

    # Globalization View - W21
    if "globalGoodOverallW21" in row and row["globalGoodOverallW21"] != 99:
        global_map = {
            1: "👎 Strongly negative view of globalisation",
            2: "↘️ Mostly negative view of globalisation",
            3: "⚖️ Neutral perspective on globalisation",
            4: "↗️ Mostly positive view of globalisation",
            5: "👍 Strongly positive view of globalisation",
        }
        policies.append(global_map.get(row["globalGoodOverallW21"], ""))

    # Change Preferences - W27
    change_preferences = {
        "radicalW27": ("🔄", "We need to fundamentally change how society works"),
        "harkBackW27": ("🕰️", "Things in Britain were better in the past"),
    }
    for var, (emoji, statement) in change_preferences.items():
        val = row.get(var, 99)
        if val != 99:
            response = {
                5: f"💯 Strongly agree: {statement}",
                4: f"👍 Agree: {statement}",
                3: f"😐 Neutral: {statement}",
                2: f"👎 Disagree: {statement}",
                1: f"🚫 Strongly disagree: {statement}",
            }.get(val, "")
            if response:
                policies.append(response)

    # Immigration Levels - W29
    if "immigSelfW29" in row and row["immigSelfW29"] != 99:
        position = row["immigSelfW29"]
        if position >= 7:
            policies.append("🌍 Support allowing many more immigrants to the UK")
        elif position <= 3:
            policies.append("🚫 Believe UK should allow many fewer immigrants")
        else:
            policies.append("⚖️ Satisfied with current immigration levels")

    # Israel-Palestine Conflict - W28
    if "israelPalestineW28" in row and row["israelPalestineW28"] != 99:
        stance = row["israelPalestineW28"]
        stance_map = {
            1: "🇮🇱 Strongly sympathise with Israel over Palestine",
            2: "🇮🇱 Lean toward Israel over Palestine",
            3: "🤝 Neutral on Israeli-Palestinian conflict",
            4: "🇵🇸 Lean toward Palestine over Israel",
            5: "🇵🇸 Strongly sympathise with Palestine over Israel",
        }
        policies.append(stance_map.get(stance, ""))

    # Economic Values (values1) - W27/W29
    economic_values = {
        "lr1W27W29": "Government should redistribute income from rich to poor",
        "lr2W27W29": "Big business takes advantage of ordinary people",
        "lr3W27W29": "Workers don't get fair share of nation's wealth",
        "lr4W27W29": "There is one law for the rich and one for the poor",
        "lr5W27W29": "Management exploits employees when possible",
    }
    for var, statement in economic_values.items():
        val = row.get(var, 99)
        if val != 99:
            response = {
                5: f"💯 Strongly agree: {statement}",
                4: f"👍 Agree: {statement}",
                3: f"😐 Neutral: {statement}",
                2: f"👎 Disagree: {statement}",
                1: f"🚫 Strongly disagree: {statement}",
            }.get(val, "")
            if response:
                policies.append(response)

    # Social Values (values2) - W27/W29
    social_values = {
        "al1W27W29": "Young people lack respect for traditional values",
        "al2W27W29": "Death penalty appropriate for some crimes",
        "al3W27W29": "Schools should teach obedience to authority",
        "al4W27W29": "Need censorship to uphold morals",
        "al5W27W29": "Stiffer sentences for lawbreakers",
    }
    for var, statement in social_values.items():
        val = row.get(var, 99)
        if val != 99:
            response = {
                5: f"💯 Strongly agree: {statement}",
                4: f"👍 Agree: {statement}",
                3: f"😐 Neutral: {statement}",
                2: f"👎 Disagree: {statement}",
                1: f"🚫 Strongly disagree: {statement}",
            }.get(val, "")
            if response:
                policies.append(response)

    # Culture Wars - W26/W27
    culture_war_issues = {
        "cwLanguageW26W27": ("🗣️", "People are too easily offended by language"),
        "cwStatuesW26W27": (
            "🏛️",
            "Keep statues of prominent historical figures, even if they profited from slavery",
        ),
        "cwTrainingW26W27": (
            "🏢",
            "Workplaces should end mandatory diversity training",
        ),
        "cwAuthorsW26W27": (
            "📚",
            "School and university curriculums should include more female/non-white authors",
        ),
        "cwTransW26W27": ("🏳️‍⚧️", "Transgender women in female sports"),
        "cwParentsW26W27": (
            "👪",
            "BBC children's TV shows should portray more families with same-sex parents",
        ),
    }
    for var, (emoji, statement) in culture_war_issues.items():
        val = row.get(var, 99)
        if val != 99:
            response = {
                5: f"💯 Strongly agree: {statement}",
                4: f"👍 Agree: {statement}",
                3: f"😐 Neutral: {statement}",
                2: f"👎 Disagree: {statement}",
                1: f"🚫 Strongly disagree: {statement}",
            }.get(val, "")
            if response:
                policies.append(response)

    # Scottish Independence - W29
    if "scotReferendumIntentionW29" in row and row.get("countryW29") == 2:
        val = row["scotReferendumIntentionW29"]
        if val == 1:
            policies.append("🏴󠁧󠁢󠁳󠁣󠁴󠁿 Would vote Yes for Scottish independence")
        elif val == 0:
            policies.append("🇬🇧 Would vote No to Scottish independence")

    # British Pride - W27
    if "britishPrideW27" in row and row["britishPrideW27"] != 99:
        pride_map = {
            5: "💯 Strongly agree: I feel proud to be British",
            4: "👍 Agree: I feel proud to be British",
            3: "😐 Neutral: I feel proud to be British",
            2: "👎 Disagree: I feel proud to be British",
            1: "🚫 Strongly disagree: I feel proud to be British",
        }
        policies.append(pride_map.get(row["britishPrideW27"], ""))

    # Deficit Reduction - W27
    if "deficitReduceW27" in row and row["deficitReduceW27"] != 99:
        deficit_map = {
            4: "🚨 Completely necessary to eliminate deficit",
            3: "⚠️ Important but not essential to eliminate deficit",
            2: "✨ It is desirable but not required to eliminate deficit",
            1: "🟢 No need to eliminate deficit at all",
        }
        policies.append(deficit_map.get(row["deficitReduceW27"], ""))

    # Monarchy Support - W25
    if "monarchW25" in row and row["monarchW25"] != 99:
        monarch_map = {
            5: "💯 Strongly support: Keeping the monarchy",
            4: "👍 Support: Keeping the monarchy",
            3: "😐 Neutral: Keeping the monarchy",
            2: "👎 Oppose: Keeping the monarchy",
            1: "🚫 Strongly oppose: Keeping the monarchy",
        }
        policies.append(monarch_map.get(row["monarchW25"], ""))

    # Scottish Devolution Max - W21
    if "scotDevoMaxW21" in row and row.get("countryW21") == 2:
        devo_map = {
            5: "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Strongly support many more powers for the Scottish Parliament",
            4: "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Support some more powers for the Scottish Parliament",
            3: "⚖️ Support maintaining the Scottish Parliament's current powers",
            2: "🇬🇧 Support fewer powers for the Scottish Parliament",
            1: "🇬🇧 Strongly support many fewer powers for the Scottish Parliament",
        }
        policies.append(devo_map.get(row["scotDevoMaxW21"], ""))

    # Economic Ideology - W20
    ideology_items = {
        "jobForAllW20": ("👷", "Government should provide jobs for all"),
    }
    for var, (emoji, statement) in ideology_items.items():
        val = row.get(var, 99)
        if val != 99:
            response = {
                5: f"💯 Strongly agree: {statement}",
                4: f"👍 Agree: {statement}",
                3: f"😐 Neutral: {statement}",
                2: f"👎 Disagree: {statement}",
                1: f"🚫 Strongly disagree: {statement}",
            }.get(val, "")
            if response:
                policies.append(response)

    # Public Service Cuts Assessment - W26
    service_issues = {
        "cutsTooFarNationalW26": ("🏛️", "Public spending cuts have"),
        "cutsTooFarNHSW26": ("🏥", "NHS spending cuts have"),
        "cutsTooFarLocalW26": ("🏘️", "Local service cuts have"),
        "privatTooFarW26": ("🏭", "Private sector in public services has"),
        "enviroProtectionW26": ("🌳", "Environmental protections have"),
    }
    for var, (emoji, text) in service_issues.items():
        val = row.get(var, 99)
        if val not in [99, None]:
            if val in [1, 2]:
                policies.append(f"{emoji} {text} not gone far enough")
            elif val == 3:
                policies.append(f"{emoji} {text} been about right")
            elif val in [4, 5]:
                policies.append(f"{emoji} {text} gone too far")

    # Public vs Private Efficiency - W26
    if "pubPrivEfficientW26" in row and row["pubPrivEfficientW26"] not in [99, None]:
        efficiency_value = row["pubPrivEfficientW26"]
        if efficiency_value <= 3:
            policies.append(
                "🏭 The private sector offers better value for domestic utilities"
            )
        elif 4 <= efficiency_value <= 6:
            policies.append(
                "⚖️ Mixed on private vs public sector efficiency for utilities"
            )
        elif 7 <= efficiency_value <= 10:
            policies.append(
                "🏛️ The public sector provides better value for domestic utilities"
            )

    # Defense Spending - W25
    if "natSecuritySpendingW25" in row and row["natSecuritySpendingW25"] != 99:
        defense_map = {
            5: "🛡️ Strongly support increased defense spending",
            4: "🛡️ Support increased defense spending",
            3: "⚖️ Keep defense spending the same",
            2: "🕊️ Support reduced defense spending",
            1: "🕊️ Strongly support defense spending cuts",
        }
        policies.append(defense_map.get(row["natSecuritySpendingW25"], ""))

    # Nuclear Weapons Policy - W23
    if "keepNukesW23" in row and row["keepNukesW23"] != 99:
        nuke_map = {
            5: "💯 Strongly support: Keeping nuclear weapons",
            4: "👍 Support: Keeping nuclear weapons",
            3: "😐 Neutral: Keeping nuclear weapons",
            2: "👎 Oppose: Keeping nuclear weapons",
            1: "🚫 Strongly oppose: Keeping nuclear weapons",
        }
        policies.append(nuke_map.get(row["keepNukesW23"], ""))

    # Local Funding Fairness - W21
    if "localFairShareW21" in row and row["localFairShareW21"] != 99:
        funding_map = {
            1: "🏘️ My area gets much less funding than its fair share",
            2: "🏠 My area gets somewhat less funding than its fair share",
            3: "⚖️ My area gets fair funding share",
            4: "🏛️ My area gets somewhat more funding than its fair share",
            5: "💰 My area gets much more funding than its fair share",
        }
        policies.append(funding_map.get(row["localFairShareW21"], ""))

    # EU Referendum Repeat - W29
    if "euRefDoOverW29" in row and row["euRefDoOverW29"] != 99:
        policies.append(
            "🇪🇺 Support another EU membership referendum"
            if row["euRefDoOverW29"] == 1
            else "🚫 Oppose new EU referendum"
        )

    # Rail Nationalization - W26
    if "renationaliseRailW26" in row and row["renationaliseRailW26"] != 99:
        rail_map = {
            1: "🚫 Strongly oppose: Rail nationalisation",
            2: "👎 Disagree: Rail nationalisation",
            3: "😐 Neutral: Rail nationalisation",
            4: "👍 Agree: Rail nationalisation",
            5: "💯 Strongly agree: Rail nationalisation",
        }
        policies.append(rail_map.get(row["renationaliseRailW26"], ""))

    # Overseas Aid Policy - W27
    if "overseasAidW27" in row and row["overseasAidW27"] != 99:
        aid_map = {
            1: "🚫 Strongly disagree: Ending foreign aid",
            2: "👎 Disagree: Ending foreign aid",
            3: "😐 Neutral: Ending foreign aid",
            4: "👍 Agree: Ending foreign aid",
            5: "💯 Strongly agree: Ending foreign aid",
        }
        policies.append(aid_map.get(row["overseasAidW27"], ""))

    # Current Policy Support - Various
    policy_support = {
        "abolishPrivSchoolW27": ("🏫", "Abolish private education"),
        "votesAt16W28": ("🗳️", "Lower voting age to 16"),
        "rwandaFlightsW27": ("🇷🇼", "Rwanda asylum plan"),
        "newTownW27": ("🏘️", "Build new towns for housing"),
        "militaryServiceW28": ("🎖️", "Compulsory youth service"),
        "inheritanceTaxW28": ("💰", "Abolish inheritance tax"),
        "breakfastClubW28": ("🍳", "Free school breakfast clubs"),
        "banSmokeW27": ("🚭", "Generational smoking prohibition"),
        "govtEnergyW27": ("⚡", "Create government-owned renewable energy company"),
    }

    for var, (emoji, desc) in policy_support.items():
        val = row.get(var, 99)
        if val != 99:
            response = {
                5: f"💯 Strongly agree: {desc}",
                4: f"👍 Agree: {desc}",
                3: f"😐 Neutral: {desc}",
                2: f"👎 Disagree: {desc}",
                1: f"🚫 Strongly disagree: {desc}",
            }.get(val, "")
            if response:
                policies.append(response)

    # Pension and School Funding - W28
    more_issues = {
        "tripleLockW28": ("💼", "Maintain pension triple lock"),
        "privVATW28": ("🏫", "Keep private school VAT exemption"),
    }

    for var, (emoji, desc) in more_issues.items():
        val = row.get(var, 99)
        if val != 99:
            response = {
                5: f"💯 Strongly agree: {desc}",
                4: f"👍 Agree: {desc}",
                3: f"😐 Neutral: {desc}",
                2: f"👎 Disagree: {desc}",
                1: f"🚫 Strongly disagree: {desc}",
            }.get(val, "")
            if response:
                policies.append(response)

    return [p for p in policies if p]


def get_country_emoji(country_code):
    country_emojis = {
        1: "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        2: "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
        3: "🏴󠁧󠁢󠁷󠁬󠁳󠁿",
    }
    return country_emojis.get(country_code, "")


def get_eu_referendum_intention(code):
    intention_map = {
        0: "🇪🇺 I would vote to rejoin the EU today.",
        1: "🚫 I would vote to stay out of the EU today.",
    }
    return intention_map.get(code, None)


def get_eu_referendum_vote(code):
    vote_map = {
        0: "🇪🇺 I voted to remain in the EU in 2016.",
        1: "🚫 I voted to leave the EU in 2016.",
    }
    return vote_map.get(code, None)


def get_social_grade(soc_grade_code):
    social_grade_map = {
        1: "(A) higher managerial/professional.",
        2: "(B) intermediate managerial/professional.",
        3: "(C1) supervisory/clerical.",
        4: "(C2) skilled manual worker.",
        5: "(D) semi/unskilled manual worker.",
        6: "(E) lowest grade worker.",
    }
    return social_grade_map.get(soc_grade_code) if pd.notna(soc_grade_code) else None


def get_working_status(status_code):
    status_map = {
        4: ("🔍", "unemployed and looking for work."),
        5: ("🎓", "a full time university student."),
        6: ("📚", "a full time student."),
        7: ("🌴", "retired."),
        8: ("🏠", "not in paid work."),
    }
    if pd.notna(status_code) and status_code in status_map:
        emoji, status = status_map[status_code]
        return f"{emoji} I am {status}"
    return None
