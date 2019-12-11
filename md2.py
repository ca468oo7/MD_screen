import os

def insert_para(fil, ins, pos):
	with open(fil, 'r') as f:
		content = f.readlines()
	with open(fil, 'w') as f1:
		for line in content:
			if pos in line:
				line = ins + line
			f1.write(line)

ligand_id = raw_input('Ligand 3 letter ID: ')
#ligand_id = 'unk'
lig_l = ligand_id.lower()
lig_u = ligand_id.upper()

os.system('echo "15" | gmx genion -s ions.tpr -o solv_ions.gro -p topol.top -pname NA -nname CL -neutral')

os.system('gmx grompp -f em.mdp -c solv_ions.gro -p topol.top -o em.tpr -maxwarn 10')

os.system('gmx mdrun -nt 20 -v -deffnm em')

os.system('echo "0 & ! a H*\nq" | gmx make_ndx -f {:s}.gro -o index_{:s}.ndx'.format(lig_l,lig_l))

os.system('echo "3" | gmx genrestr -f {:s}.gro -n index_{:s}.ndx -o posre_{:s}.itp -fc 1000 1000 1000'.format(lig_l,lig_l,lig_l))

insert_para('topol.top', '; Ligand position restraints\n#ifdef POSRES\n#include "posre_{:s}.itp"\n#endif\n\n', 'Include water topology')

os.system('echo "1 | 13\nq" | gmx make_ndx -f em.gro -o index.ndx')

#gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -n index.ndx -o nvt.tpr -maxwarn 10

#gmx mdrun -nt 20 -deffnm nvt

#gmx grompp -f npt.mdp -c nvt.gro -t nvt.cpt -r nvt.gro -p topol.top -n index.ndx -o npt.tpr -maxwarn 10

#gmx mdrun -nt 20 -deffnm npt

#gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -n index.ndx -o md_0_1.tpr -maxwarn 10

#gmx grompp -nt 20 -deffnm md_0_1
