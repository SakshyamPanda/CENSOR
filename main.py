import numpy as np
import scipy.integrate
from scipy.stats import lognorm
from plots import plot, pv_total
from generalisedFunctions import generalised_PDF, generalised_CDF, generalised_PDF_mean


# This short code produces the distribution of the present value (PV) of the
# cost for the first phase of a security breach as well as the value at risk (VaR).
# in the code we are using u_i instead of Z_i used in the paper.

# u_dist we use two different distributions (of the present value which expresses cyber risk)
# these are 1) prob dist function and 2) cumulative dist function

##### Parameter Values
# Discount factor (same notation with the paper).
rho = 0.3

# Parameter of exponential distribution (same notation with the paper, random values).
lambda_1 = 2
lambda_2 = 3
lambda_3 = 5
lambda_list = [lambda_1, lambda_2, lambda_3]

# In the benchmark case the cost is fixed and assumed equal to 10. According
# to Eq.(1), k = A.R.S, however, the values of A, R and S are not
# clear at the moment. In terms of linking T5.3 and T5.4 with other WPs we
# would need to have:

# A         = ? (This is likely to be defined exogenously)
# R         = ? (Taken from another WP?)
# S         = ? (Taken from another WP?)

# so that
# k         = A*R*S;

# For now, I simply assume that (determines the range of PV distribution)
k_1 = 10
k_2 = 9
k_3 = 11

# Creating the range of distribution for the different values.
# The PV cannot exceed the value of k.
v_1 = np.arange(0.0, k_1, 0.1)
v_2 = np.arange(0.0, k_2, 0.1)
v_3 = np.arange(0.0, k_3, 0.1)

# Distribution of PV for Phase 1 of the attack
pv_anPDF_1 = generalised_PDF(1,lambda_list,rho,k_1,v_1)
pv_anCDF_1 = generalised_CDF(1,lambda_list,rho,k_1,v_1)

# Sanity check: integral pf PDF equal to 1
f = lambda x:(lambda_1/rho * k_1**(-lambda_1/rho) * x**(lambda_1/rho-1))
tem = scipy.integrate.quad(f,0,k_1)
print(f'f1--{sum(tem)}')

# Empirical Model: It may not always be possible to derive the analytical
# expression of the PDF and CDF, so we should also produce the simulated version.

tau_1 = np.random.exponential(1/lambda_1,100000)           # sampling tau from an exponential distribution
tau_11 = np.random.lognormal(0.5,1,100000)                          # sampling tau from an log-normal distribution
pv_emp_1 = k_1 * np.exp(-rho*tau_1)
pv_emp_11 = k_1 * np.exp(-rho*tau_11)
# print(f'e1: {pv_emp_1}')
# print(f'e11: {pv_emp_11}')



# Distribution of PV for phase 2 attack
pv_anPDF_2 = generalised_PDF(2,lambda_list,rho,k_2,v_2)
pv_anCDF_2 = generalised_CDF(2,lambda_list,rho,k_2,v_2)

# Sanity check: integral pf PDF equal to 2
f = lambda x:(lambda_1*lambda_2/(lambda_2-lambda_1)*1/(k_2*rho)*((x/k_2)**(lambda_1/rho -1)-(x/k_2)**(lambda_2/rho - 1)))
tem = scipy.integrate.quad(f,0,k_2)
print(f'f2--{sum(tem)}')

tau_2 = np.random.exponential(1/lambda_2,100000)           # sampling tau from an exponential distribution
tau_21 = np.random.lognormal(0.25,1.5,100000)                          # sampling tau from an log-normal distribution
pv_emp_2 = k_2 * np.exp(-rho*(tau_1+tau_2))
pv_emp_21 = k_2 * np.exp(-rho*(tau_11+tau_21))
# print(f'e2: {pv_emp_2}')
# print(f'e21: {pv_emp_21}, {tau_21}')


#Distribution of PV for phase 3 attack
pv_anPDF_3 = generalised_PDF(3,lambda_list,rho,k_3,v_3)
pv_anCDF_3 = generalised_CDF(3,lambda_list,rho,k_3,v_3)

# Sanity check: integral pf PDF equal to 3
prod_lambda_3 = lambda_1 * lambda_2 * lambda_3
f = lambda x:(prod_lambda_3/((lambda_1-lambda_3)*(lambda_2-lambda_3))*1/(rho*x)*(x/k_3)**(lambda_3/rho)
            + prod_lambda_3/((lambda_2-lambda_1)*(lambda_3-lambda_1))*1/(rho*x)*(x/k_3)**(lambda_1/rho)
            + prod_lambda_3/((lambda_1-lambda_2)*(lambda_3-lambda_2))*1/(rho*x)*(x/k_3)**(lambda_2/rho))
tem = scipy.integrate.quad(f,0,k_3)
print(f'f3--{sum(tem)}')


tau_3 = np.random.exponential(1/lambda_3,100000)           # sampling tau from an exponential distribution
tau_31 = np.random.lognormal(1,0.75,100000)                          # sampling tau from an log-normal distribution
pv_emp_3 = k_2 * np.exp(-rho*(tau_1+tau_2+tau_3))
pv_emp_31 = k_2 * np.exp(-rho*(tau_11+tau_21+tau_31))
# print(f'e3: {pv_emp_3}')
# print(f'e31: {pv_emp_31}')

# Total PV
pv_1 = pv_emp_1 + pv_emp_2 + pv_emp_3
pv_2 = pv_emp_11 + pv_emp_21 + pv_emp_31


# Plotting the results
# plots for phase 1
plot(v_1,pv_anPDF_1,pv_anCDF_1,pv_emp_1,pv_emp_11,phase='Phase 1')

# plots for phase 2
plot(v_2,pv_anPDF_2,pv_anCDF_2,pv_emp_2,pv_emp_21,phase='Phase 2')

# plots for phase 3
plot(v_3,pv_anPDF_3,pv_anCDF_3,pv_emp_3,pv_emp_31,phase='Phase 3')

# plots for pv total
pv_total(pv_1,pv_2,phase='Total')
