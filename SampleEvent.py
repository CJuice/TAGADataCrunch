###################################
# Script:  SampleEvent.py
# Author:  CJuice on GitHub
# Date:  20170921
# Purpose:  SampleEvent Class. Contains state and behavior for a sampling event object.
#           Created for EPA TAGA Data processing per a customer request project
#           Originally applied to TCEQ Toxicology request.
# Inputs:
# Outputs:
###################################
class SampleEvent(object):
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.dictChemicals = {}

    def setSpatial(self, tupCoordinates):
        self.lat = tupCoordinates[0]
        self.lon = tupCoordinates[1]
        self.spatialIsSet = True

    def getSpatialTuple(self):
        return (self.lat, self.lon)

    def calculateMaxChemValuesAndReturnDict(self):
        dictMaxChemValues = {}
        for key in self.dictChemicals:
            # print "key: {}, items: {}".format(key, self.dictChemicals[key])
            dictMaxChemValues[key] = max(self.dictChemicals[key])
        return dictMaxChemValues

    def storeChemical(self, tupLineContents, intSensorNameIndex, intSensorReadingIndex):
        # Store the chemical name and value for this line
        strChemName = tupLineContents[intSensorNameIndex]
        #Had a few issues with data transfer. Some readings converted to 0.  stripping and casting to float below
        strChemReading = tupLineContents[intSensorReadingIndex]
        strChemReading = strChemReading.strip()
        try:
            floatChemReading = float(strChemReading)
            # print floatChemReading
        except:
            print "issue with strChemReading conversion to float"
            return


        # if the chemical is already stored in the chemicals dictionary that means a list of readings already exists, so append the value to the list
        # Else, add the chemical name KEY and then create the chemical values list VALUE
        if self.dictChemicals.get(strChemName):
            # chemical previously added
            self.dictChemicals.get(strChemName).append(floatChemReading)
        else:
            # first time for chemical
            self.dictChemicals[strChemName] = [floatChemReading]
