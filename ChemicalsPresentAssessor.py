###################################
# Script:  ChemicalsPresentAssessor.py
# Author:  CJuice on GitHub
# Date:  20170921
# Purpose:  When get EPA TAGA data files, put them all in a folder together.
#           Then, run this on the folder, it steps through every .csv file in the folder.
#           The script checks the attributes in the SensorName column to see what chemicals were measured.
#           The code makes a Set and prints it out.
#           If it is set(['BENZENE', 'XYLENE', 'TRICHLOROETHENE', 'DICHLOROETHENE', 'TETRACHLOROETHENE', 'TOLUENE']) then you are good.
# Inputs: None
# Outputs: Printed set of chemicals from data
###################################

import os, sys

strFileDirectory = raw_input("File Directory: ") #r"M:\IRGIS\Mapping\AGprojects\FY2018\511047_TraciePhillips\Request_20170914\ProcessedDataSets"
strSensorName = "SensorName"
setChemicalTypesStandard = set(['BENZENE', 'XYLENE', 'TRICHLOROETHENE', 'DICHLOROETHENE', 'TETRACHLOROETHENE', 'TOLUENE'])

for (dirname, dirs, files) in os.walk(strFileDirectory):
    for filename in files:
        if filename.endswith(".csv"):
            thefile = os.path.join(dirname,filename)
            setChemicalSet = set()
            fhand = open(thefile)
            count = 0
            intIndexOfSensorName = 0
            for line in fhand:
                lsLine = line.split(",")
                if count == 0:
                    # print type(lsLine)
                    try:
                        intIndexOfSensorName = lsLine.index(strSensorName)
                    except:
                        print "error in detecting 'SensorName' in file headers"
                        print (strSensorName in lsLine)
                        print lsLine
                else:
                    setChemicalSet.add(lsLine[intIndexOfSensorName])
                count += 1
            fhand.close()
            del fhand
            print thefile
            print setChemicalSet
            print "Standard: set(['BENZENE', 'XYLENE', 'TRICHLOROETHENE', 'DICHLOROETHENE', 'TETRACHLOROETHENE', 'TOLUENE'])"
            print "Equivalent: {}".format(setChemicalSet == setChemicalTypesStandard)