from ortools.linear_solver import pywraplp
import numpy as np


def main(A,R,S,E):
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')

    # Create the variables x and y.
    x = solver.NumVar(0, 1, 'x')
    # y = solver.NumVar(0, 2, 'y')

    print('Number of variables =', solver.NumVariables())

    # Create a linear constraint, 0 <= x + y <= 2.
    solver.Add()
    print('Number of constraints =', solver.NumConstraints())

    # Create the objective function, 3 * x + y.
    objective = solver.Objective()
    objective.SetCoefficient(x, 3)
    objective.SetCoefficient(y, 1)
    objective.SetMaximization()

    solver.Solve()

    print('Solution:')
    print('Objective value =', objective.Value())
    print('x =', x.solution_value())
    print('y =', y.solution_value())


if __name__ == '__main__':
    vulnerabilities = 2
    A = [10,30,20]
    R = [[0.2,0.4],[0.2,0.3],[0.6,0]]
    S = [[0.4,0.4],[0.6,0.4],[0.2,0.1]]
    E = [[0.5,0.1],[0.4,0.5],[0.3,0.7],[0.3,0.5],[0.1,0.1]]


    c = np.inner(R,S)
    print(c)
    # main(A,R,S,E)
