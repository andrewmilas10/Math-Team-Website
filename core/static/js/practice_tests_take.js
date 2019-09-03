end = Number(end);

// this example takes 2 seconds to run
// var end = Date.now()+.5*60*1000;
console.log(end);
if (end == 0 || end == -1) {
    var isRestarting = true;
    end = Date.now()+30*60*1000;
}

console.log("starting timer...");
// expected output: starting timer...

function changeTimer() {
    var timer = document.getElementById("timer");
    var millis = end - Date.now();
    var seconds = Math.floor(millis/1000)%60;
    if (seconds < 10) {
        seconds = "0"+seconds
    }
    if (millis <= 1000) {
        timer.innerText = "Time: 0:00";
    } else {
        timer.innerText = "Time: "+Math.floor(millis/60000)+":"+seconds;
    }
    console.log("seconds left = " + Math.floor(millis/1000));
    if (millis <= 1000) {
        var answers = [];
        for (var i=1; i<=5; i++) {
            answers.push(document.getElementById("answer"+i).value);
            document.getElementById("answer"+i).disabled = true;
        }
        document.getElementById("submit").disabled = true;
        $.ajax({
            type: "POST",
            url: "/end_timer",
            data: {csrfmiddlewaretoken: token,
                answers: ""+answers,
                topic: topic},   /* Passing the text data */
            success : function(data) {
                // $("html").html( data );
                $("#score").text(data)
            }
        });
        document.getElementById("endTime").style.visibility = "visible";

    } else {
        setTimeout(changeTimer, 1000);
    }
}

if (! Number(viewSolutions)) {
     $.ajax({
        type: "POST",
        url: "/start_timer",
        data: {csrfmiddlewaretoken: token,
              end: ""+end,
              topic: topic},   /* Passing the text data */
    });

    var counter = 1;
    while (document.getElementById("answer"+counter)) {
        // if (currAnswers[counter-1])
        if (!isRestarting && currAnswers.split("'")[2*counter-1].replace(" ", "") != "''" ) {
            console.log(currAnswers);
            document.getElementById("answer"+counter).value = currAnswers.split("'")[2*counter-1].replace(/'/g, "");
        }

        $("#answer"+counter).on('input', function(){
            var id = this.id.substring(6);
            $.ajax({
                type: "POST",
                url: "/edit_answers",
                data: {csrfmiddlewaretoken: token,
                      answer: this.value,
                      id: id,
                      topic: topic},   /* Passing the text data */
            });

        });
        counter++;
    }

    changeTimer();
} else {
    var counter = 1;
    while (document.getElementById("solutionBtn"+counter)) {
            console.log(currAnswers.split("'")[2*counter-1]);
        if (currAnswers.split("'")[2*counter-1].replace(" ", "") != "''" ) {
            document.getElementById("answer"+counter).value = currAnswers.split("'")[2*counter-1].replace(/'/g, "");
        }
        document.getElementById("answer"+counter).disabled = true;
        if (Number(distribution.split(",")[counter-1])) {
            var pic = document.getElementById("correct"+counter);
            pic.src = pic.src.replace("incorrect.png", "correct.png");
            pic.style.width = "40px";
        }
        $("#solutionBtn"+counter).click(function(){
            var id = this.id.substring(11);
            console.log(id);
            this.style.display = "none";
            document.getElementById("solution"+id).style.display = "block";

        });
        counter++;
    }
}

