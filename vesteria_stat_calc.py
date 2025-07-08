import cplex

# globals
max_level = 60

my_prob = cplex.Cplex()

my_prob.set_problem_type(cplex.Cplex.problem_type.LP)
my_prob.objective.set_sense(my_prob.objective.sense.minimize)

names = ["str", "vit", "int", "dex"]
objective = [1,1,1,1]    # minimizing str + vit + int + dex
lb = [0,0,0,0]     # all stats must be >= 0 
ub = [cplex.infinity, cplex.infinity, cplex.infinity, cplex.infinity]

my_prob.variables.add(obj=objective,
                      lb=lb,
                      ub=ub,
                      names=names)


# Below are constraints when wearing my nova gear
# Preferred Stats
opt_str = 51
opt_vit = 51
opt_int = 151
opt_dex = 91

use_yeti_ex = False

base_str = 33 + 2
base_vit = 22 + 6 + 4 + 16 + 10 * use_yeti_ex     # 6 from vit anc chest still pending, 16 from vib mod
base_int = 44 + 12 + 4    # 3 from int anc chest still pending, 9 from 3 anc int on mace pending
base_dex = 28 + 4

constraints = [
    [["str"], [1]],     # str >= 51 - base_str
    [["vit"], [1]],     # vit >= 51 - base_vit
    [["int"], [1]],     # int >= 151 - base_int
    [["dex"], [1]]      # dex >= 91 - base_dex
]
rhs = [opt_str-base_str, opt_vit-base_vit, opt_int-base_int, opt_dex-base_dex]                 # Right-hand sides
senses = ["G", "G", "G", "G"]              # 'G' for greater than or equal to

my_prob.linear_constraints.add(lin_expr=constraints,
                               senses=senses,
                               rhs=rhs)

# Below are constraints when wearing my ghostflame
# Preferred Stats
opt_str = 51
opt_vit = 31
opt_int = 151
opt_dex = 71

use_yeti_ex = False

base_str = 45 + 9        # helio gives 40, and anc should be ~4-5 str, to be conservative let's say 4 str each
base_vit = 6 + 6 + 16 + 10 * use_yeti_ex     # 6 from vit anc chest still pending
base_int = 27 + 3 + 6   # 3 from int anc chest still pending, 6 from anc helms
base_dex = 12

constraints = [
    [["str"], [1]],     # str >= 51 - base_str
    [["vit"], [1]],     # vit >= 31 - base_vit
    [["int"], [1]],     # int >= 151 - base_int
    [["dex"], [1]]      # dex >= 71 - base_dex
]
rhs = [opt_str-base_str, opt_vit-base_vit, opt_int-base_int, opt_dex-base_dex]                 # Right-hand sides
senses = ["G", "G", "G", "G"]              # 'G' for greater than or equal to

my_prob.linear_constraints.add(lin_expr=constraints,
                               senses=senses,
                               rhs=rhs)

# Solve the problem
my_prob.solve()

# Print results
print("Solution status:", my_prob.solution.get_status_string())
print("Objective value:", my_prob.solution.get_objective_value())
print("Total level stats available with XX: ", (max_level - 1) * 3 + 19)
print("Variable values:")
for var_name in names:
    value = my_prob.solution.get_values(var_name)
    print(f"  {var_name} = {value}")