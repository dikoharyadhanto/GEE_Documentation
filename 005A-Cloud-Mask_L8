// --------------LANDSAT 8 ------------------------------------

// Membuat fungsi cloud mask
var maskL8 = function(image) { // var maskL8 berisi fungsi untuk melakukan masking pixel
  var qa = image.select('BQA'); //yang dimasking pixel2 yang beracuan di layer BQA
  var mask = qa.bitwiseAnd(1<<4).eq(0); // pixel2 tersebut memiliki kode 1 - 4 akan dibolong jadi 0 nilainya
  return image.updateMask(mask); //pixel2 yg bolong tersebut ditambal sama perekaman lain
}

//Menentukan ID Citra, waktu perekaman, fungsi cloud masking, fungsi reducer dan geomer 
var composite = ee.ImageCollection("LANDSAT/LC08/C01/T1_RT")
.filterDate('2020-01-01','2021-09-28')
.map(maskL8) //terapkan fungsi maskL8
.median() // fungsi reducer
.clip(geometry) //potong seluas area 'geometry'

//Menentukan Composite Band yang Digunakan
var RGBTrue = composite.select(['B4', 'B3', 'B2']);

//Menentukan range nilai band dan mode
var RGBparam = { min: 0, max: 20000,}; //kalo mode berwarna

//Visualisasi Citra
Map.addLayer(RGBTrue, RGBparam, 'Jawa_L8_True');
