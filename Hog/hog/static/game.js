var game = {};
game.turn = -1;
game.score0 = 0;
game.score1 = 0;
game.started = false;

//Get the name of the player
var name = prompt("What is your name?");

//Inital code to welcome and wait for the game to start.
function init() {
  ($('#waiting')[0]).innerHTML = "Welcome " + name + "!" + "<br>" +
    "Waiting for opponent";
  $.getJSON( "/join/"+name, {
      format: "json"
    })
      .done(function( data ) {
        //This starts the server polling
        updateValues(data);
        updateDOM();
        poll();
    });
}


function rollDice() {
  //Get the number they have in the box
  roll($('#diceNumber')[0].value);
}

function roll(number) {
  //If it's the correct players turn, roll the dice
  if (game.turn == game.id) {
    $.getJSON( "/play/"+game.game+"/"+game.id+"/"+number, {
        format: "json"
      })
  }
}


//Ask the server the status of the game
function poll() {
  game.interval = setTimeout(function () {
    $.getJSON( "/status/"+game.game, {
        format: "json"
      })
      .done(function( data ) {
        //Once we have the information from the server, update the values of our game and the DOM.
        updateValues(data);
        updateDOM();
        poll();
      });
  }, 500);
};



function updateValues(data) {
  for (var attrname in data) { game[attrname] = data[attrname]; }
  if(game.started == false && game.turn != -1){
    $("#waiting").hide();
    $("#gameContent").show()
  }
  if(game.score0 > 100) {
    $("#winner")[0].innerHTML = game.player0 + " has won!";
    $("#roll").prop("disabled", true);
    clearInterval(game.interval)
  }
  if(game.score1 > 100) {
    $("#winner")[0].innerHTML = game.player1 + " has won!";
    $("#roll").prop("disabled", true);
    clearInterval(game.interval)
  }
}

function updateDOM() {
   $('#score0')[0].innerHTML = game.score0;
   $('#score1')[0].innerHTML = game.score1;
   $('#player0')[0].innerHTML = game.player0;
   $('#player1')[0].innerHTML = game.player1;
   if(game.turn == 0) {
     $("#p1").css("background", "#88ff88");
     $("#p2").css("background", "#ffffff");
   } else if(game.turn == 1) {
     $("#p1").css("background", "#ffffff");
     $("#p2").css("background", "#88ff88");
   }
}
init();
