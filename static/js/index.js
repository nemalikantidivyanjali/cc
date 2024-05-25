

let sisbroField = document.getElementById('brosisdiv');

function changeChose(){
    let chooseField = document.getElementById('choose');
    console.log(chooseField)
    if (chooseField.value == 'Yes'){
        sisbroField.hidden = false;
    } else {
        sisbroField.hidden = true;
    }
}