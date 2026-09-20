WITH daily_economy AS (
        SELECT 
            day, 
            COUNT(DISTINCT player_id) AS active_players,
            SUM (
                CASE
                    WHEN  gold_change > 0 
                    THEN gold_change
                    ELSE 0
                END
            ) as gold_earned,

            SUM (
                CASE 
                    WHEN gold_change <0
                    THEN - gold_change
                    ELSE 0
                END 
            ) AS gold_spent
            FROM player_events
            GROUP BY day
    )
    SELECT
        day,
        active_players,
        ROUND(1.0*gold_earned / active_players,2) AS avg_gold_earned,
        ROUND(1.0*gold_spent /active_players,2) AS avg_gold_spend
    FROM 
        daily_economy
        --player_events

ORDER BY 
    day; 