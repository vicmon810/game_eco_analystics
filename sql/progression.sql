WITH stage_stats AS (
    SELECT 
        stage, 
        COUNT(*) AS total_battles,
        COUNT(DISTINCT player_id) AS unique_players,
        SUM(
            CASE
                WHERE battle_result = 'win'
                THEN 1
                ELSE 0
            END
        ) AS total_wins,
        SUM(
            CASE 
                WHERE battle_result = 'loss'
                THEN 1
                ELSE 0
            END
        ) AS total_losses
    FROM
        player_events
    WHERE 
        event_name = 'battle_complete'
    AND 
        battle_result IN ('win','loss')
    GROUP BY 
        stage
) 

SELECT
    stage, 
    unique_players,
    total_battles,
    total_wins,
    total_losses,
    ROUND(
        100.0 * total_wins/NULLIF(total_battles,0),2
    ) AS win_rate,
    ROUND(
        1.0 * total_battles/NULLIF(unique_players,0),2
    ) AS avg_battle_per_player
FROM 
    stage_stats
ORDER BY
    stage;