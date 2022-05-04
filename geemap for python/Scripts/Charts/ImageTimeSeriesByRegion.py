# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/geemap/tree/master/examples/template/template.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/geemap/blob/master/examples/template/template.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/geemap/blob/master/examples/template/template.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
</table>
"""

# %%
"""
## Install Earth Engine API and geemap
Install the [Earth Engine Python API](https://developers.google.com/earth-engine/python_install) and [geemap](https://geemap.org). The **geemap** Python package is built upon the [ipyleaflet](https://github.com/jupyter-widgets/ipyleaflet) and [folium](https://github.com/python-visualization/folium) packages and implements several methods for interacting with Earth Engine data layers, such as `Map.addLayer()`, `Map.setCenter()`, and `Map.centerObject()`.
The following script checks if the geemap package has been installed. If not, it will install geemap, which automatically installs its [dependencies](https://github.com/giswqs/geemap#dependencies), including earthengine-api, folium, and ipyleaflet.
"""

# %%
# Installs geemap package
import subprocess

try:
    import geemap
except ImportError:
    print("Installing geemap ...")
    subprocess.check_call(["python", "-m", "pip", "install", "geemap"])

# %%
import ee
import geemap

# %%
"""
## Create an interactive map 
The default basemap is `Google Maps`. [Additional basemaps](https://github.com/giswqs/geemap/blob/master/geemap/basemaps.py) can be added using the `Map.add_basemap()` function. 
"""

# %%
Map = geemap.Map(center=[40, -100], zoom=4)
Map

# %%
"""
## Add Earth Engine Python script 
"""

# %%
# Add Earth Engine dataset
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


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl()  # This line is not needed for ipyleaflet-based Map.
Map
