Create DATABASE Manufacturing_Project;
USE Manufacturing_Project;

CREATE TABLE ALL_PROD_DATA (

Buyer VARCHAR(100),

Delivery_Period VARCHAR(100),

Department_Name VARCHAR(100),

Operation_Name VARCHAR(100),

Machine_Code VARCHAR(50),

Emp_Name VARCHAR(100),

Fiscal_Date VARCHAR(50),

Fiscal_Year INT,

Manufactured_Qty BIGINT,

Rejected_Qty BIGINT,

Processed_Qty BIGINT

);

## KPI Card 1 - Manufactured Qty
 
SELECT 
CONCAT(
ROUND(SUM(Manufactured_Qty)/1000000,0),
'M'
) AS Manufactured_Qty
FROM ALL_PROD_DATA;


## KPI Card 2 Rejected Qty
SELECT 
CONCAT(
ROUND(SUM(Rejected_Qty)/1000,0),
'K'
) AS Rejected_Qty
FROM ALL_PROD_DATA;

## KPI Card 3 Processed Qty
SELECT 
CONCAT(
ROUND(SUM(Processed_Qty)/1000000,0),
'M'
) AS Processed_Qty
FROM ALL_PROD_DATA;

## KPI Card 4 Wastage Qty%
SELECT 
CONCAT(
ROUND(
(SUM(Rejected_Qty)/SUM(Manufactured_Qty))*100,
2
),
'%'
) AS Wastage_Percentage
FROM ALL_PROD_DATA;

### Visuals KPI's 
## KPI 5. Employee Wise Rejected Qty
SELECT 
Emp_Name,
SUM(Rejected_Qty) AS Rejected_Qty
FROM ALL_PROD_DATA
GROUP BY Emp_Name
ORDER BY SUM(Rejected_Qty) DESC
LIMIT 10;

## KPI 6. Machine Wise Rejected Qty
SELECT 
`Machine_Code`,
SUM(`Rejected_Qty`) AS Rejected_Qty
FROM ALL_PROD_DATA
GROUP BY `Machine_Code`
ORDER BY Rejected_Qty DESC;

## KPI 7. Production Comparison Trend
SELECT 
Fiscal_Date AS Production_Date,
SUM(Manufactured_Qty) AS Manufactured_Qty
FROM ALL_PROD_DATA
GROUP BY Fiscal_Date
ORDER BY STR_TO_DATE(Fiscal_Date,'%d-%m-%Y');

## KPI 8. Manufacture Vs Rejected
SELECT 
SUM(`Manufactured_Qty`) AS Manufactured_Qty,
SUM(`Rejected_Qty`) AS Rejected_Qty
FROM ALL_PROD_DATA;

## KPI 9. Department Wise Manufacture Vs Rejected
SELECT 
`Department_Name`,
SUM(`Manufactured_Qty`) AS Manufactured_Qty,
SUM(`Rejected_Qty`) AS Rejected_Qty
FROM ALL_PROD_DATA
GROUP BY `Department_Name`;

## KPI 10. Operation Wise Rejected Qty
SELECT 
`Operation_Name`,
SUM(`Rejected_Qty`) AS Rejected_Qty
FROM ALL_PROD_DATA
GROUP BY `Operation_Name`
ORDER BY Rejected_Qty DESC;



