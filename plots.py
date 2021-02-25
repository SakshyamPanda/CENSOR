import matplotlib.pyplot as plt
# from sklearn import preprocessing
# import seaborn as sns

def plot(v,pv_anPDF,pv_anCDF,pv_emp_exp,pv_emp_log,phase):
    plt.hist(pv_emp_exp,bins=100,density=1,color='blue',alpha=0.6,label='Simulated PDF (exponential)')
    # sns.distplot(pv_emp, hist=True, kde=False, bins=100, norm_hist=True)
    plt.plot(v,pv_anPDF,'r--',label='Analytical PDF (exponential)')
    plt.plot(v,pv_anCDF,'k:',label='Analytical CDF (exponential)')
    plt.hist(pv_emp_log,bins=100,density=1,color='green',alpha=0.7,label='Simulated PDF (log-norm)')
    plt.xlabel('Present Value '+ '('+phase+')')
    plt.ylabel('Frequency')
    plt.legend(loc='best')
    plt.show()


def pv_total(pv1,pv2,phase):
    plt.hist(pv1,bins=100,density=1,color='blue',alpha=0.6,label='Simulated PDF (exponential)')
    plt.hist(pv2,bins=100,density=1,color='green',alpha=0.7,label='Simulated PDF (log-norm)')
    plt.xlabel('Present Value '+ '('+phase+')')
    plt.ylabel('Frequency')
    plt.legend(loc='best')
    plt.show()
