import csv

def modify_and_store():
    with open("./population.csv","r") as file:
        reader = csv.reader(file)
        nodes = nodes = [ n for n in file][2:]

        country_names = csv.reader(nodes, delimiter = ',')

        res = []
    with open("./updatepop.csv","w") as genfile:    
        for info in country_names:
            n, cpays, pop, date, perc, source = info[0], info[1], info[2], info[3], info[4], info[5] 
            genfile.write('%s,%s,%s,7/1/2014,%s,%s,null,null\n' % (n,cpays,pop,str(perc),source))
    return
