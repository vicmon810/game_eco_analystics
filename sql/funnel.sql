WITH total_players AS (
    SELECT COUNT(DISTINCT player_id) AS total
    FROM player_events
),

funnel AS (

    SELECT
        1 AS step,
        'Game Start' AS stage,
        COUNT(DISTINCT player_id) AS players
    FROM player_events
    WHERE event_name = 'game_start'

    UNION ALL

    SELECT
        2,
        'Tutorial Complete',
        COUNT(DISTINCT player_id)
    FROM player_events
    WHERE event_name = 'tutorial_complete'

    UNION ALL

    SELECT
        3,
        'First Battle',
        COUNT(DISTINCT player_id)
    FROM player_events
    WHERE event_name = 'battle_complete'
      AND day = 0

    UNION ALL

    SELECT
        4,
        'Hero Recruit',
        COUNT(DISTINCT player_id)
    FROM player_events
    WHERE event_name = 'hero_recruit'
      AND day = 0

    UNION ALL

    SELECT
        5,
        'Hero Upgrade',
        COUNT(DISTINCT player_id)
    FROM player_events
    WHERE event_name = 'hero_upgrade'
      AND day = 0

    UNION ALL

    SELECT
        6,
        'D1 Return',
        COUNT(DISTINCT player_id)
    FROM player_events
    WHERE day = 1
)

SELECT
    f.step,
    f.stage,
    f.players,

    ROUND(
        100.0 * f.players / t.total,
        2
    ) AS pct_of_installs

FROM funnel f
CROSS JOIN total_players t

ORDER BY f.step;