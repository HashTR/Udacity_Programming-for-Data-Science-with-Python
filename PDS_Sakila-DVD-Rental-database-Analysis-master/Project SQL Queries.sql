/* Query 1 used for the first question: Who are the top 5 actors participated in DVD Rental Movies? */
SELECT 	actor_name, count_movies
FROM
	(SELECT a.actor_id, a.first_name||' '||a.last_name actor_name, COUNT(*) count_movies
	FROM actor a
	JOIN film_actor fa
	ON a.actor_id=fa.actor_id
	GROUP BY 1,2
	ORDER BY 3 DESC
	LIMIT 5) t

/* Query 2 used for the second question: Is there any relation between film duration and its count of rental? */
WITH flc AS (SELECT film_id, NTILE(10) OVER(ORDER BY length) length_quartile
			 				FROM film)
SELECT length_decile, COUNT(*) rental_count
FROM flc
JOIN inventory i
ON flc.film_id=i.film_id
JOIN rental r
ON i.inventory_id=r.inventory_id
GROUP BY 1
ORDER BY 1

/* Query 3 used for the third question: What is the percentage of total payments made for the top two paid categories with respect to the rest? */
WITH cshare AS
				(SELECT c.name category, sum(amount) total_amount
				 FROM category c
				 JOIN film_category fc
				 ON c.category_id=fc.category_id
				 JOIN film f
				 ON f.film_id=fc.film_id
				 JOIN inventory i
				 ON i.film_id=f.film_id
				 JOIN rental r
				 ON r.inventory_id=i.inventory_id
				 JOIN payment p
				 ON p.rental_id=r.rental_id
				 GROUP BY 1
				 ORDER BY 2 DESC),

	toptwoshare AS (SELECT * FROM cshare LIMIT 2),

	classtable AS (SELECT CASE WHEN cshare.category=toptwoshare.category
				   				THEN 'TOP TWO PAID CATEGORIES'
				   				ELSE 'OTHER CATEGORIES'
				   				END category_class,
				   		SUM(cshare.total_amount) class_total
					FROM cshare
					LEFT JOIN toptwoshare
					ON cshare.category=toptwoshare.category
					GROUP BY 1
					ORDER BY 2)
SELECT category_class, ROUND(class_total/SUM(class_total) OVER(),3) Percentage
FROM classtable

/* Query 4 used for the fourth question: For the top 10 paying customers, according to their monthly payments during 2007, find the customer who paid the most difference in terms of successive monthly payments? */
WITH top10monwith_diff AS
	(SELECT payment_month, full_name,
	pay_per_mon-COALESCE(LAG(pay_per_mon) OVER (PARTITION BY full_name ORDER BY payment_month),0) diff
	FROM
		(WITH top10 AS (SELECT c.customer_id, c.first_name||' '||last_name full_name, SUM(amount) totalpaid
						FROM payment p
						JOIN customer c
						ON p.customer_id=c.customer_id
						GROUP BY 1
						ORDER BY 3 DESC
						LIMIT 10)
			SELECT DATE_TRUNC('month',payment_date) payment_month, top10.full_name, SUM(amount) pay_per_mon
			FROM payment p
			JOIN top10
			ON p.customer_id=top10.customer_id
			WHERE DATE_PART('year',payment_date)=2007
			GROUP BY 1,2
			ORDER BY 3) top10mon)

SELECT *
FROM top10monwith_diff
WHERE diff=(SELECT MAX(diff) FROM top10monwith_diff)
