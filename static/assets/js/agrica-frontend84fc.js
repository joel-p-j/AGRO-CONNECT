;(function($) {
    'use strict';
    $(window).on( 'elementor/frontend/init', function() {


        //-------------------Banner-------------------//

        elementorFrontend.hooks.addAction('frontend/element_ready/agricabanner.default',function($scope) {

            const bannerFade = new Swiper(".banner-fade", {
                // Optional parameters
                direction: "horizontal",
                loop: true,
                autoplay: false,
                effect: "fade",
                fadeEffect: {
                    crossFade: true
                },

                // If we need pagination
                pagination: {
                    el: '.banner-pagination',
                    type: 'bullets',
                    clickable: true,
                },

                // Navigation arrows
                navigation: {
                    nextEl: ".swiper-button-next",
                    prevEl: ".swiper-button-prev"
                }

                // And if we need scrollbar
                /*scrollbar: {
                el: '.swiper-scrollbar',
              },*/
            });
        });

        //-------------------service-------------------//

        elementorFrontend.hooks.addAction('frontend/element_ready/agricaservices.default',function($scope) {

            const serviceOneCarousel = new Swiper(".service-style-two-carousel", {
                // Optional parameters
                loop: true,
                freeMode: true,
                grabCursor: true,
                slidesPerView: 1,
                spaceBetween: 30,
                autoplay: true,
                // Navigation arrows
                navigation: {
                    nextEl: ".swiper-button-next",
                    prevEl: ".swiper-button-prev"
                },
                breakpoints: {
                    768: {
                        slidesPerView: 2,
                    },
                    1400: {
                        slidesPerView: 3,
                        spaceBetween: 60,
                    }
                },
            });
        });

        //-------------------history-------------------//

        elementorFrontend.hooks.addAction('frontend/element_ready/agricahistory.default',function($scope) {

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
        });

        //-------------------brand-------------------//

        elementorFrontend.hooks.addAction('frontend/element_ready/agricabrand.default',function($scope) {

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
        });


        //-------------------product-------------------//

        elementorFrontend.hooks.addAction('frontend/element_ready/agricaproductscart.default',function($scope) {

            const proCatCarousel = new Swiper(".pro-cat-carousel", {
                // Optional parameters
                loop: true,
                slidesPerView: 1,
                spaceBetween: 30,
                autoplay: true,
                pagination: {
                    el: ".product-pagination",
                    clickable: true,
                },
                // Navigation arrows
                navigation: {
                    nextEl: ".product-button-next",
                    prevEl: ".product-button-prev"
                },
                breakpoints: {
                    768: {
                        slidesPerView: 2,
                    },
                    992: {
                        slidesPerView: 2,
                        spaceBetween: 55,
                    }
                },
            });
        });

        //-------------------galeery-------------------//

        elementorFrontend.hooks.addAction('frontend/element_ready/agricagalleryes.default',function($scope) {

            const galleryOne = new Swiper(".gallery-style-one-carousel", {
                // Optional parameters
                loop: true,
                freeMode: true,
                grabCursor: true,
                slidesPerView: 1,
                spaceBetween: 30,
                autoplay: false,
                pagination: {
                    el: ".swiper-pagination",
                    clickable: true,
                },
                breakpoints: {
                    991: {
                        slidesPerView: 2,
                    },
                    1400: {
                        slidesPerView: 3,
                    }
                },
            });
        });

        //-------------------galeery-------------------//

        elementorFrontend.hooks.addAction('frontend/element_ready/agricachoseus.default',function($scope) {

            function animateElements() {
                $('.progressbar').each(function() {
                    var elementPos = $(this).offset().top;
                    var topOfWindow = $(window).scrollTop();
                    var percent = $(this).find('.circle').attr('data-percent');
                    var animate = $(this).data('animate');
                    if (elementPos < topOfWindow + $(window).height() - 30 && !animate) {
                        $(this).data('animate', true);
                        $(this).find('.circle').circleProgress({
                            // startAngle: -Math.PI / 2,
                            value: percent / 100,
                            size: 130,
                            thickness: 3,
                            lineCap: 'round',
                            emptyFill: '#f1f1f1',
                            fill: {
                                gradient: ['#49a760', '#49a760']
                            }
                        }).on('circle-animation-progress', function(event, progress, stepValue) {
                            $(this).find('strong').text((stepValue * 100).toFixed(0) + "%");
                        }).stop();
                    }
                });

            }

            animateElements();
            $(window).scroll(animateElements);
            
        });

        //-------------------team-------------------//

        elementorFrontend.hooks.addAction('frontend/element_ready/agricateam.default',function($scope) {

            const teamCarousel = new Swiper(".team-style-one-carousel", {
                // Optional parameters
                loop: true,
                freeMode: true,
                grabCursor: true,
                slidesPerView: 1,
                spaceBetween: 30,
                autoplay: true,
                pagination: {
                    el: ".swiper-pagination",
                    clickable: true,
                },
                // Navigation arrows
                navigation: {
                    nextEl: ".swiper-button-next",
                    prevEl: ".swiper-button-prev"
                },
                breakpoints: {
                    768: {
                        slidesPerView: 2,
                    }
                },
            });
            
        });

        //-------------------team-------------------//

        elementorFrontend.hooks.addAction('frontend/element_ready/agricaproductsfilter.default',function($scope) {

            $('#gallery-masonary,#shop-masonary').imagesLoaded(function() {

                /* Filter menu */
                $('.mix-item-menu').on('click', 'button', function() {
                    var filterValue = $(this).attr('data-filter');
                    $grid.isotope({
                        filter: filterValue
                    });
                });

                /* filter menu active class  */
                $('.mix-item-menu button').on('click', function(event) {
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
            
        });

        //-------------------cta-------------------//

        elementorFrontend.hooks.addAction('frontend/element_ready/agricacta.default',function($scope) {

            const brandOneCarousel = new Swiper(".brand-style-one-carousel", {
                // Optional parameters
                loop: true,
                slidesPerView: 2,
                spaceBetween: 15,
                autoplay: true,
                breakpoints: {
                    768: {
                        slidesPerView: 3,
                        spaceBetween: 30,
                    },
                    992: {
                        slidesPerView: 3,
                        spaceBetween: 30,
                    }
                },
            });
            
        });

         elementorFrontend.hooks.addAction('frontend/element_ready/agricawhychoseus.default',function($scope) {

            function animateElements() {
                $('.progressbar').each(function() {
                    var elementPos = $(this).offset().top;
                    var topOfWindow = $(window).scrollTop();
                    var percent = $(this).find('.circle').attr('data-percent');
                    var animate = $(this).data('animate');
                    if (elementPos < topOfWindow + $(window).height() - 30 && !animate) {
                        $(this).data('animate', true);
                        $(this).find('.circle').circleProgress({
                            // startAngle: -Math.PI / 2,
                            value: percent / 100,
                            size: 130,
                            thickness: 3,
                            lineCap: 'round',
                            emptyFill: '#f1f1f1',
                            fill: {
                                gradient: ['#49a760', '#49a760']
                            }
                        }).on('circle-animation-progress', function(event, progress, stepValue) {
                            $(this).find('strong').text((stepValue * 100).toFixed(0) + "%");
                        }).stop();
                    }
                });

            }

            animateElements();
            $(window).scroll(animateElements);

        });

        //-------------------service-------------------//

        elementorFrontend.hooks.addAction('frontend/element_ready/agricatestimonials.default',function($scope) {

            const testimonialCarousel = new Swiper(".testimonial-carousel", {
                // Optional parameters
                direction: "horizontal",
                loop: true,
                autoplay: true,
                effect: "fade",
                fadeEffect: {
                    crossFade: true
                },

                // And if we need scrollbar
                /*scrollbar: {
                el: '.swiper-scrollbar',
              },*/
            });


            const testimonialTwoCarousel = new Swiper(".testimonial-style-two-carousel", {
                // Optional parameters
                direction: "horizontal",
                loop: true,
                autoplay: true,
                effect: "fade",
                fadeEffect: {
                    crossFade: true
                },
                pagination: {
                    el: ".swiper-pagination",
                    clickable: true,
                },

                // And if we need scrollbar
                /*scrollbar: {
                el: '.swiper-scrollbar',
              },*/
            });
        });

        
        

        
        

    });
}(jQuery));