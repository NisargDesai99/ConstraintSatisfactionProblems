# Nisarg Desai npd10030
# Sanketh Reddy spr150430


import sys
from CSP import CSP
from CSP import Constraint

if __name__ == '__main__':

	if len(sys.argv) <= 1:
		print("Enter file names for variable and constraint inputs")
		exit()

	in_var = sys.argv[1]
	in_cons = sys.argv[2]
	procedure = sys.argv[3]

	var_file = open(in_var)
	cons_file = open(in_cons)

	variables = []
	domains = {}

	# print('parsing variables and domains...')
	for line in var_file.readlines():
		line_split = line.strip().split(':')

		var = line_split[0]
		domain_values_str = line_split[1].strip().split(' ')
		domain_values = [int(item) for item in domain_values_str]

		# print(var, domain_values)

		variables.append(var)
		domains[var] = domain_values

	constraints = []
	# print('parsing constraints...')
	for line in cons_file.readlines():
		line_split = line.strip().split(' ')
		con = Constraint(line_split)
		constraints.append(con)
		# print(line_split)

	csp = CSP(variables, domains, constraints, procedure)
	solution = csp.backtrack()
	print(solution[2])

	# out_file = open('ex-'+procedure+'.out', 'w+')
	# out_file.write(solution[1])
	# out_file.close()



