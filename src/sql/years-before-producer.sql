select 
	tuot.last_name, 
	tuot.first_name,
	count(distinct year) years_before_producer

from 
	(select first_name, last_name from tekijat where category='Tuottaja') tuot, 
	tekijat 

where 
	tekijat.first_name = tuot.first_name
	and tekijat.last_name = tuot.last_name 
	and year < 
		(
			select year 
			from tekijat 
			where first_name = tuot.first_name 
				and last_name = tuot.last_name 
				and category = 'Tuottaja'
		) 

group by 
	first_name, last_name

order by
	last_name, first_name
