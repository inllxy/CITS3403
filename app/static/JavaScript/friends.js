// static/js/friends.js

// pass current user ID from template into JS
const CURRENT_USER_ID = {{ current_user.id }};

// In-memory Set of your friend IDs
let friends = new Set();

// Fetch & render both your friends and all users lists
async function loadFriends() {
  // 1) Get your current friends
  let res = await fetch('/api/friends');
  let { friendIds, friends: friendList } = await res.json();
  friends = new Set(friendIds);

  // render “Your Friends”
  const fl = document.getElementById('friendsList');
  fl.innerHTML = friendList.map(f => `
    <div data-user-id="${f.id}">
      ${f.name}
      <button class="btn-remove" data-user-id="${f.id}">Unfriend</button>
    </div>
  `).join('');

  // 2) Get all users
  res = await fetch('/api/users');
  let { users } = await res.json();
  const all = document.getElementById('allUsersList');
  all.innerHTML = users.map(u => {
    const isFriend = friends.has(u.id);
    return `
      <div data-user-id="${u.id}">
        ${u.name}
        <button class="${isFriend?'btn-remove':'btn-add'}"
                data-user-id="${u.id}">
          ${isFriend?'Remove':'Add'} Friend
        </button>
      </div>
    `;
  }).join('');

  // hook up each Add/Remove button
  document.querySelectorAll('#allUsersList button, #friendsList .btn-remove')
    .forEach(btn => {
      btn.onclick = () => toggleFriend(parseInt(btn.dataset.userId));
    });

  updatePrivateVisibility();
}

// Toggle friend on/off via your API
async function toggleFriend(userId) {
  const action = friends.has(userId) ? 'remove' : 'add';
  await fetch(`/api/friends/${action}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ userId })
  });
  await loadFriends();
}

// Hide non-friends’ private cards
function updatePrivateVisibility() {
  document.querySelectorAll('.private-card').forEach(card => {
    const owner = parseInt(card.dataset.ownerId, 10);
    const isMine   = owner === CURRENT_USER_ID;
    const isFriend = friends.has(owner);
    card.classList.toggle('hidden', !isMine && !isFriend);
  });
}

// run on page load
window.addEventListener('DOMContentLoaded', loadFriends);