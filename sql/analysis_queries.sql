
-- Customer segmentation summary
SELECT 
    behavior_type,
    COUNT(*) as customer_count,
    AVG(age) as avg_age,
    COUNT(CASE WHEN gender = 'M' THEN 1 END) as male_count,
    COUNT(CASE WHEN gender = 'F' THEN 1 END) as female_count
FROM customers 
GROUP BY behavior_type
ORDER BY customer_count DESC;

-- Monthly transaction trends
SELECT 
    strftime('%Y-%m', transaction_date) as month,
    COUNT(*) as transaction_count,
    ROUND(SUM(amount), 2) as total_revenue,
    ROUND(AVG(amount), 2) as avg_transaction_amount
FROM transactions
GROUP BY strftime('%Y-%m', transaction_date)
ORDER BY month;

-- Top customers by total spending
SELECT 
    c.customer_id,
    c.age,
    c.gender,
    c.behavior_type,
    COUNT(t.transaction_id) as transaction_count,
    ROUND(SUM(t.amount), 2) as total_spent,
    ROUND(AVG(t.amount), 2) as avg_transaction
FROM customers c
JOIN transactions t ON c.customer_id = t.customer_id
GROUP BY c.customer_id, c.age, c.gender, c.behavior_type
ORDER BY total_spent DESC
LIMIT 20;

-- RFM analysis with customer info
SELECT 
    r.customer_id,
    r.recency,
    r.frequency,
    r.monetary_total,
    r.monetary_avg,
    c.behavior_type,
    c.age,
    c.gender
FROM rfm_analysis r
JOIN customers c ON r.customer_id = c.customer_id
ORDER BY r.monetary_total DESC;
