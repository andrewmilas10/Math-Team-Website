end = Number(end);

// this example takes 2 seconds to run
// var end = Date.now()+.5*60*1000;
if (end == "0" || end == "-1") {
    end = Date.now()+.2*60*1000;
}
console.log("starting timer...");
// expected output: starting timer...

 $.ajax({
        type: "POST",
        url: "/start_timer",
        data: {csrfmiddlewaretoken: token,
              end: ""+end,
              topic: topic},   /* Passing the text data */
});

function changeTimer() {
    var timer = document.getElementById("timer");
    var millis = end - Date.now();
    var seconds = Math.floor(millis/1000)%60;
    if (seconds < 10) {
        seconds = "0"+seconds
    }
    timer.innerText = "Time: "+Math.floor(millis/60000)+":"+seconds;
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

changeTimer();





