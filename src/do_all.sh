 #!/bin/bash
 
for i in *.sql; 
 	do ./gen.sh $i; 
done

python first-year.py > ~/www/speksi/tekijat/data/first-year.json
