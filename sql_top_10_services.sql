SELECT 
medical_service,
COUNT(*)

FROM dataset_slot
GROUP BY medical_service
ORDER BY COUNT(*) DESC
LIMIT 10
