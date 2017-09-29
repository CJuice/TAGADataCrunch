###################################
# Script:  ToxicologyDataCrunch4.py
# Author:  CJuice on GitHub
# Date:  20170921
# Purpose: US EPA TAGA Data from sampling events requires processing before being visualized in
#           a map. This script evaluates each data file for the max reading at each unique gps location.
#           Multiple readings at the same location are evaluated for the max value for each chemical sampled for.
#           Once processed, the data is used to create a feature class in the users defined geodatabase. The
#           chemical data can then be visualized in a mapping software.
#           NOTE: Run the ChemicalsPresentAssessor.py script on the files before running this script.
#           The EPA Trace Atmospheric Gas Analyzer (TAGA) is a self-contained mobile laboratory capable of real-time sampling and of outdoor air or emissions.
# Inputs: Workspace .gdb, File directory containing .csv data files.
# Outputs: feature classes
###################################

import sys, os
import SampleEvent
from arcpy import env
from arcpy import management
from arcpy import conversion
'''*** ASSUMPTIONS: All lat lon data is presorted so it is not in a mixed order. Basically, if
                    muliple readings occurred at the same lat lon then a max does need to be calculated.
                    Most sampling events are one reading per unique lat lon pair because the sampling is mobile.
                    Excel file names are compatible with ArcGIS. If not, manipulate names.'''

#VARIABLES
    #define folder where .csv data files are located
strFileDirectory = raw_input("File directory of .csv data files: ")
strDeleteChars = ', \/:*?"<>|'
    #define output folder for processed csv files
strOutputCSVFileDirectory = raw_input("Output file directory for processed maximum value .csv data files: ")
    #define geodatabase where feature classes will be stored
env.workspace = raw_input("Workspace gdb: ")
env.overwriteOutput = True
    #define header names
strSensorReading = "SensorReading"
strSensorName = "SensorName"
strLatitude = "Latitude"
strLongitude = "Longitude"
    #index of header in header record tuple
intSensorReadingIndex = 0
intSensorNameIndex = 0
intLatitudeIndex = 0
intLongitudeIndex = 0
    #new column headers
strMaxBENZENEHeader = "BENZENE_MAX"
strMaxDICHLOROETHENEHeader = "DICHLOROETHENE_MAX"
strMaxTETRACHLOROETHENEHeader = "TETRACHLOROETHENE_MAX"
strMaxTOLUENEHeader = "TOLUENE_MAX"
strMaxTRICHLOROETHENEHeader = "TRICHLOROETHENE_MAX"
strMaxXYLENEHeader = "XYLENE_MAX"
    #chemical names
strBENZENE = "BENZENE"
strDICHLOROETHENE = "DICHLOROETHENE"
strTETRACHLOROETHENE = "TETRACHLOROETHENE"
strTOLUENE = "TOLUENE"
strTRICHLOROETHENE = "TRICHLOROETHENE"
strXYLENE = "XYLENE"
    #List of files
lsCurrentFiles = []
lsNewFiles = []
    #Statistics file name prefix
strStatFileIndicator = "_STAT.txt"

#FUNCTIONALITY
#Run through all .csv files in the file directory and add their path to the lsCurrentFiles
def removeIllegalCharacters(value, deletechars):
    for c in deletechars:
        value = value.replace(c,'')
    return value;

for (dirname, dirs, files) in os.walk(strFileDirectory):
    for filename in files:
        if filename.endswith(".csv"):
            strLegalFileName = removeIllegalCharacters(filename, strDeleteChars)
            os.rename(os.path.join(dirname, filename), os.path.join(dirname, strLegalFileName))
            theFile = os.path.join(dirname, strLegalFileName)
            lsCurrentFiles.append(theFile)
            strNewFileNameString = "ProcessedMAX_{}".format(strLegalFileName)
            lsNewFiles.append(os.path.join(strOutputCSVFileDirectory, strNewFileNameString))
        else:
            continue
# sys.exit() #TESTING shortcut

