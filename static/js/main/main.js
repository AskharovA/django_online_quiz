let navUser = document.querySelector('.user-nav');
let navHome = document.querySelector('.home-nav');

document.querySelector('.head-user-button').onclick = () => {
    navUser.style.display = 'block';
}
document.querySelector('.home-url-btn').onclick = () => {
    navHome.style.display = 'block';
}

document.addEventListener('click', function (e){
    if (!e.target.closest('.head-user-button') && navUser.style.display === 'block'){
    navUser.style.display = 'none';
    }
    if (!e.target.closest('.home-url-btn') && navHome.style.display === 'block'){
    navHome.style.display = 'none';
    }
    if (e.target.id === 'message-close-btn') {
        e.target.parentNode.parentNode.innerHTML = '';
}
})
