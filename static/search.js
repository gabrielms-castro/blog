(() => {
  const input = document.getElementById('search-input');
  const resultsList = document.getElementById('search-results');

  if (!input || !resultsList) return;

  let index = [];

  fetch('/search-index.json')
    .then(r => r.json())
    .then(data => { index = data; })
    .catch(() => {});

  function highlight(text, query) {
    if (!query) return text;
    const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    return text.replace(new RegExp(`(${escaped})`, 'gi'), '<mark>$1</mark>');
  }

  function search(query) {
    const q = query.trim().toLowerCase();
    if (!q) return [];
    return index.filter(post =>
      post.title.toLowerCase().includes(q) ||
      post.tags.some(tag => tag.toLowerCase().includes(q))
    );
  }

  function render(matches, query) {
    if (matches.length === 0) {
      resultsList.innerHTML = '<li class="search-no-results">No results found</li>';
    } else {
      resultsList.innerHTML = matches.map(post => {
        const tagsHtml = post.tags.length
          ? post.tags.map(t => `<span class="tag tag--sm">${t}</span>`).join('')
          : '';
        return `
          <li class="search-result-item">
            <a href="${post.url}" class="search-result-link">
              <span class="result-title">${highlight(post.title, query)}</span>
              ${tagsHtml ? `<span class="result-tags">${tagsHtml}</span>` : ''}
            </a>
          </li>`;
      }).join('');
    }
    resultsList.hidden = false;
  }

  function close() {
    resultsList.hidden = true;
  }

  input.addEventListener('input', () => {
    const q = input.value;
    if (!q.trim()) { close(); return; }
    render(search(q), q.trim());
  });

  input.addEventListener('keydown', e => {
    if (e.key === 'Escape') { close(); input.blur(); }
  });

  document.addEventListener('click', e => {
    if (!e.target.closest('.search-wrap')) close();
  });
})();
