'use strict';


function voteOnLetter(change) {
  const params = {
    change: change
  }

  const http = new XMLHttpRequest()
  http.open('POST', '/')
  http.setRequestHeader('Content-type', 'application/json')
  http.send(JSON.stringify(params)) 
  http.onload = function() {
      location.reload()
  }
}


window.addEventListener('load', function () {

  $("#upvote-letter-button").click(function() {
    console.log("Upvoting today's letter")
    voteOnLetter("up")
  });

  $("#downvote-letter-button").click(function() {
    console.log("Downvoting today's letter")
    voteOnLetter("down")
  });
});