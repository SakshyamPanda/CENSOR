import numpy as np
import scipy.integrate
from scipy.stats import lognorm
from plots import plot, pv_total


# This short code produces the distribution of the present value (PV) of the
# cost for the first phase of a security breach as well as the value at risk (VaR).


# PDF generalised function
def generelised_PDF(atk_phase,lambda_list,rho,k,u_dist):
    temp_lambda = np.zeros(shape=(atk_phase,atk_phase))
    temp_PDF = np.zeros(shape=(atk_phase,len(u_dist)))
    for i in range(atk_phase):
        for j in range(atk_phase):
            if j == i:
                temp_lambda[i][j] = lambda_list[i]
            else:
                temp_lambda[i][j] = float(lambda_list[j]/(lambda_list[j]-lambda_list[i]))

    lambda_product = np.multiply.reduce(temp_lambda, axis=1)
    for i in range(atk_phase):
        temp_PDF[i] = ([1/(rho * k) * lambda_product[i] * (j/k)**(lambda_list[i]/rho-1) for j in u_dist])

    PDF = np.sum(temp_PDF, axis=0)
    return(PDF)


##### Parameter Values
# Discount factor.
rho = 0.3

# Parameter of exponential distribution.
lambda_1 = 2
lambda_2 = 3
lambda_3 = 5

# In the benchmark case the cost is fixed and assumed equal to 10. According
# to Eq.(1), k = A.R.S, however, the values of A, R and S are not
# clear at the moment. In terms of linking T5.3 and T5.4 with other WPs we
# would need to have:

# A         = ? (This is likely to be defined exogenously)
# R         = ? (Taken from another WP?)
# S         = ? (Taken from another WP?)

# so that
# k         = A*R*S;

# For now, I simply assume that:
k_1 = 10
k_2 = 9
k_3 = 11

# The PV cannot exceed the value of k.
v_1 = np.arange(0.0, k_1, 0.1)
v_2 = np.arange(0.0, k_2, 0.1)
v_3 = np.arange(0.0, k_3, 0.1)



# Distribution of PV for phase 1 attack
lambda_list_1 = [lambda_1]
pv_anPDF_1 = generelised_PDF(1,lambda_list_1,rho,k_1,v_1)

# Sanity check: integral pf PDF equal to 1
f = lambda x:(lambda_1/rho * k_1**(-lambda_1/rho) * x**(lambda_1/rho-1))
tem = scipy.integrate.quad(f,0,k_1)
print(f'f1--{sum(tem)}')

# Empirical Model: It may not always be possible to derive the analytical
# expression of the PDF and CDF, so we should also produce the simulated version.

tau_1 = np.random.exponential(1/lambda_1,100000)           # sampling tau from an exponential distribution
tau_11 = lognorm.rvs(0.5,1,100000)                          # sampling tau from an log-normal distribution
pv_emp_1 = k_1 * np.exp(-rho*tau_1)
pv_emp_11 = k_1 * np.exp(-rho*tau_11)
print(f'e1: {pv_emp_1}')
print(f'e11: {pv_emp_11}')



# Distribution of PV for phase 2 attack
lambda_list_2 = [lambda_1, lambda_2]
pv_anPDF_2 = generelised_PDF(2,lambda_list_2,rho,k_2,v_2)

# Sanity check: integral pf PDF equal to 2
f = lambda x:(lambda_1*lambda_2/(lambda_2-lambda_1)*1/(k_2*rho)*((x/k_2)**(lambda_1/rho -1)-(x/k_2)**(lambda_2/rho - 1)))
tem = scipy.integrate.quad(f,0,k_2)
print(f'f2--{sum(tem)}')

tau_2 = np.random.exponential(1/lambda_2,100000)           # sampling tau from an exponential distribution
tau_21 = lognorm.rvs(0.25,1.5,100000)                          # sampling tau from an log-normal distribution
pv_emp_2 = k_2 * np.exp(-rho*(tau_1+tau_2))
pv_emp_21 = k_2 * np.exp(-rho*(tau_11+tau_21))
print(f'e2: {pv_emp_2}')
print(f'e21: {pv_emp_21}')



#Distribution of PV for phase 3 attack
lambda_list_3 = [lambda_1, lambda_2, lambda_3]
pv_anPDF_3 = generelised_PDF(3,lambda_list_3,rho,k_3,v_3)

# Sanity check: integral pf PDF equal to 3
prod_lambda_3 = lambda_1 * lambda_2 * lambda_3
f = lambda x:(prod_lambda_3/((lambda_1-lambda_3)*(lambda_2-lambda_3))*1/(rho*x)*(x/k_3)**(lambda_3/rho)
            + prod_lambda_3/((lambda_2-lambda_1)*(lambda_3-lambda_1))*1/(rho*x)*(x/k_3)**(lambda_1/rho)
            + prod_lambda_3/((lambda_1-lambda_2)*(lambda_3-lambda_2))*1/(rho*x)*(x/k_3)**(lambda_2/rho))
tem = scipy.integrate.quad(f,0,k_3)
print(f'f3--{sum(tem)}')


tau_3 = np.random.exponential(1/lambda_3,100000)           # sampling tau from an exponential distribution
tau_31 = lognorm.rvs(1,0.75,100000)                          # sampling tau from an log-normal distribution
pv_emp_3 = k_2 * np.exp(-rho*(tau_1+tau_2+tau_3))
pv_emp_31 = k_2 * np.exp(-rho*(tau_11+tau_21+tau_31))
print(f'e3: {pv_emp_3}')
print(f'e31: {pv_emp_31}')

# Total PV
pv_1 = pv_emp_1 + pv_emp_2 + pv_emp_3
pv_2 = pv_emp_11 + pv_emp_21 + pv_emp_31


# Plotting the results
# plots for phase 1
plot(v_1,pv_anPDF_1,pv_emp_1,pv_emp_11,phase='Phase 1')

# plots for phase 2
plot(v_2,pv_anPDF_2,pv_emp_2,pv_emp_21,phase='Phase 2')

# plots for phase 3
plot(v_3,pv_anPDF_3,pv_emp_3,pv_emp_31,phase='Phase 3')

# plots for pv total
pv_total(pv_1,pv_2,phase='Total')
