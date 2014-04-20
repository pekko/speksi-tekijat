select 
	category,
	count(*) total,
	count(distinct first_name, last_name) uniq
from tekijat
group by category