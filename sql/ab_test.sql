-- ==========================================
-- Early-Game Analytics
-- A/B Test Analysis
-- ==========================================

WITH ab_test_players AS (

    SELECT
        player_id,
        "group",
        upgraded,
        stage5_win,
        ending_gold

    FROM ab_test_result

),

summary AS (

    SELECT

        "group",

        -- Total players
        COUNT(DISTINCT player_id) AS players,

        -- Players who upgraded their hero
        SUM(
            CASE
                WHEN upgraded = 1 THEN 1
                ELSE 0
            END
        ) AS upgraded_players,

        -- Players who won Stage 5
        SUM(
            CASE
                WHEN stage5_win = 1 THEN 1
                ELSE 0
            END
        ) AS winning_players,

        -- Average remaining gold
        AVG(ending_gold) AS avg_ending_gold

    FROM ab_test_players

    GROUP BY "group"

)

SELECT

    "group",

    players,

    upgraded_players,

    ROUND(
        100.0 * upgraded_players
        / NULLIF(players, 0),
        2
    ) AS upgrade_rate_pct,

    winning_players,

    ROUND(
        100.0 * winning_players
        / NULLIF(players, 0),
        2
    ) AS stage5_win_rate_pct,

    ROUND(
        avg_ending_gold,
        2
    ) AS avg_ending_gold

FROM summary

ORDER BY "group";