from parser import *
from progress.bar import *
file = open('CVE.csv')
a = file.readline()
file = file.readlines()
bar = ChargingBar("Выполнено:", max=len(file))
for line in file:
    get_table(line[4:])
    bar.next()
