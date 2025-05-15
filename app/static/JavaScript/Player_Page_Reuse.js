// Fetch competition data (replace '/api/competitions' with your actual API endpoint)
async function fetchCompetitions() {
  const response = await fetch('/api/competitions'); // Ensure this endpoint returns competition data with the bracket field
  return await response.json();
}

// Calculate the number of matches a player has played
function calculateMatchesPlayed(playerName, competitions) {
  let matchCount = 0;

  competitions.forEach(competition => {
    const bracket = competition.bracket;

    // Process both winner and loser brackets
    ['winner', 'loser'].forEach(bracketType => {
      if (bracket[bracketType]) {
        Object.values(bracket[bracketType]).forEach(roundMatches => {
          roundMatches.forEach(match => {
            if (match.player1 === playerName || match.player2 === playerName) {
              matchCount++;
            }
          });
        });
      }
    });
  });

  return matchCount;
}

function calculateMatchesWon(playerName, competitions) {
  let matchesWon = 0;

  competitions.forEach(competition => {
    const bracket = competition.bracket;

    // Process both winner and loser brackets
    ['winner', 'loser'].forEach(bracketType => {
      if (bracket[bracketType]) {
        Object.values(bracket[bracketType]).forEach(roundMatches => {
          roundMatches.forEach(match => {
            if (match.player1 === playerName && match.score1 > match.score2) {
              matchesWon++;
            } else if (match.player2 === playerName && match.score2 > match.score1) {
              matchesWon++;
            }
            else if ((match.player1 == playerName || match.player2 == playerName) && match.score1 == match.score2) { //need to decide who gets the win in the case of a tie
              if (match.player1 == playerName) {
                matchesWon++;
              }
              // ALTER THIS TO BE THE PLAYER WHO WON THE TIE
            }
          });
        });
      }
    });
  });

  return matchesWon;
}

// Attach event listeners to all player cards
document.addEventListener('DOMContentLoaded', async () => {
  const playerCards = document.querySelectorAll('.player-card'); // Select all player cards
  const competitions = await fetchCompetitions(); // Fetch competition data once
  console.log(competitions); 

  playerCards.forEach(card => {
    card.addEventListener('click', () => {
      const playerName = card.getAttribute('data-player-id'); // Get the player's name from the card
      const modalId = card.getAttribute('data-bs-target'); // Get the modal ID
      const modal = document.querySelector(modalId); // Select the corresponding modal

      if (modal) {
        const matchesPlayed = calculateMatchesPlayed(playerName, competitions);
        const matchesWon = calculateMatchesWon(playerName, competitions);

        // Update modal content
        modal.querySelector('.matchesPlayed').textContent = matchesPlayed;
        modal.querySelector('.matchesWon').textContent = matchesWon;
        modal.querySelector('.winRate').textContent = matchesPlayed
          ? Math.round((matchesWon / matchesPlayed) * 100) + '%'
          : '0%';
      }
    });
  });
});