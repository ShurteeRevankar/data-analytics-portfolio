SELECT * FROM ZOMATO;

SELECT count(RestaurantID) as total_restaurant from zomato;

SELECT COUNT(DISTINCT(CITY)) as TOTAL_CITY from zomato;

SELECT COUNT(DISTINCT(CountryCode)) as TOTAL_COUNTRY from zomato;

SELECT city, count(RestaurantID) as total_restaurant from zomato GROUP BY city ORDER BY TOTAL_RESTAURANT DESC;

SELECT year(DATEKEY_OPENING) AS YEAR, monthname(DATEKEY_OPENING) AS MONTH_NAME,country_code.Country,CITY, COUNT(restaurantid)as NO_OF_RESTAURANT_OPENED,Has_Table_booking,Has_Online_delivery FROM ZOMATO INNER JOIN country_code ON zomato.COUNTRYCODE = country_code.Country_Code GROUP BY year,month_name,CITY,Country,Has_Table_booking,Has_Online_delivery ORDER BY year;

SELECT RATING, count(RestaurantID)AS NO_OF_RESTAURANT FROM ZOMATO GROUP BY RATING ORDER BY RATING;

SELECT Average_Cost_for_two FROM ZOMATO;

SELECT CURRENCY, count(RestaurantID)AS NO_OF_RESTAURANT FROM ZOMATO GROUP BY CURRENCY;

SELECT HAS_TABLE_BOOKING, count(RestaurantID)AS NO_OF_RESTAURANT,case
when HAS_TABLE_BOOKING = "YES" THEN concat((count(RestaurantID)/SUM(count(RestaurantID)) OVER ())*100,"%")
ELSE concat((count(RestaurantID)/SUM(count(RestaurantID)) OVER ())*100,"%") END 
AS "%_RESTAURANT"
 FROM ZOMATO GROUP BY HAS_TABLE_BOOKING;

SELECT HAS_ONLINE_DELIVERY, count(RestaurantID)AS NO_OF_RESTAURANT,case
when HAS_ONLINE_DELIVERY = "YES" THEN concat((count(RestaurantID)/SUM(count(RestaurantID)) OVER ())*100,"%")
ELSE concat((count(RestaurantID)/SUM(count(RestaurantID)) OVER ())*100,"%") END 
AS "%_RESTAURANT"
 FROM ZOMATO GROUP BY HAS_ONLINE_DELIVERY;	

