document.addEventListener('DOMContentLoaded', () => {
    // COMPETITION modal
    const compModal = document.getElementById('addCompetitionModal');
    document.getElementById('openModal').addEventListener('click', () => {
      compModal.style.display = 'flex';
    });
    compModal.querySelector('.close').addEventListener('click', () => {
      compModal.style.display = 'none';
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
  
    
  
    // LIKE & COMMENT handlers
    document.querySelectorAll('.competition-card').forEach(card => {
      const likeBtn = card.querySelector('.like');
      const commBtn = card.querySelector('.comment');
      const likeCount = likeBtn.querySelector('.count');
      const poster = card.querySelector('.result-image');
      const bracket = card.querySelector('.bracket-display');
      const compId = card.dataset.compId;
  
      card.querySelector('.btn-result').addEventListener('click', () => {
        poster.style.display = poster.style.display === 'block' ? 'none' : 'block';
      });
      card.querySelector('.btn-details').addEventListener('click', () => {
        bracket.style.display = bracket.style.display === 'block' ? 'none' : 'block';
      });
  
      likeBtn.addEventListener('click', async () => {
        const res = await fetch('/dashboard/api/like', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ comp_id: compId })
        });
        const data = await res.json();
        likeCount.textContent = data.likes;
      });
  
      commBtn.addEventListener('click', () => {
        document.getElementById('commentModal').style.display = 'flex';
        window.currentCompId = compId;
        window.currentCard = card;
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
  
    // BRACKET generator
    const bracketContainer = document.getElementById('bracket');
    document.getElementById('numPlayers').addEventListener('change', function () {
      bracketContainer.innerHTML = '';
      const num = parseInt(this.value, 10);
      if (!num) return;
      const rounds = Math.log2(num);
      for (let r = 1; r <= rounds; r++) {
        const rd = document.createElement('div');
        rd.className = 'round';
        rd.innerHTML = `<h3>Round ${r}</h3>`;
        const matches = num / Math.pow(2, r);
        for (let m = 1; m <= matches; m++) {
          const md = document.createElement('div');
          md.className = 'match';
          md.innerHTML = `
            <input name="round${r}_match${m}_player1" placeholder="P1" required>
            <input name="round${r}_match${m}_player2" placeholder="P2" required>
          `;
          rd.appendChild(md);
        }
        bracketContainer.appendChild(rd);
      }
    });
  });
  