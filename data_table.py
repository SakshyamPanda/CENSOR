import pandas as pd
import random

# function reads the all cwe list and creates the data table
def cwe_data_table():
    df = pd.read_csv('data/combined_nvd.csv')
    data = pd.DataFrame(df)
    data.loc[data["CVSS_V3_attackComplexity"] == "LOW", "CVSS_V3_attackComplexity"] = 1
    data.loc[data["CVSS_V3_attackComplexity"] == "HIGH", "CVSS_V3_attackComplexity"] = 2
    data.loc[data["CVSS_V3_privilegesRequired"] == "NONE", "CVSS_V3_privilegesRequired"] = 1
    data.loc[data["CVSS_V3_privilegesRequired"] == "LOW", "CVSS_V3_privilegesRequired"] = 2
    data.loc[data["CVSS_V3_privilegesRequired"] == "HIGH", "CVSS_V3_privilegesRequired"] = 3
    data.loc[data["CVSS_V3_userInteraction"] == "NONE", "CVSS_V3_userInteraction"] = 0
    data.loc[data["CVSS_V3_userInteraction"] == "REQUIRED", "CVSS_V3_userInteraction"] = 1
    top_CWE_2020 = ["CWE-79", "CWE-787", "CWE-20", "CWE-125", "CWE-119", "CWE-89", "CWE-200", "CWE-416", "CWE-352", "CWE-78", "CWE-190", "CWE-22", "CWE-476", "CWE-287", "CWE-434", "CWE-732", "CWE-94", "CWE-522", "CWE-611", "CWE-798", "CWE-502", "CWE-269", "CWE-400", "CWE-306", "CWE-862"]
    CWE = data.CWE.unique()
    temp = []
    for i in CWE:
        cwe = data[data["CWE"] == i]
        cvss_mean = cwe["CVSS_V3_baseScore"].mean()
        cvss_min = data["CVSS_V3_baseScore"].min()
        cvss_max = data["CVSS_V3_baseScore"].max()
        privileges_mean = round(cwe["CVSS_V3_privilegesRequired"].mean(),2)
        interaction_mean = round(cwe["CVSS_V3_userInteraction"].mean(),2)
        Sv_cwe = (cvss_mean - cvss_min)/(cvss_max - cvss_min)
        # temp.append([i, cwe.shape[0], cvss_mean, cvss_min, cvss_max, round(cwe["CVSS_V3_severity"].mean(),2), round(cwe["CVSS_V3_exploitability"].mean(),2), round(cwe["CVSS_V3_complexity"].mean(),2), Sv_cwe])
        temp.append([i, cwe.shape[0], round(cvss_mean,2), round(cwe["CVSS_V3_exploitabilityScore"].mean(),2), round(cwe["CVSS_V3_attackComplexity"].mean(),2), privileges_mean, interaction_mean, privileges_mean + interaction_mean, Sv_cwe])
    rec = pd.DataFrame(temp)
    # rec.columns = ['CWE', 'NVD_count', 'Avg_CVSS_V3', 'min_CVSS_V3', 'max_CVSS_V3', 'avg_CVSS_V3_severity', 'avg_CVSS_V3_exploitability', 'avg_CVSS_V3_complexity', 'Sv_cwe']
    rec.columns = ['CWE', 'NVD_count', 'Avg_CVSS_V3_baseScore', 'Avg_CVSS_V3_exploitabilityScore', 'Avg_CVSS_V3_attackComplexity', 'Avg_CVSS_V3_privilegesRequired', 'Avg_CVSS_V3_userInteraction', 'Avg_CVSS_V3_time', 'Sv_cwe']
    rec['CWE_score'] = round((rec['NVD_count'] - rec['NVD_count'].min())/(rec['NVD_count'].max() - rec['NVD_count'].min()) * rec['Sv_cwe'] * 100, 2)

    # saving all data
    rec.sort_values(by='NVD_count', ascending=False).to_csv('data/all_CWE_table.csv', index=False)

    # filtering top 25 2020 CWE
    rec.loc[rec['CWE'].isin(top_CWE_2020)].sort_values(by='NVD_count', ascending=False).to_csv('data/top_25_CWE_table.csv', index=False)

# function reads the controls-cwe mapping and creates the efficaacy table
# Efficacy table has each control with levels L and H
def control_efficacy_table():
    df = pd.read_excel('data/cwe-cisIG1-mapping.xlsx', engine='openpyxl')
    data = pd.DataFrame(df).dropna(axis='columns')
    # print(control_data.columns)
    efficacy_data = pd.DataFrame()
    efficacy_data['Rank'] = data['Rank']
    efficacy_data['ID'] = data['ID']
    for i in range(len(efficacy_data['ID'])):
        for col in list(data.columns):
            if col != 'ID' and col != 'Rank':
                eff1 = round(random.uniform(0.4,0.94),3)
                eff2 = round(random.uniform(0,eff1),3)
                efficacy_data.loc[i,str(col)+'_L'] = eff2
                efficacy_data.loc[i,str(col)+'_H'] = eff1
    efficacy_data.to_csv(r'data/control_efficacy_table.csv', index=False)


if __name__ == "__main__":
    cwe_data_table()
    # control_efficacy_table()
