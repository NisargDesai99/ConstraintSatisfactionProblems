# CS 4365 - Artificial Intelligence
# Nisarg Desai - npd160030
# Sanketh Reddy - spr150430

import sys
import lib

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

	for line in var_file.readlines():
		line_split = line.strip().split(':')

		var = line_split[0]
		domain_values_str = line_split[1].strip().split(' ')
		domain_values = [int(item) for item in domain_values_str]

		variables.append(var)
		domains[var] = domain_values

	constraints = []
	for line in cons_file.readlines():
		line_split = line.strip().split(' ')
		con = lib.Constraint(line_split)
		constraints.append(con)

	# initialize csp and solve it
	csp = lib.CSP(variables, domains, constraints, procedure)
	solution = lib.backtrack(csp)
	print(solution[2])


