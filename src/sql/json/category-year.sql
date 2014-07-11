select category, year, count(*) 
from tekijat
where category != ""
group by category, year