from modeller import *
from modeller.scripts import complete_pdb 
from modeller.optimizers import conjugate_gradients, molecular_dynamics, actions


def refine(atmsel, code, trcfil):
    # at T=1000, max_atom_shift for 4fs is cca 0.15 A.
    md = molecular_dynamics(cap_atom_shift=0.39, md_time_step=4.0,
                            md_return='FINAL')
    init_vel = True
    for (its, equil, temps) in ((200, 20, (150.0, 250.0, 400.0, 700.0, 1000.0)),
                                (200, 600,
                                 (1000.0, 800.0, 600.0, 500.0, 400.0, 300.0))):
        for temp in temps:
            md.optimize(atmsel, init_velocities=init_vel, temperature=temp,
                         max_iterations=its, equilibrate=equil, actions=[actions.write_structure(10, code+'.D9999%04d.pdb'),
                     actions.trace(10, trcfil)])
            init_vel = False


def Optimizemodel(pdb_file):
	"""
	This functions returns a file with the optimized model from the input pdb. 
	It also returns the energies. 
	"""

	env = environ()
	env.io.atom_files_directory = ['../atom_files']
	env.edat.dynamic_sphere = True

	env.libs.topology.read(file='$(LIB)/top_heav.lib')
	env.libs.parameters.read(file='$(LIB)/par.lib')

	code, ext = pdb_file.split('.')
	mdl = complete_pdb(env, pdb_file)
	mdl.write(file=code+'.ini')

	# Select all atoms:
	atmsel = selection(mdl)
	mpdf2 = atmsel.energy(edat=energy_data(dynamic_sphere=True))
	# Generate the restraints:
	#mdl.restraints.make(atmsel, restraint_type='improper', spline_on_site=False)
	#mdl.restraints.make(atmsel, restraint_type='bond', spline_on_site=False)
	#mdl.restraints.make(atmsel, restraint_type='sphere', spline_on_site=False)
	mdl.restraints.make(atmsel, restraint_type='stereo', spline_on_site=False)
	mdl.restraints.write(file=code+'.rsr')

	mpdf1 = atmsel.energy()


	# Create optimizer objects and set defaults for all further optimizations
	cg = conjugate_gradients(output='REPORT')
	md = molecular_dynamics(output='REPORT')

	# Open a file to get basic stats on each optimization
	trcfil = open(code+'.D00000001', 'w')

	# Run CG on the all-atom selection; write stats every 5 steps
	cg.optimize(atmsel, max_iterations=20, actions=actions.trace(5, trcfil))
	# Run MD; write out a PDB structure (called '1fas.D9999xxxx.pdb') every
	# 10 steps during the run, and write stats every 10 steps
	md.optimize(atmsel, temperature=300, max_iterations=50,
            actions=[actions.write_structure(10, code+'.D9999%04d.pdb'),
                     actions.trace(10, trcfil)])
	#refine(atmsel, code, trcfil)
	# Finish off with some more CG, and write stats every 5 steps
	cg.optimize(atmsel, max_iterations=20,
            actions=[actions.trace(5, trcfil)])

	mpdf = atmsel.energy(edat=energy_data(dynamic_sphere=False))

	print("The initial energy of " + code + " is " + str(mpdf1[0]))
	print("The final energy of " + code + " is " + str(mpdf[0]))
	print("The final energy of " + code + " is " + str(mpdf2[0]))

	mdl.write(file=code+'_optimized.pdb')


if __name__ == '__main__':
	Optimizemodel('2f1d/chain_B_A.pdb')








