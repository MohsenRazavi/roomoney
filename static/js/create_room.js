var x = document.getElementById("create_room_btn");
var y = document.getElementById("create_room_form");
var z = document.getElementById("title");

y.hidden = true

function toggle() {
  x.hidden = true
  y.hidden = false
  z.innerHTML = "Creating new room"
}