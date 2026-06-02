console.log("MindSync AI Loaded Successfully");

let time = 25 * 60;

let timerRunning = false;

let countdown;

function startTimer(){

    if(timerRunning){
        return;
    }

    timerRunning = true;

    countdown = setInterval(() => {

        let minutes = Math.floor(time / 60);

        let seconds = time % 60;

        seconds = seconds < 10 ? "0" + seconds : seconds;

        document.getElementById("timer").innerText =
            `${minutes}:${seconds}`;

        time--;

        if(time < 0){

            clearInterval(countdown);

            alert("Focus Session Complete!");

            timerRunning = false;
        }

    }, 1000);
}


function resetTimer(){

    clearInterval(countdown);

    time = 25 * 60;

    timerRunning = false;

    document.getElementById("timer").innerText = "25:00";
}