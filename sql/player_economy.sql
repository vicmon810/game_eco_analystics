WITH ranked_events AS(
    SELECT 
        player_id, 
        day, 
        event_time,
        gold_balance,
        ROW_NUMBER() OVER (
            PARTITION BY player_id, day 
            ORDER BY event_time DESC
        ) as rn 
    FROM 
        player_events
),
daily_final_balance AS(
    SELECT
        player_id, 
        day, 
        gold_balance
    FROM ranked_events
    WHERE rn = 1
)

SELECT 
    day, 
    COUNT(*) AS active_players,
    ROUND(AVG(gold_balance),2) AS avg_end_gold_balance,
    SUM(
        CASE 
            WHEN gold_balance < 80
            THEN 1
            ELSE 0
        END
    ) AS low_gold_players,
    ROUND (100.0 * SUM(
        CASE WHEN gold_balance < 80
        THEN 1
        ELSE 0
        END
    )/ COUNT(*),2) AS low_gold_rate_pct
    --MIN(gold_balance) AS min_gold_balance,
    --MAX(gold_balance) AS max_gold_balance
FROM
    daily_final_balance
GROUP BY 
    day 
ORDER BY 
    day;