const startTime = 5; // время в минутах
let time = +document.querySelector('#timer_duration').value - 2;
let text_time = +document.querySelector('#text_answer_timer_duration').value - 2
let interval;

let display = document.getElementById('time-display');
let timerBar = document.getElementById('timer-bar');
// timerBar.style.width = '100%';

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
