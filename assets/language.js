(() => {
  const button = document.querySelector('.language-toggle');
  if (!button) return;
  const key = 'monsoon-isle-language';
  let language = 'en';
  try { if (localStorage.getItem(key) === 'zh') language = 'zh'; } catch (_) {}
  function apply() {
    document.documentElement.lang = language === 'zh' ? 'zh-CN' : 'en';
    document.querySelectorAll('[data-en][data-zh]').forEach(element => {
      element.innerHTML = element.dataset[language];
    });
    document.querySelectorAll('[data-alt-en]').forEach(element => {
      element.alt = language === 'zh' ? element.dataset.altZh : element.dataset.altEn;
    });
    document.title = language === 'zh' ? 'Monsoon Isle — 游戏与小小的乐趣' : 'Monsoon Isle — A little island. A world of play.';
    document.querySelector('meta[name="description"]').content = language === 'zh'
      ? 'Monsoon Isle 游戏团队主页。探索 The Arrow，查阅游戏隐私政策并联系团队。'
      : 'Meet Monsoon Isle, discover The Arrow, read our privacy policy and get in touch.';
    button.textContent = language === 'zh' ? 'English' : '中文';
    button.setAttribute('aria-label', language === 'zh' ? 'Switch to English / 切换为英语' : 'Switch to Chinese / 切换为中文');
  }
  button.addEventListener('click', () => {
    language = language === 'en' ? 'zh' : 'en';
    apply();
    try { localStorage.setItem(key, language); } catch (_) {}
  });
  apply();
  button.hidden = false;
})();
