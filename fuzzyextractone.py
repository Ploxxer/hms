from fuzzywuzzy import process
import pandas as pd

correct_with_rating = []

df_madris = pd.read_csv("madris.csv")
# df_madris['DEGREE DESCR'].str.strip(" ")
df_harvard = pd.read_csv("my_harvard.csv")

df_madris['DEGREE DESCR'] = 'X' + df_madris['DEGREE DESCR'].astype(str)
df_madris['DEGREE DESCR'] = df_madris['DEGREE DESCR'].str.upper()

df_temp_madris = df_madris['DEGREE DESCR'].values
df_temp_harvard = df_harvard['Degree'].values

for row in df_temp_madris:
    x = process.extractOne(row, df_temp_harvard)
    correct_with_rating.append({"Correct_Degree(my.harvard)" : x[0], "Tested_Degree(madris)" : row.strip(" "), "Rating" : x[1]})

df_processed_data = pd.DataFrame(correct_with_rating)

df_processed_data = df_processed_data.sort_values(by = "Rating", ascending=False)

columnsTitles=["Correct_Degree(my.harvard)","Tested_Degree(madris)","Rating"]
df_processed_data=df_processed_data.reindex(columns=columnsTitles)
print(df_processed_data)

df_processed_data.to_csv("processed_data.csv")

equal_100 = []
below_100 = []

#For rows with rating equal to 100, use the degree abrv from the my.harvard table
#For rows with rating below 100, use the degree abrv from the madris table
for index, row in df_processed_data.iterrows():
    # print(row['Correct_Degree'], row['Rating'])
    if(row['Rating'] == 100):
        equal_100.append({"Degree" : row['Correct_Degree(my.harvard)'], "Rating" : row["Rating"]})
    elif(row["Rating"] < 100):
        below_100.append({"Degree" : row['Tested_Degree(madris)'], "Rating" : row["Rating"]})

df_madris_equal_100 = pd.DataFrame(equal_100)
df_madris_below_100 = pd.DataFrame(below_100)

print("Rating equal 100")
print(df_madris_equal_100)
print("Rating below 100")
print(df_madris_below_100)
