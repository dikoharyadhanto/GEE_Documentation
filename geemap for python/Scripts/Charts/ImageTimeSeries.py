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
# Plot Landsat 8 band value means in a section of San Francisco and
# demonstrate interactive charts.

sanFrancisco =
    ee.Geometry.Rectangle(-122.45, 37.74, -122.4, 37.8)

landsat8Toa = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
    .filterDate('2015-12-25', '2016-12-25') \
    .select('B[1-7]')

# Create an image time series chart.
chart = ui.Chart.image.series({
  'imageCollection': landsat8Toa,
  'region': sanFrancisco,
  'reducer': ee.Reducer.mean(),
  'scale': 200
})

# Add the chart to the map.
chart.style().set({
  'position': 'bottom-right',
  'width': '500px',
  'height': '300px'
})
Map.add(chart)

# Outline and center San Francisco on the map.
sfLayer = ui.Map.Layer(sanFrancisco, {'color': 'FF0000'}, 'SF')
Map.layers().add(sfLayer)
Map.setCenter(-122.47, 37.7, 9)

# Create a label on the map.
label = ui.Label('Click a point on the chart to show the image for that date.')
Map.add(label)

# When the chart is clicked, update the map and label.
chart.onClick(function(xValue, yValue, seriesName) {
  if (!xValue) return;  # Selection was cleared.

  # Show the image for the clicked date.
  equalDate = ee.Filter.equals('system:time_start', xValue)
  image = ee.Image(landsat8Toa.filter(equalDate).first())
  l8Layer = ui.Map.Layer(image, {
    'gamma': 1.3,
    'min': 0,
    'max': 0.3,
    'bands': ['B4', 'B3', 'B2']
  })
  Map.layers().reset([l8Layer, sfLayer])

  # Show a label with the date on the map.
  label.setValue((new Date(xValue)).toUTCString())
})


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl()  # This line is not needed for ipyleaflet-based Map.
Map
