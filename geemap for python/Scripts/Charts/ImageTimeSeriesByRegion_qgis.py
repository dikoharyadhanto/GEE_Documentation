import ee 
from ee_plugin import Map 

# Plot a time series of a band's value in regions of the American West.

COLOR = {
  'CITY': 'ff0000',
  'DESERT': '0000ff',
  'FOREST': '00ff00'
}

city = ee.Feature(    # San Francisco.
    ee.Geometry.Rectangle(-122.45, 37.74, -122.4, 37.8),
    {'label': 'City'})
forest = ee.Feature(  # Tahoe National Forest.
    ee.Geometry.Rectangle(-121, 39.4, -120.8, 39.8),
    {'label': 'Forest'})
desert = ee.Feature(  # Black Rock Desert.
    ee.Geometry.Rectangle(-119.15, 40.8, -119, 41),
    {'label': 'Desert'})
westernRegions = ee.FeatureCollection([city, forest, desert])

# Get brightness temperature data for 1 year.
landsat8Toa = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA')
temps2013 = landsat8Toa.filterBounds(westernRegions) \
    .filterDate('2015-12-25', '2016-12-25') \
    .select('B10')

# Convert temperature to Celsius.

def func_cjv(image):
  return image.addBands(image.subtract(273.15).select([0], ['Temp']))

temps2013 = temps2013.map(func_cjv)




tempTimeSeries = ui.Chart.image.seriesByRegion({
  'imageCollection': temps2013,
  'regions': westernRegions,
  'reducer': ee.Reducer.mean(),
  'band': 'Temp',
  'scale': 200,
  'xProperty': 'system:time_start',
  'seriesProperty': 'label'
})
tempTimeSeries.setChartType('ScatterChart')
tempTimeSeries.setOptions({
  'title': 'Temperature over time in regions of the American West',
  'vAxis': {
    'title': 'Temperature (Celsius)'
  },
  'lineWidth': 1,
  'pointSize': 4,
  'series': {
    '0': '{color': COLOR.CITY},
    '1': '{color': COLOR.FOREST},
    '2': '{color': COLOR.DESERT}
  }
})

print(tempTimeSeries)

Map.addLayer(desert, {'color': COLOR.DESERT})
Map.addLayer(forest, {'color': COLOR.FOREST})
Map.addLayer(city, {'color': COLOR.CITY})
Map.setCenter(-121, 39.4, 6)
