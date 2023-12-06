document.querySelector('.delete-quiz-btn').addEventListener('click', function (event){
    const deleteConfirm = confirm('Вы уверены, что хотите удалить викторину?');

    if (!deleteConfirm){
        event.preventDefault();
    }
})