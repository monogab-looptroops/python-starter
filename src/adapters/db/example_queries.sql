-- SQL
CREATE TABLE IF NOT EXISTS example (
    id SERIAL PRIMARY KEY,
    info TEXT,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

-- SQL
INSERT INTO example(info, created_on)
VALUES ( :Info , CURRENT_TIMESTAMP);

-- SQL
SELECT *
FROM example
WHERE created_on >= :StartTimestamp
ORDER BY info;


