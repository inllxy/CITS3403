const competitions = [
    {
      month: 'Mar.',
      day: '6',
      logo: 'https://sf.esports.capcom.com/capcomcup/cc11/assets/img/com_logo_cc11.png',
      title: 'Capcom Cup 11<br>Top16 Champion',
      // The iframe src to be inserted into the Details Offcanvas
      detailTitle: 'Result Details',
      detailSrc: 'SF6_Bracket.html',
      // The image to be inserted into the Result Offcanvas
      resultTitle: 'Quick Result',
      resultImage: 'https://.../results_day4_001.webp',
      compLink: 'https://sf.esports.capcom.com/capcomcup/cc11/en/'
    },
    {
      month: 'Apr.',
      day: '12',
      logo: 'https://sf.esports.capcom.com/wp-content/uploads/2025/03/web_CPT2025_Premire_evo-japan.png',
      title: 'EVO Japan 2025',
      detailTitle: 'Result Details',
      detailSrc: 'Another_Bracket.html',
      resultTitle: 'Podium Photo',
      resultImage: 'https://.../podium.webp',
      compLink: 'https://.../other_tourney'
    },
   
    // ...more records...
  ];

document.addEventListener('DOMContentLoaded', () => {
  // 1. First, fetch the template file
  fetch('../Template/CompetitionTemplate.html')
    .then(r => r.text())
    .then(text => {
      document.getElementById('template-container').innerHTML = text;
      const tpl = document.getElementById('competition-item-template');
      const list = document.getElementById('competition-list');

      competitions.forEach((item, idx) => {
        // 2. Clone the template
        const clone = tpl.content.cloneNode(true);

        // 3. Generate unique IDs
        const detailId = `offcan_detail_${idx}`;
        const resultId = `offcan_result_${idx}`;

        // 4. Fill the buttons' data-bs-target attributes
        clone.querySelector('.btn-details').dataset.bsTarget = `#${detailId}`;
        clone.querySelector('.btn-result').dataset.bsTarget  = `#${resultId}`;
        clone.querySelector('.btn-comp').href                = item.compLink;

        // 5. Fill the card's main content
        clone.querySelector('.month').textContent         = item.month;
        clone.querySelector('.day').textContent           = item.day;
        clone.querySelector('.logo').src                  = item.logo;
        clone.querySelector('.title').innerHTML           = item.title;

        // 6. Rename the cloned offcanvas and populate its content
        const offDetail = clone.querySelector('.offcanvas-detail');
        offDetail.id = detailId;
        offDetail.querySelector('#offcanvasLabelDetail').textContent = item.detailTitle;
        offDetail.querySelector('.detail-body').innerHTML = 
          `<iframe src="${item.detailSrc}" class="w-100" style="min-height:70vh;border:none;"
                   title="${item.detailTitle}"></iframe>`;

        const offResult = clone.querySelector('.offcanvas-result');
        offResult.id = resultId;
        offResult.querySelector('#offcanvasLabelResult').textContent = item.resultTitle;
        offResult.querySelector('.result-body').innerHTML = 
          `<img src="${item.resultImage}" alt="${item.resultTitle}" 
                style="width:100%;height:auto;">`;

        // 7. Insert into the page
        list.appendChild(clone);
      });
    })
    .catch(e => console.error('Fail to load Template', e));
});