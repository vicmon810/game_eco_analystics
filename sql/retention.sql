-- Early-game retention analysis
-- D1, D3 and D7 exact-day retention

WITH total_players AS (
    SELECT COUNT(DISTINCT player_id) AS players
    FROM player_events
),

retained_players AS (
    SELECT
        day,
        COUNT(DISTINCT player_id) AS retained_players
    FROM player_events
    WHERE day IN (1, 3, 7)
    GROUP BY day
)

SELECT
    r.day,
    r.retained_players,
    t.players AS total_players,
    ROUND(
        100.0 * r.retained_players / t.players,
        2
    ) AS retention_rate_pct
FROM retained_players r
CROSS JOIN total_players t
ORDER BY r.day;