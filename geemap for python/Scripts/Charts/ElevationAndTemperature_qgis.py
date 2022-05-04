import ee 
from ee_plugin import Map 

# Plot elevation and seasonal temperatures along SF-Reno transect.

reno = [-119.821944, 39.527222]
sf = [-122.416667, 37.783333]
transect = ee.Geometry.LineString([reno, sf])

# Get brightness temperature data for 1 year.
landsat8Toa = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA')
temperature = landsat8Toa.filterBounds(transect) \
    .select(['B10'], ['temp'])

def func_hhg(image):
      # Kelvin to Celsius.
      return image.subtract(273.15) \
          .set('system:time_start', image.get('system:time_start')) \
    .map(func_hhg)






# Calculate bands for seasonal temperatures and elevations; composite into
# a single image.
summer = temperature.filterDate('2014-06-21', '2014-09-23') \
    .reduce(ee.Reducer.mean()) \
    .select([0], ['summer'])
winter = temperature.filterDate('2013-12-21', '2014-03-20') \
    .reduce(ee.Reducer.mean()) \
    .select([0], ['winter'])
elevation = ee.Image('USGS/NED');  # Extract the elevation profile.
startingPoint = ee.FeatureCollection(ee.Geometry.Point(sf))
distance = startingPoint.distance(500000)
image = distance.addBands(elevation).addBands(winter).addBands(summer)

# Extract band values along the transect line.
array = image.reduceRegion(ee.Reducer.toList(), transect, 1000) \
                 .toArray(image.bandNames())

# Sort points along the transect by their distance from the starting point.
distances = array.slice(0, 0, 1)
array = array.sort(distances)

# Create arrays for charting.
elevationAndTemp = array.slice(0, 1);  # For the Y axis.
# Project distance slice to create a 1-D array for x-axis values.
distance = array.slice(0, 0, 1).project([1])

# Generate and style the chart.
chart = ui.Chart.array.values(elevationAndTemp, 1, distance) \
    .setChartType('LineChart') \
    .setSeriesNames(['Elevation', 'Winter 2014', 'Summer 2014']) \
    .setOptions({
      'title': 'Elevation and temperatures along SF-to-Reno transect',
      'vAxes': {
        '0': {
          'title': 'Average seasonal temperature (Celsius)'
        },
        '1': {
          'title': 'Elevation (meters)',
          'baselineColor': 'transparent'
        }
      },
      'hAxis': {
        'title': 'Distance from SF (m)'
      },
      'interpolateNulls': True,
      'pointSize': 0,
      'lineWidth': 1,
      # Our chart has two Y axes: one for temperature and one for elevation.
      # The Visualization API allows us to assign each series to a specific
      # Y axis, which we do here:
      'series': {
        '0': '{targetAxisIndex': 1},
        '1': '{targetAxisIndex': 0},
        '2': '{targetAxisIndex': 0}
      }
    })

print(chart)
Map.setCenter(-121, 38.5, 7)
Map.addLayer(elevation, {'min': 4000, 'max': 0})
Map.addLayer(transect, {'color': 'FF0000'})
