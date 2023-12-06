document.getElementById('start-game-btn').onclick = () => {
    WS.send(JSON.stringify({
        "start-game": "'start-game'",
    }))
}

document.addEventListener('click', function (event) {
    if (event.target.classList.contains('get-category-btn')) {
        let send_data = JSON.stringify({
        'choose-category': event.target.id,
        'game-id': gameId,
    })
        WS.send(send_data);
    }
})

document.getElementById('start-category-btn').onclick = () => {
            WS.send(JSON.stringify({
            "start-category": "start-category",
    }))
}