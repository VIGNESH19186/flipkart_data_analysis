
-- ============================================================
-- FLIPKART E-COMMERCE DATA ANALYTICS PROJECT
-- Database: MySQL 8.0
-- Database Name: flipkart
-- Table Name: flipkard_dataset
-- Dataset: Imported CSV Dataset
-- Total Queries: 25
-- No LIMIT Clauses
-- Compatible with ONLY_FULL_GROUP_BY
-- ============================================================


-- 1. CREATE AND SELECT DATABASE

CREATE DATABASE IF NOT EXISTS flipkart;

USE flipkart;


-- 2. VIEW COMPLETE DATASET

SELECT *
FROM flipkard_dataset;


-- 3. TOTAL NUMBER OF RECORDS

SELECT
    COUNT(*) AS total_records
FROM flipkard_dataset;


-- 4. CHECK TABLE STRUCTURE

DESCRIBE flipkard_dataset;


-- 5. SORT SELLERS IN ASCENDING ORDER

SELECT *
FROM flipkard_dataset
ORDER BY seller ASC;


-- 6. SORT SELLERS AND PRODUCTS ALPHABETICALLY

SELECT *
FROM flipkard_dataset
ORDER BY
    seller ASC,
    product_name ASC;


-- 7. FIND UNIQUE SELLERS

SELECT DISTINCT seller
FROM flipkard_dataset
ORDER BY seller ASC;


-- 8. FIND UNIQUE SELLER CITIES

SELECT DISTINCT seller_city
FROM flipkard_dataset
ORDER BY seller_city ASC;


-- 9. FIND UNIQUE PRODUCT CATEGORIES

SELECT DISTINCT category
FROM flipkard_dataset
ORDER BY category ASC;


-- 10. PRODUCT-WISE MINIMUM AND MAXIMUM PRICE

SELECT
    product_name,
    MIN(price) AS minimum_price,
    MAX(price) AS maximum_price
FROM flipkard_dataset
GROUP BY product_name
ORDER BY product_name ASC;


-- 11. PRODUCT-WISE FINAL PRICE ANALYSIS

SELECT
    product_name,
    MIN(final_price) AS minimum_final_price,
    MAX(final_price) AS maximum_final_price,
    ROUND(AVG(final_price), 2) AS average_final_price
FROM flipkard_dataset
GROUP BY product_name
ORDER BY average_final_price DESC;


-- 12. SORT LISTING DATES MONTH-WISE
-- Assumption: listing_date format is DD-MM-YYYY

SELECT
    seller,
    product_name,
    listing_date,
    STR_TO_DATE(listing_date, '%d-%m-%Y') AS converted_date
FROM flipkard_dataset
ORDER BY
    MONTH(STR_TO_DATE(listing_date, '%d-%m-%Y')) ASC,
    STR_TO_DATE(listing_date, '%d-%m-%Y') ASC;


-- 13. FIND SELLERS BELOW THEIR CITY'S OVERALL
-- AVERAGE SELLER RATING

WITH seller_avg AS (
    SELECT
        seller_city,
        seller,
        AVG(seller_rating) AS avg_rating
    FROM flipkard_dataset
    GROUP BY
        seller_city,
        seller
),

city_avg AS (
    SELECT
        seller_city,
        AVG(seller_rating) AS city_rating
    FROM flipkard_dataset
    GROUP BY seller_city
)

SELECT
    s.seller_city,
    s.seller,
    ROUND(s.avg_rating, 2) AS seller_average_rating,
    ROUND(c.city_rating, 2) AS city_average_rating
FROM seller_avg s
JOIN city_avg c
    ON s.seller_city = c.seller_city
WHERE s.avg_rating < c.city_rating
ORDER BY
    s.seller_city ASC,
    s.avg_rating ASC;


-- 14. MONTHLY AVERAGE PRICE FOR EACH PRODUCT
-- Corrected for ONLY_FULL_GROUP_BY

SELECT
    product_name,
    YEAR(STR_TO_DATE(listing_date, '%d-%m-%Y')) AS year,
    MONTH(STR_TO_DATE(listing_date, '%d-%m-%Y')) AS month,
    MONTHNAME(
        STR_TO_DATE(listing_date, '%d-%m-%Y')
    ) AS month_name,
    ROUND(AVG(final_price), 2) AS monthly_average_price
FROM flipkard_dataset
GROUP BY
    product_name,
    YEAR(STR_TO_DATE(listing_date, '%d-%m-%Y')),
    MONTH(STR_TO_DATE(listing_date, '%d-%m-%Y')),
    MONTHNAME(STR_TO_DATE(listing_date, '%d-%m-%Y'))
ORDER BY
    year ASC,
    month ASC,
    product_name ASC;


-- 15. COMPLETE PRODUCT SUMMARY

