import numpy as np
import pandas as pd

def readDf():
    source_df = pd.DataFrame()
    last_id = 0
    for fi in range(1,10):
        columns_to_drop = ['timestamp_gps','latitude','longitude']
        df_l = pd.read_csv(f"dataset/PVS {fi}/dataset_gps_mpu_left.csv")
        # drop columns
        df_l = df_l.drop(columns=columns_to_drop)
        # rename columns by add "l_" to the column name
        df_l.columns = ["l_"+col for col in df_l.columns]

        # rename l_timestamp to time
        df_l = df_l.rename(columns={"l_timestamp":"time"})

        # subtract the first timestamp from the time column
        df_l["time"] = df_l["time"] - df_l["time"].iloc[0]

        df_r = pd.read_csv(f"dataset/PVS {fi}/dataset_gps_mpu_right.csv")
        # drop columns
        columns_to_drop = ['timestamp','timestamp_gps','latitude','longitude']
        df_r = df_r.drop(columns=columns_to_drop)
        # rename columns by add "r_" to the column name
        df_r.columns = ["r_"+col for col in df_r.columns]

        # merge the two dataframes
        df = pd.concat([df_l, df_r], axis=1)

        df_label = pd.read_csv(f"dataset/PVS {fi}/dataset_labels.csv")

        # get these columns from df_label: no_speed_bump	speed_bump_asphalt	speed_bump_cobblestone
        df_label = df_label[["no_speed_bump","speed_bump_asphalt","speed_bump_cobblestone"]]

        # create a class dataframe with the labels, if no_speed_bump is 1, then the class is 0, if speed_bump_asphalt is 1, then the class is 1, if speed_bump_cobblestone is 1, then the class is 2
        df_class = pd.DataFrame()
        df_class["class"] = df_label.idxmax(axis=1).map({"no_speed_bump":0, "speed_bump_asphalt":1, "speed_bump_cobblestone":2})

        # merge the class dataframe with the main dataframe
        df = pd.concat([df, df_class], axis=1)

        # check if NaN values exist
        #print(df.isnull().sum())

        class_0 = []
        class_1 = []
        class_2 = []
        for i in range(0, len(df)-200, 50):
            window = df.iloc[i:i+200]
            if 0 in window["class"].unique() and 1 not in window["class"].unique() and 2 not in window["class"].unique():
                class_0.append(window.drop(columns=["class"]).to_numpy())
            elif 1 in window["class"].unique():
                class_1.append(window.drop(columns=["class"]).to_numpy())
            elif 2 in window["class"].unique():
                class_2.append(window.drop(columns=["class"]).to_numpy())

        # print the number of windows for each class
        #print(len(class_0), len(class_1), len(class_2))

        len_to_keep = max(len(class_1), len(class_2))*2

        class_1 = np.array(class_1)
        class_2 = np.array(class_2)

        # randomly select the same number of windows for class_0
        class_0 = np.array(class_0)
        np.random.seed(42)
        np.random.shuffle(class_0) # shuffle the array
        class_0 = class_0[:len_to_keep]


        
        for i in range(len(class_0)):
            tmp_df = pd.DataFrame(class_0[i], columns=df.columns[:-1])
            tmp_df["id"] = i + last_id
            tmp_df["class"] = 0
            source_df = pd.concat([source_df, tmp_df], axis=0)
        
        #print("\tLen of Class 0: " , len(class_0))
        
        last_id = source_df["id"].iloc[-1] + 1

        #print("\tLast id: ", last_id)

        for j in range(len(class_1)):
            tmp_df = pd.DataFrame(class_1[j], columns=df.columns[:-1])
            tmp_df["id"] = j+last_id
            tmp_df["class"] = 1
            source_df = pd.concat([source_df, tmp_df], axis=0)
        
        #print("\tLen of Class 1: " , len(class_1))
        
        last_id = source_df["id"].iloc[-1] + 1

        #print("\tLast id: ", last_id)

        for k in range(len(class_2)):
            tmp_df = pd.DataFrame(class_2[k], columns=df.columns[:-1])
            tmp_df["id"] = k+last_id
            tmp_df["class"] = 2
            source_df = pd.concat([source_df, tmp_df], axis=0)
        
        #print("\tLen of Class 2: " , len(class_2))
        
        print("Len of current data: " , len(class_0)+len(class_1)+len(class_2))
        
        last_id = source_df["id"].iloc[-1] + 1
        print("Last id: ", last_id)
    
    return source_df