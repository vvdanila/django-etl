# Django ETL

A Django project run in Docker that allows the processing of large datasets by using Celery.

## Introduction

The data ingestion is chunked and saved in batches to the database following a wait time between chunks.

## Triggering the data processing

```shell
curl --location 'http://localhost:8000/run-task/' \
--header 'Content-Type: application/json' \
--data '{
    "task": "process_fifa_players_dataset"
}'
```

## Accessing the Male Player data ordered by date and grouped by potential

```shell
curl --location 'http://localhost:8000/male_players/'
```

## Notes

Accessing the data before the ingestion has finished can lead to database locks as both are accessing the same table.
This project is a proof of concept and is not production ready in the current state.

## TODOs

Add unit tests

## Datasets

The dataset of male players has been sourced from [Kaggle](https://www.kaggle.com/datasets/stefanoleone992/fifa-23-complete-player-dataset?resource=download&select=male_players.csv)
The male players file has been split from the original to only contain 100MB. 

## Formatting 

The project has been formatted with black.
