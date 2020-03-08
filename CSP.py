

class Constraint:

	# TODO
	def __init__(self, clause_as_list):
		self.var1 = clause_as_list[0]
		self.operator = clause_as_list[1]
		self.var2 = clause_as_list[2]

	# TODO
	def satsified(self, assignment):
		if self.operator == '>':
			return assignment[self.var1] > assignment[self.var2]
		elif self.operator == '<':
			return assignment[self.var1] < assignment[self.var2]
		elif self.operator == '=':
			return assignment[self.var1] == assignment[self.var2]
		elif self.operator == '!=':
			return assignment[self.var1] == assignment[self.var2]
		else:
			print('Constraint.satisfied(): no operator match')
			return None


	def __str__(self):
		return self.var1 + ' ' + self.operator + ' ' + self.var2


	def __repr__(self):
		return self.var1 + ' ' + self.operator + ' ' + self.var2


class CSP:

	# list of variable names
	# dictionary of var names (key) and list of domain values (value)
	# constraint list? dict?

	def __init__(self, variables, domains, constraints: [Constraint]):
		self.variables: [] = variables
		self.domains: {} = domains
		self.constraints: [Constraint] = constraints

		self.constraint_involvement = {}
		for con in self.constraints:
			if con.var1 not in self.constraint_involvement:
				self.constraint_involvement[con.var1] = [con]
			else:
				self.constraint_involvement[con.var1].append(con)

			if con.var2 not in self.constraint_involvement:
				self.constraint_involvement[con.var2] = [con]
			else:
				self.constraint_involvement[con.var2].append(con)

		print(self.constraint_involvement)


	def select_unassigned_variable(self):
		final_var = ''

		# most constrained variable heuristic
		min_len = 100000
		min_variable = ''
		num_changes = 0    # keeps track of number of changes to min_len, if it is 1 it means there was a tie
		for (key,val) in self.domains.items():
			# TODO: ignore variables that have already been selected
			curr = len(val)
			if curr < min_len:
				min_variable = key
				min_len = curr
				num_changes += 1

		# there is a tie, so use most constrainING variable
		if num_changes == 1:
			print('most constraining variable heuristic')

			num_changes = 0    # in case there is a tie with this heuristic as well

			max_involved_variable = ''
			max_involvement = -1
			for (constraint_var, constraint_list) in self.constraint_involvement:
				curr_involvement = len(constraint_list)
				if curr_involvement > max_involvement:
					max_involvement = curr
					max_involved_variable = constraint_var
					num_changes += 1

			final_var = max_involved_variable

			# TODO: sort alphabetically
			# if num_changes == 1:
		else:
			final_var = min_variable

		if final_var == '':
			print('CSP.select_unassigned_variable(): error selecting variable')
			# stop program
			exit()

		return final_var


	def is_assignment_valid(self, assignment):
		valid = False

		for constraint in self.constraints:
			if constraint.var1 not in assignment or constraint.var2 not in assignment:
				return False

			valid = valid and constraint.satisfied(assignment)

		return valid


	def order_domain_values(self, variable, assignment):
		print('in order_domain_values()')

		print('iterating over constraints that "' + variable + '" is involved in')
		for constraint in self.constraint_involvement[variable]:
			print(variable, ':', constraint)

			# iterate over each constraint
			#  iterate over each value for given variable?
			#	iterate over each value for opposing variable (ex: given variable = F and constraint = F > A => opposing variable = A)
			#		check if this value satisfies the constraint... if it does not then increment num_invalid_values

		return []


	def select_value(self, variable, assignment):
		print('current assignment:', assignment, '| variable:', variable)


	def backtrack(self):
		return self.__recursive_backtrack({})


	def __recursive_backtrack(self, assignment):
		valid_assignment = self.is_assignment_valid(assignment)

		if valid_assignment:
			return assignment

		selected_var = self.select_unassigned_variable()
		print('selected var:', selected_var)

		for value in self.order_domain_values(selected_var, assignment):
			print('order_domain_value - value:', value)


