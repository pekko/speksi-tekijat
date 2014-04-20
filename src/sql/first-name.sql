SELECT first_name, count(distinct last_name, first_name) 'count'
FROM `tekijat`
group by first_name
order by count desc, first_name