SELECT
    product_name,
    category,
    COUNT(*) AS total_listings,
    MIN(price) AS minimum_price,
    MAX(price) AS maximum_price,
    ROUND(AVG(price), 2) AS average_price,
    ROUND(AVG(final_price), 2) AS average_final_price,
    ROUND(AVG(rating), 2) AS average_product_rating,
    ROUND(AVG(seller_rating), 2) AS average_seller_rating
FROM flipkard_dataset
GROUP BY
    product_name,
    category
ORDER BY
    category ASC,
    product_name ASC;


-- 16. CATEGORY-WISE ANALYSIS

SELECT
    category,
    COUNT(*) AS total_listings,
    ROUND(AVG(price), 2) AS average_price,
    ROUND(AVG(final_price), 2) AS average_final_price,
    ROUND(AVG(rating), 2) AS average_rating,
    SUM(units_sold) AS total_units_sold
FROM flipkard_dataset
GROUP BY category
ORDER BY total_units_sold DESC;


-- 17. BEST-SELLING PRODUCTS

SELECT
    product_name,
    category,
    SUM(units_sold) AS total_units_sold
FROM flipkard_dataset
GROUP BY
    product_name,
    category
ORDER BY total_units_sold DESC;


-- 18. PRODUCT RATINGS ANALYSIS

SELECT
    product_name,
    ROUND(AVG(rating), 2) AS average_rating,
    SUM(units_sold) AS total_units_sold
FROM flipkard_dataset
GROUP BY product_name
ORDER BY average_rating DESC;


-- 19. CITY-WISE SELLER ANALYSIS

SELECT
    seller_city,
    COUNT(DISTINCT seller) AS total_sellers,
    COUNT(*) AS total_listings,
    ROUND(AVG(seller_rating), 2) AS average_seller_rating,
    SUM(units_sold) AS total_units_sold
FROM flipkard_dataset
GROUP BY seller_city
ORDER BY total_units_sold DESC;


-- 20. PRODUCTS ABOVE OVERALL AVERAGE FINAL PRICE

SELECT
    product_name,
    final_price
FROM flipkard_dataset
WHERE final_price > (
    SELECT AVG(final_price)
    FROM flipkard_dataset
)
ORDER BY final_price DESC;


-- 21. DISCOUNT AMOUNT AND DISCOUNT PERCENTAGE

SELECT
    product_name,
    price AS original_price,
    final_price,
    price - final_price AS discount_amount,
    ROUND(
        ((price - final_price) / NULLIF(price, 0)) * 100,
        2
    ) AS discount_percentage
FROM flipkard_dataset
ORDER BY discount_percentage DESC;


-- 22. MONTHLY SALES ANALYSIS

SELECT
    YEAR(STR_TO_DATE(listing_date, '%d-%m-%Y')) AS year,
    MONTH(STR_TO_DATE(listing_date, '%d-%m-%Y')) AS month,
    MONTHNAME(
        STR_TO_DATE(listing_date, '%d-%m-%Y')
    ) AS month_name,
    SUM(units_sold) AS total_units_sold,
    ROUND(AVG(final_price), 2) AS average_final_price
FROM flipkard_dataset
GROUP BY
    YEAR(STR_TO_DATE(listing_date, '%d-%m-%Y')),
    MONTH(STR_TO_DATE(listing_date, '%d-%m-%Y')),
    MONTHNAME(STR_TO_DATE(listing_date, '%d-%m-%Y'))
ORDER BY
    year ASC,
    month ASC;


-- 23. SELLERS WITH AVERAGE RATING ABOVE 4

SELECT
    seller,
    seller_city,
    ROUND(AVG(seller_rating), 2) AS average_seller_rating
FROM flipkard_dataset
GROUP BY
    seller,
    seller_city
HAVING AVG(seller_rating) > 4
ORDER BY average_seller_rating DESC;


-- 24. PRODUCTS WITH MORE THAN 1000 UNITS SOLD

SELECT
    product_name,
    SUM(units_sold) AS total_units_sold
FROM flipkard_dataset
GROUP BY product_name
HAVING SUM(units_sold) > 1000
ORDER BY total_units_sold DESC;


-- 25. OVERALL BUSINESS PERFORMANCE

SELECT
    COUNT(*) AS total_listings,
    COUNT(DISTINCT seller) AS total_sellers,
    COUNT(DISTINCT seller_city) AS total_cities,
    COUNT(DISTINCT product_name) AS total_products,
    ROUND(AVG(price), 2) AS average_original_price,
    ROUND(AVG(final_price), 2) AS average_final_price,
    ROUND(AVG(rating), 2) AS average_product_rating,
    ROUND(AVG(seller_rating), 2) AS average_seller_rating,
    SUM(units_sold) AS total_units_sold
FROM flipkard_dataset
show flipkart
SELECT COUNT(*) FROM flipkard_dataset;

SELECT * FROM flipkard_dataset;


-- ============================================================
-- END OF FLIPKART E-COMMERCE DATA ANALYTICS PROJECT
-- ============================================================
