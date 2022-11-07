var x = document.getElementById("login_form");
var y = document.getElementById("signup_form");

x.hidden = true
y.hidden = true

function toggle_login() {

  if (x.hidden === true) {
    x.hidden = false;
    y.hidden = true;
  } else {
    x.hidden = true;
  }
}

function toggle_signup() {

  if (y.hidden === true) {
    y.hidden = false;
    x.hidden = true;
  } else {
    y.hidden = true;
  }
}