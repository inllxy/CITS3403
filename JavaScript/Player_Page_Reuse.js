// Mapping of player IDs to modal content (title and body text)
const playerInfo = {
  punk: {
    title: 'Punk',  // Display name for Punk
<<<<<<< Updated upstream
    matchesPlayed: 0,  // Placeholder for matches played
    matchesWon: 0  // Placeholder for matches won
  },
  menard: {
    title: 'MenaRD',  // Display name for MenaRD
    matchesPlayed: 0,  // Placeholder for matches played
    matchesWon: 0  // Placeholder for matches won
=======
    body: 'PUNK 1111111111111111'  // Placeholder details for Punk; replace with real data
  },
  menard: {
    title: 'MenaRD',  // Display name for MenaRD
    body: 'MenaRD 2222222222222222'  // Placeholder details for MenaRD
>>>>>>> Stashed changes
  }
};

// Select the reusable player modal element
const playerModal = document.getElementById('playerModal');

// Listen for Bootstrap's 'show' event on the modal
playerModal.addEventListener('show.bs.modal', event => {
  // event.relatedTarget is the card that triggered the modal
  const card = event.relatedTarget;
  // Read the player ID from data attribute
  const id = card.getAttribute('data-player-id');
  
  // Look up the corresponding info or use fallback
<<<<<<< Updated upstream
  const info = playerInfo[id] || { title: 'Unknown Player'};
  
  // Inject the title and body into the modal elements
  playerModal.querySelector('.modal-title').textContent = info.title;
  playerModal.querySelector('.matchesPlayed').textContent = info.matchesPlayed;
  playerModal.querySelector('.matchesWon').textContent = info.matchesWon;
  playerModal.querySelector('.winRate').textContent = info.matchesPlayed ? Math.round((info.matchesWon / info.matchesPlayed) * 100) + '%' : '0%';
  

  
=======
  const info = playerInfo[id] || { title: 'Unknown Player', body: 'No information available.' };
  
  // Inject the title and body into the modal elements
  playerModal.querySelector('.modal-title').textContent = info.title;
  playerModal.querySelector('.modal-body').textContent = info.body;
>>>>>>> Stashed changes
});

// Note: To add more players,
// extend the playerInfo object with new keys matching data-player-id values
// and provide appropriate title/body text.
