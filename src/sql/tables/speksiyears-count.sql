select years, count(*) from (
	select last_name, first_name, count(distinct year) years 
	from tekijat 
	group by last_name, first_name 
	order by years desc, last_name, first_name
) temp
group by years
order by years desc
