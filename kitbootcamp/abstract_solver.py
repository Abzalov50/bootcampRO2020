import abc


class AbstractSolver(abc.ABC):
    @abc.abstractmethod
    def optimize(self, **args):
        """Optimize problem defined by the model, with the given parameters.

        Return:
          Optimization model

        """
        pass

    @abc.abstractmethod
    def add_constr(self, constr, **params):
        """Add a new constraint `constr' to the model with the given parameters.

        Args:
           constr (object): Constraints as equality, inequality, etc.
           params (dict): Dictionary in which the keys are the name
              of the parameters and the values are their new values.

        Return:
          Optimization model

        """
        pass

    @abc.abstractmethod
    def add_var(self, **params):
        """Add a new optimization variable to the model, with the given parameters.

        Args:
           params (dict): Dictionary in which the keys are the name
              of the parameters and the values are their new values.

        Return:
          Variable

        """
        pass

    @abc.abstractmethod
    def get_param(self, param_name, *args, **kwargs):
        """Get the value of solver's parameter `param_name'

        Args:
           param_name (str): Parameter name

        Return:
          Solver parameter value

        """
        pass

    @abc.abstractmethod
    def set_param(self, param_name, *args, **kwargs):
        """Set the parameter `param_name' from model `m',
        to the new values given by `args' and `kwargs'

        Args:
           param_name (str): Parameter name

        """
        pass

    @abc.abstractmethod
    def set_objective(self, func, sense='max', **params):
        """Set the objective function `func' to the model
        with the given sense and parameters.

        Args:
           func (object): Objective function
           sense (object): Whether it is `max' or `min' (default: 'max')
           params (dict): Dictionary in which the keys are the name
              of the parameters and the values are their new values.

        Return:
          Optimization model

        """
        pass

    def get_var_by_name(self, name):
        """Return the value of optimization variable,
        with the given name.

        Args:
           name (str): Variable name

        Return:
          Optimization variable value

        """
        pass

    def get_var_handle(self, name):
        """Return variable handle

        Args:
           name (str): Variable name

        Return:
          Optimization variable handle

        """
        pass

    def get_constr_by_name(self, name):
        """Return the constraint identified by the given name.

        Args:
           name (str): Constraint name

        Return:
          Constraint handle

        """
        pass

    def get_constrs(self):
        """Return all the constraints of the model.

        Return:
          Constraint handles

        """
        pass

    def remove_constr(self, name):
        """Remove the constraint identified by the given name.

        Args:
           name (str): Constraint name

        """
        pass

    @abc.abstractmethod
    def get_vars(self):
        """Return the values of ALL the optimization variables
        of the model.

        Return:
          Values of optimization variables (probably as a LIST)

        """
        pass

    @abc.abstractmethod
    def get_optimum_value(self):
        """Return the optimum value of the model.

        Return:
          Optimum value

        """
        pass

    @abc.abstractmethod
    def changeRHS(self, name, value):
        """Change the RHS of the constraint of the given name, to the given value."""
        pass

    @abc.abstractmethod
    def get_status(self):
        pass

    @abc.abstractmethod
    def get_objbound(self):
        pass

    @abc.abstractmethod
    def get_gap(self):
        pass

    @abc.abstractmethod
    def get_nodecount(self):
        pass

    @abc.abstractmethod
    def update(self):
        """Update the model, after some modifications.
        THIS FUNCTION IS SPECIFIC TO GUROBI SOLVER.

        Return:
          Model

        """
        pass

    @abc.abstractmethod
    def free_transform(self):
        """Remove the transformed model. 
        Necessary before modifying an already solved model.
        THIS FUNCTION IS SPECIFIC TO SCIP SOLVER.
        """
        pass

    @abc.abstractmethod
    def write_model(self, fullname, ext='lp'):
        """Write the model into a file.

        Args:
          fullname (str): path+name
          ext (str): Extension of the file written

        """
        pass

    @abc.abstractmethod
    def computeIIS(self):
        """When model is INFEASIBLE or UNBOUNDED, 
        compute an Irreducible Inconsistent Subsystem (IIS).

        """
        pass

    @abc.abstractmethod
    def quicksum(expr):
        """Take a list of numerical expressions on
        optimization variables and performs the sum.

        Args:
           expr (list): Optimization model

        Return:
          Model

        """
        return sum(expr)
