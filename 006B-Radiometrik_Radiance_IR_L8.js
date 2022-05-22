var dataset = ee.ImageCollection("LANDSAT/LC08/C01/T1_RT")
.filterBounds(geometry)
.filterDate('2021-01-01','2021-09-28')
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

var celcius_mean = celcius.mean().clip(geometry);
var suhu_param = {min: 25, max: 33, palette: ['blue','limegreen','yellow','darkorange','red']};

//Visualisasi Citra
Map.addLayer(celcius_mean, suhu_param, 'Rata-Rata Suhu Bulan Januari - September 2021 DKI Jakarta (LANDSAT 8)');
