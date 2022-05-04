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
# Plot min to max temperature disparity in US states.

# Import US state boundaries.
states = ee.FeatureCollection('TIGER/2018/States')

# Import temperature normals and calculate annual mean of monthly min and max.
normClim = ee.ImageCollection('OREGONSTATE/PRISM/Norm81m') \
  .select(['tmin', 'tmax']) \
  .mean()

# Calculate mean max and min temperature per state.
states = normClim.reduceRegions({
  'collection': states,
  'reducer': ee.Reducer.mean(),
  'scale': 5e4}) \
  .filter(ee.Filter.NotNull(['tmax', 'tmin']))

# Calculate max to min temperature difference per state and set as a property.

def func_ifr(state):
  dif = state.getNumber('tmax').subtract(state.getNumber('tmin'))
  return state.set('tdif', dif)

states = states.map(func_ifr) \
.filter(ee.Filter.NotNull(['tdif']))

# Get states with the greatest mean max and min temperature disparity.
greatestDif = states.limit(6, 'tdif', False)

# Define color properties for chart series.
color = {
  'high': 'ff0000',
  'low': '0000ff'
}

# Prepare the chart.
greatestDifChart =
  ui.Chart.feature.byFeature(greatestDif, 'NAME', ['tmax', 'tmin']) \
    .setChartType('LineChart') \
    .setOptions({
      'title': 'States with Greatest Temperature Disparity',
      'vAxis': {
        'title': 'Temperature (Celsius)'
      },
      'lineWidth': 1,
      'pointSize': 4,
      'series': {
        '0': '{color': color.high},
        '1': '{color': color.low}
      }
    })



# The Chart.feature helper functions plot property values in different ways.
# Chart.feature.byFeatures() allows us to plot *features* on the x-axis, with
# a separate series for each *property*. Chart.feature.byProperties() puts
# *properties* on the x-axis, with a separate series for each *feature*.
# Chart.feature.groups() gives us a little more flexibility. It lets us specify
# a custom xProperty and a custom seriesProperty. The *values* of these
# properties determine the x-axis and series values for each feature. In this
# case, to plot min and max temps in by disparity, we need a separate feature
# for each low and each high. On the chart the X values are difference and the
# series names indicates low and high temperature.

# Define a function to set a temp and series property.
def individualTemps(label):

def func_sgc(feature):
    return feature.set({
      'temp': feature.get(label),
      'series': label
    })

  return states.map(func_sgc)








# Make min and max collections using and merge them.
highs = individualTemps('tmax')
lows = individualTemps('tmin')
tempsByDif = highs.merge(lows)

# Prepare the chart.
tempsByDifChart =
  ui.Chart.feature.groups(tempsByDif, 'tdif', 'temp', 'series') \
    .setChartType('ScatterChart') \
    .setOptions({
      'title': 'Mean Temperature Disparity US States',
      'hAxis': {
        'title': 'Temperature disparity'
      },
      'vAxis': {
        'title': 'Temperature (Celsius)'
      },
      'pointSize': 4,
      'series': {
        '0': '{color': color.high},
        '1': '{color': color.low}
      }
    })

print(greatestDifChart)
print(tempsByDifChart)


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl()  # This line is not needed for ipyleaflet-based Map.
Map
