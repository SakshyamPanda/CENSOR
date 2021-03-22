import numpy as np
 

# Generalised function for PDF
def generalised_PDF(atk_phase,lambda_list,rho,k,u_dist):
    temp_lambda = np.zeros(shape=(atk_phase,atk_phase))
    temp_PDF = np.zeros(shape=(atk_phase,len(u_dist)))
    for i in range(atk_phase):
        for j in range(atk_phase):
            if j == i:
                # print(f'{i}; j-->{j}')
                temp_lambda[i][j] = lambda_list[i]
            else:
                temp_lambda[i][j] = float(lambda_list[j]/(lambda_list[j]-lambda_list[i]))
    lambda_product = np.multiply.reduce(temp_lambda,axis=1)
    for i in range(atk_phase):
        temp_PDF[i] = ([1/(rho * k) * lambda_product[i] * (j/k)**(lambda_list[i]/rho-1) for j in u_dist])
    PDF = np.sum(temp_PDF, axis=0) # this is the present value for PDF
    return(PDF)


# Generalised function for CDF
def generalised_CDF(atk_phase,lambda_list,rho,k,u_dist):
    temp_lambda = np.zeros(shape=(atk_phase,atk_phase))
    temp_CDF = np.zeros(shape=(atk_phase,len(u_dist)))
    for i in range(atk_phase):
        for j in range(atk_phase):
            if j == i:
                temp_lambda[i][j] = 1
            else:
                temp_lambda[i][j] = float(lambda_list[j]/(lambda_list[j]-lambda_list[i]))
    lambda_product = np.multiply.reduce(temp_lambda,axis=1)
    for i in range(atk_phase):
        temp_CDF[i] = [(j/k)**(lambda_list[i]/rho) * lambda_product[i] for j in u_dist]
    CDF = np.sum(temp_CDF, axis=0) # this is the present value for CDF
    return(CDF)


# Generalised Funtion for Mean
def generalised_PDF_mean(atk_phase,lambda_list,rho,k):
    temp_lambda = np.zeros(shape=(atk_phase,atk_phase))
    temp_mean = []
    for i in range(atk_phase):
        for j in range(atk_phase):
            if j == i:
                temp_lambda[i][j] = 1 # Have to check
            else:
                temp_lambda[i][j] = float(lambda_list[j]/(lambda_list[j]-lambda_list[i]))
    lambda_product = np.multiply.reduce(temp_lambda,axis=1)
    for i in range(atk_phase):
        temp_mean[i] = lambda_list[i]/(lambda_list[i]+rho)*lambda_product[i]
    mean_value = k*np.sum(temp_mean)
    return(mean_value)
