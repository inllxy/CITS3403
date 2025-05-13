// Mapping of player IDs to modal content (title and body text)
const playerInfo = {
  Punk: {
    title: 'Punk',  // Display name for Punk
    matchesPlayed: 0,  // Placeholder for matches played
    matchesWon: 0  // Placeholder for matches won
  },
  MenaRD: {
    title: 'MenaRD', 
    matchesPlayed: 0,  
    matchesWon: 0  
  },
  Kusanagi: {
    title: 'Kusanagi',  
    matchesPlayed: 0,  
    matchesWon: 0  
  },
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
  const info = playerInfo[id] || { title: 'Unknown Player'};
  
  // Inject the title and body into the modal elements
  playerModal.querySelector('.modal-title').textContent = info.title;
  playerModal.querySelector('.matchesPlayed').textContent = info.matchesPlayed;
  playerModal.querySelector('.matchesWon').textContent = info.matchesWon;
  playerModal.querySelector('.winRate').textContent = info.matchesPlayed ? Math.round((info.matchesWon / info.matchesPlayed) * 100) + '%' : '0%';
  

  
});

// Note: To add more players,
// extend the playerInfo object with new keys matching data-player-id values
// and provide appropriate title/body text.
