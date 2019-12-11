#This script is for convenient one-step set up for ligands binding to protein.
#Protocol refered from GROMACS Protein-Ligand Complex tutorial by Justin A. Lemkul, Ph.D.
#Virginia Tech Department of Biochemistry, http://www.mdtutorials.com/gmx/complex/index.html
#Prepare ligand mol2 file, str file (from CGenFF server), and protein pdb without hydrogen:
#lig.mol2, lig.str, lig.itp, lig.prm, lig_ini.pdb, protein_noH.pdb, em.mdp, nvt.mdp, npt.mdp, md.mdp, charmm36-mar2019.ff in the same folder
#By Fang Fu, Hao Li

import os
import shutil
import time

def insert_para(fil, ins, pos):
	with open(fil, 'r') as f:
		content = f.readlines()
	with open(fil, 'w') as f1:
		for line in content:
			if pos in line:
				line = ins + line
			f1.write(line)

protein_name = raw_input('Protein name:')

ligand_id = raw_input('Ligand 3 letter ID:')
#ligand_id = 'unk'
lig_l = ligand_id.lower()
lig_u = ligand_id.upper()

os.system("""sed -i 's/UD1/{:s}/g' *.mdp""".format(lig_u)

os.system('echo "1\n1" | gmx pdb2gmx -f {:s}_noH.pdb -o {:s}_processed.gro'.format(protein_name,protein_name))
os.system('gmx editconf -f {:s}_ini.pdb -o {:s}.gro'.format(lig_l, lig_l))

shutil.copy('{:s}_processed.gro'.format(protein_name), 'complex.gro')
with open('complex.gro', 'r') as comp:
    comp_con = comp.readlines()
with open('{:s}.gro'.format(lig_l), 'r') as lig:
    lig_con = lig.readlines()
comp_con[1] = str(int(comp_con[1][:-1]) + int(lig_con[1][:-1])) + '\n'

with open('complex.gro','w') as comp_new:
    for i in range(0, len(comp_con)-1):
        comp_new.write(comp_con[i])
    for i in range(2, len(lig_con)-1):
        comp_new.write(lig_con[i])
    comp_new.write(comp_con[-1])

with open('topol.top' ,'r') as top:
    top_con = top.readlines()

with open('topol.top' ,'w') as top_new:
    for line in top_con:
        if 'Include water topology' in line:
            line = '; Include ligand topology\n#include "{:s}.itp"\n\n; Include water topology\n'.format(lig_l)

        elif '[ moleculetype ]' in line:
            line = '; Include ligand parameters\n#include "{:s}.prm"\n\n[ moleculetype ]\n'.format(lig_l)
        
        top_new.write(line)
    top_new.write('{:s}       1\n'.format(lig_u))

os.system('gmx editconf -f complex.gro -o newbox.gro -bt triclinic -d 1.0 -c')
os.system('gmx solvate -cp newbox.gro -cs spc216.gro -p topol.top -o solv.gro')

os.system('gmx grompp -f ions.mdp -c solv.gro -p topol.top -o ions.tpr -maxwarn 10')

if 'ions.tpr' in os.listdir(os.getcwd()):
    print 'Ligand topology good.'
    time.sleep(5)
    os.system('echo "{:s}" | python2 md2.py'.format(lig_l)        

