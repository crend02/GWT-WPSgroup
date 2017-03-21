from pywps.Process import WPSProcess

# do not show insecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# requests for http request, json to parse json
import requests
import json

# load different packages

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import geopandas as gpd
import fiona; fiona.supported_drivers
from scipy import ndimage
import matplotlib.pylab as pylab
import numpy as np
import os

# do not show insecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class Process(WPSProcess):

     buffer_size = 0
     bin_size = 10


     # init process
     def __init__(self):
         WPSProcess.__init__(
		self,
         	identifier="coordinates",  # the same as the file name
         	version="0.1",
         	title="Coordinates process",
         	storeSupported="false",
         	statusSupported="false",
         	abstract="Abstract of coordinates process",
         	grassLocation=False)
	 self.Answer = self.addLiteralOutput(identifier="density",
                                            title="Density plot AdvGeoWebTech")

     def execute(self):
        self.heatmap(smoothing=1.5)

     # function to add different suffix to filename
     def add_prefix(self, filename):
     # from time import localtime
          import time
          return "%s_%s" % (time.strftime("%Y%m%d-%H%M%S"), filename)



     # heatmap
     def getCoords(self):
        # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        # getting gps JSON
        r = requests.get("https://localhost:8443/api/1.0/GPS", verify = False)
        data = json.loads(r.content)
        # parsing JSON string to array
    	x = []
    	y = []

    	minLat = 90
    	minLon = 180
    	maxLat = -90
    	maxLon = -180

        isFirstTime = True        

    	index = 0
    	for row in data:
    	  lat = float(row["latitude"])
    	  lon = float(row["longitude"])

          x.append(lat)
          
          y.append(lon)


          if(isFirstTime):
            minLat = lat
            maxLat = lat
            minLon = lon
            maxLon = lon
            isFirstTime = False		
	  
    	  if lat < minLat:
                minLat = lat
          elif lat > maxLat:
                maxLat = lat

    	  if lon < minLon:
                minLon = lon
          elif lon > maxLon:
                maxLon = lon

    	minLat -= self.buffer_size
        maxLat += self.buffer_size
        minLon -= self.buffer_size
        maxLon += self.buffer_size

    	z = {}
    	z["x"] = x
    	z["y"] = y
    	z["minX"] = minLon
    	z["maxX"] = maxLon
    	z["minY"] = minLat
    	z["maxY"] = maxLat

        self.bbox = self.addBBoxOutput(identifier = "bbox",
                          title = "BBox")
        self.bbox.setValue([[minLat, minLon], [maxLat, maxLon]])

    	return z

     def heatmapShifting(self, heatmap):
        for j in range(0, len(heatmap)):
            histogram = heatmap[j]
            for i in range(0, len(histogram)):
    		histogram[i] = histogram[i] + 1

        return heatmap

     def heatmap(self, bins=(20,20), smoothing=1.3, cmap='jet'):
        def getx(pt):
            return pt.coords[0][0]

        def gety(pt):
            return pt.coords[0][1]

        z = self.getCoords()
        x = z["x"] #list(d.geometry.apply(getx))
        y = z["y"] #list(d.geometry.apply(gety))

        heatmap, xedges, yedges = np.histogram2d(y, x, bins=bins)
        extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]

        heatmap =  self.heatmapShifting(heatmap)

        logheatmap = np.log(heatmap)
        logheatmap[np.isneginf(logheatmap)] = 0
        logheatmap = ndimage.filters.gaussian_filter(logheatmap, smoothing, mode='nearest')

        fig = plt.imshow(logheatmap, cmap=cmap, extent=extent, alpha=0.3)
        plt.axis('off')
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        plt.gca().invert_yaxis()
        plt.savefig("/var/www/FrontEnd/images/"+ self.add_prefix("heatmap.png"), bbox_inches='tight', pad_inches = 0,  transparent=True)
        self.Answer.setValue("/var/www/FrontEnd/images/"+ self.add_prefix("heatmap.png"))
        posturl = "https://localhost:8443/api/1.0/timeslider/%s/[[%s, %s], [%s, %s]]" %(self.add_prefix("heatmap.png"), z["minX"], z["minY"], z["maxX"], z["maxY"])
        postreq = requests.post(posturl, verify = False)

