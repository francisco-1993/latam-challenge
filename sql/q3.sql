WITH user_mentions AS (
  SELECT
    username AS mentioned_username
  FROM 
    `${PROJECT_ID}.${DATASET_ID}.${TABLE_ID}`
    ,UNNEST(mentioned_usernames) AS username
)
SELECT
  mentioned_username,
  COUNT(1) AS mention_count
FROM user_mentions
GROUP BY 1
ORDER BY mention_count DESC
LIMIT 10