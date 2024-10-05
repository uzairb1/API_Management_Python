WITH GmailUsers AS (
    SELECT 
        [address.country] as country, 
        COUNT(*) AS gmail_users
    FROM 
        faker_data
    WHERE 
        email LIKE '%gmail%'
    GROUP BY 
        country
),
RankedCountries AS (
    SELECT 
        country, 
        gmail_users,
        DENSE_RANK() OVER (ORDER BY gmail_users DESC) AS country_rank
    FROM 
        GmailUsers
)

SELECT 
    country, 
    gmail_users, 
    country_rank
FROM 
    RankedCountries
WHERE 
    country_rank <= 3
ORDER BY 
    country_rank;
