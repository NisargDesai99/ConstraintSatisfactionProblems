

class Constraint:

	# TODO
	def __init__(self, clause_as_list):
		self.var1 = clause_as_list[0]
		self.operator = clause_as_list[1]
		self.var2 = clause_as_list[2]


	# TODO
	def satisfied(self, assignment):

		# print('satisfied(',assignment,') with constraint:', self, end="")

		if self.operator == '>':
			# print(':', assignment[self.var1] > assignment[self.var2])
			return assignment[self.var1] > assignment[self.var2]
		elif self.operator == '<':
			# print(':', assignment[self.var1] < assignment[self.var2])
			return assignment[self.var1] < assignment[self.var2]
		elif self.operator == '=':
			# print(':', assignment[self.var1] < assignment[self.var2])
			return assignment[self.var1] == assignment[self.var2]
		elif self.operator == '!=':
			# print(':', assignment[self.var1] < assignment[self.var2])
			return assignment[self.var1] == assignment[self.var2]
		else:
			print('Constraint.satisfied(): no operator match')
			return None


	def get_opposing_var(self, variable):
		if self.var1 == variable:
			return self.var2
		else:
			return self.var1


	def __str__(self):
		return self.var1 + ' ' + self.operator + ' ' + self.var2


	def __repr__(self):
		return self.var1 + ' ' + self.operator + ' ' + self.var2


