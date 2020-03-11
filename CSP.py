

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


	def __select_unassigned_variable(self, assignment):
		if len(assignment) == len(self.variables):
			print('CSP.__select_unassigned_variable(): all variables already selected')
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

			num_changes = 0    # in case there is a tie with this heuristic as well
			max_involved_variable = ''
			max_involvement = -1
			for (constraint_var, constraint_list) in self.constraint_involvement.items():
				if constraint_var in assignment:
					continue

				# calcuate current constraint involvement of constraint_var
				curr_involvement = 0
				for con in constraint_list:
					# to ignore constraint if the given var is already in the assignment
					if con.var1 == constraint_var and con.var2 in assignment:
						continue
					elif con.var2 == constraint_var and con.var1 in assignment:
						continue
					curr_involvement += 1

				if curr_involvement > max_involvement:
					max_involvement = curr_involvement
					max_involved_variable = constraint_var
					num_changes += 1

			# TODO: sort alphabetically
			if num_changes == 1:
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
			complete = (satisfied) if count == 0 else (complete and satisfied)
			count += 1

		return complete and len(assignment) == len(self.variables)


	def __order_domain_values(self, given_var, assignment):
		vals_removed_per_var = {}
		for val in self.domains[given_var]:
			vals_removed_per_var[val] = self.__count_values_removed(given_var, val, assignment)

		sorted_vals_removed = {k: v for k, v in sorted(vals_removed_per_var.items(), key=lambda item: item[1])}
		return [key for key in sorted_vals_removed.keys()]


	def __count_values_removed(self, given_var, val, current_assignment):
		num_removed_vals = 0
		temp_assign = {given_var : val}

		if given_var not in self.constraint_involvement:
			return 0

		for constraint in self.constraint_involvement[given_var]:
			adjacent_var = constraint.get_opposing_var(given_var)
			if adjacent_var in current_assignment:
				continue
			for adjacent_val in self.domains[adjacent_var]:
				temp_assign[adjacent_var] = adjacent_val
				if not constraint.satisfied(temp_assign):
					num_removed_vals += 1

		return num_removed_vals


	def is_assignment_consistent(self, assignment, variable):

		is_consistent = True
		count = 0

		if variable not in self.constraint_involvement:
			return True

		for constraint in self.constraint_involvement[variable]:
			if constraint.var1 == variable and constraint.var2 not in assignment:
				continue
			elif constraint.var2 == variable and constraint.var1 not in assignment:
				continue
			satisfied = constraint.satisfied(assignment)
			is_consistent = (satisfied) if count == 0 else (is_consistent and satisfied)
			count += 1

		return is_consistent


	def forward_checking(self, assignment):
		pass


	def backtrack(self):
		return self.__recursive_backtrack({}, '', 1)


	def __recursive_backtrack(self, assignment, str_bldr, step_counter):
		complete_assignment = self.__is_assignment_complete(assignment)

		if complete_assignment:
			str_bldr += str(step_counter) + '. ' + (''.join( [(str(key) + '=' + str(value) + ',') for (key,value) in assignment.items()] ))
			str_bldr = str_bldr[:-1]
			str_bldr += '  solution'
			str_bldr += '\n'
			step_counter += 1
			return ('success', assignment, str_bldr, step_counter)

		selected_var = self.__select_unassigned_variable(assignment)

		for value in self.__order_domain_values(selected_var, assignment):

			assignment[selected_var] = value

			if self.is_assignment_consistent(assignment, selected_var):
				result = self.__recursive_backtrack(assignment, str_bldr, step_counter)
				str_bldr = result[2]
				step_counter = result[3]
				if not result[0] == 'failure':
					return ('success',result[1], result[2], result[3])
			else:
				str_bldr += str(step_counter) + '. ' + (''.join( [(str(key) + '=' + str(value) + ',') for (key,value) in assignment.items()] ))
				str_bldr = str_bldr[:-1]
				str_bldr += '  failure'
				str_bldr += '\n'
				step_counter += 1

			del assignment[selected_var]

		return ('failure', assignment, str_bldr, step_counter)
