import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)

N_PLAYERS = 10_000
MAX_DAYS = 7

rows = []

start_date = pd.Timestamp("2026-01-01")


def add_event(
    player_id,
    day,
    event_name,
    stage=None,
    gold_change=0,
    purchase_value=0,
):
    event_time = (
        start_date
        + pd.Timedelta(days=int(day))
        + pd.Timedelta(minutes=np.random.randint(0, 1440))
    )

    rows.append(
        {
            "player_id": player_id,
            "event_time": event_time,
            "day": day,
            "event_name": event_name,
            "stage": stage,
            "gold_change": gold_change,
            "purchase_value": purchase_value,
        }
    )


for player_id in range(1, N_PLAYERS + 1):

    # Every player installs / starts the game
    add_event(player_id, 0, "game_start")

    # -------------------------
    # Tutorial
    # -------------------------

    tutorial_complete = np.random.rand() < 0.90

    if not tutorial_complete:
        continue

    add_event(player_id, 0, "tutorial_complete")

    # -------------------------
    # First battle
    # -------------------------

    first_battle = np.random.rand() < 0.92

    if not first_battle:
        continue

    won_first_battle = np.random.rand() < 0.85

    add_event(
        player_id,
        0,
        "battle_complete",
        stage=1,
    )

    if not won_first_battle:
        continue

    # Battle reward
    add_event(
        player_id,
        0,
        "currency_earned",
        gold_change=120,
    )

    # -------------------------
    # Hero recruit
    # -------------------------

    recruited = np.random.rand() < 0.85

    if recruited:
        add_event(
            player_id,
            0,
            "hero_recruit",
        )

    # -------------------------
    # Hero upgrade
    # -------------------------

    upgraded = recruited and np.random.rand() < 0.72

    if upgraded:
        add_event(
            player_id,
            0,
            "hero_upgrade",
            gold_change=-100,
        )

    # Players who upgrade early are slightly more likely to return
    retention_multiplier = 1.15 if upgraded else 0.90

    # -------------------------
    # Days 1-7
    # -------------------------

    base_return_prob = 0.42

    active = True

    for day in range(1, MAX_DAYS + 1):

        if not active:
            break

        return_prob = (
            base_return_prob
            * retention_multiplier
            * (0.88 ** (day - 1))
        )

        if np.random.rand() > return_prob:
            active = False
            break

        add_event(player_id, day, "session_start")

        # Daily reward
        add_event(
            player_id,
            day,
            "daily_reward",
            gold_change=50,
        )

        # Player attempts between 1 and 4 battles
        battles = np.random.randint(1, 5)

        for _ in range(battles):

            stage = min(
                2 + day + np.random.randint(0, 3),
                10,
            )

            # Stage 5 deliberately harder
            if stage == 5:
                win_probability = 0.48
            else:
                win_probability = 0.75

            won = np.random.rand() < win_probability

            add_event(
                player_id,
                day,
                "battle_complete",
                stage=stage,
            )

            if won:
                add_event(
                    player_id,
                    day,
                    "currency_earned",
                    gold_change=40,
                )

        # Some players upgrade again
        if np.random.rand() < 0.35:
            add_event(
                player_id,
                day,
                "hero_upgrade",
                gold_change=-80,
            )

        # Small amount of monetisation
        if np.random.rand() < 0.025:
            purchase = np.random.choice(
                [1.99, 4.99, 9.99]
            )

            add_event(
                player_id,
                day,
                "purchase",
                purchase_value=purchase,
            )


df = pd.DataFrame(rows)

df = df.sort_values(
    ["player_id", "event_time"]
).reset_index(drop=True)

# Calculate running gold balance
df["gold_balance"] = (
    df.groupby("player_id")["gold_change"]
    .cumsum()
)

output_dir = Path("data")
output_dir.mkdir(exist_ok=True)

output_file = output_dir / "player_events.csv"

df.to_csv(output_file, index=False)

print(df.head())
print()
print(f"Players: {df['player_id'].nunique():,}")
print(f"Events: {len(df):,}")
print(f"Saved to: {output_file}")