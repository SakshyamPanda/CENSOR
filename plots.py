import matplotlib.pyplot as plt
# from sklearn import preprocessing
# import seaborn as sns

def plot(v,pv_anPDF,pv_emp_exp,pv_emp_log,phase):
    plt.hist(pv_emp_exp,bins=100,density=1)
    # sns.distplot(pv_emp, hist=True, kde=False, bins=100, norm_hist=True)
    plt.plot(v,pv_anPDF,'r--')
    # plt.hist(pv_emp_log,bins=100,density=1,color='green')
    plt.xlabel('Present Value '+ '('+phase+')')
    plt.ylabel('Frequency')
    plt.show()


def pv_total(pv1,pv2,phase):
    plt.hist(pv1,bins=100,density=1)
    plt.xlabel('Present Value '+ '('+phase+')')
    plt.ylabel('Frequency')
    plt.show()
