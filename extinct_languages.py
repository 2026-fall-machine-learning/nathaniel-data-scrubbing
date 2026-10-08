import pandas as pd

extinct_languages = pd.read_csv("extinct_languages.csv")

endangerment_order = [
    "Vulnerable",
    "Definitely endangered",
    "Severely endangered",
    "Critically endangered",
    "Extinct",
]
endangerment_dummies = pd.get_dummies(extinct_languages["Degree of endangerment"]).astype(int)
endangerment_dummies = endangerment_dummies[endangerment_order]

extinct_languages_summary = pd.concat(
    [extinct_languages[["Name in English", "Number of speakers"]], endangerment_dummies],
    axis=1,
)
extinct_languages_summary = extinct_languages_summary.rename(columns={"Number of speakers": "Speakers"})

# keep the ten languages with the most speakers, largest first
extinct_languages_summary = extinct_languages_summary.sort_values(
    "Speakers", ascending=False
).head(10)

# drop the decimal from the speaker counts now that NaN rows are excluded
extinct_languages_summary["Speakers"] = extinct_languages_summary["Speakers"].astype(int)

print(extinct_languages_summary.to_string(index=False))
