SELECT last_name, count(distinct last_name, first_name) 'count'
FROM `tekijat`
group by last_name
order by count desc, last_name
