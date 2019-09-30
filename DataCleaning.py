import pandas as pd
import sys
import os
import math
import re
from io import StringIO

#Reading files
def listAndReadFiles(inputFolder,multiplier):
    data_to_write = pd.DataFrame()
    for root, dirs, files in os.walk(inputFolder,topdown=True):
        k = 1
        for name in files:
            path = os.path.join(root,name)
            print(path)
            dataset = pd.read_csv(path,header = None,encoding="utf-8",sep= ",")

            dataOneFile = clean_file(dataset,multiplier)
            data_to_write = data_to_write.append(dataOneFile)
    return data_to_write


def oneShotReadAll(inputFolder,multiplier):
    data_to_write = pd.DataFrame()
    for root, dirs, files in os.walk(inputFolder,topdown=True):
        k = 1
        for name in files:
            path = os.path.join(root,name)
            #print(path)

            dataset = pd.read_csv(path,header = None,encoding="utf-8",sep= ",")
            data_to_write = data_to_write.append(dataset)
    dataOneFile = clean_file(data_to_write,multiplier)
    return dataOneFile

#writing to output file
def writeFiles(dataframe,outputFile):
    dataframe.to_csv(outputFile, header=None, index=None, sep=',', mode='a')

def clean_file(dataset,multiplier):


    columns_name = dataset.columns
    dataset[5] = dataset[2]-dataset[1]
    print("lenght of dataset is : ", len(dataset[1]))
    #calculating the mean for annotations and standard deviation
    annotation_std = dataset.groupby(dataset[0])[5].describe()

    #setting the keys for annotations
    primary_key = annotation_std.index
    new_data_list = []
    std_keys = {}
    mean_keys = {}

    for key in primary_key:
        mean_keys[key] = annotation_std.loc[key]["mean"]
        std_keys[key] = annotation_std.loc[key]["std"]


    for index,rows in dataset.iterrows():
        for key in primary_key:
            try:
                #setting the upper and lowerBound
                upperBound = mean_keys[key]+std_keys[key]*float(multiplier)
                lowerBound = mean_keys[key]-std_keys[key]*float(multiplier)


                if(rows[0]==key and ((rows[5]> upperBound) or (rows[5]< lowerBound))):
                    new_data_list.append(rows)
            except:
                # for handling the NAN values
                new_data_list.append(rows)



    # dropping the column containing average
    new_data_frame = pd.DataFrame(new_data_list)
    try:
        new_data_frame = new_data_frame.drop([5],axis=1).reset_index()
    except:
        pass
    return new_data_frame

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("Usage : python %s inputfiledirectory outputfileDirectory\n" % sys.argv[0])
        raise SystemExit(1)
    inputFolder = sys.argv[1]
    outputFile = sys.argv[2]
    std  = input("enter the required standard deviation")
    temp_test = ""
    data_to_write = listAndReadFiles(inputFolder,std)
    writeFiles(data_to_write,outputFile)
    reply = input("do you want to do the whole stuff in one DataFrame? type YES or NO")

    if(reply.casefold() == "yes"):
        data1_to_write = oneShotReadAll(inputFolder,std)
        outputFile=outputFile+"fullstuff"+".csv"
        writeFiles(data1_to_write,outputFile)
    else:
        exit(0)
