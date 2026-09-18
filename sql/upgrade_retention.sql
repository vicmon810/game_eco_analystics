WITH player_cohorts AS (
    SELECT
        p.player_id
        ,
        CASE
            WHEN EXISTS(
                SELECT 1
                FROM 
                    player_events u 
                WHERE 
                    u.player_id = p.player_id
                AND 
                    u.day = 0
                AND 
                    u.event_name = 'hero_upgrade'
            )
            THEN 
                1
            ELSE
                0
        END AS upgraded_day0
        ,
        CASE
            WHEN EXISTS(
                SELECT 
                    1
                FROM
                    player_events d1 
                WHERE 
                    d1.player_id = p.player_id
                AND 
                    d1.day = 1
            )
            THEN
                1
            ELSE
                0
        END AS retained_d1
    
    FROM (
        SELECT DISTINCT
            player_id
        FROM 
            player_events
    ) p 
)


SELECT 
    CASE
        WHEN 
            upgraded_day0 = 1
        THEN 
            'Upgraded on Day 0'
        ELSE 
            'Did not upgrade'
    END AS player_group,

    COUNT(*) AS players, 

    SUM(retained_d1) AS retained_players,

    ROUND(100.0 * SUM(retained_d1)/COUNT(*),2)
    AS d1_retention_pct
FROM
    player_cohorts
GROUP BY 
    upgraded_day0
ORDER BY 
    upgraded_day0 DESC;
