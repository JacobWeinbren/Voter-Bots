import re
from collections import defaultdict


def extract_demographics(file_content):
    age_distribution = defaultdict(int)
    race_distribution = defaultdict(int)
    gender_distribution = defaultdict(int)

    # Regular expressions for extracting information
    age_pattern = r"aged (\d+)"
    race_pattern = r"I'm a ([\w\s]+) (?:British |)(?:Atheist/Agnostic|Anglican|Catholic|Methodist|Baptist|Presbyterian|United Reformed|Brethren|Buddhist|Sikh|Muslim|Hindu)"
    gender_pattern = r"(man|woman)"

    # Split the content into individual profiles
    profiles = file_content.split("\n\n")

    for profile in profiles:
        # Extract age
        age_match = re.search(age_pattern, profile)
        if age_match:
            age = int(age_match.group(1))
            age_group = f"{age // 10 * 10}-{age // 10 * 10 + 9}"
            age_distribution[age_group] += 1

        # Extract race
        race_match = re.search(race_pattern, profile)
        if race_match:
            race = race_match.group(1).strip()
            race_distribution[race] += 1

        # Extract gender
        gender_match = re.search(gender_pattern, profile)
        if gender_match:
            gender = gender_match.group(1)
            gender_distribution[gender] += 1

    return age_distribution, race_distribution, gender_distribution


def print_distribution(distribution, title):
    print(f"\n{title}:")
    total = sum(distribution.values())
    for key, value in sorted(distribution.items()):
        percentage = (value / total) * 100
        print(f"{key}: {value} ({percentage:.2f}%)")


# Read the file content
with open("Britain/tweets/tweets.txt", "r") as file:
    content = file.read()

# Extract demographics
age_dist, race_dist, gender_dist = extract_demographics(content)

# Print distributions
print_distribution(age_dist, "Age Distribution")
print_distribution(race_dist, "Race Distribution")
print_distribution(gender_dist, "Gender Distribution")
