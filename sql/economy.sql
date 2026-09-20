WITH daily_economy AS (
        SELECT 
            day, 
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
        gold_earned,
        gold_spent,
        gold_earned - gold_spent AS net_gold_change,
        ROUND(
            100.0 * gold_spent / NULLIF(gold_earned,0),2
        ) AS spend_rate_pct
    FROM 
        daily_economy
        --player_events

ORDER BY 
    day; 