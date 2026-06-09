USE hospitality_db;
show tables;

-- Imported 5 CSV files data and created table for the same

select * from dim_date;
select * from dim_hotels;
select * from dim_rooms;
select * from fact_aggregated_bookings;
select * from fact_bookings;

desc fact_aggregated_bookings;
desc fact_bookings;

-- 1 Total Revenue
Select CONCAT(ROUND(SUM(revenue_realized)/1000000 ,2), "M") AS Total_Revenue
FROM fact_bookings; 

-- 2 Occupancy
SELECT CONCAT(ROUND(SUM(successful_bookings) / SUM(capacity) * 100 ,2), " %") AS Occupancy_Percentage 
FROM fact_aggregated_bookings;

-- 3 Cancellation rate
SELECT CONCAT(ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM fact_bookings),2)," %") AS Cancellation_Percentage
FROM fact_bookings
WHERE booking_status = 'Cancelled';

-- 4 Total Booking
SELECT CONCAT(ROUND(COUNT(*)/1000,2),"K") AS Total_Bookings
FROM fact_bookings;

-- 5 calculate realization percentage, successful "Checked Out" bookings over all bookings that have occurred
SELECT CONCAT(Round((COUNT(*) * 100/ (SELECT COUNT(*) FROM fact_bookings WHERE booking_status IN ('Checked Out', 'No Show'))),2)," %") AS Realization_Percentage
FROM fact_bookings
WHERE booking_status = 'Checked Out';

-- 6 Trend Analysis 
-- i -> Revenue over Months
SELECT  MONTH(check_in_date_new) AS Month, Concat(Round(SUM(revenue_realized)/1000000,2)," M") AS Revenue 
FROM fact_bookings 
GROUP BY Month 
ORDER BY Month;

-- ii -> Daily Revenue 
SELECT check_in_date_new, Concat(Round(SUM(revenue_realized)/1000000,2)," M") AS Daily_Revenue 
FROM fact_bookings 
GROUP BY check_in_date_new 
ORDER BY check_in_date_new;

-- 7 Weekday  & Weekend  Revenue and Booking
SELECT 
CASE WHEN DAYOFWEEK(check_in_date_new) IN (1, 7) THEN 'Weekend' ELSE 'Weekday' END AS Day_Type, 
Concat(Round(SUM(revenue_realized)/1000000,2)," M") AS Revenue, CONCAT(ROUND(COUNT(*)/1000,2)," K") AS Total_Bookings
FROM fact_bookings
GROUP BY Day_Type;

-- 8 Revenue by State & hotel
SELECT h.city, h.property_name, CONCAT(ROUND(SUM(f.revenue_realized)/1000000,2)," M") AS Total_Revenue
FROM fact_bookings f
JOIN dim_hotels h ON f.property_id = h.property_id
GROUP BY h.city, h.property_name
ORDER BY Total_Revenue DESC;

-- 9 Class Wise Revenue
SELECT r.room_class, CONCAT(ROUND(SUM(f.revenue_realized)/1000000, 2), " M") AS Total_Revenue
FROM fact_bookings f
JOIN dim_rooms r ON f.room_category = r.room_id
GROUP BY r.room_class 
ORDER BY SUM(f.revenue_realized) DESC;

-- 10 Checked out, cancel, No show
SELECT booking_status, CONCAT(round(COUNT(*)/1000,2)," K") AS Status_Count FROM fact_bookings
GROUP BY booking_status;

-- 11 Weekly trend (Revenue, Total booking, Occupancy) 

SELECT 
    WEEK(fb.check_in_date_new) AS Week_No,
    SUM(fb.revenue_realized) AS Weekly_Revenue,
    COUNT(fb.booking_id) AS Weekly_Bookings,
    (SUM(fab.successful_bookings) / SUM(fab.capacity)) * 100 AS Weekly_Occupancy_Pct
FROM fact_bookings fb
JOIN fact_aggregated_bookings fab 
    ON fb.property_id = fab.property_id 
    AND fb.check_in_date_new = fab.check_in_date_new
GROUP BY Week_No
ORDER BY Week_No ASC;