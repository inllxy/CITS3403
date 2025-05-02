document.addEventListener('DOMContentLoaded', () => {
    fetch('../Html/NavBar.html')
      .then(resp => resp.text())
      .then(html => {
        document
          .getElementById('navbar-placeholder')
          .innerHTML = html;
      })
      .catch(err => console.error('Fali to load Navbar', err));
  });