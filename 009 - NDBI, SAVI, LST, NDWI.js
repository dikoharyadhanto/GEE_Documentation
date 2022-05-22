var S2A = ee.ImageCollection("COPERNICUS/S2_SR")
.filterDate('2021-01-01', '2022-04-30')
.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 90))
.map(maskS2clouds)
.median()
.clip(KBB);

function maskS2clouds(image) {
  var qa = image.select('QA60');
  var cloudBitMask = 1<<10;
  var cirrusBitMask = 1<<11;
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
  .and(qa.bitwiseAnd(cirrusBitMask).eq(0));
  return image.updateMask(mask).divide(1);
}

//Sentinel RGB
var RGBTrue = S2A.select(['B4','B3','B2']);
var RGBParam = {min:0, max:3000,};
Map.addLayer(RGBTrue, RGBParam, 'Sentinel RGB 432');

//variable
var nir = S2A.select('B8');
var swir = S2A.select('B11');
var red = S2A.select('B4');
var green = S2A.select('B3');
var a = 1.428;
var b = 1;

//NDBI
var ndbi = swir.subtract(nir).divide(swir.add(nir)).rename('NDBI S2A');

var NDBIParam = {min:-1, max:1, palette:['white','orange','red']};
Map.addLayer(ndbi, NDBIParam, 'NDBI KBB 2021');

//SAVI
var savi = nir.subtract(red).multiply(a).divide(nir.add(red).add(b));

var SAVIParam = {min:-1, max:1, palette:['white','yellow','green']};
Map.addLayer(savi, SAVIParam, 'SAVI KBB 2021');

//NDWI
var ndwi = green.subtract(nir).divide(green.add(nir));

var NDWIParam = {min:-1, max:1, palette:['white','#91bfff','#255fdb']};
Map.addLayer(ndwi, NDWIParam, 'NDWI KBB 2021');

//LST
var dataset = ee.ImageCollection("LANDSAT/LC08/C01/T1_RT")
.filterBounds(KBB)
.filterDate('2021-01-01','2022-04-30')
.filter(ee.Filter.lt('CLOUD_COVER', 10))
.select('B10');

//karena kita akan mendapatkan kumpulan scene, maka dengan fungsi ini kita hanya memilih salah satu scene
var first = dataset.first(); 

//mendapatkan nilai faktor radiance dan nilai ketetapan K
var A = first.get('RADIANCE_ADD_BAND_10'); //Nilai faktor penambah radiance
var B = first.get('RADIANCE_MULT_BAND_10'); //Nilai faktor pengali radiance
var K1 = first.get('K1_CONSTANT_BAND_10'); //nilai tetapan K1 untuk konversi ke Kelvin
var K2 = first.get('K2_CONSTANT_BAND_10'); //nilai tetapan K2 untuk konversi ke Kelvin

print('A =', A)
print('B =', B)
print('K1 = ', K1)
print('K2 = ', K2)

//Konversi ke Celcius
var celcius = dataset.map(function(img){
  var id = img.id();
  return img.expression('((1321.08/(log(774.89/((TIR*0.0003342)+0.1)+1)))-272.15)', {'TIR' : img})
  .rename('B10')
  .copyProperties(img, ['system:time_start']);
});

var celcius_mean = celcius.mean().clip(KBB);
var suhu_param = {min: 25, max: 33, palette: ['white','yellow','orange','darkorange','red']};

//Visualisasi Citra
Map.addLayer(celcius_mean, suhu_param, 'Thermal KBB 2021');

//Export to Drive
Export.image.toDrive({
  image: celcius_mean,
  description: 'thermal_KBB',
  scale: 30,
  maxPixels: 600000000,
  region: KBB
});