class CSP:

	# list of variable names
	# dictionary of var names (key) and list of domain values (value)
	# constraint list? dict?

	def __init__(self, variables, domains, constraints: [Constraint], procedure):
		self.variables: [] = variables
		self.domains: {} = domains
		self.constraints: [Constraint] = constraints
		self.fc = (False if procedure == 'none' else True)

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

		print('variables:', self.variables)
		print('constraints:', self.constraints)
		print('constraint_involvement:', self.constraint_involvement)

	def __select_unassigned_variable(self, assignment):
		if len(assignment) == len(self.variables):
			print('all variables already selected')
			exit()

		final_var = ''

		# most constrained variable heuristic
		min_len = 100000
		min_variable = ''
		num_changes = 0    # keeps track of number of changes to min_len, if it is 1 it means there was a tie
		for (key,val) in self.domains.items():
			# TODO: ignore variables that have already been selected
			if key in assignment:
				continue
			curr = len(val)
			if curr < min_len:
				min_variable = key
				min_len = curr
				num_changes += 1

		# there is a tie, so use most constrainING variable
		if num_changes == 1:
			# print('most constraining variable heuristic')

			num_changes = 0    # in case there is a tie with this heuristic as well

			max_involved_variable = ''
			max_involvement = -1
			for (constraint_var, constraint_list) in self.constraint_involvement.items():
				if constraint_var in assignment:
					continue
				curr_involvement = len(constraint_list)
				if curr_involvement > max_involvement:
					max_involvement = curr
					max_involved_variable = constraint_var
					num_changes += 1

			# TODO: sort alphabetically
			if num_changes == 1:
				# print('alphabetical selection')
				x = sorted(self.variables)
				for var in x:
					if var in assignment:
						continue
					else:
						return var

			else:
				final_var = max_involved_variable
		else:
			final_var = min_variable

		if final_var == '':
			print('CSP.__select_unassigned_variable(): error selecting variable')
			# stop program
			exit()

		return final_var


	def __is_assignment_complete(self, assignment):
		complete = False

		count = 0
		for constraint in self.constraints:
			if constraint.var1 not in assignment or constraint.var2 not in assignment:
				return False
			satisfied = constraint.satisfied(assignment)
			complete = (complete and satisfied) if count == 0 else (satisfied)
			count += 1

		return complete and len(assignment) == len(self.variables)


	def __order_domain_values(self, given_var, assignment):
		# print('in __order_domain_values()')

		vals_removed_per_var = {}

		for val in self.domains[given_var]:
			vals_removed_per_var[val] = self.__count_values_removed(given_var, val)
		
		sorted_vals_removed = {k: v for k, v in sorted(vals_removed_per_var.items(), key=lambda item: item[1])}
		# print(sorted_vals_removed)

		# print('iterating over constraints that "' + given_var + '" is involved in')
		# for constraint in self.constraint_involvement[given_var]:
		# 	print(given_var, ':', constraint)

		# 	# iterate over each constraint
		# 	# 	iterate over each value for given variable?
		# 	#		iterate over each value for opposing variable (ex: given variable = F and constraint = F > A => opposing variable = A)
		# 	#			check if this value satisfies the constraint... if it does not then increment num_invalid_values

		# 	for val in self.domains[given_var]:
		# 		print('val in domain of ' + given_var + ': ' + str(val))

		# 		opposing_var = constraint.get_opposing_var(given_var)
		# 		# self.__count_values_removed((given_var,val), opposing_var)

		# 		for opposing_val in self.domains[opposing_var]:
		# 			print('opposing val in domain of ' + opposing_var + ': ' + str(opposing_val))

		# 			vals_removed_per_var[val] += self.__count_values_removed({given_var:val, opposing_var:opposing_val})

		return [key for (key,val) in sorted_vals_removed.items()]

	def __count_values_removed(self, given_var, val):
		
		num_removed_vals = 0
		temp_assign = {given_var : val}

		if given_var not in self.constraint_involvement:
			return 0

		for constraint in self.constraint_involvement[given_var]:
			# print('checking constraint:', constraint)
			adjacent_var = constraint.get_opposing_var(given_var)
			for adjacent_val in self.domains[adjacent_var]:
				temp_assign[adjacent_var] = adjacent_val
				if not constraint.satisfied(temp_assign):
					num_removed_vals += 1
		
		# print('(' + given_var + ' : ' + str(val) + ') = ' + str(num_removed_vals))
		return num_removed_vals


	# def __count_values_removed(self, curr_var_val_tuple, opposing_var):

	# 	assignment = {curr_var_val_tuple[0] : curr_var_val_tuple[1]}
	# 	for opposing_val in self.domains[opposing_var]:

	# def __count_values_removed(self, temp_assignment):
	# 	print('in count values removed:', temp_assignment)
	# 	return 0
	
	def is_assignment_consistent(self, assignment, variable):

		is_consistent = True
		count = 0

		if variable not in self.constraint_involvement:
			return True

		for constraint in self.constraint_involvement[variable]:
			# print('checking constraint:', constraint, ' with assignment:', assignment)
			# print('constraint.var1:', constraint.var1)
			# print('constraint.var2:', constraint.var2)
			# print('variable:', variable)
			if constraint.var1 == variable and constraint.var2 not in assignment:
				# print('first')
				continue
			elif constraint.var2 == variable and constraint.var1 not in assignment:
				# print('second')
				continue
			satisfied = constraint.satisfied(assignment)
			# print(constraint, satisfied)
			is_consistent = (is_consistent and satisfied) if count == 0 else (satisfied)
			count += 1

		# print('is_consistent:', is_consistent)
		return is_consistent
		# return True


	def backtrack(self):
		return self.__recursive_backtrack({})


	def __recursive_backtrack(self, assignment):
		complete_assignment = self.__is_assignment_complete(assignment)

		if complete_assignment:
			return assignment

		selected_var = self.__select_unassigned_variable(assignment)
		# print('selected var:', selected_var)

		for value in self.__order_domain_values(selected_var, assignment):
			# print('order_domain_value - value:', value)

			assignment[selected_var] = value
			# print('\nassignment -', selected_var, ':', value, '\n')

			if self.is_assignment_consistent(assignment, selected_var):
				result = self.__recursive_backtrack(assignment)
				# print('checking validity of: ', assignment)
				# print('result:', result)
				if not result == None:
					return result
				
			del assignment[selected_var]

		return None
