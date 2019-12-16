#Prepare files to send to high throughput computing center. If you don't have access
#to those centers, run the MD commands on you own machine.
import os


path = os.getcwd()

f = open('all.txt', 'r+')
f.seek(0, os.SEEK_END)

for folder in os.listdir(path):
	if 'ZINC' in folder:
		os.system('cp -a ..//Starting//. '+folder)
		os.chdir(folder)
		#print os.getcwd()
		os.system('./md1.sh')
		os.chdir(path)
		if 'em.gro' in os.listdir(path+'//'+folder):
			f.write(folder + ' good\n')
		else:
			f.write(folder + ' bad\n')


f.close()
