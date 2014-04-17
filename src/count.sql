select last_name, first_name, count(*) hits
from tekijat
group by last_name, first_name
order by hits desc, last_name, first_name