import csv
import time

from datetime import datetime

from celery import shared_task

from .models import MalePlayer


@shared_task
def process_fifa_players_dataset():
    chunk_size = 1000
    wait_time = 0.5

    file_path = "datasets/fifa_23_male_players.csv"
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        chunk = []

        for i, row in enumerate(reader):
            player_id = row["player_id"]
            player_url = row["player_url"]
            fifa_version = row["fifa_version"]
            fifa_update = row["fifa_update"]
            fifa_update_date = datetime.strptime(
                row["fifa_update_date"], "%Y-%m-%d"
            ).date()
            short_name = row["short_name"]
            long_name = row["long_name"]
            player_positions = row["player_positions"]
            overall = int(row["overall"])
            potential = int(row["potential"])

            chunk.append(
                MalePlayer(
                    player_id=player_id,
                    player_url=player_url,
                    fifa_version=fifa_version,
                    fifa_update=fifa_update,
                    fifa_update_date=fifa_update_date,
                    short_name=short_name,
                    long_name=long_name,
                    player_positions=player_positions,
                    overall=overall,
                    potential=potential,
                )
            )

            if i % chunk_size == 0 and i > 0:
                MalePlayer.objects.bulk_create(chunk)
                chunk = []
                time.sleep(wait_time)

        if chunk:
            MalePlayer.objects.bulk_create(chunk)
