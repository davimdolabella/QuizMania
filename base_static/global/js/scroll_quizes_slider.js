$('.quizes').slick({
    centerMode: true,
    Infinity:true,
    lazyLoad: 'ondemand',
    centerPadding: '100px',
    slidesToShow: 5,
    speed: 250,
    
    responsive: [
      {
        breakpoint: 1170,
        settings: {
          
          centerMode: true,
          centerPadding: '40px',
          slidesToShow: 3
        }
      },
      {
        breakpoint: 550,
        settings: {
          speed:150,
          centerMode: true,
          centerPadding: '40px',
          slidesToShow: 1
        }
      }
    ]
  });