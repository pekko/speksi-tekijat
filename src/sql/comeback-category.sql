select comeback_category, count(*) c 
from (
	select diff.comeback_category, max(diff.diff) break
	from (
		select temp.*, max(temp.start), temp.stop - max(temp.start) - 1 diff
		from 
		(
			select a.last_name, a.first_name, a.category comeback_category, b.category retire_category, a.year stop, b.year start
			from tekijat a, tekijat b
			where a.last_name = b.last_name and a.first_name = b.first_name and a.year > b.year
		) temp
		group by temp.first_name, temp.last_name, temp.comeback_category, temp.stop
	) diff
	group by diff.first_name, diff.last_name, diff.comeback_category
	having break > 0 
) comebacks
group by comeback_category
order by c desc
