from fuzzywuzzy import process
import pandas as pd
import time

start_time = time.time()

correct_with_rating = []

#initial csvs are read in here, madris dataframe is the one most likely to be altered
df_madris = pd.read_csv("madris_institutions.csv")

df_harvard = pd.read_csv("cs_externalorgs.csv")


#extract relevant columns and data ie. name, id
df_real_madris = df_madris['institution_name'].values
univ_list_real = df_real_madris.tolist()

df_madris['institution_name'] = df_madris['institution_name'].str.upper()

df_temp_harvard = df_harvard["OTH_NAME_SORT_SRCH"].values

df_temp_harvard_id = df_harvard["EXT_ORG_ID"].values

df_temp_madris = df_madris['institution_name'].values

df_temp_madris_id = df_madris['institution_id'].values

madris_id_list = df_temp_madris_id.tolist()
harvard_id_list = df_temp_harvard_id.tolist()

univ_list = df_temp_madris.tolist()

univ_new_list = []
madris_final_list = []

#replaces univ., coll, etc.
for ind,line in enumerate(univ_list):
    if "UNIV." in str(line):
        univ_new_list.append(line.replace("UNIV.", "UNIVERSITY"))

    elif "COMM." in str(line):
        univ_new_list.append(line.replace("COMM.", "COMMUNITY"))

    elif "COL." in str(line):
        univ_new_list.append(line.replace("COL.", "COLLEGE"))

    elif "COLL." in str(line):
        if "COLLEGE" not in str(line):
            univ_new_list.append(line.replace("COLL.", "COLLEGE"))

    elif "INST." in str(line):
        univ_new_list.append(line.replace("INST.", "INSTITUTE"))

    elif "&" in str(line):
        univ_new_list.append(line.replace("&", "AND"))

    else:
        univ_new_list.append(line)

#some universities in madris have their country of origin added in the university name after the last comma
#counts occurences of commas and removes every character after the last comma if comma_count != 0
#special characters and whitespace is removed as well afterwards

for ind, line in enumerate(univ_new_list):
    comma_count = 0
    for character in str(line):
        if "," == character:
            comma_count +=1

    temp_list = str(line).split(",")
    temp_list_2 = []

    if(comma_count != 0):
        del(temp_list[comma_count])

    for i in temp_list:
        j = i.replace(' ', '').replace("'", "").replace(".", "")
        temp_list_2.append(j)

    temp = "".join(temp_list_2)

    madris_final_list.append(temp)


harvard_combined = dict(zip(df_temp_harvard,df_temp_harvard_id))

df_madris_altered = pd.DataFrame(madris_final_list)

df_madris_altered.columns = ["institution_name"]

df_temp_madris_2 = df_madris_altered['institution_name'].values

print(harvard_combined)

#do the actual fuzzymatching here
for row in df_temp_madris_2:
    x = process.extract(row, df_temp_harvard, limit=2)
    correct_with_rating.append({"Correct_Univ_1(my.harvard)" : x[0], "Tested_Univ(madris)" : row.strip(" "), "Correct_Univ_2(my.harvard)" : x[1], "Best_Rating" : x[0][1]})
    print(correct_with_rating)

df_processed_data = pd.DataFrame(correct_with_rating)
columnsTitles=["Correct_Univ_1(my.harvard)","Correct_Univ_2(my.harvard)","Tested_Univ(madris)","Best_Rating"]
df_processed_data=df_processed_data.reindex(columns=columnsTitles)

#put in madris id column
df_processed_data["institution_id"] = madris_id_list
df_processed_data = df_processed_data.sort_values(by = "Best_Rating", ascending=False)


#put in harvard id columns
correct_univ_1 = df_processed_data["Correct_Univ_1(my.harvard)"].values
correct_univ_2 = df_processed_data["Correct_Univ_2(my.harvard)"].values

org_id_1 = []
org_id_2 = []

for i in range(len(correct_univ_1)):
    a, b = correct_univ_1[i]
    c, d = correct_univ_2[i]
    if a in harvard_combined:
        org_id_1.append(harvard_combined[a])
    if c in harvard_combined:
        org_id_2.append(harvard_combined[c])


print(org_id_1)
df_processed_data["org_id_1"] = org_id_1

df_processed_data["org_id_2"] = org_id_2
print(org_id_2)

columnsTitles=["Correct_Univ_1(my.harvard)","org_id_1","Correct_Univ_2(my.harvard)","org_id_2","Tested_Univ(madris)","institution_id","Best_Rating"]
df_processed_data=df_processed_data.reindex(columns=columnsTitles)

#exports processed_data dataframe to a csv file
df_processed_data.to_csv("processed_data_limit_2_universities_forealthistime.csv")

print(df_processed_data)

print(str(time.time()-start_time))


