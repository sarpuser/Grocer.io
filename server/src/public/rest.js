function create_account() {
	let first_name = document.getElementById("fname").value;
	let last_name = document.getElementById("lname").value;
	let email = document.getElementById("email").value;
	let address = document.getElementById("address").value;
	let city = document.getElementById("city").value;
	let state = document.getElementById("state").value;
	let zipcode = document.getElementById("zipcode").value;	
	let order_day = document.getElementById("order_day").value;
	let order_method = document.getElementById("order_method").value;

	let url = "/adduser/" + first_name + "/" + last_name + "/" + email + "/" + address + "/" + city + "/" + state + "/" + zipcode + "/" + order_day + "/" + order_method

	fetch(url)
		.then(response=>response.json())
		.then(function(response){
			if (response['create_user_success'] == 1) {
				window.open('/user/' + response['email'], '_self');
			};
		});
}

function log_out() {
	window.open('/', '_self');
}

function view_cart() {
	let email = document.getElementById("email").value;
	url = "/cart/" + email;
	window.open(url, '_self');
}

function new_user() {
	window.open('/newuser', '_self');
}

function login_button() {
	let email = document.getElementById('email').value;
	let url = '/user/' + email;
	window.open(url, '_self');
}