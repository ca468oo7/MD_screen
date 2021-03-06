#For docking into allosteric site, check if the compound is in desired site by 
#coordinates, change line 18 cutoffs to tune the area of active site (NOT allosteric sitea)
#sdf can be converted from maegz file generated by Schrodinger Glide
import os

f = open('test.sdf','r')
f1 = open('good.sdf','w')
f2 = open('bad.sdf', 'w')



con = ['\n']
flag = True
while con[-1] != '':
    con.append(f.readline())
    if con[-1].startswith('M  V30') and 'COUNTS' not in con[-1]:
        try:
            if float(con[-1].split()[4]) < 52 and float(con[-1].split()[5]) < 63 and float(con[-1].split()[6]) < 61:
                flag = False
        except:
            pass
    if '$$$$' in con[-1]:
        con.pop(0)
        if flag == True:
            for line in con:
                f1.write(line)
        else:
            for line in con:
                f2.write(line)
        con = ['\n']
        flag = True
    
f.close()
f1.close()
f2.close()
