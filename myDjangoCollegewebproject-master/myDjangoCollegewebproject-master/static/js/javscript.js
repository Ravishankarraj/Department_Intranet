const navSlide = () => {
	const burger = document.querySelector('.burger');
	const nav = document.querySelector('.nav-links');
	const navLinks = document.querySelectorAll('.nav-links li');
	console.log("Javascript");

	burger.addEventListener('click',() =>{

		nav.classList.toggle('nav-active');
		
		// animation links

		navLinks.forEach((link, index) =>{

			if(link.style.animation){
				link.style.animation = ``;

			}
			else{
				link.style.animation = `navLinkFade 0.5s ease forwards ${ index / 7 + 0.5}s`
				
			}
		});

		// Burger animation

		burger.classList.toggle('toggle');

	});

	
}

// Drop down navigation bar

function dropList() {
  document.getElementById("myDropdown").classList.toggle("show");
}
window.onclick = function(e) {
  if (!e.target.matches('.dropbtn')) {
  let myDropdown = document.getElementById("myDropdown");
    if (myDropdown.classList.contains('show')) {
      myDropdown.classList.remove('show');
    }
  }
}

navSlide();