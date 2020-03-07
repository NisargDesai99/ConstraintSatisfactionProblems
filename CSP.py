

class Constraint:

	# TODO
	def __init__(self):
		pass

	# TODO
	def satsified(self):
		pass


class CSP:

	# list of variable names
	# dictionary of var names (key) and list of domain values (value)
	# constraint list? dict?

	def __init__(self, variables, domains, constraints):
		self.variables = variables
		self.domains = domains
		self.constraints = constraints

		self.constraint_involvement = {}
		for con in self.constraints:
			if con[0] not in self.constraint_involvement:
				self.constraint_involvement[con[0]] = [con]
			else:
				self.constraint_involvement[con[0]].append(con)

			if con[2] not in self.constraint_involvement:
				self.constraint_involvement[con[0]] = [con]
			else:
				self.constraint_involvement[con[2]].append(con)
		
	def select_unassigned_variable(self):
		tie_exists = False
		
		final_var = ''
		
		# most constrained variable heuristic
		min_len = 100000
		min_variable = ''
		num_changes = 0    # keeps track of number of changes to min_len, if it is 1 it means there was a tie
		for (key,val) in self.variables.items():
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
#             if num_changes == 1:    
		else:
			final_var = min_variable
		
		if final_var == '':
			print('error selecting variable')
			# stop program
			# exit()
		
		return final_var



