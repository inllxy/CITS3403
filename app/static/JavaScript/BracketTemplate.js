// Old code for bracket generation - maintained for reference and future use of template with Bracket.html

// 1. Define player matchups for each side and each round
const players = {
    winner: {
      round1: [['A','B'], ['C','D'], ['E','F'], ['G','H']],
      round2: [['A','C'], ['E','G']],
      round3: [['A','E']],
      round4: [['A','I']],
      // Add more rounds here if needed, e.g. round5: [['X','Y'], ['Z','W']],
    },
    loser: {
      round1: [['I','J'], ['K','L'], ['M','N'], ['O','P']],
      round2: [['I','B'], ['K','D'], ['M','F'], ['O','H']],
      round3: [['I','K'], ['M','O']],
      round4: [['I','C'], ['M','E']],
      round5: [['I','M']],
      round6: [['I','E']],
      // Add more rounds for the loser bracket as desired
    },
};
  
// 2. Define the corresponding scores for each matchup
const scores = {
    winner: {
      round1: [[3,2], [1,4], [5,0], [2,3]],
      round2: [[3,2], [1,4]],
      round3: [[1,4]],
      round4: [[4,1]],
      // round5: [[2,3], [5,1]],
    },
    loser: {
      round1: [[4,1], [0,5], [3,3], [2,4]],
      round2: [[4,1], [0,5], [3,3], [2,4]],
      round3: [[4,1], [0,5]],
      round4: [[4,1], [0,5]],
      round5: [[4,1]],
      round6: [[4,1]],
      // Add more score arrays matching any extra rounds
    },
};
  
// 3. Optional: control the order of rounds explicitly
const rounds = {
    winner: ['round1','round2','round3','round4' /*,'round5'*/],
    loser:  ['round1','round2','round3','round4','round5','round6']
};
  
// 4. Build the brackets array dynamically
const brackets = [];
  
// Create a single bracket object (you can push multiple if needed)
const bracket = { winner: {}, loser: {} };
  
for (const level of ['winner', 'loser']) {
    // Reference to either bracket.winner or bracket.loser
    const sideObj = bracket[level];
  
    // Iterate through each defined round
    for (const roundKey of rounds[level]) {
      // Initialize this round as an empty object
      sideObj[roundKey] = {};
  
      // Retrieve matchup pairs and scores (or empty arrays if undefined)
      const matchPairs = players[level][roundKey] || [];
      const matchScores = scores[level][roundKey] || [];
  
      // Loop over each match in the round
      for (let i = 0; i < matchPairs.length; i++) {
        const [p1, p2] = matchPairs[i];          // player IDs
        const [s1, s2] = matchScores[i] || [];   // scores
  
        // Dynamically assign match1, match2, … objects
        sideObj[roundKey][`match${i+1}`] = {
          player1: `${p1}`,               // format player name
          player2: `${p2}`,
          team1:   `Team ${p1}`,                 // corresponding team name
          team2:   `Team ${p2}`,
          score1:  s1,
          score2:  s2,
          winner: function() {
            // Determine winner based on scores
            if (this.score1 === this.score2) {
              // In case of tie, default to player2
              return this.player2;
            }
            return this.score1 > this.score2 ? this.player1 : this.player2;
          },
        };
      };
    };
};
  
// Push the constructed bracket into the array
brackets.push(bracket);

// load the parameter for competition -- need to put each comp data with specific parameter
// document.addEventListener('DOMContentLoaded', () => {
//   const urlParams = new URLSearchParams(window.location.search);
//   const competitionId = urlParams.get('competition');

//   if (competitionId) {
//     console.log(`Loading bracket for competition: ${competitionId}`);
//     // Fetch or load competition-specific data here
//   }
// });

document.addEventListener('DOMContentLoaded', () => {
    // 1. Directly retrieve the <template> element from the DOM
  const tpl = document.getElementById('bracket-template').content;
  const clone = tpl.cloneNode(true);
  clone.id = `${competition}-bracket`;
  Object.keys(brackets[competition]).forEach((level) => {
    const tpl = document.getElementById('bracket-template').content;
    const clone = tpl.cloneNode(true);
    clone.id = `${competition}-bracket`;
    Object.keys(brackets[competition][level]).forEach((round, rNum) => {
      Object.keys(brackets[competition][level][round]).forEach((matchKey, i) => {
        const match = brackets[competition][level][round][matchKey];

        // Hides optional extra match of the grand final if the winner of the first match is from the winner bracket
        if (level === 'winner' && round === 'round4' && matchKey === 'match1' && match.winner() === match.player1) {
            clone.querySelector(`.GrandFinal .optional`).style.display = 'none';
            clone.querySelector(`.GrandFinal`).style.marginTop = '170px';
            clone.querySelector(`.GrandFinal .match`).style.marginBottom = '0px';
        };

        const p1MatchElement = clone.querySelector(`.round-${rNum + 1}-${level} .match${i + 1}-player1`);
        p1MatchElement.querySelector('.player_name').id = `${match.player1}`;
        p1MatchElement.querySelector('.player_name').innerHTML = `
        <a href="../players" target="_parent">${match.player1}</a>`;
        p1MatchElement.querySelector('.player_team').textContent = match.team1;
        p1MatchElement.querySelector('.score').textContent = match.score1;

        const p2MatchElement = clone.querySelector(`.round-${rNum + 1}-${level} .match${i + 1}-player2`);
        p2MatchElement.querySelector('.player_name').id = `${match.player2}`;
        p2MatchElement.querySelector('.player_name').innerHTML = `
        <a href="../players" target="_parent">${match.player2}</a>`;
        p2MatchElement.querySelector('.player_team').textContent = match.team2;
        p2MatchElement.querySelector('.score').textContent = match.score2;
      });
    });
    clone.querySelector('.bracket-wrap').id = `${competition}-bracket`;
    document.getElementById('bracket-container').appendChild(clone);
    // document.getElementById(`${competition}-bracket`).style.display = 'none';

  });
});
