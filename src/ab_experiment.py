import numpy as np 
import pandas as pd 
import sqlite3
import os
from pathlib import Path
from dotenv import load_dotenv
from statsmodels.stats.proportion import proportions_ztest
load_dotenv()

np.random.seed(1234)
DB_PATH = Path(os.getenv("DB_PATH"))
conn = sqlite3.connect(DB_PATH)

rng = np.random.default_rng(123)

query = """
    SELECT DISTINCT player_id
    FROM player_events
    WHERE event_name = 'battle_complete'
    AND stage =5
"""

player = pd.read_sql_query(query, conn )

conn.close()

# print(player.head())
# print(len(player))
player["group"] = np.random.choice(
    ["control", "treatment"],
    size=len(player),
    p= [0.5,0.5]
)
# print(player["group"].value_counts())

player["upgrade_probability"] = np.where(
    player["group"] == "treatment",
    0.65,
    0.45
)

player["upgraded"] = (
    np.random.random(len(player))
    < player["upgrade_probability"]
)

player["win_probability"] = np.where(
    player["upgraded"],
    0.58,
    0.45
)

player["stage5_win"] = (
    np.random.random(len(player)) < player['win_probability']
)


control = player[player["group"] == 'control']

treatment = player[player["group"] == 'treatment']

wins = np.array([
    treatment['stage5_win'].sum()
    ,control['stage5_win'].sum()
])

total = np.array([
    len(treatment),
    len(control)]
)

z_stat, p_value = proportions_ztest(
    wins,total
)
print("="*40)
print(f"p-vlaue:{p_value:.4f}")
p_treatment = treatment["stage5_win"].mean()
p_control = control["stage5_win"].mean()

difference = (p_treatment - p_control)

#SE
se = np.sqrt(
    p_treatment *(1-p_treatment)/len(treatment)
    +
    p_control * (1-p_control)/ len(control)
)

#CI
ci_low = difference - 1.96 * se
ci_high = difference + 1.96 * se

print(
    f"Lift: {difference:.2%}"
)

print(
    f"95% CI: "
    f"[{ci_low:.2%}, {ci_high:.2%}]"
)

player["bouns_gold"] = np.where(
    player['group'] == 'treatment',
    100, 
    0
)

player['gold_spend_on_upgrade'] = np.where(
    player['upgraded'],
    80, 0
)

player["starting_gold"] = np.maximum(
    np.random.normal(
        loc=100,
        scale=45,
        size=len(player)
    ),0
)

player["ending_gold"] = (
    player['starting_gold']+ player['bouns_gold'] - player['gold_spend_on_upgrade']
)

summary = (
    player
    .groupby("group")
    .agg(
        players=("player_id", "count"),
        upgrade_rate=("upgraded", "mean"),
        win_rate=("stage5_win", "mean"),
        avg_ending_gold=("ending_gold", "mean")
    )
)

summary["upgrade_rate"] *= 100
summary["win_rate"] *= 100
print("="*40)
print(summary)
player.to_csv(
    "data/ab_test_results.csv",
    index=False
)

conn = sqlite3.connect(
    DB_PATH
)

player.to_sql(
    "ab_test_result",
    conn,
    if_exists="replace",
    index=False
)

conn.close()