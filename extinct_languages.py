import pandas as pd

extinct_languages = pd.read_csv("extinct_languages.csv")

endangerment_dummies = pd.get_dummies(extinct_languages["Degree of endangerment"]).astype(int)

extinct_languages_summary = pd.concat(
    [extinct_languages[["Name in English", "Number of speakers"]], endangerment_dummies],
    axis=1,
)

print(extinct_languages_summary)
