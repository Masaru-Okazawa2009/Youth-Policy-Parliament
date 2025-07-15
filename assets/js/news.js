fetch('data/news.json')
  .then(r => r.json())
  .then(items => {
    const list = document.getElementById('news-list');
    items.sort((a,b)=> new Date(b.date)-new Date(a.date))
      .forEach(n => {
        list.insertAdjacentHTML('beforeend', `
          <article class="news-item">
            <h3>${n.title}</h3>
            <time datetime="${n.date}">${n.date}</time>
            <p>${n.body}</p>
          </article>
        `);
      });
  });
