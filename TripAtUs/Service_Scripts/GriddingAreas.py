# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 08:14:13 2020

@author: vidis
"""

from qgis.core import *
from qgis.PyQt.QtCore import QVariant

"""
Code to divide polygons into square-grid systems
--> In the eventuality that we were to use TSP to grid our search space

"""

def cut_polygon_into_windows(p, window_height, window_width):

    crs = p.crs().toWkt()
    extent = p.extent()
    (xmin, xmax, ymin, ymax) = (extent.xMinimum(), extent.xMaximum(), extent.yMinimum(), extent.yMaximum())

    # Create the grid layer
    vector_grid = QgsVectorLayer('Polygon?crs='+ crs, 'vector_grid' , 'memory')
    prov = vector_grid.dataProvider()

    # Create the grid layer
    output = QgsVectorLayer('Polygon?crs='+ crs, 'output' , 'memory')
    outprov = output.dataProvider()

    # Add ids and coordinates fields
    fields = QgsFields()
    fields.append(QgsField('ID', QVariant.Int, '', 10, 0))
    outprov.addAttributes(fields)

    # Generate the features for the vector grid
    id = 0
    y = ymax
    while y >= ymin:
        x = xmin
        while x <= xmax:
            point1 = QgsPoint(x, y)
            point2 = QgsPoint(x + window_width, y)
            point3 = QgsPoint(x + window_width, y - window_height)
            point4 = QgsPoint(x, y - window_height)
            vertices = [point1, point2, point3, point4] # Vertices of the polygon for the current id
            inAttr = [id]
            feat = QgsFeature()
            feat.setGeometry(QgsGeometry().fromPolygon([vertices])) # Set geometry for the current id
            feat.setAttributes(inAttr) # Set attributes for the current id
            prov.addFeatures([feat])
            x = x + window_width
            id += 1
        y = y - window_height

    index = QgsSpatialIndex() # Spatial index
    for ft in vector_grid.getFeatures():
        index.insertFeature(ft)

    for feat in p.getFeatures():
        geom = feat.geometry()
        idsList = index.intersects(geom.boundingBox())
        for gridfeat in vector_grid.getFeatures(QgsFeatureRequest().setFilterFids(idsList)):
            tmp_geom = QgsGeometry(gridfeat.geometry())
            tmp_attrs = gridfeat.attributes()
            if geom.intersects(tmp_geom):
                int = QgsGeometry(geom.intersection(tmp_geom))
                outfeat = QgsFeature()
                outfeat.setGeometry(int)
                outfeat.setAttributes(tmp_attrs)
                outprov.addFeatures([outfeat])

    output.updateFields()

    return output


## Load the layer
#p = QgsVectorLayer('C:/path_to_your_file/input.shp', 'display name', 'ogr')
#
## Set width and height as you want
#window_width = 300
#window_height = 300
#
## Run the function
#output = cut_polygon_into_windows(p, window_height, window_width)
#
## Add the layer to the Layers panel
#QgsMapLayerRegistry.instance().addMapLayers([output])

"""
This code also aims to divide a polygon shape into square grids

"""


import math
import numpy

def getArray(grid):
    n = numpy.zeros((grid[-1][0]+1, grid[-1][1]+1))
    for (y,x) in grid:
        n[y, x] = 1
    return n

# Determines if the new point is within the bounds
def getBoundingSquare(newCoord, npArr):
    try:
        if npArr[int(math.floor(newCoord[0])),int(math.floor(newCoord[1]))] == 1 and \
        npArr[int(math.floor(newCoord[0])),int(math.ceil(newCoord[1]))] == 1 and \
        npArr[int(math.ceil(newCoord[0])),int(math.floor(newCoord[1]))] == 1 and \
        npArr[int(math.ceil(newCoord[0])),int(math.ceil(newCoord[1]))] == 1:
            return 1
        else:
            return 0
    except IndexError:
        return 0

# Creates the new points using the desired side length
def interpolator(grid, side_length):
    startCorner = grid[0]
    endCorner = grid[-1]
    npArr = getArray(grid)
    newGrid = []
    if side_length < 1:
        exprY = int((endCorner[0]+1)*1//side_length-1)
        exprX = int((endCorner[1]+1)*1//side_length-1)
    else:
        exprY = int((endCorner[0]+1))
        exprX = int((endCorner[1]+1))
    for y in range(startCorner[0], exprY):
        for x in range(startCorner[1], exprX):
            newCoord = (y*side_length+startCorner[0], x*side_length+startCorner[1])
            newCoord2 = (float(y+startCorner[0]), float(x+startCorner[1]))
            if getBoundingSquare(newCoord, npArr):
                newGrid.append(newCoord)
            if getBoundingSquare(newCoord2, npArr) and newCoord2 not in newGrid:
                newGrid.append(newCoord2)
    newGrid.sort()
    return newGrid

def subdivide(grid, side_length):
    grid = interpolator(grid, float(side_length))
    subSquares = []
    while len(grid) >= 4:
        sy, sx = grid[0]
        if (sy+side_length, sx+side_length) in grid:
            square = []
            for y in range(2):
                for x in range(2):
                    if (sy+y*side_length, sx+x*side_length) in grid:
                        square.append((sy+y*side_length, sx+x*side_length))
                        if not(y == 1 or x == 1):
                            grid.remove((sy+y*side_length, sx+x*side_length))

            if square not in subSquares and (len(square) == (side_length+1)**2 or len(square) == 4):
                subSquares.append(square)
            (startY, startX) = square[0]
            (endY, endX) = square[-1]
            counter = 0
            while counter < len(grid):
                item = grid[counter]
                if (item[0] < endY and item[1] < endX):
                    grid.remove(item)
                else:
                    counter += 1
        else:
            grid.pop(0)
    allowed = 0
    for item in grid:
        for square in subSquares:
            if item in square:
                allowed += 1
                continue
    if len(grid) > allowed:
        print('Could not divide entire polygon')
    for square in subSquares:
        print(square)
    return subSquares


