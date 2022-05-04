import ee 
from ee_plugin import Map 

# Generate day-of-year charts from Landsat 8 images.

city = ee.Feature(    # San Francisco.
    ee.Geometry.Rectangle(-122.42, 37.78, -122.4, 37.8),
    {'label': 'City'})
forest = ee.Feature(  # Tahoe National Forest.
    ee.Geometry.Rectangle(-121, 39.4, -120.99, 39.45),
    {'label': 'Forest'})
desert = ee.Feature(  # Black Rock Desert.
    ee.Geometry.Rectangle(-119.02, 40.95, -119, 41),
    {'label': 'Desert'})
westernRegions = ee.FeatureCollection([city, forest, desert])

landsat8Toa = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
    .filterBounds(westernRegions)
landsat8Toa = landsat8Toa.select('B[1-7]')

# Create a chart using a sequence of arguments.
bands = ui.Chart.image.doySeries(landsat8Toa, forest, None, 200)
print(bands)

# Create a chart using a dictionary of named arguments.
years = ui.Chart.image.doySeriesByYear({
  'imageCollection': landsat8Toa,
  'bandName': 'B1',
  'region': forest,
  'scale': 200
})
print(years)

regions = ui.Chart.image.doySeriesByRegion({
  'imageCollection': landsat8Toa,
  'bandName': 'B1',
  'regions': westernRegions,
  'scale': 500,
  'seriesProperty': 'label'
})
print(regions)

Map.addLayer(westernRegions)
Map.setCenter(-121, 39.4, 6)
