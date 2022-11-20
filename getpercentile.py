import pandas as pd

# """ Opportunistic Scoring """
# transition = pd.read_csv("/Users/nithucarthikeyan/Downloads/Sports/flask/Data/Opportunistic_Scoring_01.csv")[["PLAYER" ,"Poss"]]
# cut = pd.read_csv("/Users/nithucarthikeyan/Downloads/Sports/flask/Data/Opportunistic_Scoring_02.csv")[["PLAYER" ,"Poss"]]
# other = pd.read_csv("/Users/nithucarthikeyan/Downloads/Sports/flask/Data/Opportunistic_Scoring_03.csv")[["PLAYER" ,"Poss"]]

# mergedscore = pd.merge(transition, cut, on="PLAYER", how="outer")
# mergedscore = pd.merge(mergedscore, other, on="PLAYER", how="outer")
# #mergedscore.columns.values[0] = "Player"
# mergedscore['Total Possesion'] = mergedscore["Poss_x"] + mergedscore["Poss_y"]  + mergedscore["Poss"]
# mergedscore.columns.values[0] = "Player"
# print(mergedscore)

# mergedscore.to_csv("Opportunistic scoring.csv")

# final_merge2 = pd.merge(final, mergedscore, on="Player", how="outer")
# print(final_merge2)
# final_merge2.to_csv("test final merge")


#Metric for Rim Finishing vs Distance/Floater Finishing
rim_finishing = pd.read_csv('/Users/nithucarthikeyan/Downloads/Sports/flask/Data/Rim_vs_Distance.csv')[["('Player',)", "('Team',)", "('Restricted Area', 'FGA')", "('In The Paint (Non-RA)', 'FGA')"]]
final = pd.DataFrame()
final["player"] = rim_finishing["('Player',)"]
final.columns.values[0] = "Player"

rim_finishing[ "('Restricted Area', 'FGA')"] = rim_finishing[ "('Restricted Area', 'FGA')"].replace("-", '0').fillna('0').astype(str)
rim_finishing["('In The Paint (Non-RA)', 'FGA')"] = rim_finishing["('In The Paint (Non-RA)', 'FGA')"].replace("-", 0).fillna(0).astype(float)

#Convert Restircted Area column to number
to_string = pd.to_numeric(rim_finishing[ "('Restricted Area', 'FGA')"])
paint = rim_finishing["('In The Paint (Non-RA)', 'FGA')"] 

total = to_string  + paint
final["Restricted Area Percentage"] = pd.to_numeric(to_string/total)

print(final)



# #Self Creation
self_creation = pd.read_csv("/Users/nithucarthikeyan/Downloads/Sports/flask/Data/Self_Creation.csv")[["Player", "2FGM %AST"]]
final= pd.merge(final, self_creation, on="Player", how="outer")
print(final)
final.to_csv("Final.csv")

# #Interior vs Exterior, percentage of scoring?
made_shots = pd.read_csv("/Users/nithucarthikeyan/Downloads/Sports/flask/Data/Interior_vs_Exterior.csv")[["('Player',)", "('Restricted Area', 'FGM')", "('In The Paint (Non-RA)', 'FGM')"]]
total_scoring = pd.read_csv("/Users/nithucarthikeyan/Downloads/Sports/flask/Data/General.csv")[["Player", "PTS", "FGM", "FGA"]]

made_shots["('Restricted Area', 'FGM')"] = made_shots["('Restricted Area', 'FGM')"].replace("-", 0).fillna(0).astype(float)
made_shots["('In The Paint (Non-RA)', 'FGM')"] = made_shots["('In The Paint (Non-RA)', 'FGM')"].replace("-", 0).fillna(0).astype(float)

made_shots["Player"] = made_shots["('Player',)"]
made_shots.values[0] = "Player"

merged1 =  pd.merge(final, made_shots, on="Player", how="outer")
merged1 = merged1.fillna(0)
print(merged1)
merged1["Total Paint"] = merged1["('Restricted Area', 'FGM')"] + merged1["('In The Paint (Non-RA)', 'FGM')"]
merged2 = pd.merge(merged1, total_scoring, on="Player", how="outer")

final["Interior scoring %"] = 2 * merged1["Total Paint"]/merged2["PTS"]
print(final)


#print(final)
final.to_csv("Final.csv")

# Shots off 0-1 dribbles
# zero_dribble = pd.read_csv("/Users/nithucarthikeyan/Downloads/Sports/flask/Data/0_Low_Dribbles.csv")[["('PLAYER',)",
# "('Field Goals', '2FGA')"]]
# one_dribble = pd.read_csv("/Users/nithucarthikeyan/Downloads/Sports/flask/Data/one_dribble.csv")[["Unnamed: 0_level_0",
# "('Field Goals', '2FGA')"]]
# zero_dribble.columns.values[0] = "Player"
# one_dribble.columns.values[0] = "Player"
# zero_dribble.columns.values[1] = "0 dribble shots"
# one_dribble.columns.values[1] = "1 dribble shots"
# merged_dribbles1 = pd.merge(final, zero_dribble, on="Player", how="outer")
# merged_dribbles2 = pd.merge(merged_dribbles1, one_dribble, on="Player", how="outer")
# print(merged_dribbles2)
# merged_finaldribbles = pd.merge(merged_dribbles2, total_scoring, on="Player", how="outer")
# final["Low Dribble %"] = (merged_finaldribbles["0 dribble shots"] + merged_finaldribbles["1 dribble shots"])/merged_finaldribbles["FGA"]
# print(final)
# merged_dribbles.to_csv("totaldribbles2.csv")

#Drive vs Pullup
# of drives

drives = pd.read_csv("/Users/nithucarthikeyan/Downloads/Sports/flask/Data/Drive_vs_Pullup_(Drive).csv") [["PLAYER",
"DRIVES"]]

pullup = pd.read_csv("/Users/nithucarthikeyan/Downloads/Sports/flask/Data/Drive_vs_Pullup_(Pullup).csv") [["PLAYER", "FGA" ]]
drives.columns.values[0] = "Player"
pullup.columns.values[0] = "Player"
merged_drives = pd.merge(final, drives, on="Player", how="outer")
# final["player"] = rim_finishing["('Player',)"]
# final.columns.values[0] = "Player"
finalmergeddrives = pd.merge(merged_drives, pullup, on="Player", how="outer")
final["Drive vs Pullup Ratio"] = finalmergeddrives["DRIVES"]/finalmergeddrives["FGA"]
#final["Drive Pass %"] = finalmergeddrives["PASS %"]
final.to_csv("Final.csv")
print(final)

#Drive Pass %
drivePass =  pd.read_csv("/Users/nithucarthikeyan/Downloads/Sports/flask/Data/Drive_Pass_Out.csv") [["PLAYER",
"PASS%"]]
drivePass.columns.values[0] = "Player"
finalDrive = pd.merge(final, drivePass,  on="Player", how="outer")
final["Drive Pass %"] = finalDrive["PASS%"]
print(final)
final.to_csv("Final.csv")

#Average dribble per touch
dribbletouch = pd.read_csv("/Users/nithucarthikeyan/Downloads/Sports/flask/Data/Average_Dribbles.csv") [["Player",
"Avg Drib Per Touch"]]
finalTouch = pd.merge(final, dribbletouch,  on="Player", how="outer")
final["Avg Dribble Per Touch"] = finalTouch["Avg Drib Per Touch"]
print(final)

#Opportunistic Scoring

final.to_csv("Final.csv")



