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
    // 1. Directly retrieve the <template> element from the DOM
    const tpl = document.getElementById('competition-item-template').content;
    const list = document.getElementById('competition-list');
  
    competitions.forEach((item, idx) => {
      // 2. Clone the template
      const clone = tpl.cloneNode(true);
  
      // 3. Generate unique IDs for the detail and result offcanvas
      const detailId = `offcan_detail_${idx}`;
      const resultId = `offcan_result_${idx}`;
  
      // 4. Populate buttons and links
      const btnDetail = clone.querySelector('.btn-details');
      btnDetail.dataset.bsTarget = `#${detailId}`;
      const btnResult = clone.querySelector('.btn-result');
      btnResult.dataset.bsTarget  = `#${resultId}`;
      clone.querySelector('.btn-comp').href = item.compLink;
  
      // 5. Fill main content
      clone.querySelector('.month').textContent = item.month;
      clone.querySelector('.day').textContent   = item.day;
      clone.querySelector('.logo').src          = item.logo;
      clone.querySelector('.title').innerHTML   = item.title;
  
      // 6. Configure Offcanvas Details
      const offDetail = clone.querySelector('.offcanvas-detail');
      offDetail.id = detailId;
      offDetail.querySelector('#offcanvasLabelDetail').textContent = item.detailTitle;
      offDetail.querySelector('.detail-body').innerHTML = `
        <iframe src="${item.detailSrc}"
                class="w-100" style="min-height:70vh;border:none;"
                title="${item.detailTitle}">
        </iframe>`;
  
      // 7. Configure Offcanvas Snapshot
      const offResult = clone.querySelector('.offcanvas-result');
      offResult.id = resultId;
      offResult.querySelector('#offcanvasLabelResult').textContent = item.resultTitle;
      offResult.querySelector('.result-body').innerHTML = `
        <img src="${item.resultImage}"
             alt="${item.resultTitle}"
             style="width:100%;height:auto;">`;
  
      // 8. Finally, append the clone to the list
      list.appendChild(clone);
    });
  });
  
