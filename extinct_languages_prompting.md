# Extinct Languages Prompting Log

## Prompts (word for word)

1. I want to use extinct_languages.csv to create a summary table that includes name in english, speakers, and degree of endangerment. Use one-hot encoding on the degree of endangerment column to split it into three columns with 1 or 0 as the values.
2. Put all the code in a file called extinct_languages.py, and no not run it, I will run to test it
3. This is a solid foundation, but I would like to make a few changes: remove the row number column from the start of the table, sort from largest to smallest by number of speakers, format number of speakers without the decimal, and only include the top ten results
4. Change number of speakers column label to speakers, and update the order of the one-hot encoded columns to: vulnerable, definitely endangered, severely endangered, critically endangered, extinct, do not run, I will run it manually
5. That looks good, now create a md file called exinct_languages_prompting that contains all of my prompts from this session, also include any questions you asked me and what my answers were

## Clarifying Questions Asked

1. **Question:** The "Degree of endangerment" column in extinct_languages.csv actually has 5 unique categories (Vulnerable, Definitely endangered, Severely endangered, Critically endangered, Extinct), not 3. How would you like to handle this?
   - Choices offered: One-hot encode all 5 categories as their own 0/1 columns (ignore the "three" count) / Group the 5 categories into 3 broader buckets, then one-hot encode those 3 / Only include 3 specific categories (and I'll tell you which) as 0/1 columns, dropping/excluding the rest
   - **Answer:** One-hot encode all 5 categories as their own 0/1 columns (ignore the "three" count)

2. **Question:** Should the resulting summary table just be printed to the console (matching animals.py/inventory.py), or also saved to a new CSV file?
   - Choices offered: Just print it (matches existing scripts) / Print it and also save to a new CSV file
   - **Answer:** Just print it (matches existing scripts)

## Final Python (extinct_languages.py)

```python
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
```
