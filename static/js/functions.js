function hide(){
    var x = document.getElementById("messages");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

function toggle(id){
    var x = document.getElementById(id);
    if (x.style.display === "none"){
        x.style.display = "block";
    }
    else {
        x.style.display = "none";
    }
}

function disable(){
    document.getElementById("auth_button").disabled = true;
}