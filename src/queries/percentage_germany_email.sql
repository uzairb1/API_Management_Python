SELECT 
    printf("%4f",COUNT(CASE WHEN email = 'gmail' THEN 1 END) * 100.0) / COUNT(*) AS gmail_percentage_in_germany
FROM 
    faker_data
WHERE 
    [address.country] = 'Germany';