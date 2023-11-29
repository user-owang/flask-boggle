//guess feedback messages
const okMsg = "Great guess!";
const notBoard = "That word is not found on the current game board!";
const notWord = "That's not a word!";
const alreadyGuessed = "You already found that word!";

//Dom elements
const $found = $(".found ul");
const $good = $(".good");
const $bad = $(".bad");
const $form = $("#form");
const $timer = $("#timer");
const $text = $("#guess");
const $submit = $("#start");
const $score = $("#score");
const $numGuess = $("#numGuess");

//game trackers g is # of guesses
let g = 0;
let time = 60;
let score = 0;

class Timer {
  constructor(secs) {
    this.secs = secs;
    this.countdown = null;
  }
  start() {
    this.countdown = setInterval(this.tick, 1000);
  }
  tick() {
    if (time > 0) {
      $timer.empty();
      time -= 1;
      $timer.append(`${time} seconds`);
    }
  }
  cancel() {
    clearInterval(this.countdown);
    this.countdown = null;
  }
  endGame() {
    $text.val("");
    $text.prop("disabled", true);
    $submit.prop("disabled", true);
    this.cancel();
  }
}

const timer = new Timer(time);

//dom helper functions
function update(jqueryElement, val) {
  jqueryElement.clear();
  jqueryElement.append(val);
}
function hideMsgs() {
  $good.hide();
  $bad.hide();
}

//Submit handler with dom update support
async function submitHandler(evt) {
  evt.preventDefault();

  const guess = $("#guess").val();

  if (g === 0) {
    timer.start();
    setTimeout(timer.endGame, time * 1000);
  }
  hideMsgs();

  if ($found.is(":contains(guess)")) {
    update($bad, `<p>${alreadyGuessed}</p>`);
    $bad.show();
    return $("#guess").val("");
  }

  g += 1;
  update($numGuess, `${g} Guesses`);

  const resp = await axios({
    url: `/logic`,
    method: "GET",
    data: `${guess}`,
  });

  console.log("get sent");
  switch (resp.data.result) {
    case "ok":
      update($good, `<p>${okMsg}</p>`);
      $good.show();
      $found.append(`<li>${guess}</li>`);
      score += guess.length;
      update($score, `${score} Points`);
      $found.append(`<li>${guess}</li>`);
      return $("#guess").val("");
    case "not-on-board":
      update($bad, `<p>${notBoard}</p>`);
      $bad.show();
      return $("#guess").val("");
    case "not-word":
      update($bad, `<p>${notWord}</p>`);
      $bad.show();
      return $("#guess").val("");
  }
}

$("#form").on("submit", submitHandler);
