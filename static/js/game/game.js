let lobbyCode = document.querySelector("#game_code").value
const WS = new WebSocket("wss://" + window.location.host + "/ws/game/" + lobbyCode + "/");

WS.onopen = function (e) {
    console.log("Connected")
}

WS.onmessage = function (e) {
    let data = JSON.parse(e.data)
    if ("update-players" in data) {
        document.querySelector('#update-players').click();
    }
    if ('get-categories' in data) {
        document.querySelector('#get-categories').click();
    }
    if ('next-question' in data) {
        document.querySelector('#next-question').click();
    }
    if ('send-statistics' in data) {
        document.querySelector("#get-statistics").click();
    }
    if ('start-category' in data) {
        let categories = document.querySelectorAll('.game-category')
        for (let i = 0; i < categories.length; i++) {
            if (categories[i].classList.contains('choose-category')) {
                categories[i].classList.remove('choose-category')
            }
        }
        let categoryId = data['start-category'];
        let categoryBtn = document.getElementById(`category-${categoryId}`);
        categoryBtn.classList.add('choose-category');
        correct.play();
    }
    if ('game-is-finished' in data) {
        document.querySelector('#finish-game').click();
    }
}

let correct = document.querySelector('#correct');
correct.volume = 0.25;

let gameId = document.querySelector('#game_code').value;

let questionAudio;

function setVolume(value) {
    let audioElements = document.querySelectorAll('.audio-element');
    for (let i = 0; i < audioElements.length; i++) {
        audioElements[i].volume = value;
    }
}

let playCategoryInterval;
let readyTime = 50;
