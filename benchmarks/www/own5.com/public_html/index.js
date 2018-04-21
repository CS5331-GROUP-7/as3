window.onload = function() {

	var receiver = document.getElementById('secondpage').contentWindow;

	var btn = document.getElementById('exploit');

	function sendMessage(e) {
		e.preventDefault();

		alert("Pressed");

		receiver.postMessage('Hi there!', 'own5secondpage.html');
	}

	btn.addEventListener('click', sendMessage);
}
