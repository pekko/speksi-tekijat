 #!/bin/bash
 
for i in *.sql; 
 	do ./gen.sh $i; 
done

python first-year.py > ../data/first-year.json
