from fuzzywuzzy import process
import pandas as pd
import time

#alters data in harvard to better match with altered madris data

df_harvard = pd.read_csv("cs_externalorgs.csv")

df_temp_harvard = df_harvard["OTH_NAME_SORT_SRCH"].values

altered = []

for line in df_temp_harvard:
    if "UNIV" in str(line):
        if "UNIVERSIDAD" in str(line):
            altered.append(line)
        elif "UNIVERSITY" not in str(line):
            altered.append(line.replace("UNIV", "UNIVERSITY"))
        else:
            altered.append(line)

    if "SCI" in str(line):
        if "SCIENCE" in str(line):
            altered.append(line)
        elif "SCIENCE" not in str(line):
            altered.append(line.replace("SCI", "SCIENCE"))
        else:
            altered.append(line)

    if "SCH" in str(line):
        if "SCHOOL" not in str(line):
            altered.append(line.replace("SCH", "SCHOOL"))
        else:
            altered.append(line)

    elif "CMTY" in str(line):
        if "COMMUNITY" not in str(line):
            altered.append(line.replace("COMM", "COMMUNITY"))
        else:
            altered.append(line)

    elif "COLL" in str(line):
        if "COLLEGE" not in str(line):
            altered.append(line.replace("COLL", "COLLEGE"))
        else:
            altered.append(line)

    elif "INST" in str(line):
        if "INSTITUTE" not in str(line):
            altered.append(line.replace("INST", "INSTITUTE"))
        else:
            altered.append(line)

    else:
        altered.append(line)

print(len(altered))

print(len(df_temp_harvard))

df_harvard["OTH_NAME_SORT_SRCH"] = altered

df_harvard.to_csv("altered_names.csv")

