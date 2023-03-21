function openLoginForm(){
    document.getElementById("login_signup_form").style.display = "block";
}

function closeLoginForm(){
    document.getElementById("login_signup_form").style.display = "none";
}

function toggleProfileDropdown(){

    var x = document.getElementById("profile-dropdown");
    if (x.style.display == "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

function openWorkOptions(){
    var check_box = document.getElementById("options-check-box");
    var display_options = document.getElementById("work-options");

    if(check_box.checked == true){
        display_options.style.display = "block";
    }
    else{
        display_options.style.display = "none";
    }
}

function openLogin(){
    var display_signup = document.getElementsByClassName("form-signup");
    var signupl = display_signup.length;

    document.getElementById("login").style.backgroundColor="azure";
    document.getElementById("signup").style.backgroundColor="transparent";

    for (let i = 0; i < signupl; i++) {
        display_signup[i].style.display = "none";
    }
    document.getElementById("submit").textContent = "Login";
}

function openSignup(){
    var display_login = document.getElementsByClassName("form-signup");
    var loginl = display_login.length;

    document.getElementById("login").style.backgroundColor="transparent";
    document.getElementById("signup").style.backgroundColor="azure";

    for (let i = 0; i < loginl; i++) {
        display_login[i].style.display = "block";
    }
    document.getElementById("submit").textContent = "Sign up";
}


function toggleDeleteAccount(){

    var x = document.getElementById("delete-account");
    if (x.style.display == "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}















