//-----------Koreksi Radiometrik-------------------------

var single = ee.Image('LANDSAT/LC08/C01/T1/LC08_122064_20210815');

//variabel faktor pengali dan penambah dari reflektan
var ApB1 = single.get('REFLECTANCE_ADD_BAND_1');
var MpB1 = single.get('REFLECTANCE_MULT_BAND_1');

// karena nilai reflektan sama untuk setiap band, maka terapin ajah satu band
// beda kayak radiance yg nilai faktor pengali dan penambahnya beda-beda
print(ApB1);
print(MpB1);

//Kalkulasi nilai reflektan
var ref = single.multiply(0.000019999999494757503).add(-0.10000000149011612)

//Menentukan Composite Band yang Digunakan
var RGBTrue = ref.select(['B4', 'B3', 'B2']);

//Menentukan range nilai band dan mode
var RGBparam = { min: 0, max: 0.3,}; //karna sudah nilai reflektan, nilainya 0-1

Map.addLayer(RGBTrue, RGBparam, 'True_DKI');


//---------------Menggunakan Citra yang sudah dikalibrasi (TOA Reflectance)---------------------------------

// Membuat fungsi cloud mask
var maskL8 = function(image) { // var maskL8 berisi fungsi untuk melakukan masking pixel
  var qa = image.select('BQA'); //yang dimasking pixel2 yang beracuan di layer BQA
  var mask = qa.bitwiseAnd(1<<4).eq(0); // pixel2 tersebut memiliki kode 1 - 4 akan dibolong jadi 0 nilainya
  return image.updateMask(mask); //pixel2 yg bolong tersebut ditambal sama perekaman lain
}

//Menentukan ID Citra, waktu perekaman, fungsi cloud masking, fungsi reducer dan geomer 
var L8REF = ee.ImageCollection("LANDSAT/LC08/C01/T1_RT_TOA")
.filterDate('2020-01-01','2021-09-28')
.map(maskL8) //terapkan fungsi maskL8
.median() // fungsi reducer
.clip(geometry) //potong seluas area 'geometry'

//Menentukan Composite Band yang Digunakan
var RGBTrue = L8REF.select(['B4', 'B3', 'B2']);

//Menentukan range nilai band dan mode
var RGBparam = { min: 0, max: 0.3,}; //kalo mode berwarna

//Visualisasi Citra
Map.addLayer(RGBTrue, RGBparam, 'Jawa_L8_TOA_True');
