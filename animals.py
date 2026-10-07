import pandas as pd

animals = pd.read_csv("animals.csv")

# parse "mm:ss" race_time into total seconds for averaging
minutes, seconds = animals["race_time"].str.split(":", expand=True).astype(int).values.T
animals["race_time_seconds"] = minutes * 60 + seconds

animals_grouped = animals.groupby("meat_eater").agg({
    "animal": list,
    "legs": list,
    "tail": list,
    "race_time": list,
    "race_time_seconds": "mean",
})

# convert the averaged seconds back to "mm:ss"
animals_grouped["avg_race_time"] = animals_grouped["race_time_seconds"].apply(
    lambda s: f"{int(s) // 60:02d}:{int(s) % 60:02d}"
)
animals_grouped = animals_grouped.drop(columns="race_time_seconds")

print(animals_grouped)
