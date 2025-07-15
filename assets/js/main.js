/* 共通ヘッダー・フッター挿入 & FontAwesome ロード */
function ensureFA() {
  if (!document.querySelector('link[data-fa]')) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href =
      'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css';
    link.setAttribute('data-fa', '');
    document.head.appendChild(link);
  }
}

async function inject(path, selector) {
  const res = await fetch(path);
  if (res.ok) {
    document.querySelector(selector).innerHTML = await res.text();
  }
}

window.addEventListener('DOMContentLoaded', async () => {
  ensureFA();
  await inject('header.html', 'header');
  await inject('footer.html', 'footer');
});
