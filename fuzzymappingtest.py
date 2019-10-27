from fuzzywuzzy import process
import pandas as pd
schoolname_madris = []
schoolname_new = []

correct_with_rating = []

df1 = pd.read_csv("Workbook1.csv")
df2 = pd.read_csv("Workbook2.csv")

df1_alt = df1['school'].values
df2_alt = df2['school'].values

df_new = pd.DataFrame(columns=["school", "rating"])
for row in df2_alt:
    x = process.extractOne(row, df1_alt)
    correct_with_rating.append({"school" : x[0], "rating" : x[1]})
    print(correct_with_rating)

df_new = pd.DataFrame(correct_with_rating)

columnsTitles=["school","rating"]
df=df_new.reindex(columns=columnsTitles)

print(df)



# correct = ["Boston University"]
#
# incorrect = ["Boston University", "BU" , "BostonUniv"]
#
# for line in incorrect:
#     print(str(line) + " " + str(process.extractOne(line, correct)))
