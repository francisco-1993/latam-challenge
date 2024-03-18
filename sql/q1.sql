WITH
  TOP_DATES AS (

  SELECT
    DATE(date) AS date,
    COUNT(1) AS total_tweets
  FROM
    `${PROJECT_ID}.${DATASET_ID}.${TABLE_ID}` 
  GROUP BY
    date
  ORDER BY
    total_tweets DESC
  LIMIT
    10 ),

  USER_TWEETS AS (

  SELECT
    DATE(t.date) AS date,
    t.username,
    COUNT(1) AS tweet_count
  FROM
        `${PROJECT_ID}.${DATASET_ID}.${TABLE_ID}` t
  INNER JOIN
    TOP_DATES td
  ON
    DATE(t.date) = td.date
  GROUP BY
    date,
    username 
  )
SELECT
  ut.date,
  ut.username AS top_user
FROM
  USER_TWEETS ut
INNER JOIN (
  SELECT
    date,
    MAX(tweet_count) AS max_tweet_count
  FROM
    USER_TWEETS
  GROUP BY
    date ) max_ut
ON
  ut.date = max_ut.date
  AND ut.tweet_count = max_ut.max_tweet_count
