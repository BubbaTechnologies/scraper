#Matthew Groholski
#July 22nd, 2023

from crontab import CronTab

import properties
import os
import subprocess
import re2 as re

def mvFilesFromSubdirectories(path: str, moveDirectory: str):
    dirList = [f.path for f in os.scandir(path) if f.is_dir()]
    for i in dirList:
        root, _, files = next(os.walk(i))
        for file in files:
            subprocess.run(["mv", "{0}/{1}".format(root, file), moveDirectory])
        subprocess.run(["rm", "-r", "{0}".format(root)])

def calculateRating(file)->float:
    text = file.read()
    clothingCreatedCount = len(re.findall("Created ", text))
    queueCount = len(re.findall(" to queue", text))
    return clothingCreatedCount/queueCount

def scheduleJobs(totalGroups:int, route:str):
    pass

def main():
    #Removes old groupings
    mvFilesFromSubdirectories(properties.INFO_PATH, properties.INFO_PATH)

    #Calculates ratings per json file
    fileList = [f.path for f in os.scandir(properties.INFO_PATH) if f.is_file()]
    ratings = []
    for file in fileList:
        basename = os.path.splitext(os.path.basename(file))[0]
        totalRating = 0
        if os.path.exists("{0}/{1}".format(properties.OUTPUT_PATH, basename)):
            outputList = [f.path for f in os.scandir("{0}/{1}".format(properties.OUTPUT_PATH, basename)) if f.is_file()]
            fileCount = 0
            for outputFilename in outputList:
                if fileCount > properties.PREVIOUS_OUTPUT_RATING:
                    fileCount += 1
                    with open(outputFilename) as outputFile:
                        totalRating += calculateRating(outputFile)
        ratings.append((basename, totalRating / properties.PREVIOUS_OUTPUT_RATING))

    ratings.sort(key = lambda x: x[1])
    groupNumber = 0
    for i in range(len(ratings)):
        if i % properties.SCRAPER_GROUP_MAX_AMOUNT == 0:
            groupNumber += 1
            subprocess.run(["mkdir","{0}/group{1}".format(properties.INFO_PATH, str(groupNumber))])
        subprocess.run(["mv","{0}/{1}.json".format(properties.INFO_PATH, ratings[i][0]),"{0}/group{1}".format(properties.INFO_PATH, str(groupNumber))])
    
    scheduleJobs(groupNumber, properties.INFO_PATH)

if __name__=="__main__":
    main()