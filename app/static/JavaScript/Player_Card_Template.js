 const players = [
    {
      id: 'Punk',
      name: 'Punk',
      imageSrc: 'https://sf.esports.capcom.com/wp-content/uploads/2024/08/rere.CPT2024_Winners_EVO_Punk_square.jpg',
      badgeText: 'PREMIER',
      eventLine1: 'EVO Championship Series',
      eventLine2: 'Champion',
      socialLinks: [
        { platform: 'Twitter', url: 'https://x.com/PunkDaGod', icon: 'twitter' },
        { platform: 'Twitch',  url: 'https://www.twitch.tv/punkdagod', icon: 'twitch' }
      ]
    },
    {
      id: 'MenaRD',
      name: 'MenaRD',
      imageSrc: 'https://sf.esports.capcom.com/wp-content/uploads/2024/08/re.CPT2024_Winners_CCC_MENARD_square.jpg',
      badgeText: 'PREMIER',
      eventLine1: 'Cream City Convergence',
      eventLine2: 'Tournament Winner',
      socialLinks: [
        { platform: 'Twitter', url: 'https://x.com/_MenaRD__', icon: 'twitter' },
        { platform: 'Twitch',  url: '', icon: 'twitch' }
      ]
    },
    {
      id: 'Kusanagi',
      name: 'Kusanagi',
      imageSrc: 'https://sf.esports.capcom.com/wp-content/uploads/2024/08/CPT2024_Winners_UFA_KUSANAGI_aquare.jpg',
      badgeText: 'PREMIER',
      eventLine1: 'Fighting Arena',
      eventLine2: 'World Class Player',
      socialLinks: [
        { platform: 'Twitter', url: 'https://x.com/MaivineKusanagi', icon: 'twitter' },
        { platform: 'Twitch',  url: '', icon: 'twitch' }
      ]
    },
    // ... more player data objects
  ];

  const container = document.getElementById('playerContainer');
  const template = document.getElementById('playerCardTemplate');

  players.forEach(player => {
    const clone = template.content.cloneNode(true);
    // Replace placeholders
    clone.querySelector('.player-card').dataset.playerId = player.id;
    clone.querySelector('img').src = player.imageSrc;
    clone.querySelector('img').alt = player.name;
    clone.querySelector('.badge').textContent = player.badgeText;
    clone.querySelector('.card-title').textContent = player.name;
    const textP = clone.querySelector('.card-text');
    textP.innerHTML = `${player.eventLine1}<br>${player.eventLine2}`;

    // Populate social links
    const footer = clone.querySelector('.card-footer');
    footer.innerHTML = '';
    player.socialLinks.forEach(link => {
      const a = document.createElement('a');
      a.href = link.url;
      a.target = '_blank';
      a.setAttribute('aria-label', link.platform);
      const i = document.createElement('i');
      i.className = `bi bi-${link.icon}`;
      i.style.fontSize = '2rem';
      a.appendChild(i);
      footer.appendChild(a);
    });

    container.appendChild(clone);
  });