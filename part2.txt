//Mencari dan Memfilter Citra Landsat 8 DKI Jakarta
var landsat8_dki = ee.ImageCollection('LANDSAT/LC08/C01/T1') 
.filterBounds(geometry)
.filterDate('2021-06-01', '2021-09-27');

//Menampilkan Hasil Pencarian
print(landsat8_dki);

//Menentukan ID Citra
var citra_dki = ee.Image('LANDSAT/LC08/C01/T1/LC08_122064_20210815')

//Menentukan Composite Band yang Digunakan
var RGBTrue = citra_dki.select(['B4', 'B3', 'B2']);
var singleB5 = citra_dki.select('B5');
var singleB3 = citra_dki.select('B3');
var singleB1 = citra_dki.select('B1');

//Menentukan range nilai band dan mode
var greyscale = {min: 0, max: 30000, palette: ['black', 'white']}; //Kalo mode grayscale
var RGBparam = { min: 0, max: 30000,}; //kalo mode berwarna

//Visualisasi Citra
Map.addLayer(RGBTrue, RGBparam, 'True_DKI');
Map.addLayer(singleB5, greyscale, 'band5_DKI');
Map.addLayer(singleB3, greyscale, 'band3_DKI');
Map.addLayer(singleB1, greyscale, 'band1_DKI');
