"""This module contains the classes of some common Optimization solvers.
There are all instances of the abstract class `AbstractSolver', so that
they have the same interface.

Author: Arnold N'GORAN (arnoldngoran at gmail.com)
Date:   24/01/2020
"""
import numpy as np
import pyscipopt as scip

flag = False
try:
    flag = True
    import gurobipy as grb
except ImportError:
    print('**** Gurobi is not installed, so I do not load it')

from ems.components.abstract_comp import AbstractSolver


if flag:
    class GRB(AbstractSolver):
        "The Gurobi solver"
        name = 'Gurobi'
        PLUS_INFINITY = grb.GRB.INFINITY
        MINUS_INFINITY = -grb.GRB.INFINITY
        BINARY = grb.GRB.BINARY
        MAX = grb.GRB.MAXIMIZE
        MIN = grb.GRB.MINIMIZE
        CLS = grb
        STATUS = grb.GRB.Status
        STATUS_INF_OR_UNBD = grb.GRB.Status.INF_OR_UNBD

        def __init__(self, problem_name='lp_prob'):
            self.nodecount = None
            self.objval = None
            self.isMIP = None
            self.m = GRB.CLS.Model(problem_name)

        def optimize(self):
            self.m.optimize()
            self.isMIP = self.m.IsMIP
            self.objval = self.get_optimum_value()

        def add_constr(self, constr, **params):
            self.m.addConstr(constr, **params)

        def add_var(self, **params):
            return self.m.addVar(**params)

        def set_objective(self, func, sense='max', **params):
            if sense == 'max':
                sense = self.MAX
            elif sense == 'min':
                sense = self.MIN
            else:
                raise Exception('GUROBI:: Invalid optimization SENSE !!')
            self.m.setObjective(func, sense)

        def get_var_by_name(self, name):
            return self.m.getVarByName(name).X

        def get_var_handle(self, name):
            return self.m.getVarByName(name)

        def get_constr_by_name(self, name):
            return self.m.getConstrByName(name)

        def remove_constr(self, name):
            self.m.remove(self.m.getConstrByName(name))

        def get_vars(self):
            return self.m.getVars()

        def get_constrs(self):
            return self.m.getConstrs()

        def get_optimum_value(self):
            return self.m.objval

        def get_objbound(self):
            return self.get_param('ObjBound')

        def get_gap(self):
            return self.get_param('MIPGap')

        def get_nodecount(self):
            return self.get_param('nodecount')

        def get_param(self, name):
            #print(dir(self.m))
            return self.m.getAttr(name)

        def set_param(self, name, value):
            self.m.setParam(name, value)

        def changeRHS(self, name, value):
            self.m.setAttr('RHS', [self.get_constr_by_name(name)], [value])

        def get_status(self):
            return self.m.status

        def computeIIS(self):
            self.m.computeIIS()

        def quicksum(self, expr):
            return GRB.CLS.quicksum(expr)

        def write_model(self, fullname, ext='lp'):
            self.m.write(fullname+'.'+ext)

        def free_transform(self):
            pass

        def update(self):
            """Call this function systematically when you modify a model,
            even though Gurobi updates the model dynamically."""
            self.m.update()


class SCIP(AbstractSolver):
    """The SCIP solver"""
    name = 'SCIP'
    PLUS_INFINITY = MINUS_INFINITY = None
    BINARY = 'B'
    CONTINOUS = 'C'
    INTEGER = 'I'
    MIN = 'minimize'
    MAX = 'maximize'
    CLS = scip
    STATUS = scip.scip.PY_SCIP_STATUS
    STATUS_INF_OR_UNBD = scip.scip.PY_SCIP_STATUS.INFORUNBD

    def __init__(self, problem_name='lp_prob'):
        self.objval = None
        self.isMIP = None
        self.nodecount = None
        self.opt_vars = None
        self.m = self.CLS.Model(problem_name)

    def add_constr(self, constr, **params):
        self.m.addCons(constr, **params)

    def add_var(self, **params):
        return self.m.addVar(**params)

    def set_objective(self, func, sense='max', **params):
        if sense == 'max':
            sense = self.MAX
        elif sense == 'min':
            sense = self.MIN
        else:
            raise Exception('SCIP:: Invalid optimization SENSE !!')
        self.m.setObjective(func, sense)

    def optimize(self):
        self.m.optimize()
        self.objval = self.get_optimum_value()
        self.isMIP = None   # To be defined
        ## Necessary because SCIP does not a function to retrieve
        # variables by their `name'. This is quite strange that SCIP does not provide a better interface
        #self.freeTransform()        
        self.opt_constrs = self.get_constrs()
        self.opt_vars = self.get_vars()

    def get_optimum_value(self):
        return self.m.getObjVal()

    def get_var_by_name(self, name):
        return self.m.getVal(self.opt_vars[name])

    def get_var_handle(self, name):
        return self.opt_vars[name]

    def get_constr_by_name(self, name):
        return self.m.getConss(self.opt_constrs[name])

    def get_constrs(self):
        self.opt_constrs = {str(v):v for v in self.m.getConss()}
        return self.opt_constrs

    def get_vars(self):
        self.opt_vars = {str(v):v for v in self.m.getVars()}
        return self.opt_vars

    def get_param(self, name):
        return self.m.__getattribute__(name)

    def get_objbound(self):
        return self.m.getPrimalbound()

    def get_gap(self):
        return self.getGap()

    def get_nodecount(self):
        return self.getNNodes()

    def set_param(self, name, value):
        self.m.setParam(name, value)

    def changeRHS(self, name, value):
        self.m.chgRhs(self.get_constr_by_name(name), value)

    def get_status(self):
        return self.m.getStatus()

    def remove_constr(self, name):
        # Provided that the Transformed model has been freed
        # Otherwise, you can miss some constraints
        constrs = self.get_constrs()
        self.m.delCons(constrs[name])

    def write_model(self, fullname, ext='cip'):
        self.m.writeProblem(fullname+'.'+ext)

    def computeIIS(self):
        raise Exception('/!\ ComputeIIS NOT IMPLEMENTED')

    def quicksum(self,expr):
        return SCIP.CLS.quicksum(expr)
        #return np.sum(expr)

    def free_transform(self):
        #print('**** WARNING: Verify if it is the RECOMMENDED way to do it.')
        self.m.freeTransform()

    def update(self):
        pass
