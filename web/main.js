var filepath = ""
var infoArea = document.getElementById( 'file-upload-filename' );
// var input = document.getElementById( 'input' );

async function getfilepath() {
    // var data = document.getElementById("fileToUpload").value

    var dosya_path = await eel.btn_ResimyoluClick()();
        if (dosya_path) {
            console.log(dosya_path);
            eel.dummy(dosya_path)(function(ret){document.getElementById("file-upload-filename").innerHTML = "selected song: " + ret})
        }
        // document.getElementById("filename_display").value=dosya_path;
        filepath = dosya_path
        // infoArea.textContent = 'File name: ' + filepath;
        // document.getElementById("upload_text").value=dosya_path;
        // 
    return dosya_path
    // var data = document.getElementById("fileToUpload").files[0].name;
    // console.log(data)
    
}

async function generateBeatMap() {
  var difficulty = document.getElementById( 'difficulty' ).value
  if (filepath) {
    // var savePath = await eel.btn_SavePathClick()();
    document.getElementById("generate").innerHTML = '<i class="fa fa-spinner fa-spin"></i>  Loading';
    await eel.generate(filepath, difficulty)(function(ret){
      
    document.getElementById("generate").innerHTML = "Generate BeatMap";
    var pop_up_button = document.getElementById("pop_up_message");
    pop_up_button.click(); // this will trigger the click event
  })}
    
    


else{
  //TODO: wriet error message
}
}

// // input.addEventListener( 'change', showFileName );
// function showFileName( event ) {
  
//   // the change event gives us the input it occurred in 
//   // var filepath = event.srcElement;
  
// //   // the input has an array of files in the `files` property, each one has a name that you can use. We're just using the name here.
//   // var fileName = input.files[0].name;
  
//   // use fileName however fits your app best, i.e. add it into a div
//   // infoArea.textContent = 'File name: ' + fileName;
//   document.getElementById('file-upload-filename')[0].innerHTML = filepath;
//   // infoArea.setAttribute("value", filepath);

// }