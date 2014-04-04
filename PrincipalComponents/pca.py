# -*- coding: utf-8 -*-
"""
/***************************************************************************
 pca
                                 A QGIS plugin
 Principal Component Analysis for rasters
                             -------------------
        begin                : 2013-04-29
        copyright            : (C) 2013 by Stavros Georgousis
        email                : grgeosteve@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import QFileInfo
from osgeo import gdal
from osgeo.gdalconst import *
import numpy
from qgis.core import QgsRasterLayer, QgsMapLayerRegistry

def pca(inputRasterFileName, outputRasterFileName, outPCBands):
    # Open the input raster file
    # register the gdal drivers
    gdal.AllRegister()

    # Open and assign the contents of the raster file to a dataset
    dataset = gdal.Open(inputRasterFileName, GA_ReadOnly)

    # Compute raster covariance matrix    
    bandMean = numpy.empty(dataset.RasterCount)
    for i in xrange(dataset.RasterCount):
        band = dataset.GetRasterBand(i+1).ReadAsArray(0, 0,
                                                      dataset.RasterXSize,
                                                      dataset.RasterYSize)
        bandMean[i] = numpy.amin(band, axis = None)

    covMatrix = numpy.empty((dataset.RasterCount, dataset.RasterCount))
    for i in xrange(dataset.RasterCount):
        band = dataset.GetRasterBand(i+1)
        bandArray = band.ReadAsArray(0, 0,
                                     dataset.RasterXSize,
                                     dataset.RasterYSize).astype(numpy.float).flatten()

        bandArray = bandArray - bandMean[i]
        covMatrix[i][i] = numpy.var(bandArray)

    band = None
    bandArray = None

    for i in xrange(1, dataset.RasterCount):
        band1 = dataset.GetRasterBand(i+1)
        bandArray1 = band1.ReadAsArray(0, 0,
                                       dataset.RasterXSize,
                                       dataset.RasterYSize).astype(numpy.float).flatten()
        bandArray1 = bandArray1 - bandMean[i]

        for j in xrange(i + 1, dataset.RasterCount):
            band2 = dataset.GetRasterBand(j+1)
            bandArray2 = band2.ReadAsArray(0, 0,
                                           dataset.RasterXSize,
                                           dataset.RasterYSize).astype(numpy.float).flatten()

            bandArray2 = bandArray2 - bandMean[j]

            covMatrix[i][j] = covMatrix[j][i] = numpy.cov(bandArray1, bandArray2)[0][1]

    # Calculate the eigenvalues and the eigenvectors of the covariance
    # matrix and calculate the principal components        
    eigenvals, eigenvectors = numpy.linalg.eig(covMatrix)

    # Just for testing
    print eigenvals
    print eigenvectors

    # Create a lookup table and sort it according to
    # the index of the eigenvalues table
    # In essence the following code sorts the eigenvals
    indexLookupTable = [i for i in xrange(dataset.RasterCount)]

    for i in xrange(dataset.RasterCount):
        for j in xrange(dataset.RasterCount - 1, i, -1):
            if eigenvals[indexLookupTable[j]] > eigenvals[indexLookupTable[j - 1]]:
                temp = indexLookupTable[j]
                indexLookupTable[j] = indexLookupTable[j - 1]
                indexLookupTable[j - 1] = temp

    # Calculate and save the resulting dataset
    driver = gdal.GetDriverByName("GTiff")
    outDataset = driver.Create(outputRasterFileName,
                               dataset.RasterXSize,
                               dataset.RasterYSize,
                               outPCBands,
                               gdal.GDT_Float32)

    for i in xrange(outPCBands):
        pc = 0
        for j in xrange(dataset.RasterCount):
            band = dataset.GetRasterBand(j + 1)
            bandAdjustArray = band.ReadAsArray(0, 0, dataset.RasterXSize,
                                               dataset.RasterYSize).astype(numpy.float) - bandMean[j]

            pc = pc + eigenvectors[j, indexLookupTable[i]] * bandAdjustArray

        pcband = outDataset.GetRasterBand(i + 1)
        pcband.WriteArray(pc)

    # Check if there is geotransformation or geoprojection
    # in the input raster and set them in the resulting dataset
    if dataset.GetGeoTransform() != None:
        outDataset.SetGeoTransform(dataset.GetGeoTransform())

    if dataset.GetProjection() != None:
        outDataset.SetProjection(dataset.GetProjection())


    # write the statistics of the PCA into a file
    # first organize the statistics into lists
    covBandPC = [['' for i in xrange(dataset.RasterCount + 1)] for j in xrange(dataset.RasterCount + 1)]
    covBandPC[0][0] = "Cov.Eigenvectors"
    for j in xrange(1, 1 + dataset.RasterCount):
        header = 'PC' + str(j)
        covBandPC[0][j] = header
    for i in xrange(1, 1 + dataset.RasterCount):
        vertical = "Band" + str(i)
        covBandPC[i][0] = vertical
    for i in xrange(1, 1 + dataset.RasterCount):
        for j in xrange(1, 1 + dataset.RasterCount):
            covBandPC[i][j] = "%.3f" % eigenvectors[i - 1, indexLookupTable[j - 1]]


    covEigenvalMat = [['' for i in xrange(dataset.RasterCount + 1)] for j in xrange(5)]
    covEigenvalMat[0][0] = "Bands"
    covEigenvalMat[1][0] = "Cov.Eigenvalues"
    covEigenvalMat[2][0] = "Sum of Eigenvalues"
    covEigenvalMat[3][0] = "Eigenvalues/Sum"
    covEigenvalMat[4][0] = "Percentages(%)"

    eigvalSum = 0.0
    sum = numpy.sum(eigenvals)
    for i in xrange(dataset.RasterCount):
        covEigenvalMat[0][i + 1] = "PC" + str(i + 1)
        covEigenvalMat[1][i + 1] = "%.3f" % eigenvals[indexLookupTable[i]]
        eigvalSum = eigvalSum + eigenvals[indexLookupTable[i]]
        covEigenvalMat[2][i + 1] = "%.3f" % eigvalSum
        covEigenvalMat[3][i + 1] = "%.3f" % (eigvalSum / sum)
        covEigenvalMat[4][i + 1] = "%.1f" % (eigvalSum / sum * 100.0)

    # Debug printout
    print covBandPC
    print covEigenvalMat

    statText = ""
    statFileName = outputRasterFileName.split('.')[0] + "_statistics.txt"
    statFile = open(statFileName, "w")
    for i in xrange(len(covBandPC)):
        for j in xrange(len(covBandPC[0])):
            statText = statText + covBandPC[i][j]
            if (j < len(covBandPC[0]) - 1):
                statText = statText + " "
        statText = statText + "\n"

    statText = statText + "\n"

    for i in xrange(len(covEigenvalMat)):
        for j in xrange(len(covEigenvalMat[0])):
            statText = statText + covEigenvalMat[i][j]
            if (j < len(covEigenvalMat[0]) - 1):
                statText = statText + " "
        statText = statText + "\n"

    statFile.write(statText)
    statFile.close()
    dataset = None
    outDataset = None

    # insert the output raster into QGIS interface
    outputRasterFileInfo = QFileInfo(outputRasterFileName)
    baseName = outputRasterFileInfo.baseName()
    rasterLayer = QgsRasterLayer(outputRasterFileName, baseName)
    if not rasterLayer.isValid():
        print "Layer failed to load"
    QgsMapLayerRegistry.instance().addMapLayer(rasterLayer)
