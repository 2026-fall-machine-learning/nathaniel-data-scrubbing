CREATE OR REPLACE TABLE animals AS
SELECT * FROM read_csv_auto('animals.csv');

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
