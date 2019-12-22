ovaj primer sam ja pisala, ne znaci da je dobar,
kopiran je iz pr3, zato se sve zove book osim podatka kojim se specificira ulazni csv

probaj sa 
cat SalesJan2009.csv | ./mapper.py | sort | ./reducer.py 
RADI
sad asve cita kao 1 red, treba prebaciti razmak na kraju