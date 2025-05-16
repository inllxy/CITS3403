// Fetch competition data
async function fetchCompetitions() {
  const response = await fetch('/api/competitions'); // Ensure this endpoint returns competition data with the bracket field
  return await response.json();
}

// Calculate the number of matches a player has played
function calculateMatchesPlayed(pName, competitions) {
  let matchCount = 0;

  competitions.forEach(competition => {
    const bracket = competition.bracket;

    // Process both winner and loser brackets
    ['winner', 'loser'].forEach(bracketType => {
      if (bracket[bracketType]) {
        Object.values(bracket[bracketType]).forEach(roundMatches => {
          roundMatches.forEach(match => {
            const player1 = match.player1.toLowerCase(); // Ensure player names are in lowercase
            const player2 = match.player2.toLowerCase(); // Ensure player names are in lowercase
            if (player1 === pName || player2 === pName) {
              matchCount++;
            }
          });
        });
      }
    });
  });

  return matchCount;
}

function calculateMatchesWon(pName, competitions) {
  // Initialize matches won counter
  let matchesWon = 0;

  competitions.forEach(competition => {
    const bracket = competition.bracket;

    // Process both winner and loser brackets
    ['winner', 'loser'].forEach(bracketType => {
      if (bracket[bracketType]) {
        Object.values(bracket[bracketType]).forEach(roundMatches => {
          roundMatches.forEach(match => {
            const player1 = match.player1.toLowerCase(); // Ensure player names are in lowercase
            const player2 = match.player2.toLowerCase(); // Ensure player names are in lowercase
            if (player1 === pName && match.score1 > match.score2) {
              matchesWon++;
            } else if (player2 === pName && match.score2 > match.score1) {
              matchesWon++;
            }
            else if ((player1 == pName || player2 == pName) && match.score1 == match.score2) { //need to decide who gets the win in the case of a tie
              if (player1 == pName) { //tie handling logic
                matchesWon++;
              }
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

  playerCards.forEach(card => {
    card.addEventListener('click', () => {
      const playerName = card.getAttribute('data-player-id'); // Get the player's name from the card
      const pName = playerName.toLowerCase(); // Ensure playerName is in lowercase
      const modalId = card.getAttribute('data-bs-target'); // Get the modal ID
      const modal = document.querySelector(modalId); // Select the corresponding modal

      if (modal) {
        const matchesPlayed = calculateMatchesPlayed(pName, competitions);
        const matchesWon = calculateMatchesWon(pName, competitions);

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