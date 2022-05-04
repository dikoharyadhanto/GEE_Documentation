import ee 
from ee_plugin import Map 

# Plot a histogram of elevation in Colorado.

elevation = ee.Image('CGIAR/SRTM90_V4')
colorado = ee.Geometry.Rectangle({
  'coords': [-109.05, 37, -102.05, 41],
  'geodesic': False
})

# Generate the histogram data.  Use minBucketWidth for nice sized buckets.
histogram = ui.Chart.image.histogram({
  'image': elevation,
  'region': colorado,
  'scale': 200,
  'minBucketWidth': 300
})
histogram.setOptions({
  'title': 'Histogram of Elevation in Colorado (meters)'
})

print(histogram)

Map.addLayer(elevation.clip(colorado))
Map.setCenter(-107, 39, 6)
