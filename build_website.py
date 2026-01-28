<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-R7XMFE1GNF"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-R7XMFE1GNF');
    </script>

    <title>FreeTalkEasy Flashcards</title>
    
    <link rel="icon" href="logo/logo.png" type="image/png" sizes="32x32">
    <link rel="icon" href="logo/logo.png" type="image/png" sizes="192x192">
    <link rel="apple-touch-icon" href="logo/logo.png">

    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; }
        :root { --primary-color: #4a90e2; --bg-color: #f5f7fa; --card-shadow: 0 2px 4px rgba(0,0,0,0.08); }
        body { font-family: 'Noto Sans TC', sans-serif; background-color: var(--bg-color); margin: 0; padding: 0; min-height: 100vh; padding-bottom: 90px; }

        /* Landing Page */
        #landing-screen { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; padding: 40px 15px; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); width: 100%; }
        .logo-container { text-align: center; margin-bottom: 30px; }
        .earth-logo { width: 130px; height: 130px; object-fit: contain; border-radius: 50%; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2)); }
        
        .site-title { font-size: 42px; color: #fff; font-weight: 700; margin: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }
        .site-subtitle { font-size: 16px; color: rgba(255,255,255,0.8); margin: 0; }
        
        .lang-list { display: flex; flex-direction: column; gap: 12px; width: 100%; max-width: 400px; margin-bottom: 30px; }
        .lang-btn { display: flex; align-items: center; background: white; border: none; border-radius: 12px; padding: 15px; width: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.1); cursor: pointer; text-decoration: none; }
        .lang-flag-img { width: 36px; height: 27px; margin-right: 15px; border-radius: 4px; object-fit: cover; }
        .lang-name { font-size: 16px; color: #2a5298; font-weight: bold; flex-grow: 1; text-align: left; }

        /* App Screen */
        #app-screen { display: none; flex-direction: column; align-items: center; padding: 20px; width: 100%; }
        .top-nav { width: 100%; max-width: 1200px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 1px solid #ddd; padding-bottom: 10px; }
        .back-btn { background: none; border: none; font-size: 16px; color: #666; cursor: pointer; } /* 🟢 已移除隱藏文字的設定 */
        .current-lang-display { font-weight: bold; color: var(--primary-color); font-size: 18px; }

        .filters { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; width: 100%; max-width: 1200px; margin-bottom: 15px; }
        select, button { padding: 12px; font-size: 15px; border-radius: 8px; border: 1px solid #ddd; background: white; width: 100%; }
        
        /* Sticky Controls */
        .sticky-controls { position: fixed; bottom: 0; left: 0; width: 100%; background: white; box-shadow: 0 -2px 10px rgba(0,0,0,0.1); padding: 12px 15px; display: flex; gap: 10px; z-index: 1000; justify-content: center; }
        .sticky-controls button { flex: 1; max-width: 160px; border-radius: 25px; }
        #btn-autoplay { background: var(--primary-color); color: white; font-weight: bold; border: none; }
        #btn-autoplay.playing { background: #f39c12; animation: pulse 1.5s infinite; }
        @keyframes pulse { 0% {transform:scale(1);} 50% {transform:scale(1.05);} 100% {transform:scale(1);} }

        /* Settings Panel */
        #settings-panel { position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%); width: 90%; max-width: 380px; background: white; border-radius: 12px; box-shadow: 0 5px 20px rgba(0,0,0,0.2); padding: 15px; z-index: 1001; display: none; border: 1px solid #eee; }
        #settings-panel.show { display: block; animation: slideUp 0.3s ease-out; }
        @keyframes slideUp { from {transform:translate(-50%,20px);opacity:0;} to {transform:translate(-50%,0);opacity:1;} }
        .setting-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; font-size: 14px; }
        .toggle-switch { position: relative; width: 40px; height: 24px; }
        .toggle-switch input { opacity: 0; width: 0; height: 0; }
        .slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #ccc; transition: .4s; border-radius: 24px; }
        .slider:before { position: absolute; content: ""; height: 18px; width: 18px; left: 3px; bottom: 3px; background-color: white; transition: .4s; border-radius: 50%; }
        input:checked + .slider { background-color: var(--primary-color); }
        input:checked + .slider:before { transform: translateX(16px); }

        /* Cards */
        #card-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 10px; width: 100%; max-width: 1200px; flex: 1; }
        .category-header { grid-column: 1 / -1; padding: 15px 0 5px 0; margin-top: 10px; color: #2a5298; font-weight: bold; border-bottom: 2px solid #e0e0e0; font-size: 1.1em; }
        
        .card { background: white; border-radius: 12px; padding: 12px; box-shadow: var(--card-shadow); cursor: pointer; display: flex; flex-direction: column; justify-content: space-between; min-height: 140px; border: 2px solid transparent; }
        .card.playing { border-color: #4a90e2; transform: scale(1.05); z-index: 10; }
        .main-word { font-size: 20px; font-weight: bold; color: #2c3e50; margin-bottom: 5px; word-break: break-word; }
        .phonetic { font-size: 13px; color: #888; font-style: italic; margin-bottom: 10px; }
        .footer-translation { margin-top: auto; padding-top: 8px; border-top: 1px dashed #eee; font-size: 13px; color: #555; }

        /* Footer */
        .landing-footer, .app-footer { margin-top: 20px; text-align: center; color: #999; font-size: 12px; width: 100%; }
        .landing-links { margin: 15px 0; }
        .landing-links a { color: rgba(255,255,255,0.8); margin: 0 5px; text-decoration: none; }
        .app-footer a { color: #aaa; margin: 0 5px; text-decoration: none; }
        .bmc-btn { background-color: #FFDD00; color: #000; font-weight: bold; text-decoration: none; padding: 10px 25px; border-radius: 25px; display: inline-flex; align-items: center; gap: 8px; margin-bottom: 10px; }
    </style>
</head>
<body>
    
    <audio id="global-audio-player" preload="auto" style="display:none;"></audio>

    <div id="landing-screen">
        <div class="logo-container">
            <div class="logo-title-wrapper">
                <img src="logo/logo.png" class="earth-logo" alt="Logo">
                <h1 class="site-title">FreeTalkEasy</h1>
            </div>
            <p class="site-subtitle">請選擇學習語言 / Select Language</p>
        </div>
        
        <div class="lang-list">
            <div class="lang-btn" onclick="selectLanguage('CN_ENG', '🇺🇸 英語')"><img src="https://flagcdn.com/w80/us.png" class="lang-flag-img"><span class="lang-name">英語 (English)</span>➜</div>
            <div class="lang-btn" onclick="selectLanguage('CN_JP', '🇯🇵 日語')"><img src="https://flagcdn.com/w80/jp.png" class="lang-flag-img"><span class="lang-name">日語 (Japanese)</span>➜</div>
            <div class="lang-btn" onclick="selectLanguage('CN_KR', '🇰🇷 韓語')"><img src="https://flagcdn.com/w80/kr.png" class="lang-flag-img"><span class="lang-name">韓語 (Korean)</span>➜</div>
            <div class="lang-btn" onclick="selectLanguage('CN_VN', '🇻🇳 越語')"><img src="https://flagcdn.com/w80/vn.png" class="lang-flag-img"><span class="lang-name">越語 (Vietnamese)</span>➜</div>
            <div class="lang-btn" onclick="selectLanguage('CN_TH', '🇹🇭 泰語')"><img src="https://flagcdn.com/w80/th.png" class="lang-flag-img"><span class="lang-name">泰語 (Thai)</span>➜</div>
            <div class="lang-btn" onclick="selectLanguage('CN_ID', '🇮🇩 印尼語')"><img src="https://flagcdn.com/w80/id.png" class="lang-flag-img"><span class="lang-name">印尼語 (Indonesia)</span>➜</div>
            <div class="lang-btn" onclick="selectLanguage('CN_FR', '🇫🇷 法語')"><img src="https://flagcdn.com/w80/fr.png" class="lang-flag-img"><span class="lang-name">法語 (French)</span>➜</div>
            <div class="lang-btn" onclick="selectLanguage('CN_DE', '🇩🇪 德語')"><img src="https://flagcdn.com/w80/de.png" class="lang-flag-img"><span class="lang-name">德語 (German)</span>➜</div>
            <div class="lang-btn" onclick="selectLanguage('CN_ES', '🇪🇸 西語')"><img src="https://flagcdn.com/w80/es.png" class="lang-flag-img"><span class="lang-name">西語 (Spanish)</span>➜</div>
            <div class="lang-btn" onclick="selectLanguage('CN_CON', '🇭🇰 廣東話')"><img src="https://flagcdn.com/w80/hk.png" class="lang-flag-img"><span class="lang-name">廣東話 (Cantonese)</span>➜</div>
            <div class="lang-btn" onclick="selectLanguage('CN_ZH', '🇹🇼 中文')"><img src="https://flagcdn.com/w80/tw.png" class="lang-flag-img"><span class="lang-name">中文 (Chinese Mode)</span>➜</div>
            <div class="lang-btn" onclick="selectLanguage('CN_RU', '🇷🇺 俄語')"><img src="https://flagcdn.com/w80/ru.png" class="lang-flag-img"><span class="lang-name">俄語 (Russian)</span>➜</div>
        </div>

        <div class="landing-footer">
            <a href="https://www.buymeacoffee.com/freetalkeasy" target="_blank" class="bmc-btn"><i class="fas fa-coffee"></i> Buy me a coffee</a>
            <div class="landing-links">
                <a href="seo_pages/sitemap.html">單字列表</a> | <a href="seo_pages/about.html">關於本站</a> | <a href="seo_pages/privacy.html">隱私政策</a>
            </div>
            <p style="color:rgba(255,255,255,0.5); font-size:11px;">&copy; 2026 FreeTalkEasy. All rights reserved.</p>
        </div>
    </div>

    <div id="app-screen">
        <div class="top-nav">
            <button class="back-btn" onclick="goBackToHome()"><span>⬅</span> 回首頁 (Back)</button>
            <div class="current-lang-display" id="display-lang-name">英語</div>
        </div>

        <div class="filters">
            <select id="category-filter"><option value="all">📚 所有主分類</option></select>
            <select id="sub-category-filter" disabled><option value="all">📌 所有次分類</option></select>
        </div>

        <div id="card-container">Loading...</div>

        <footer class="app-footer">
            <a href="https://www.buymeacoffee.com/freetalkeasy" target="_blank" class="bmc-btn"><i class="fas fa-coffee"></i> Buy me a coffee</a>
            <div style="margin-top:10px;">
                <a href="seo_pages/sitemap.html">單字列表</a> | <a href="seo_pages/about.html">關於</a> | <a href="seo_pages/privacy.html">隱私</a>
            </div>
            <p style="margin-top:10px; font-size:11px;">&copy; 2026 FreeTalkEasy.</p>
        </footer>

        <div id="settings-panel">
            <div style="font-weight:bold; margin-bottom:15px; border-bottom:1px solid #eee; padding-bottom:5px;">
                <i class="fas fa-cog"></i> 播放設定 <span onclick="toggleSettings()" style="float:right; cursor:pointer;">✕</span>
            </div>
            <div class="setting-row">
                <span>🔁 重複次數</span>
                <select id="repeat-count-select">
                    <option value="1">1 次</option><option value="2">2 次</option><option value="3">3 次</option><option value="5">5 次</option>
                </select>
            </div>
            <div class="setting-row">
                <span>⚡ 播放速度</span>
                <select id="speed-select">
                    <option value="0.5">0.5x (慢)</option><option value="0.75">0.75x (稍慢)</option><option value="1.0" selected>1.0x (正常)</option><option value="1.25">1.25x (稍快)</option><option value="1.5">1.5x (快)</option>
                </select>
            </div>
            <div class="setting-row">
                <span>🗣️ 解釋語言</span>
                <select id="mother-tongue-select">
                    <option value="CN_ZH">🇹🇼 中文</option><option value="CN_ENG">🇺🇸 英語</option><option value="CN_JP">🇯🇵 日語</option><option value="CN_KR">🇰🇷 韓語</option><option value="CN_VN">🇻🇳 越語</option>
                </select>
            </div>
            <div class="setting-row">
                <span>🎧 朗讀解釋</span>
                <label class="toggle-switch"><input type="checkbox" id="tts-toggle" checked><span class="slider"></span></label>
            </div>
        </div>

        <div class="sticky-controls">
            <button id="btn-settings" onclick="toggleSettings()" style="background:#f0f0f0; color:#555;">⚙ 設定</button>
            <button id="btn-autoplay">▶ 自動播放</button>
            <button id="btn-reset" style="background:white; color:#e74c3c; border:1px solid #e74c3c;">🗑️ 重置</button>
        </div>
    </div>

    <script src="data.js"></script>
    <script>
        // 核心變數
        let currentLang = 'CN_ENG';
        let isAutoPlaying = false;
        let visibleCards = [];
        let autoPlayTimer = null;
        let autoPlayIndex = 0;
        let repeatCount = 1;
        let playbackSpeed = 1.0;
        let enableTTS = true;
        let explanationLang = 'CN_ZH';
        const globalPlayer = document.getElementById('global-audio-player');

        // 初始化
        window.onload = () => {
            if (typeof vocabData === 'undefined') { alert("⚠️ data.js 讀取失敗，請確認是否執行 Python 程式！"); return; }
            populateCategories();
            loadSettings();
            
            // 讀取上次語言
            const lastLang = localStorage.getItem('fte_last_lang');
            const lastLangName = localStorage.getItem('fte_last_lang_name');
            if (lastLang && lastLangName) selectLanguage(lastLang, lastLangName, true);
        };

        // 載入設定
        function loadSettings() {
            const savedRepeat = localStorage.getItem('fte_repeat');
            if (savedRepeat) { repeatCount = parseInt(savedRepeat); document.getElementById('repeat-count-select').value = repeatCount; }
            
            const savedSpeed = localStorage.getItem('fte_speed');
            if (savedSpeed) { playbackSpeed = parseFloat(savedSpeed); document.getElementById('speed-select').value = playbackSpeed; }

            const savedMT = localStorage.getItem('fte_mt');
            if (savedMT) { explanationLang = savedMT; document.getElementById('mother-tongue-select').value = explanationLang; }
        }

        // 設定監聽
        document.getElementById('repeat-count-select').addEventListener('change', (e) => { repeatCount = parseInt(e.target.value); localStorage.setItem('fte_repeat', repeatCount); });
        document.getElementById('speed-select').addEventListener('change', (e) => { playbackSpeed = parseFloat(e.target.value); localStorage.setItem('fte_speed', playbackSpeed); });
        document.getElementById('mother-tongue-select').addEventListener('change', (e) => { explanationLang = e.target.value; localStorage.setItem('fte_mt', explanationLang); });
        document.getElementById('tts-toggle').addEventListener('change', (e) => { enableTTS = e.target.checked; });

        function toggleSettings() { document.getElementById('settings-panel').classList.toggle('show'); }

        // 語言選擇
        function selectLanguage(code, name, isAutoLoad=false) {
            currentLang = code;
            document.getElementById('display-lang-name').innerText = name;
            document.getElementById('landing-screen').style.display = 'none';
            document.getElementById('app-screen').style.display = 'flex';
            localStorage.setItem('fte_last_lang', code);
            localStorage.setItem('fte_last_lang_name', name);
            if(!isAutoLoad) {
                document.getElementById('category-filter').value = 'all';
                updateSubCategories('all');
            }
            renderCards();
            window.scrollTo(0,0);
        }

        function goBackToHome() {
            stopAutoPlay();
            document.getElementById('app-screen').style.display = 'none';
            document.getElementById('landing-screen').style.display = 'flex';
        }

        // 分類篩選
        const catFilter = document.getElementById('category-filter');
        const subCatFilter = document.getElementById('sub-category-filter');

        function populateCategories() {
            const cats = [...new Set(vocabData.map(i => i.category))];
            cats.forEach(c => { if(c) { const o=document.createElement('option'); o.value=c; o.innerText=c; catFilter.appendChild(o); }});
        }

        catFilter.addEventListener('change', () => { stopAutoPlay(); updateSubCategories(catFilter.value); renderCards(); });
        subCatFilter.addEventListener('change', () => { stopAutoPlay(); renderCards(); });

        function updateSubCategories(main) {
            subCatFilter.innerHTML = '<option value="all">📌 所有次分類</option>';
            subCatFilter.disabled = (main === 'all');
            if(main === 'all') return;
            const subs = [...new Set(vocabData.filter(i => i.category === main).map(i => i.subcategory).filter(s=>s))];
            subs.forEach(s => { const o=document.createElement('option'); o.value=s; o.innerText=s; subCatFilter.appendChild(o); });
        }

        // 播放控制
        const btnAuto = document.getElementById('btn-autoplay');
        btnAuto.addEventListener('click', () => { if(isAutoPlaying) stopAutoPlay(); else startAutoPlay(); });
        document.getElementById('btn-reset').addEventListener('click', () => { if(confirm("重置學習紀錄？")) { localStorage.clear(); location.reload(); } });

        function startAutoPlay() {
            visibleCards = Array.from(document.querySelectorAll('.card'));
            if(visibleCards.length===0) return;
            isAutoPlaying = true;
            btnAuto.innerHTML = '⏹ 停止';
            btnAuto.classList.add('playing');
            document.getElementById('settings-panel').classList.remove('show');
            autoPlayIndex = 0;
            playCardSequence(visibleCards[0]);
        }

        function stopAutoPlay() {
            isAutoPlaying = false;
            btnAuto.innerHTML = '▶ 自動播放';
            btnAuto.classList.remove('playing');
            globalPlayer.pause();
            document.querySelectorAll('.card.playing').forEach(c => c.classList.remove('playing'));
        }

        function playCardSequence(card) {
            if(!isAutoPlaying || !card) { stopAutoPlay(); return; }
            card.scrollIntoView({behavior:'smooth', block:'center'});
            document.querySelectorAll('.card.playing').forEach(c => c.classList.remove('playing'));
            card.classList.add('playing');

            let count = 0;
            const playLoop = () => {
                if(!isAutoPlaying) return;
                const src = card.dataset.audio;
                if(!src) { finishCard(); return; }
                
                globalPlayer.src = src;
                globalPlayer.playbackRate = playbackSpeed;
                globalPlayer.onended = () => {
                    count++;
                    if(count < repeatCount) setTimeout(playLoop, 500);
                    else setTimeout(playExpl, 500);
                };
                globalPlayer.onerror = () => { console.log("Audio Error"); finishCard(); };
                globalPlayer.play().catch(e => { console.log("Play Blocked"); finishCard(); });
            };

            const playExpl = () => {
                if(!isAutoPlaying) return;
                if(!enableTTS) { finishCard(); return; }
                const item = vocabData.find(v => v.id == card.dataset.id);
                if(item && item[explanationLang] && item[explanationLang].audio) {
                    globalPlayer.src = `${item[explanationLang].folder}/${item[explanationLang].audio}`;
                    globalPlayer.playbackRate = 1.1; // 解釋稍微快一點
                    globalPlayer.onended = finishCard;
                    globalPlayer.onerror = finishCard;
                    globalPlayer.play().catch(finishCard);
                } else finishCard();
            };

            const finishCard = () => {
                if(!isAutoPlaying) return;
                // 更新點擊數
                const id = card.dataset.id;
                const n = (parseInt(localStorage.getItem('fte_'+id)||'0')) + 1;
                localStorage.setItem('fte_'+id, n);
                card.querySelector('.click-cnt').innerText = n;
                
                autoPlayIndex++;
                if(autoPlayIndex < visibleCards.length) setTimeout(() => playCardSequence(visibleCards[autoPlayIndex]), 800);
                else stopAutoPlay();
            };

            playLoop();
        }

        // 渲染卡片
        const container = document.getElementById('card-container');
        function renderCards() {
            container.innerHTML = '';
            const sCat = catFilter.value;
            const sSub = subCatFilter.value;
            let lastCat = "", lastSub = "";

            vocabData.forEach(item => {
                if(sCat !== 'all' && item.category !== sCat) return;
                if(sCat !== 'all' && sSub !== 'all' && item.subcategory !== sSub) return;
                if(!item[currentLang]) return;

                // 分類標題
                const cCat = item.category || "未分類";
                const cSub = item.subcategory || "";
                if(cCat !== lastCat || (cSub !== lastSub && cSub !== "")) {
                    const div = document.createElement('div');
                    div.className = 'category-header';
                    div.innerHTML = `${cCat} ${cSub ? '<i class="fas fa-angle-right" style="color:#ccc;margin:0 5px;"></i> '+cSub : ''}`;
                    container.appendChild(div);
                    lastCat = cCat; lastSub = cSub;
                }

                // 卡片
                const clicks = parseInt(localStorage.getItem('fte_'+item.id)||'0');
                const card = document.createElement('div');
                card.className = `card ${clicks>=10?'level-3':clicks>=3?'level-2':clicks>=1?'level-1':'level-0'}`;
                card.dataset.audio = item[currentLang].audio ? `${item[currentLang].folder}/${item[currentLang].audio}` : '';
                card.dataset.id = item.id;

                let footerText = `🇹🇼 ${item.cn}`;
                if(currentLang === 'CN_ZH') {
                    footerText = `🇺🇸 ${item.CN_ENG?.word || ''}`; 
                } else if (item.CN_ENG?.word) {
                    footerText += `<br><span style="color:#ccc;font-size:11px;">🇺🇸 ${item.CN_ENG.word}</span>`;
                }

                card.innerHTML = `
                    <div style="display:flex;justify-content:space-between;color:#ccc;font-size:10px;">
                        <span>${item.subcategory || item.category}</span>
                        <span class="click-cnt" style="background:#eee;padding:1px 6px;border-radius:10px;">${clicks}</span>
                    </div>
                    <div>
                        <div class="main-word">${item[currentLang].word}</div>
                        <div class="phonetic">${item[currentLang].phonetic || ""}</div>
                    </div>
                    <div class="footer-translation">${footerText}</div>
                `;

                card.onclick = () => {
                    if(isAutoPlaying) stopAutoPlay();
                    const src = card.dataset.audio;
                    if(src) {
                        globalPlayer.src = src;
                        globalPlayer.playbackRate = playbackSpeed;
                        globalPlayer.play();
                        // 點擊次數+1
                        const n = (parseInt(localStorage.getItem('fte_'+item.id)||'0')) + 1;
                        localStorage.setItem('fte_'+item.id, n);
                        card.querySelector('.click-cnt').innerText = n;
                        
                        card.classList.add('playing');
                        setTimeout(()=>card.classList.remove('playing'), 500);
                    }
                };
                container.appendChild(card);
            });
        }
    </script>
</body>
</html>