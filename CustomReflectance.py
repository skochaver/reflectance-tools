#Steve Kochaver
#kochaver.python@gmail.com
#Version Date 2013-12-13

import sys, os, math, time 
import arcpy
from arcpy import env
from arcpy.sa import *

arcpy.CheckOutExtension("spatial")

#Calculate the radiance from metadata on band.
def calcRadiance (LMAX, LMIN, QCALMAX, QCALMIN, QCAL, outfolder):
    
    LMAX = float(LMAX)
    LMIN = float(LMIN)
    QCALMAX = float(QCALMAX)
    QCALMIN = float(QCALMIN)
    offset = (LMAX - LMIN)/(QCALMAX-QCALMIN)
    inraster = Raster(QCAL)
    outname = outfolder + '//RadianceCustomFile.tif'

    arcpy.AddMessage('LMAX ='+str(LMAX))
    arcpy.AddMessage('LMIN ='+str(LMIN))
    arcpy.AddMessage('QCALMAX ='+str(QCALMAX))
    arcpy.AddMessage('QCALMIN ='+str(QCALMIN))
    arcpy.AddMessage('offset ='+str(offset))
    
    outraster = (offset * (inraster-QCALMIN)) + LMIN
    outraster.save(outname)
    
    return outname

def calcReflectance(solarDist, ESUN, solarZenith, radianceRaster, scaleFactor, outfolder):
    
    #Value for solar zenith is 90 degrees minus solar elevation (angle from horizon to the center of the sun)
    #http://landsathandbook.gsfc.nasa.gov/data_properties/prog_sect6_3.html
    solarZenith = ((90.0 - (float(solarElevation)))*math.pi)/180 #Converted from degrees to radians
    solarDist = float(solarDist)
    ESUN = float(ESUN)
    radiance = Raster(radianceRaster)
    outname = outfolder + '//ReflectanceCustomFile.tif'
    
    arcpy.AddMessage('solarDist ='+str(solarDist))
    arcpy.AddMessage('solarDistSquared ='+str(math.pow(solarDist, 2)))
    arcpy.AddMessage('ESUN ='+str(ESUN))
    arcpy.AddMessage('solarZenith ='+str(solarZenith))

    outraster = (math.pi * radiance * math.pow(solarDist, 2)) / (ESUN * math.cos(solarZenith)) * scaleFactor
    outraster.save(outname)

    #outnull = SetNull(outraster, outraster, "Value > 0")
    #outnull.save('ReflectanceB'+str(band)+'null.tif')

    
    return outname

def getESUN(bandNum, SIType):
    SIType = SIType
    ESUN = {}
    #from NASA's Landsat7 User Handbook Table 11.3 http://landsathandbook.gsfc.nasa.gov/pdfs/Landsat7_Handbook.pdf
    #ETM+ Solar Spectral Irradiances(generated using the Thuillier solar spectrum)
    if SIType == 'ETM+ Thuillier':
        ESUN = {'b1':1997,'b2':1812,'b3':1533,'b4':1039,'b5':230.8,'b7':84.90,'b8':1362}

    #from NASA's Landsat7 User Handbook Table 11.3 http://landsathandbook.gsfc.nasa.gov/data_prod/prog_sect11_3.html
    #ETM+ Solar Spectral Irradiances (generated using the combined Chance-Kurucz Solar Spectrum within MODTRAN 5)
    if SIType == 'ETM+ ChKur':
        ESUN = {'b1':1970,'b2':1842,'b3':1547,'b4':1044,'b5':225.7,'b7':82.06,'b8':1369}

    #from NASA's Landsat7 User Handbook Table 9.1 http://landsathandbook.gsfc.nasa.gov/pdfs/Landsat7_Handbook.pdf
    #from the LPS ACCA algorith to correct for cloud cover
    if SIType == 'LPS ACAA Algorithm':
        ESUN = {'b1':1969,'b2':1840,'b3':1551,'b4':1044,'b5':225.7,'b7':82.06,'b8':1368}

    #from Revised Landsat-5 TM Radiometric Calibration Procedures and Postcalibration
    #Dynamic Ranges Gyanesh Chander and Brian Markham. Nov 2003. Table II. http://landsathandbook.gsfc.nasa.gov/pdfs/L5TMLUTIEEE2003.pdf
    #Landsat 4 ChKur
    if SIType == 'Landsat 5 ChKur':
        ESUN = {'b1':1957,'b2':1825,'b3':1557,'b4':1033,'b5':214.9,'b7':80.72}
    
    #from Revised Landsat-5 TM Radiometric Calibration Procedures and Postcalibration
    #Dynamic Ranges Gyanesh Chander and Brian Markham. Nov 2003. Table II. http://landsathandbook.gsfc.nasa.gov/pdfs/L5TMLUTIEEE2003.pdf
    #Landsat 4 ChKur
    if SIType == 'Landsat 4 ChKur':
        ESUN = {'b1':1957,'b2':1826,'b3':1554,'b4':1036,'b5':215,'b7':80.67} 

    bandNum = str(bandNum)
    
    return ESUN[bandNum]

#////////////////////////////////////MAIN LOOP///////////////////////////////////////

#Parameters from Arc

 
arcpy.env.overwriteOutput = True

BANDFILE = str(arcpy.GetParameterAsText(0))
outfolder = str(arcpy.GetParameterAsText(1))
LMAX = float(arcpy.GetParameterAsText(2))
LMIN = float(arcpy.GetParameterAsText(3))
QCALMAX = float(arcpy.GetParameterAsText(4))
QCALMIN =  float(arcpy.GetParameterAsText(5))

try:
    ESUNVAL = float(arcpy.GetParameterAsText(9))
except:
    ESUNVAL = 0

solarZenith = float(arcpy.GetParameterAsText(6))
solarDist = float(arcpy.GetParameterAsText(7))
scaleFactor = float(arcpy.GetParameterAsText(8))

bandNum = 'b' + str(arcpy.GetParameterAsText(11))
getSI = str(arcpy.GetParameterAsText(10))
SIType = str(arcpy.GetParameterAsText(12))



if getSI == 'true':
    ESUNVAL = getESUN(bandNum, SIType)
    

radianceRaster = calcRadiance(LMAX, LMIN, QCALMAX, QCALMIN, BANDFILE, outfolder)

reflectanceRaster = calcReflectance(solarDist, ESUNVAL, solarZenith, radianceRaster, scaleFactor, outfolder)

