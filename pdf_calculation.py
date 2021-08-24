import numpy as np
import pandas as pd
import scipy.integrate
from scipy.stats import lognorm
from plots import plot, pv_total
from generalisedFunctions import generalised_PDF, generalised_CDF, generalised_PDF_mean



#=========================================

# PDF calculation
def PDFCalculation(lambda_list,rho,eZn_cap):
    pv_anPDF = []
    pv_anCDF = []
    pv_emp_exp = []
    pv_emp_log = []
    v_1 = np.arange(0.0, eZn_cap[0], 100)
    v_2 = np.arange(0.0, eZn_cap[1], 100)
    v_3 = np.arange(0.0, eZn_cap[2], 100)
    v_list = [v_1, v_2, v_3]
    tau_exp_list = [np.random.exponential(1/i,100000) for i in lambda_list]
    tau_log_list = [np.random.lognormal(0.5,1,100000),np.random.lognormal(0.25,1.5,100000),np.random.lognormal(1,0.75,100000)]
    for i in range(3):
        pv_anPDF.append(generalised_PDF(i+1,lambda_list,rho,eZn_cap[i],v_list[i]))
        pv_anCDF.append(generalised_CDF(i+1,lambda_list,rho,eZn_cap[i],v_list[i]))
        if i == 0:
            tau = tau_exp_list[0]
            tau_log = tau_log_list[0]
        elif i == 1:
            tau = tau_exp_list[0] + tau_exp_list[1]
            tau_log = tau_log_list[0] + tau_log_list[1]
        else:
            tau = tau_exp_list[0] + tau_exp_list[1] + tau_exp_list[2]
            tau_log = tau_log_list[0] + tau_log_list[1] + tau_log_list[2]
        pv_emp_exp.append(eZn_cap[i] * np.exp(-rho*tau))
        pv_emp_log.append(eZn_cap[i] * np.exp(-rho*tau_log))

    # 95th percentile of analytical results
    pv_emp_exp_95 = [round(np.percentile(i,95),3) for i in pv_emp_exp]

    plot(v_list[0],pv_anPDF[0],pv_emp_exp[0],pv_emp_exp_95[0],phase='Phase 1')
    plot(v_list[1],pv_anPDF[1],pv_emp_exp[1],pv_emp_exp_95[1],phase='Phase 2')
    plot(v_list[2],pv_anPDF[2],pv_emp_exp[2],pv_emp_exp_95[2],phase='Phase 3')
    # pv_total(sum(pv_emp_exp),sum(pv_emp_log),(round(np.percentile(sum(pv_emp_exp),0.95),3)),phase='Total')

    print(f'###################################')
