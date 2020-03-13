# CS 4365 - Artificial Intelligence
# Nisarg Desai - npd160030
# Sanketh Reddy - spr150430

class Constraint:

	# TODO
	def __init__(self, clause_as_list):
		self.var1 = clause_as_list[0]
		self.operator = clause_as_list[1]
		self.var2 = clause_as_list[2]


	# TODO
	def satisfied(self, assignment):
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


	def select_unassigned_variable(self, assignment):
		if len(assignment) == len(self.variables):
			print('CSP.select_unassigned_variable(): all variables already selected')
			exit()

		final_var = ''

		# most constrained variable heuristic
		len_dict = {}
		for (key,val) in self.domains.items():
			if key in assignment:
				continue
			len_dict[key] = len(val)
		min_len = min(len_dict.values())
		min_var_tied_keys = [key for key,val in len_dict.items() if val == min_len]

		# if there is a tie, so use most constrainING variable
		if len(min_var_tied_keys) > 1:
			max_involved_dict = {}

			for variable in min_var_tied_keys:

				# ignore variables that have already been assigned
				if variable in assignment:
					continue

				constraint_list = self.constraint_involvement[variable]

				# calcuate current constraint involvement of constraint_var
				curr_involvement = 0
				for constraint in constraint_list:
					# to ignore constraint if the given var is already in the assignment
					if (constraint.var1 == variable and constraint.var2 in assignment) or (constraint.var2 == variable and constraint.var1 in assignment):
						continue
					curr_involvement += 1

				max_involved_dict[variable] = curr_involvement

			max_involvement = max(max_involved_dict.values())
			max_involvement_tied_keys = [key for key,val in max_involved_dict.items() if val == max_involvement]

			if len(max_involvement_tied_keys) > 1:
				sorted_tied_vars = [item for item in sorted(max_involvement_tied_keys)]
				for var in sorted_tied_vars:
					if var in assignment:
						continue
					else:
						return var
			else:
				final_var = max_involvement_tied_keys[0]
		else:
			final_var = min_var_tied_keys[0]

		if final_var == '':
			print('CSP.select_unassigned_variable(): error selecting variable')
			# stop program
			exit()

		return final_var


	def is_assignment_complete(self, assignment):
		consistent = False

		count = 0
		for constraint in self.constraints:
			if constraint.var1 not in assignment or constraint.var2 not in assignment:
				return False

			# check if constraint is satisfied given the assignment
			satisfied = constraint.satisfied(assignment)
			consistent = (satisfied) if count == 0 else (consistent and satisfied)
			count += 1

		# if all constraints are satisfied (consistent) and the length of the assignment dict equals num variables then assignment is complete
		return consistent and len(assignment) == len(self.variables)


	def order_domain_values(self, given_var, assignment):
		vals_removed_per_var = {}
		for val in self.domains[given_var]:
			vals_removed_per_var[val] = self.count_values_removed(given_var, val, assignment)

		# sort the vals removed dictionary by number of vals removed from least to most
		sorted_vals_removed = {k: v for k, v in sorted(vals_removed_per_var.items(), key=lambda item: item[1])}
		return sorted_vals_removed.keys()


	def count_values_removed(self, given_var, val, current_assignment):
		num_removed_vals = 0
		temp_assign = {given_var : val}

		# return 0 for vars with no constraints
		if given_var not in self.constraint_involvement:
			return 0

		# count number of removed values
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


	def forward_checking(self, assignment, newly_selected_var):

		removed_vals = {}
		if newly_selected_var not in self.constraint_involvement:
			return {}
		for constraint in self.constraint_involvement[newly_selected_var]:
			var_to_iter = constraint.var1 if constraint.var2 == newly_selected_var else constraint.var2
			if var_to_iter in assignment:
				continue
			curr_domain = {val for val in self.domains[var_to_iter]}
			for value in curr_domain:
				assignment[var_to_iter] = value
				if not constraint.satisfied(assignment):

					# save value to be removed in case there is a failure with this assignment down the road
					# and it needs to be restored
					if var_to_iter in removed_vals:
						removed_vals[var_to_iter].append(value)
					else:
						removed_vals[var_to_iter] = [value]

					# remove value
					self.domains[var_to_iter].remove(value)
				del assignment[var_to_iter]

		return removed_vals


	def restore(self, removed_vals):
		for key,val_list in removed_vals.items():
			for val in val_list:
				self.domains[key].append(val)


	def check_domains(self, csp):
		valid_domain_set = True
		for var, domain in csp.domains.items():
			valid_domain_set = valid_domain_set and (not len(domain) == 0)
		return valid_domain_set


