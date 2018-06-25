$(function () {
    initTopSwiper();
    initMenuSwiper();
});

function initTopSwiper() {
    var mySwiper = new Swiper ('#topSwiper', {
    direction: 'horizontal',
    loop: true,
    autoplay: 2000,

    // 如果需要分页器
    pagination: '.swiper-pagination',
  })
}
function initMenuSwiper() {
    var mySwiper = new Swiper ('#swiperMenu', {
    slidesPerView: 3,
    paginationClickable: true,
    spaceBetween: 2,
    loop: false,
  })
}