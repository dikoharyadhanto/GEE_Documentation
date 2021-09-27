var dataset = ee.ImageCollection('LANDSAT/LC08/C01/T1')
                  .filterBounds(jakarta)
                  .filterDate('2017-06-01', '2017-07-31');
print(dataset);

var single = ee.Image('LANDSAT/LC08/C01/T1/LC08_122064_20170617')
            
var RGBTrue = single.select(['B4', 'B3', 'B2']);

//memunculkan citra
var RGBparam = { min: 0, max: 30000,};
Map.addLayer(RGBTrue, RGBparam, 'TRUE');



