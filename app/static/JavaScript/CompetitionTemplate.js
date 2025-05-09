const competitions = [
    {
      year: 2025,
      month: 'Mar.',
      day: '6',
      logo: 'https://sf.esports.capcom.com/capcomcup/cc11/assets/img/com_logo_cc11.png',
      title: 'Capcom Cup 11<br>Top16 Champion',
      // The iframe src to be inserted into the Details Offcanvas
      detailTitle: 'Result Details',
      detailSrc: '/bracket/Bracket',
      // The image to be inserted into the Result Offcanvas
      resultTitle: 'Quick Result',
      resultImage: 'https://sf.esports.capcom.com/capcomcup/cc11/assets/img/results/results_day4_004.webp',
      compLink: 'https://sf.esports.capcom.com/capcomcup/cc11/en/'
    },
    {
      year: 2025,
      month: 'Apr.',
      day: '19',
      logo: 'https://sf.esports.capcom.com/wp-content/uploads/2025/03/web_CPT2025_Premire_evo-japan.png',
      title: 'EVO Japan 2025',
      detailTitle: 'Result Details',
      detailSrc: '/bracket/Bracket',
      resultTitle: 'Podium Photo',
      resultImage: 'https://.../podium.webp',
      compLink: 'https://.../other_tourney'
    },
   {
      year: 2024,
      month: 'Apr.',
      day: '9',
      logo: 'https://sf.esports.capcom.com/wp-content/uploads/2025/03/web_CPT2025_Premire_evo-japan.png',
      title: 'EVO Japan 2025',
      detailTitle: 'Result Details',
      detailSrc: '/bracket/Bracket',
      resultTitle: 'Podium Photo',
      resultImage: 'https://.../podium.webp',
      compLink: 'https://.../other_tourney'
    },
    // ...more records...
  ];

document.addEventListener('DOMContentLoaded', () => {
  const tpl = document.getElementById('competition-item-template').content;

  competitions.forEach((item, idx) => {
    const list = document.getElementById(`competition-list-${item.year}`);
    if (!list) {
      console.warn(`can't find #competition-list-${item.year} container`);
      return;
    }

    const clone = tpl.cloneNode(true);
    const detailId = `offcan_detail_${idx}`;
    const resultId = `offcan_result_${idx}`;

    clone.querySelector('.btn-details').dataset.bsTarget  = `#${detailId}`;
    clone.querySelector('.btn-result').dataset.bsTarget   = `#${resultId}`;
    clone.querySelector('.btn-comp').href                 = item.compLink;
    clone.querySelector('.month').textContent             = item.month;
    clone.querySelector('.day').textContent               = item.day;
    clone.querySelector('.logo').src                      = item.logo;
    clone.querySelector('.title').innerHTML               = item.title;

    const offDetail = clone.querySelector('.offcanvas-detail');
    offDetail.id = detailId;
    offDetail.querySelector('#offcanvasLabelDetail').textContent = item.detailTitle;
    offDetail.querySelector('.detail-body').innerHTML = `
      <iframe src="${item.detailSrc}"
              class="w-100" style="min-height:70vh;border:none;"
              title="${item.detailTitle}">
      </iframe>`;

    const offResult = clone.querySelector('.offcanvas-result');
    offResult.id = resultId;
    offResult.querySelector('#offcanvasLabelResult').textContent = item.resultTitle;
    offResult.querySelector('.result-body').innerHTML = `
      <img src="${item.resultImage}"
           alt="${item.resultTitle}"
           style="width:100%;height:auto;">`;

    list.appendChild(clone);
  });
});

