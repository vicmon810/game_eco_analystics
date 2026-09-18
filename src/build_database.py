import sqlite3
from pathlib import Path 

import pandas as pd 

DATA_PATH = Path("data/player_events.csv")
DB_PATH = Path("data/game_analytics.db")

def main():
    df = pd.read_csv(DATA_PATH)

    connection = sqlite3.connect(DB_PATH)

    df.to_sql(
        "player_events",
        connection,
        if_exists="replace",
        index=False
    )

    connection.execute(
        """
            CREATE INDEX IF NOT EXISTS
                idx_player_id
            ON
                player_events(player_id)
        """
    )

    connection.execute(
        """
            CREATE INDEX IF NOT EXISTS
                idx_event_name
            ON 
                player_events(event_name)
        """
    )

    connection.execute(
        """
            CREATE INDEX IF NOT EXISTS
                idx_day 
            ON
                player_events(day)
        """
    )

    connection.commit()

    count = connection.execute(
        "SELECT COUNT(*) FROM player_events"
    ).fetchone()[0]

    players = connection.execute(
        "SELECT COUNT(DISTINCT player_id) FROM player_events" 
    ).fetchone()[0]

    connection.close()
    print(f"Database created: {DB_PATH}")
    print(f"Rows: {count:,}")
    print(f"Players: {players:,}")


if __name__ == "__main__":
    main()