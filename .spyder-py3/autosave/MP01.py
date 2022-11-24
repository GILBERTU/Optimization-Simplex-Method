# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 14:41:51 2022

@author: i94gg
"""

from gurobipy import *

# Input parameters
Months = [1,2,3,4,5,6]
di = [1555, 1100, 1645, 1100, 695, 545] # Forecasted demand
u1 =[1000] #Reg_Capacity
u2 =[300] #Over_capacity
c1 =[10] #Production_cost_regular 
c2 =[15] #Production_cost_overtime 
h =[2] #inventory_hodling
b =[5] #back_ordered_cost
w_bar_o = [0] #opening back order
w_bar_n = [0] #closing back order
z_bar_o =[150]  #Opening_inventory
z_bar_n =[100] #closing_inventory

indices = range(1,len(Months)+1)

Try:
    #Create new model
    m = model("production planning with back orders")
    
    # Create a vector of variables
    unit_prod_Reg_xi = m.addVars(indices, lb=0.0,ub = u1, vtype=GRB.CONTINUOUS, name="Units Produced in Regular")
    unit_prod_Ov_yi = m.addVars(indices, lb=0.0,ub = u2, vtype=GRB.CONTINUOUS, name="Units Produced in Overtime")
    unit_inv_zi = m.addVars(indices, lb=0.0, vtype=GRB.CONTINUOUS, name="Units carried in Inventory")
    unit_bo_wi = m.addVars(indices, lb=0.0, vtype=GRB.CONTINUOUS, name="Units Back ordered")
 
    # Set objective
    m.setObjective(quicksum([c1*unit_prod_Reg_xi[i] + c2*unit_prod_Ov_yi[i] + h*unit_inv_zi[i] + b*unit_bo_wi[i]  for i in indices]),GRB.MINIMIZE)
    
    #Constraints 1
    m.addConstr(unit_inv_zi[0] == z_bar_o)
    
    #Constraints 2
    m.addConstr(unit_bo_wi[0] == w_bar_o)
    
    #Constraints 3
    for j in indices:
        m.addConstr(unit_prod_Reg_xi[j] + unit_prod_Ov_yi[j] + unit_inv_zi[j-1] - unit_inv_zi[j]  == di[j-1] + unit_bo_wi[j-1] + unit_bo_wi[j] , name= Months[j-1])
        #Note: Months and demand di are indexed starting from 0
    
        
    
    
    


    # Write formulation in LP format !!!ONLY FOR SMALL INSTANCES!!!
     m.write("production planning with back orders.lp")
    
    #Call Gurobi Optimizer
    m.optimize()
    
    # Write Output if termination is optimal
    if m.status == GRB.OPTIMAL:
        for v in m.getVars():
            print('%s = %g' % (v.varName, v.x)) 
        print('Obj = %f' % m.objVal)
    elif m.status == GRB.INFEASIBLE:
        print('LP is infea
    elif m.status == GRB.UNBOUNDED:
        print('LP is unbounded.')
except GurobiError:
    print('Error reported')
    
