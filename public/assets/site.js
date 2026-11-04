const search = document.querySelector('#city-search');
if (search) {
  const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replaceAll('-', ' ');
  search.addEventListener('input', () => {
    let count = 0;
    document.querySelectorAll('[data-city]').forEach(card => {
      card.hidden = !normalize(card.dataset.city).includes(normalize(search.value.trim()));
      if (!card.hidden) count++;
    });
    document.querySelector('.search-count').textContent = `${count} ville${count > 1 ? 's' : ''}`;
    document.querySelector('.empty-search').hidden = count > 0;
  });
}
