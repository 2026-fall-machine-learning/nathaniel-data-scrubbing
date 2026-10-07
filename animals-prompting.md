# Animals Prompting Log

## Prompts (word for word)

1. sql to aggregate animals table from animals.csv, create animals table, i plan to run in duckdb myself, don't run just gen sql
2. want to see the average race time in mm:ss, and don't want all the other totals stuff
3. Invalid Input Error: Invalid type specifier "d" for formatting a value of type float
4. im in duckdb, i want to preserve all the columns
5. that gave me the same result of only one average, i wanted to aggregate by meat eater and keep all the original columns, with the average race time in mm:ss
6. what about loose python to do this in animals.py
7. what about m code to run in power query
8. please create an animals-prompting.md file with all my prompts word for word, and just the final versions of sql, py, and m

## Final SQL (DuckDB)

```sql
-- Preserve all original columns as-is
CREATE OR REPLACE TABLE animals AS
SELECT * FROM read_csv_auto('animals.csv');

-- Aggregate by meat_eater, keeping original columns as lists, with average race time in mm:ss
SELECT
    meat_eater,
    list(animal)     AS animals,
    list(legs)       AS legs,
    list(tail)       AS tails,
    list(race_time)  AS race_times,
    printf('%02d:%02d',
        CAST(AVG(CAST(split_part(race_time, ':', 1) AS INTEGER) * 60
                 + CAST(split_part(race_time, ':', 2) AS INTEGER)) AS INTEGER) // 60,
        CAST(AVG(CAST(split_part(race_time, ':', 1) AS INTEGER) * 60
                 + CAST(split_part(race_time, ':', 2) AS INTEGER)) AS INTEGER) % 60
    ) AS avg_race_time
FROM animals
GROUP BY meat_eater;
```

## Final Python (animals.py)

```python
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
```

## Final M (Power Query)

```m
let
    Source = Csv.Document(
        File.Contents("C:\Users\nrudser\Downloads\nathaniel-data-scrubbing\animals.csv"),
        [Delimiter=",", Columns=5, Encoding=1252, QuoteStyle=QuoteStyle.None]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(PromotedHeaders, {
        {"animal", type text},
        {"meat_eater", type text},
        {"legs", Int64.Type},
        {"tail", type text},
        {"race_time", type text}
    }),

    // parse "mm:ss" race_time into total seconds for averaging
    AddSeconds = Table.AddColumn(ChangedType, "race_time_seconds", each
        let
            parts = Text.Split([race_time], ":"),
            minutes = Number.FromText(parts{0}),
            seconds = Number.FromText(parts{1})
        in
            minutes * 60 + seconds,
        Int64.Type
    ),

    Grouped = Table.Group(AddSeconds, {"meat_eater"}, {
        {"animal", each _[animal], type list},
        {"legs", each _[legs], type list},
        {"tail", each _[tail], type list},
        {"race_time", each _[race_time], type list},
        {"avg_race_time_seconds", each List.Average(_[race_time_seconds]), type number}
    }),

    // convert the averaged seconds back to "mm:ss"
    AddAvgFormatted = Table.AddColumn(Grouped, "avg_race_time", each
        let
            totalSeconds = Number.Round([avg_race_time_seconds]),
            mins = Number.IntegerDivide(totalSeconds, 60),
            secs = Number.Mod(totalSeconds, 60)
        in
            Text.PadStart(Text.From(mins), 2, "0") & ":" & Text.PadStart(Text.From(secs), 2, "0"),
        type text
    ),

    RemovedColumns = Table.RemoveColumns(AddAvgFormatted, {"avg_race_time_seconds"})
in
    RemovedColumns
```