def backtrack(csp: CSP):
	return fc_recursive_backtrack(csp, {}, '', 1) if csp.fc else recursive_backtrack(csp, {}, '', 1)


def recursive_backtrack(csp: CSP, assignment, str_bldr, step_counter):
	complete_assignment = csp.is_assignment_complete(assignment)

	# base case - stop recursion if this condition is met
	# and add a step to the string builder
	if complete_assignment:
		str_bldr += str(step_counter) + '. ' + (''.join( [(str(key) + '=' + str(value) + ',') for (key,value) in assignment.items()] ))
		str_bldr = str_bldr[:-1]
		str_bldr += '  solution'
		str_bldr += '\n'
		step_counter += 1
		return ('success', assignment, str_bldr, step_counter)

	# select a variable to assign next
	selected_var = csp.select_unassigned_variable(assignment)

	# iterate over its values after using LCV to order the values
	for value in csp.order_domain_values(selected_var, assignment):

		# temporarily assign the value
		assignment[selected_var] = value

		# start recursion if the value is consistent
		if csp.is_assignment_consistent(assignment, selected_var):
			result = recursive_backtrack(csp, assignment, str_bldr, step_counter)
			str_bldr = result[2]
			step_counter = result[3]
			if not result[0] == 'failure':
				return ('success', result[1], result[2], result[3])
		else:
			# if not consistent then add step to string builder
			str_bldr += str(step_counter) + '. ' + (''.join( [(str(key) + '=' + str(value) + ',') for (key,value) in assignment.items()] ))
			str_bldr = str_bldr[:-1]
			str_bldr += '  failure'
			str_bldr += '\n'
			step_counter += 1

		del assignment[selected_var]

	return ('failure', assignment, str_bldr, step_counter)

def fc_recursive_backtrack(csp: CSP, assignment, str_bldr, step_counter):

	complete_assignment = csp.is_assignment_complete(assignment)

	if complete_assignment:
		str_bldr += str(step_counter) + '. ' + (''.join( [(str(key) + '=' + str(value) + ',') for (key,value) in assignment.items()] ))
		str_bldr = str_bldr[:-1]
		str_bldr += '  solution'
		str_bldr += '\n'
		step_counter += 1
		return ('success', assignment, str_bldr, step_counter, csp)

	selected_var = csp.select_unassigned_variable(assignment)

	for value in csp.order_domain_values(selected_var, assignment):
		assignment[selected_var] = value

		# removed_vals temporarily stores removed domain values and their corresponding variables
		# this way if there's a constraint failure later on, removed values can be restored
		removed_vals = csp.forward_checking(assignment, selected_var)

		# check if any domains are empty - if any are empty then it is a failure
		# if none are empty then take recursive step
		if csp.check_domains(csp):
			result = fc_recursive_backtrack(csp, assignment, str_bldr, step_counter)
			str_bldr = result[2]
			step_counter = result[3]
			if not result[0] == 'failure':
				return ('success', result[1], result[2], result[3], csp)
		else:
			str_bldr += str(step_counter) + '. ' + (''.join( [(str(key) + '=' + str(value) + ',') for (key,value) in assignment.items()] ))
			str_bldr = str_bldr[:-1]
			str_bldr += '  failure'
			str_bldr += '\n'
			step_counter += 1

		# forward checking removes values that will break a constraint
		# so this step is needed to restore removed values if a constraint is broken anyways
		csp.restore(removed_vals)
		del assignment[selected_var]

	return ('failure', assignment, str_bldr, step_counter, csp)