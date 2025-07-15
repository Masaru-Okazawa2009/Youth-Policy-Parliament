/* スクロールでヒーローをフェードアウト＆折りたたみ */
window.addEventListener('DOMContentLoaded', () => {
  const hero = document.getElementById('hero');
  if (!hero) return;
  const h = hero.offsetHeight;
  const onScroll = () => {
    hero.classList.toggle('hide', window.scrollY > h * 0.6);
  };
  window.addEventListener('scroll', onScroll, { passive:true });
});
