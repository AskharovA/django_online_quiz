const startTime = 5;
let time = +document.querySelector('#timer_duration').value - 2;
let text_time = +document.querySelector('#text_answer_timer_duration').value - 2
let interval;

let display = document.getElementById('time-display');
let timerBar = document.getElementById('timer-bar');



function startTimer(duration, display, timerBar) {
    let timer = duration, minutes, seconds;

    interval = setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        const fraction = (timer / duration) * 100;
        timerBar.style.width = fraction + '%';

        if (timer < 2) {
            timerBar.style.backgroundColor = 'orangered';
        }
        else if (timer < 5) {
            timerBar.style.backgroundColor = 'gold';
        }

        if (timer === 0) {
            let options = document.querySelectorAll(".game-option");
            for (let i=0; i<options.length; i++){
                options[i].classList.add("fade-down")
            }
        }

        if (--timer < -1) {
            clearInterval(interval);
            timerBar.style.width = '100%';
            timerBar.style.backgroundColor = 'orange';
            WS.send(JSON.stringify({
                'get-statistics': 'get-statistics',
            }))
        }
    }, 1000);
}
