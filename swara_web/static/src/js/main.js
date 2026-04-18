  $(".slick-slider").slick({
   slidesToShow: 3,
   infinite:false,
   slidesToScroll: 1,
   autoplay: true,
   autoplaySpeed: 2000,
    dots: false, 
    arrows: false,
     responsive: [
        {
          breakpoint: 975,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1,
            dots: true,
          },
        },
      ],
  });


$(".mini img").click(function(){  
  $(".maxi").attr("src",$(this).attr("src").replace());
});
$(".mini-mobile img").click(function(){  
  $(".maxi").attr("src",$(this).attr("src").replace());
});

var magnifying_area =  document.getElementById("magnifying_area");
var magnifying_img =  document.getElementById("magnifying_img");

if (magnifying_area && magnifying_img) {
magnifying_area.addEventListener("mousemove",function(event){
	clientX = event.clientX - magnifying_area.offsetLeft
	clientY = event.clientY - magnifying_area.offsetTop

	var mWidth = magnifying_area.offsetWidth
	var mHeight = magnifying_area.offsetHeight
	clientX = clientX / mWidth * 50
	clientY = clientY / mHeight * 50

	//magnifying_img.style.transform = 'translate(-50%,-50%) scale(2)'
	magnifying_img.style.transform = 'translate(-'+clientX+'%, -'+clientY+'%) scale(2)'
})

magnifying_area.addEventListener("mouseleave",function(){
	magnifying_img.style.transform = 'translate(-50%,-50%) scale(1)'
})

}
$('.mini-mobile').slick({
  infinite: true,
  slidesToShow: 3, // Shows a three slides at a time
  slidesToScroll: 1, // When you click an arrow, it scrolls 1 slide at a time
  arrows: true, // Adds arrows to sides of slider
});
