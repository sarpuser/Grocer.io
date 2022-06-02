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
			}
			else if (response['create_user_success'] == -1){
				console.log('User with email already exists');
				document.getElementById('error').innerHTML = 'A user with that email already exists!';
			}
			else {
				console.log('User creation failed');
				document.getElementById('error').innerHTML = 'Could not create user. Please try again.';
			}
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
	let url = '/find/' + email;
	
	fetch(url)
		.then(response=>response.json())
		.then(function(response){
			if (response['user_found'] == 1) {
				window.open('/user/' + email, '_self');
			}
			else {
				document.getElementById('error').innerHTML = 'A user with that email could not be found. Please create an account.';
			};
	});
}

async function pair_button() {
	let email = document.getElementById('email').value;
	let url = '/pair/' + email;

	document.getElementById('pairing_status').innerHTML = 'Pairing process started. Please press the button on the hardware to complete the pairing.'

	await fetch(url);

	url = '/get_pairing_status'

	let interval = setInterval(function() {
		fetch(url)
			.then(response=>response.json())
			.then(function(response){
				if (response['pairing_status'] == 1) {
					document.getElementById('Pairing complete. You can now start using the barcode scanner!');
					clearInterval(interval);
				}
		});
	}, 1000);
}