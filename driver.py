import sys
from CSP import CSP


if __name__ == '__main__':

	if len(sys.argv) <= 1:
		print("Enter file names for variable and constraint inputs")
		exit()
	
	in_var = sys.argv[1]
	in_cons = sys.argv[2]

	var_file = open(in_var)
	cons_file = open(in_cons)

	variables = []
	domains = {}

	print('parsing variables...')
	for line in var_file.readlines():
		line_split = line.strip().split(':')
		var = line_split[0]
		domain_values = line_split[1].strip().split(' ')
		print(var, domain_values)
		variables.append(var)
		domains[var] = domain_values
	
	constraints = []
	print('parsing constraints...')
	for line in cons_file.readlines():
		line_split = line.strip().split(' ')
		constraints.append(line_split)
		print(line_split)

	csp = CSP(variables, domains, constraints)





