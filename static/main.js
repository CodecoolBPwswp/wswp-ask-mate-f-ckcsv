//Handle registration/login form
const username = document.querySelector("#username");
const password = document.querySelector("#password");
const button = document.querySelector("#user_input");
const form_length = document.querySelectorAll("form")[1].getElementsByTagName("input").length;
let valid_inputs = [];

username.addEventListener("keyup", checkFields);
password.addEventListener("keyup", checkFields);

function checkFields(e) {
	let id = "#"+e.target.getAttribute("id");

	if(document.querySelector(id).value.length > 5 && !valid_inputs.includes(e.target.getAttribute("id"))){
		valid_inputs.push(e.target.getAttribute("id"));
	} else if(document.querySelector(id).value.length < 6 && valid_inputs.includes(e.target.getAttribute("id"))) {
		let index = valid_inputs.indexOf(e.target.getAttribute("id"));
		if (index >= 0) {
		  valid_inputs.splice( index, 1 );
		}

	}

	if(valid_inputs.length == form_length) {
		button.disabled = false;
	} else {
		button.disabled = true;
	}

}
