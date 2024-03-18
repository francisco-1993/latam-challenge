WITH temp AS (
  SELECT
    DATE(date) AS date,
    username,
    COUNT(*) AS tweet_count
  FROM
    `${PROJECT_ID}.${DATASET_ID}.${TABLE_ID}`
  GROUP BY
    date,
    username
  ORDER BY
    tweet_count DESC
)

SELECT
  date,
  FIRST_VALUE(username) OVER (PARTITION BY date ORDER BY tweet_count DESC) AS top_user,
  MAX(tweet_count) AS tweet_count
FROM
  temp
GROUP BY
  date
ORDER BY
  tweet_count DESC
LIMIT
  10;