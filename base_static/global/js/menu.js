const menu = document.getElementById('menu');
const menu_content = document.querySelector('.menu-content');
menu.addEventListener('click', (e) => {
    e.stopPropagation();
    menu_content.classList.toggle('none');
});

window.addEventListener('click', (e) => {
    if (!menu.contains(e.target) && !menu_content.contains(e.target)) {
        menu_content.classList.add('none');
    }
});
