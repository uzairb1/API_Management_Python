SELECT COUNT(*) as Users_Over_60_Using_GMAIL
FROM faker_data
WHERE CAST(SUBSTR(birthday, 1, INSTR(birthday, '-') - 1) AS INTEGER) >= 60
AND email = 'gmail';
