let avatarId = document.querySelector('#avatarId');
let avatars = document.querySelector('.avatars');


document.addEventListener('click', function (e){
    if (e.target.classList.contains('choose-avatar-btn') && avatars.style.display !== 'flex'){
        avatars.style.display = 'flex';
    }
    else if (e.target.classList.contains('avatar-img')){
        avatarId.value = e.target.id;
        avatars.style.display = 'none';
    }
    else if (!e.target.classList.contains('avatar-img') &&
        !e.target.classList.contains('avatars') &&
        avatars.style.display === 'flex') {
        avatars.style.display = 'none';
    }
})
