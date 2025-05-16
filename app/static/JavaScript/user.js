document.addEventListener('DOMContentLoaded', () => {
  // competition modal
  const compModal = document.getElementById('addCompetitionModal');
  document.getElementById('openModal').addEventListener('click', () => {
    compModal.style.display = 'flex';
  });

  compModal.querySelector('.close').addEventListener('click', () => {
    compModal.style.display = 'none';
  });

  compModal.addEventListener('click', (e) => {
    if (e.target === compModal) {
      compModal.style.display = 'none';
    }
  });

  // PLAYER modal
  const playerModal = document.getElementById('addPlayerModal');
  document.getElementById('openPlayerModal').addEventListener('click', () => {
    playerModal.style.display = 'flex';
  });
  playerModal.querySelector('.close-player').addEventListener('click', () => {
    playerModal.style.display = 'none';
  });
  window.addEventListener('click', e => {
    if (e.target === playerModal) playerModal.style.display = 'none';
  });

  // BRACKET modal setup
  const bracketModal = document.getElementById('bracketModal');
  const closeBracketBtn = bracketModal.querySelector('.close-bracket');
  const bracketContent  = bracketModal.querySelector('.bracket-content');

  closeBracketBtn.addEventListener('click', () => {
    bracketModal.style.display = 'none';
  });
  window.addEventListener('click', e => {
    if (e.target === bracketModal) {
      bracketModal.style.display = 'none';
    }
  });

  // LIKE, COMMENT & DETAILS handlers
  document.querySelectorAll('.competition-card').forEach(card => {
    const likeBtn   = card.querySelector('.like');
    const commBtn   = card.querySelector('.comment');
    const likeCount = likeBtn.querySelector('.count');
    const poster    = card.querySelector('.result-image');
    const compId    = card.dataset.compId;

    // Result toggle
    card.querySelector('.btn-result').addEventListener('click', () => {
      poster.style.display = poster.style.display === 'block' ? 'none' : 'block';
    });

    // Details → show bracket in modal
    const detailsBtn = card.querySelector('.btn-details');
    detailsBtn.addEventListener('click', () => {
      bracketContent.innerHTML = card.querySelector('.bracket-data').innerHTML;
      bracketModal.style.display = 'flex';
    });

    // Like button
    likeBtn.addEventListener('click', async () => {
      const res = await fetch('/dashboard/api/like', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comp_id: compId })
      });
      const data = await res.json();
      likeCount.textContent = data.likes;
    });

    // Comment button
    commBtn.addEventListener('click', () => {
      document.getElementById('commentModal').style.display = 'flex';
      window.currentCompId = compId;
      window.currentCard   = card;
    });
  });

  // Submit comment
  document.querySelector('.comment-form button').addEventListener('click', async () => {
    const txt = document.querySelector('.comment-form textarea');
    const res = await fetch('/dashboard/api/comment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ comp_id: window.currentCompId, text: txt.value })
    });
    const data = await res.json();
    const list = document.querySelector('.comment-list');
    list.innerHTML = data.comments.map(c => `<div class="comment-item">${c}</div>`).join('');
    window.currentCard.querySelector('.comment .count').textContent = data.count;
    txt.value = '';
    document.getElementById('commentModal').style.display = 'none';
  });

  // Close comment modal
  document.querySelector('.close-comment').addEventListener('click', () => {
    document.getElementById('commentModal').style.display = 'none';
  });

  
  const openShare = document.getElementById('openShare');
  const shareSection = document.getElementById('share-section');
  if (openShare) {
    openShare.addEventListener('click', () => {
      shareSection.style.display = shareSection.style.display === 'none' ? 'block' : 'none';
    });
  }
});


