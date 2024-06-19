// $(".sidebar ul li").on("click", function () {
//     $(".sidebar ul li.active").removeClass("active");
//     $(this).addClass("active");
// });
  
// $(".open-btn").on("click", function () {
//     $(".sidebar").addClass("active");
// });
  
// $(".close-btn").on("click", function () {
//     $(".sidebar").removeClass("active");
// });  

// const toggler = document.querySelector(".btn");
// toggler.addEventListener("click",function(){
//     document.querySelector("#sidebar").classList.toggle("collapsed");
// });

// $("#menu-btn").on("click", function () {
//     $("#sidebar").toggleClass("active-nav");
//     $(".my-container").toggleClass("active-cont");
// });

// document.getElementById('menu-btn').addEventListener('click', function() {
//     console.log("ky");
//     var nav = document.getElementById('sidebar');
//     var btn = document.getElementById('menu-btn');
//     if (nav.style.marginLeft === '0px') {
//         nav.style.marginLeft = '-300px';
//         btn.style.marginLeft = '0px';
//         btn.innerHTML = '>';
//     } else {
//         nav.style.marginLeft = '0px';
//         btn.style.marginLeft = '250px';
//         btn.style.zIndex = 0;
//         btn.innerHTML = '<';
//     }
// });

const sidebarToggle = document.querySelector("#sidebar-toggle");
const sidebar = document.querySelector("#sidebar");
const mainContent = document.querySelector("#main-content");

sidebarToggle.addEventListener("click", function () {
    sidebar.classList.toggle("collapsed");
    mainContent.classList.toggle("collapsed");
});