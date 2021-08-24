import pandas as pd
import json
# from flatten_json import flatten
import csv

# extracting required data from the NVD json
def filter_data(data,num):
    temp = []
    total_cwe = set()
    # CWE_2020 = {"CWE-79", "CWE-787", "CWE-20", "CWE-125", "CWE-119", "CWE-89", "CWE-200", "CWE-416", "CWE-352", "CWE-78", "CWE-190", "CWE-22", "CWE-476", "CWE-287", "CWE-434", "CWE-732", "CWE-94", "CWE-522", "CWE-611", "CWE-798", "CWE-502", "CWE-269", "CWE-400", "CWE-306", "CWE-862"}
    for i in data['CVE_Items']:
        if len(i['impact']) != 0:
            for j in range(len(i['cve']['problemtype']['problemtype_data'][0]['description'])):
                total_cwe.add(i['cve']['problemtype']['problemtype_data'][0]['description'][j]['value'])
                temp.append([i['cve']['problemtype']['problemtype_data'][0]['description'][j]['value'],
                    i['cve']['CVE_data_meta']['ID'], i['impact']['baseMetricV3']['cvssV3']['baseScore'],
                    i['impact']['baseMetricV3']['exploitabilityScore'], i['impact']['baseMetricV3']['cvssV3']['attackComplexity'],
                    i['impact']['baseMetricV3']['cvssV3']['privilegesRequired'], i['impact']['baseMetricV3']['cvssV3']['userInteraction']])

    df = pd.DataFrame(temp)
    df.columns = ['CWE', 'CVE', 'CVSS_V3_baseScore', 'CVSS_V3_exploitabilityScore', 'CVSS_V3_attackComplexity', 'CVSS_V3_privilegesRequired', 'CVSS_V3_userInteraction']
    df.to_csv('data/nvd'+num+'.csv')


# reading the json files from NVD
with open("data/nvdcve-1.1-2019.json",encoding="utf8") as f:
    data = json.load(f)

# change the year below to the year of the NVD data you are reading
filter_data(data, "2019")
print(data['CVE_data_numberOfCVEs'])

# creating a single csv file
all_files = ['data/nvd2018.csv', 'data/nvd2019.csv']
combined_csv = pd.concat([pd.read_csv(f) for f in all_files])
combined_csv.to_csv('data/combined_nvd.csv', index=False)




# data = pd.read_json(r"data/nvdcve-1.1-2019.json")
# flatten_data = flatten(data,".")
# df = pd.json_normalize(flatten_data)
# df.head(3).to_csv('data/test.csv')
# with open("data/test.txt", 'w') as outputfile:
#     json.dump(pd,outputfile)

# data_df = pd.read_csv('data/test.txt',header=None)
# data_df.to_csv(r'data/test.csv',index=None)
# data_file = open('data/test.csv','w')
# csv_writer = csv.writer(data_file)
# csv_writer.writerow(flatten_data[0].keys())
# for row in flatten_data:
#     csv_writer.writerow(row.values())

# flatten_data = pd.DataFrame(data1)
# cleaning = pd.json_normalize(data['CVE_Items'])