#open each file in list of files
for file in lsCurrentFiles:
    print("\n___________NEW______FILE_____________\n")

    #capture index of current file so can write to the correct new file
    intIndexOfFileInList = lsCurrentFiles.index(file)
    try:
        #open the data file of interest
        fhand = open(file,"r")
    except:
        print("File: " + file + " did not open")
        sys.exit()
    try:
        #open the new file and write the headers
        fhandNew = open(lsNewFiles[intIndexOfFileInList],"w")
        fhandNew.write("{},{},{},{},{},{},{},{}\n".format(strLatitude,strLongitude,strMaxBENZENEHeader,
                                                          strMaxDICHLOROETHENEHeader,strMaxTETRACHLOROETHENEHeader,
                                                          strMaxTOLUENEHeader,strMaxTRICHLOROETHENEHeader,strMaxXYLENEHeader))
    except:
        print("File: " + lsNewFiles[intIndexOfFileInList] + " did not open")
        sys.exit()
    try:
        strStatFileName = lsNewFiles[intIndexOfFileInList].replace(".csv", strStatFileIndicator)
        fhandStat = open(strStatFileName,"w")
    except:
        print("File: {} did not open.".format(strStatFileName))
        sys.exit()

    strNewFileName = os.path.basename(lsNewFiles[intIndexOfFileInList])
    intRecordsINCount = 0
    intRecordsOUTCount = 0
    intObjectCount = 0
    for line in fhand:

        #split the line on commas and store in a tuple
        tupLineContents = line.split(",")

        #Step 1: When the line count is 0 (headers), get the index of the columns of interest.
        if intRecordsINCount == 0:
            # print tupLineContents  # TESTING
            intSensorReadingIndex = tupLineContents.index(strSensorReading)
            intSensorNameIndex = tupLineContents.index(strSensorName)
            intLatitudeIndex = tupLineContents.index(strLatitude)
            intLongitudeIndex = tupLineContents.index(strLongitude)

        # Step 2: Iterate over each line in the files. Grab the lat, lon, and chemical data from the record tuple
        elif intRecordsINCount > 0:

            #Since the coordinates repeat for six sample chemicals, store the coordinates only once
            floatLat = tupLineContents[intLatitudeIndex]
            floatLon =  tupLineContents[intLongitudeIndex]

            #Object exists already
            if 'objSampleEvent' in globals():
                if objSampleEvent.lat <> floatLat or objSampleEvent.lon <> floatLon:
                    dictMaxValues =  objSampleEvent.calculateMaxChemValuesAndReturnDict()
                    fhandNew.write("{},{},{},{},{},{},{},{}\n".format(objSampleEvent.lat,objSampleEvent.lon,
                                                                            dictMaxValues[strBENZENE],dictMaxValues[strDICHLOROETHENE],
                                                                            dictMaxValues[strTETRACHLOROETHENE],dictMaxValues[strTOLUENE],
                                                                            dictMaxValues[strTRICHLOROETHENE],dictMaxValues[strXYLENE]))
                    intRecordsOUTCount+=1
                    objSampleEvent_old = objSampleEvent
                    del objSampleEvent_old
                    objSampleEvent = SampleEvent.SampleEvent(floatLat,floatLon)
                    objSampleEvent.storeChemical(tupLineContents,intSensorNameIndex,intSensorReadingIndex)
                    continue
                else:
                    pass
            #Object doesn't exist
            else:
                objSampleEvent = SampleEvent.SampleEvent(floatLat,floatLon)
                intObjectCount+=1

            objSampleEvent.storeChemical(tupLineContents, intSensorNameIndex, intSensorReadingIndex)
        else:
            break
        intRecordsINCount+=1
    fhand.close()
    fhandNew.close()
    fhandStat.write("Records IN: {}\nRecords OUT: {}".format(intRecordsINCount,intRecordsOUTCount))
    fhandStat.close()
    del fhand, fhandNew, fhandStat, intRecordsINCount, objSampleEvent

    #Create a feature class containing all of the max chemical values per chemical per unique location
    #   For map visualization.
    strTempFileNameNoExtension = strNewFileName[0:-4]
    xyEL = management.MakeXYEventLayer(table=lsNewFiles[intIndexOfFileInList],
                                       in_x_field=strLongitude,
                                       in_y_field=strLatitude,
                                       out_layer=strTempFileNameNoExtension,
                                       spatial_reference=4269,
                                       in_z_field=None)
    conversion.FeatureClassToFeatureClass(in_features=xyEL,
                                          out_path=env.workspace,
                                          out_name=strTempFileNameNoExtension,
                                          where_clause=None,
                                          field_mapping=None,
                                          config_keyword=None)
    print "Feature class created."
