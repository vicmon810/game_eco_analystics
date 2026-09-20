SELECT 
    day, 
    COUNT(DISTINCT player_id) AS active_players 
FROM 
    player_events
--WHERE     day IN (1,3,5,7)
GROUP BY day 
ORDER BY day ;