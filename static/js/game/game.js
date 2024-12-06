let lobbyCode = document.querySelector("#game_code").value
let newInterval;
let newTimer;

// const WS = new WebSocket("wss://" + window.location.host + "/ws/game/" + lobbyCode + "/");
const WS = new WebSocket("http://" + window.location.host + "/ws/game/" + lobbyCode + "/");

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
        let newTimer2 = 1
        let newInterval2 = setInterval(function (){
            for (let i = 0; i < categories.length; i++) {
                categories[i].classList.add("category-fadeDown");
            }
        }, 1000)

    }
    if ('game-is-finished' in data) {
        document.querySelector('#finish-game').click();
    }

    if ('change_timer' in data) {
        clearInterval(interval);
        timerBar.style.width = '100%';
        timerBar.style.backgroundColor = 'orange';
        newTimer = 2
        newInterval = setInterval(function (){
            --newTimer;
            if (newTimer === 1) {
                let options = document.querySelectorAll(".game-option");
                for (let i=0; i<options.length; i++){
                    options[i].classList.add("fade-down")
                }
            }
            if (newTimer === 0) {
                clearInterval(newInterval);
                document.querySelector("#get-statistics").click();
            }
        }, 1000)
    }
    if ("correct_text_answer" in data) {
        document.getElementById(`answer-id-${data["correct_text_answer"]}`).click();
    }
}

let correct = document.querySelector('#correct');

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

document.addEventListener("click", function (event){
    if (event.target.classList.contains("game-option") || event.target.classList.contains("text-answer-button")){
            WS.send(JSON.stringify({
                "player_answered": "player_answered"
        }))
    }
    if (event.target.classList.contains("save-answer-btn")){
        WS.send(JSON.stringify({
            "correct_text_answer": event.target.id
        }))
    }
})

setVolume(0.25)