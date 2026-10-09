"""
games.py
--------
Self-contained, interactive HTML/CSS/JS relaxation mini-games rendered inside
Streamlit via `st.components.v1.html`.

Built specifically for students taking a break from study sessions, exams,
and screen fatigue. Every mini-game runs completely client-side with zero external
dependencies, fast load times, and smooth zero-rerun interactions.
"""

# ==============================================================================
# 1. GUIDED BOX BREATHING (STUDENT CALM EDITION)
# ==============================================================================
BREATHING_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
  body {
    background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 50%, #F5F3FF 100%);
    border-radius: 20px;
    padding: 30px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 380px;
    color: #1E293B;
  }
  .circle-container {
    position: relative;
    width: 200px;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 20px 0;
  }
  .outer-ring {
    position: absolute;
    width: 200px;
    height: 200px;
    border-radius: 50%;
    border: 2px dashed rgba(99, 102, 241, 0.3);
  }
  .orb {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #818CF8, #4F46E5);
    box-shadow: 0 0 35px rgba(99, 102, 241, 0.45), inset 0 0 15px rgba(255, 255, 255, 0.4);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    font-size: 16px;
    text-shadow: 0 1px 3px rgba(0,0,0,0.2);
    transition: transform 4s cubic-bezier(0.4, 0, 0.2, 1);
  }
  .phase-text {
    font-size: 20px;
    font-weight: 700;
    color: #312E81;
    margin-bottom: 6px;
    height: 28px;
  }
  .sub-text {
    font-size: 13px;
    color: #64748B;
    margin-bottom: 18px;
  }
  .btn {
    background: #4F46E5;
    color: white;
    border: none;
    padding: 11px 26px;
    border-radius: 9999px;
    font-weight: 600;
    font-size: 14px;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
    transition: all 0.2s;
  }
  .btn:hover {
    background: #4338CA;
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(79, 70, 229, 0.35);
  }
  .timer-count {
    font-size: 12px;
    opacity: 0.9;
    margin-top: 3px;
  }
  .pills {
    display: flex;
    gap: 8px;
    margin-top: 14px;
  }
  .pill {
    font-size: 11px;
    background: rgba(99, 102, 241, 0.12);
    color: #4338CA;
    padding: 3px 10px;
    border-radius: 12px;
    font-weight: 600;
  }
</style>
</head>
<body>
  <div class="phase-text" id="phaseText">Ready to reset?</div>
  <div class="sub-text">Box Breathing Technique • 4s In → 4s Hold → 4s Out → 4s Hold</div>
  
  <div class="circle-container">
    <div class="outer-ring"></div>
    <div class="orb" id="orb">
      <span id="orbText">Breathe</span>
      <span class="timer-count" id="timerCount">4s</span>
    </div>
  </div>

  <button class="btn" id="toggleBtn">▶ Start Breathing</button>

  <div class="pills">
    <span class="pill" id="p0">Inhale 4s</span>
    <span class="pill" id="p1">Hold 4s</span>
    <span class="pill" id="p2">Exhale 4s</span>
    <span class="pill" id="p3">Hold 4s</span>
  </div>

<script>
  const orb = document.getElementById('orb');
  const phaseText = document.getElementById('phaseText');
  const timerCount = document.getElementById('timerCount');
  const orbText = document.getElementById('orbText');
  const btn = document.getElementById('toggleBtn');
  const pills = [document.getElementById('p0'), document.getElementById('p1'), document.getElementById('p2'), document.getElementById('p3')];

  let running = false;
  let phaseIdx = 0;
  let countdown = 4;
  let timerInterval = null;

  const phases = [
    { title: "Breathe In Slowly...", orbMsg: "Inhale", scale: 1.55, bg: "radial-gradient(circle at 35% 35%, #818CF8, #4F46E5)" },
    { title: "Gently Hold...", orbMsg: "Hold", scale: 1.55, bg: "radial-gradient(circle at 35% 35%, #60A5FA, #2563EB)" },
    { title: "Slowly Exhale...", orbMsg: "Exhale", scale: 1.0, bg: "radial-gradient(circle at 35% 35%, #34D399, #059669)" },
    { title: "Rest & Hold...", orbMsg: "Pause", scale: 1.0, bg: "radial-gradient(circle at 35% 35%, #A78BFA, #7C3AED)" }
  ];

  function updatePills(idx) {
    pills.forEach((p, i) => {
      if (i === idx) {
        p.style.background = '#4F46E5';
        p.style.color = '#FFFFFF';
      } else {
        p.style.background = 'rgba(99, 102, 241, 0.12)';
        p.style.color = '#4338CA';
      }
    });
  }

  function nextPhase() {
    if (!running) return;
    const cur = phases[phaseIdx];
    phaseText.innerText = cur.title;
    orbText.innerText = cur.orbMsg;
    orb.style.transform = `scale(${cur.scale})`;
    orb.style.background = cur.bg;
    updatePills(phaseIdx);

    countdown = 4;
    timerCount.innerText = `${countdown}s`;

    phaseIdx = (phaseIdx + 1) % 4;
  }

  function start() {
    running = true;
    btn.innerText = '⏸ Pause Session';
    btn.style.background = '#64748B';
    phaseIdx = 0;
    nextPhase();

    timerInterval = setInterval(() => {
      countdown--;
      if (countdown <= 0) {
        nextPhase();
      } else {
        timerCount.innerText = `${countdown}s`;
      }
    }, 1000);
  }

  function stop() {
    running = false;
    clearInterval(timerInterval);
    btn.innerText = '▶ Start Breathing';
    btn.style.background = '#4F46E5';
    phaseText.innerText = 'Take a moment for yourself';
    orbText.innerText = 'Breathe';
    timerCount.innerText = '4s';
    orb.style.transform = 'scale(1)';
    orb.style.background = 'radial-gradient(circle at 35% 35%, #818CF8, #4F46E5)';
    pills.forEach(p => {
      p.style.background = 'rgba(99, 102, 241, 0.12)';
      p.style.color = '#4338CA';
    });
  }

  btn.addEventListener('click', () => {
    if (running) stop();
    else start();
  });
</script>
</body>
</html>
"""

# ==============================================================================
# 2. SATISFYING BUBBLE WRAP POP (WITH SYNTHETIC POP SOUND)
# ==============================================================================
BUBBLE_POP_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
  body {
    background: linear-gradient(135deg, #FEF3C7 0%, #FEE2E2 50%, #FDF4FF 100%);
    border-radius: 20px;
    padding: 24px;
    text-align: center;
    color: #1E293B;
  }
  .title-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 580px;
    margin: 0 auto 16px;
  }
  .badge {
    background: white;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    color: #D97706;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
  }
  .grid {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    gap: 12px;
    max-width: 580px;
    margin: 0 auto;
    padding: 16px;
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(8px);
    border-radius: 18px;
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.04);
  }
  .bubble {
    aspect-ratio: 1;
    border-radius: 50%;
    cursor: pointer;
    position: relative;
    transition: transform 0.12s ease, opacity 0.15s ease;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1), inset -3px -3px 6px rgba(0,0,0,0.1), inset 3px 3px 6px rgba(255,255,255,0.8);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .bubble::after {
    content: '';
    position: absolute;
    top: 15%;
    left: 20%;
    width: 25%;
    height: 25%;
    border-radius: 50%;
    background: rgba(255,255,255,0.75);
  }
  .bubble:hover {
    transform: scale(1.08);
  }
  .bubble.popped {
    transform: scale(0.75);
    opacity: 0.25;
    box-shadow: inset 2px 2px 4px rgba(0,0,0,0.2);
    cursor: default;
  }
  .bubble.popped::after {
    display: none;
  }
  .controls {
    margin-top: 18px;
    display: flex;
    justify-content: center;
    gap: 12px;
  }
  .btn {
    background: #D97706;
    color: white;
    border: none;
    padding: 9px 20px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(217, 119, 6, 0.25);
    transition: all 0.2s;
  }
  .btn:hover { background: #B45309; transform: translateY(-1px); }
  .sound-hint { font-size: 11px; color: #92400E; margin-top: 8px; opacity: 0.8; }
</style>
</head>
<body>
  <div class="title-bar">
    <div style="font-weight:700; color:#78350F; font-size:16px;">🫧 Study-Break Bubble Wrap</div>
    <div class="badge">Popped: <span id="score">0</span> / 40</div>
  </div>

  <div class="grid" id="grid"></div>

  <div class="controls">
    <button class="btn" id="newSheetBtn">🔄 Fresh Sheet</button>
  </div>
  <div class="sound-hint">🔊 Features procedural audio popping sounds! Click away.</div>

<script>
  const grid = document.getElementById('grid');
  const scoreEl = document.getElementById('score');
  const resetBtn = document.getElementById('newSheetBtn');
  let score = 0;
  let audioCtx = null;

  // Web Audio Synthetic Pop
  function playPopSound() {
    try {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      if (audioCtx.state === 'suspended') audioCtx.resume();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'sine';
      const freq = 450 + Math.random() * 250;
      osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(100, audioCtx.currentTime + 0.08);
      gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
      gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.08);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.08);
    } catch (e) {}
  }

  const colors = [
    'linear-gradient(135deg, #93C5FD, #60A5FA)',
    'linear-gradient(135deg, #A7F3D0, #34D399)',
    'linear-gradient(135deg, #FDE68A, #FBBF24)',
    'linear-gradient(135deg, #FBCFE8, #F472B6)',
    'linear-gradient(135deg, #C7D2FE, #818CF8)'
  ];

  function initGrid() {
    grid.innerHTML = '';
    score = 0;
    scoreEl.innerText = score;
    for (let i = 0; i < 40; i++) {
      const bubble = document.createElement('div');
      bubble.className = 'bubble';
      bubble.style.background = colors[i % colors.length];
      bubble.addEventListener('click', () => {
        if (bubble.classList.contains('popped')) return;
        bubble.classList.add('popped');
        playPopSound();
        score++;
        scoreEl.innerText = score;
      });
      grid.appendChild(bubble);
    }
  }

  resetBtn.addEventListener('click', initGrid);
  initGrid();
</script>
</body>
</html>
"""

# ==============================================================================
# 3. DOODLE & WHITEBOARD UNWIND
# ==============================================================================
DOODLE_PAD_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
  body {
    background: linear-gradient(135deg, #F0FDF4 0%, #E0F2FE 100%);
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    color: #1E293B;
  }
  .toolbar {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    background: white;
    padding: 10px 18px;
    border-radius: 16px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 14px;
    max-width: 650px;
    margin-left: auto;
    margin-right: auto;
  }
  .swatches {
    display: flex;
    gap: 6px;
    align-items: center;
  }
  .swatch {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    cursor: pointer;
    border: 2px solid white;
    box-shadow: 0 1px 4px rgba(0,0,0,0.2);
    transition: transform 0.15s;
  }
  .swatch:hover, .swatch.active {
    transform: scale(1.2);
  }
  canvas {
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.08);
    cursor: crosshair;
    touch-action: none;
    display: block;
    margin: 0 auto;
    border: 1px solid #E2E8F0;
  }
  .btn {
    border: none;
    padding: 7px 14px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }
  .btn-clear { background: #FEE2E2; color: #DC2626; }
  .btn-clear:hover { background: #FECACA; }
  .btn-save { background: #4F46E5; color: white; }
  .btn-save:hover { background: #4338CA; }
  .slider-label { font-size: 12px; font-weight: 600; color: #64748B; }
</style>
</head>
<body>
  <div class="toolbar">
    <div class="swatches">
      <div class="swatch active" style="background: #4F46E5;" data-color="#4F46E5"></div>
      <div class="swatch" style="background: #06B6D4;" data-color="#06B6D4"></div>
      <div class="swatch" style="background: #10B981;" data-color="#10B981"></div>
      <div class="swatch" style="background: #F59E0B;" data-color="#F59E0B"></div>
      <div class="swatch" style="background: #EC4899;" data-color="#EC4899"></div>
      <div class="swatch" style="background: #1E293B;" data-color="#1E293B"></div>
    </div>
    <span class="slider-label">Brush:</span>
    <input type="range" id="brushSize" min="2" max="25" value="6" style="width: 80px;">
    <button class="btn btn-clear" id="clearBtn">🧹 Clear</button>
    <button class="btn btn-save" id="saveBtn">📥 Save Doodle</button>
  </div>

  <canvas id="canvas" width="620" height="380"></canvas>

<script>
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');
  const brushSlider = document.getElementById('brushSize');
  const clearBtn = document.getElementById('clearBtn');
  const saveBtn = document.getElementById('saveBtn');
  const swatches = document.querySelectorAll('.swatch');

  let curColor = '#4F46E5';
  let painting = false;

  swatches.forEach(s => {
    s.addEventListener('click', () => {
      swatches.forEach(x => x.classList.remove('active'));
      s.classList.add('active');
      curColor = s.dataset.color;
    });
  });

  function getPos(e) {
    const rect = canvas.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    return {
      x: (clientX - rect.left) * (canvas.width / rect.width),
      y: (clientY - rect.top) * (canvas.height / rect.height)
    };
  }

  function start(e) {
    painting = true;
    const pos = getPos(e);
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
    e.preventDefault();
  }

  function draw(e) {
    if (!painting) return;
    const pos = getPos(e);
    ctx.lineTo(pos.x, pos.y);
    ctx.strokeStyle = curColor;
    ctx.lineWidth = brushSlider.value;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.stroke();
    e.preventDefault();
  }

  function stop() { painting = false; }

  canvas.addEventListener('mousedown', start);
  canvas.addEventListener('mousemove', draw);
  canvas.addEventListener('mouseup', stop);
  canvas.addEventListener('mouseleave', stop);

  canvas.addEventListener('touchstart', start);
  canvas.addEventListener('touchmove', draw);
  canvas.addEventListener('touchend', stop);

  clearBtn.addEventListener('click', () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  });

  saveBtn.addEventListener('click', () => {
    const link = document.createElement('a');
    link.download = 'study-doodle.png';
    link.href = canvas.toDataURL();
    link.click();
  });
</script>
</body>
</html>
"""

# ==============================================================================
# 4. STUDENT MEMORY MATCH (RELAXING CAMPUS ICONS)
# ==============================================================================
MEMORY_GAME_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
  body {
    background: linear-gradient(135deg, #F3E8FF 0%, #EDE9FE 50%, #E0E7FF 100%);
    border-radius: 20px;
    padding: 24px;
    text-align: center;
    color: #1E293B;
  }
  .stats-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 440px;
    margin: 0 auto 16px;
    font-size: 14px;
    font-weight: 600;
    color: #5B21B6;
  }
  .board {
    display: grid;
    grid-template-columns: repeat(4, 75px);
    gap: 12px;
    justify-content: center;
    margin: 0 auto;
  }
  .card {
    width: 75px;
    height: 75px;
    border-radius: 14px;
    background: #6D28D9;
    color: transparent;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    cursor: pointer;
    box-shadow: 0 4px 10px rgba(109, 40, 217, 0.25);
    user-select: none;
    transition: transform 0.25s, background 0.2s, color 0.2s;
  }
  .card:hover {
    transform: translateY(-2px);
  }
  .card.flipped {
    background: #FFFFFF;
    color: inherit;
    transform: rotateY(180deg);
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  }
  .card.matched {
    background: #10B981 !important;
    color: white !important;
    cursor: default;
    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
  }
  .win-banner {
    color: #047857;
    font-weight: 700;
    font-size: 15px;
    margin-top: 14px;
    min-height: 22px;
  }
  .btn {
    background: #6D28D9;
    color: white;
    border: none;
    padding: 8px 22px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    margin-top: 10px;
    transition: all 0.2s;
  }
  .btn:hover { background: #5B21B6; }
</style>
</head>
<body>
  <div class="stats-bar">
    <div>Moves: <span id="moves">0</span></div>
    <div>Matches: <span id="matches">0</span> / 8</div>
  </div>

  <div class="board" id="board"></div>
  <div class="win-banner" id="winBanner"></div>
  <button class="btn" id="restartBtn">🔄 Shuffle & Play</button>

<script>
  const board = document.getElementById('board');
  const movesEl = document.getElementById('moves');
  const matchesEl = document.getElementById('matches');
  const winBanner = document.getElementById('winBanner');
  const restartBtn = document.getElementById('restartBtn');

  const icons = ['☕', '🎧', '📚', '🌱', '🌙', '🎨', '🪐', '🫧'];
  let cards = [];
  let flipped = [];
  let matched = [];
  let moves = 0;
  let lock = false;

  function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  function initGame() {
    board.innerHTML = '';
    cards = shuffle([...icons, ...icons]);
    flipped = [];
    matched = [];
    moves = 0;
    lock = false;
    movesEl.innerText = moves;
    matchesEl.innerText = 0;
    winBanner.innerText = '';

    cards.forEach((icon, idx) => {
      const c = document.createElement('div');
      c.className = 'card';
      c.dataset.icon = icon;
      c.innerText = icon;
      c.addEventListener('click', () => onCardClick(c));
      board.appendChild(c);
    });
  }

  function onCardClick(c) {
    if (lock || c.classList.contains('flipped') || c.classList.contains('matched')) return;
    c.classList.add('flipped');
    flipped.push(c);

    if (flipped.length === 2) {
      lock = true;
      moves++;
      movesEl.innerText = moves;
      const [a, b] = flipped;

      if (a.dataset.icon === b.dataset.icon) {
        a.classList.add('matched');
        b.classList.add('matched');
        matched.push(a, b);
        matchesEl.innerText = matched.length / 2;
        flipped = [];
        lock = false;
        if (matched.length === cards.length) {
          winBanner.innerText = `🎉 You cleared the board in ${moves} moves! Brain reset complete.`;
        }
      } else {
        setTimeout(() => {
          a.classList.remove('flipped');
          b.classList.remove('flipped');
          flipped = [];
          lock = false;
        }, 750);
      }
    }
  }

  restartBtn.addEventListener('click', initGame);
  initGame();
</script>
</body>
</html>
"""

# ==============================================================================
# 5. NEW: PROCEDURAL STUDY SOUNDSCAPE MIXER (100% OFFLINE WEB AUDIO SYNTH)
# ==============================================================================
SOUNDSCAPE_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
  body {
    background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%);
    border-radius: 20px;
    padding: 24px;
    color: #F8FAFC;
    text-align: center;
  }
  .header {
    margin-bottom: 20px;
  }
  .title {
    font-size: 18px;
    font-weight: 700;
    color: #C7D2FE;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }
  .subtitle {
    font-size: 12px;
    color: #94A3B8;
    margin-top: 4px;
  }
  .mixer-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
    max-width: 580px;
    margin: 0 auto 18px;
  }
  .channel-card {
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 14px;
    padding: 14px;
    text-align: left;
    backdrop-filter: blur(10px);
    transition: border-color 0.2s;
  }
  .channel-card.active {
    border-color: #818CF8;
    box-shadow: 0 0 16px rgba(129, 140, 248, 0.2);
  }
  .card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }
  .channel-name {
    font-size: 14px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .toggle-btn {
    background: #334155;
    color: #94A3B8;
    border: none;
    padding: 5px 12px;
    border-radius: 9999px;
    font-size: 11px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s;
  }
  .toggle-btn.on {
    background: #4F46E5;
    color: white;
  }
  .slider-row {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  input[type="range"] {
    flex: 1;
    accent-color: #818CF8;
    cursor: pointer;
  }
  .footer-note {
    font-size: 11px;
    color: #64748B;
  }
</style>
</head>
<body>
  <div class="header">
    <div class="title">🎧 Campus Study Soundscape Mixer</div>
    <div class="subtitle">Procedurally synthesized white noise & nature vibes. Zero loading time, 100% offline.</div>
  </div>

  <div class="mixer-grid">
    <!-- Channel 1: Rain -->
    <div class="channel-card" id="cardRain">
      <div class="card-top">
        <span class="channel-name">🌧️ Rain on Window</span>
        <button class="toggle-btn" id="btnRain">OFF</button>
      </div>
      <div class="slider-row">
        <span style="font-size: 12px; opacity:0.7;">Vol</span>
        <input type="range" id="volRain" min="0" max="1" step="0.05" value="0.4">
      </div>
    </div>

    <!-- Channel 2: Cozy Hearth -->
    <div class="channel-card" id="cardFire">
      <div class="card-top">
        <span class="channel-name">🔥 Cozy Hearth</span>
        <button class="toggle-btn" id="btnFire">OFF</button>
      </div>
      <div class="slider-row">
        <span style="font-size: 12px; opacity:0.7;">Vol</span>
        <input type="range" id="volFire" min="0" max="1" step="0.05" value="0.4">
      </div>
    </div>

    <!-- Channel 3: Ocean Waves -->
    <div class="channel-card" id="cardOcean">
      <div class="card-top">
        <span class="channel-name">🌊 Ocean Drift</span>
        <button class="toggle-btn" id="btnOcean">OFF</button>
      </div>
      <div class="slider-row">
        <span style="font-size: 12px; opacity:0.7;">Vol</span>
        <input type="range" id="volOcean" min="0" max="1" step="0.05" value="0.35">
      </div>
    </div>

    <!-- Channel 4: Summer Night Crickets -->
    <div class="channel-card" id="cardNight">
      <div class="card-top">
        <span class="channel-name">🦗 Campus Crickets</span>
        <button class="toggle-btn" id="btnNight">OFF</button>
      </div>
      <div class="slider-row">
        <span style="font-size: 12px; opacity:0.7;">Vol</span>
        <input type="range" id="volNight" min="0" max="1" step="0.05" value="0.3">
      </div>
    </div>
  </div>

  <div class="footer-note">
    💡 Put on your headphones and blend rain + hearth for maximum focus while studying.
  </div>

<script>
  let ctx = null;

  function ensureCtx() {
    if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
    if (ctx.state === 'suspended') ctx.resume();
  }

  // --- Rain Generator (Filtered Pink Noise) ---
  let rainNode = null, rainGain = null;
  function startRain() {
    ensureCtx();
    const bufferSize = ctx.sampleRate * 2;
    const noiseBuffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    let b0 = 0, b1 = 0, b2 = 0;
    for (let i = 0; i < bufferSize; i++) {
      const white = Math.random() * 2 - 1;
      b0 = 0.99886 * b0 + white * 0.0555179;
      b1 = 0.99332 * b1 + white * 0.0750759;
      b2 = 0.96900 * b2 + white * 0.1538520;
      output[i] = (b0 + b1 + b2 + white * 0.1) * 0.15;
    }
    rainNode = ctx.createBufferSource();
    rainNode.buffer = noiseBuffer;
    rainNode.loop = true;

    const filter = ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = 1000;

    rainGain = ctx.createGain();
    rainGain.gain.value = parseFloat(document.getElementById('volRain').value);

    rainNode.connect(filter);
    filter.connect(rainGain);
    rainGain.connect(ctx.destination);
    rainNode.start();
  }
  function stopRain() {
    if (rainNode) { rainNode.stop(); rainNode.disconnect(); rainNode = null; }
  }

  // --- Fireplace Generator (Low-pass + random crackle impulses) ---
  let fireNode = null, fireGain = null, fireInterval = null;
  function startFire() {
    ensureCtx();
    const bufferSize = ctx.sampleRate * 2;
    const noiseBuffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) { output[i] = (Math.random() * 2 - 1) * 0.2; }
    fireNode = ctx.createBufferSource();
    fireNode.buffer = noiseBuffer;
    fireNode.loop = true;

    const filter = ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = 350;

    fireGain = ctx.createGain();
    fireGain.gain.value = parseFloat(document.getElementById('volFire').value);

    fireNode.connect(filter);
    filter.connect(fireGain);
    fireGain.connect(ctx.destination);
    fireNode.start();

    // Occasional subtle wood crackle
    fireInterval = setInterval(() => {
      if (Math.random() > 0.4) {
        try {
          const osc = ctx.createOscillator();
          const popGain = ctx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(200 + Math.random() * 400, ctx.currentTime);
          popGain.gain.setValueAtTime(fireGain.gain.value * 0.4, ctx.currentTime);
          popGain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.05);
          osc.connect(popGain);
          popGain.connect(ctx.destination);
          osc.start();
          osc.stop(ctx.currentTime + 0.05);
        } catch(e){}
      }
    }, 180);
  }
  function stopFire() {
    if (fireNode) { fireNode.stop(); fireNode.disconnect(); fireNode = null; }
    if (fireInterval) { clearInterval(fireInterval); fireInterval = null; }
  }

  // --- Ocean Wave Generator (Modulated Pink Noise) ---
  let oceanNode = null, oceanGain = null, oceanLfo = null;
  function startOcean() {
    ensureCtx();
    const bufferSize = ctx.sampleRate * 2;
    const buf = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
    const data = buf.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) { data[i] = (Math.random() * 2 - 1) * 0.3; }
    oceanNode = ctx.createBufferSource();
    oceanNode.buffer = buf;
    oceanNode.loop = true;

    const filter = ctx.createBiquadFilter();
    filter.type = 'bandpass';
    filter.frequency.value = 450;
    filter.Q.value = 1.0;

    oceanGain = ctx.createGain();
    oceanGain.gain.value = parseFloat(document.getElementById('volOcean').value);

    // LFO for periodic wave swell
    oceanLfo = ctx.createOscillator();
    const lfoGain = ctx.createGain();
    oceanLfo.frequency.value = 0.12; // 8-second gentle swell cycle
    lfoGain.gain.value = 300;
    oceanLfo.connect(lfoGain);
    lfoGain.connect(filter.frequency);
    oceanLfo.start();

    oceanNode.connect(filter);
    filter.connect(oceanGain);
    oceanGain.connect(ctx.destination);
    oceanNode.start();
  }
  function stopOcean() {
    if (oceanNode) { oceanNode.stop(); oceanNode.disconnect(); oceanNode = null; }
    if (oceanLfo) { oceanLfo.stop(); oceanLfo.disconnect(); oceanLfo = null; }
  }

  // --- Crickets Night Generator ---
  let cricketsInterval = null, nightGainVal = 0.3;
  function startNight() {
    ensureCtx();
    nightGainVal = parseFloat(document.getElementById('volNight').value);
    cricketsInterval = setInterval(() => {
      try {
        const osc = ctx.createOscillator();
        const g = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(4500, ctx.currentTime);
        g.gain.setValueAtTime(nightGainVal * 0.15, ctx.currentTime);
        g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.08);
        osc.connect(g);
        g.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.08);
      } catch(e){}
    }, 450);
  }
  function stopNight() {
    if (cricketsInterval) { clearInterval(cricketsInterval); cricketsInterval = null; }
  }

  // UI Event bindings
  function setupChannel(btnId, cardId, sliderId, startFn, stopFn, updateGainFn) {
    const btn = document.getElementById(btnId);
    const card = document.getElementById(cardId);
    const slider = document.getElementById(sliderId);
    let active = false;

    btn.addEventListener('click', () => {
      active = !active;
      if (active) {
        startFn();
        btn.innerText = 'ON';
        btn.classList.add('on');
        card.classList.add('active');
      } else {
        stopFn();
        btn.innerText = 'OFF';
        btn.classList.remove('on');
        card.classList.remove('active');
      }
    });

    slider.addEventListener('input', (e) => {
      if (updateGainFn) updateGainFn(parseFloat(e.target.value));
    });
  }

  setupChannel('btnRain', 'cardRain', 'volRain', startRain, stopRain, (v) => { if(rainGain) rainGain.gain.value = v; });
  setupChannel('btnFire', 'cardFire', 'volFire', startFire, stopFire, (v) => { if(fireGain) fireGain.gain.value = v; });
  setupChannel('btnOcean', 'cardOcean', 'volOcean', startOcean, stopOcean, (v) => { if(oceanGain) oceanGain.gain.value = v; });
  setupChannel('btnNight', 'cardNight', 'volNight', startNight, stopNight, (v) => { nightGainVal = v; });
</script>
</body>
</html>
"""

# ==============================================================================
# 6. NEW: ZEN SAND GARDEN & RIVER STONES
# ==============================================================================
ZEN_GARDEN_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
  body {
    background: linear-gradient(135deg, #FDF4E3 0%, #F5E6CC 100%);
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    color: #451A03;
  }
  .controls {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    margin-bottom: 14px;
    flex-wrap: wrap;
  }
  .tool-btn {
    background: #FFFBEB;
    border: 1px solid #FDE68A;
    color: #78350F;
    padding: 7px 15px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    transition: all 0.2s;
  }
  .tool-btn.active {
    background: #78350F;
    color: white;
    border-color: #78350F;
  }
  canvas {
    background: #EED9B7;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(69, 26, 3, 0.15), inset 0 2px 6px rgba(0,0,0,0.08);
    cursor: grab;
    display: block;
    margin: 0 auto;
    touch-action: none;
    border: 6px solid #D7BA8E;
  }
  .hint {
    font-size: 12px;
    color: #92400E;
    margin-top: 10px;
  }
</style>
</head>
<body>
  <div class="controls">
    <button class="tool-btn active" data-tool="rake">🪵 Zen Rake</button>
    <button class="tool-btn" data-tool="stone">🪨 River Stone</button>
    <button class="tool-btn" data-tool="sakura">🌸 Sakura Petal</button>
    <button class="tool-btn" id="smoothBtn">🧹 Smooth Sand</button>
  </div>

  <canvas id="sandCanvas" width="600" height="360"></canvas>
  <div class="hint">Drag your cursor or finger to rake soothing sand lines, or tap to place stones & petals.</div>

<script>
  const canvas = document.getElementById('sandCanvas');
  const ctx = canvas.getContext('2d');
  const toolBtns = document.querySelectorAll('.tool-btn[data-tool]');
  const smoothBtn = document.getElementById('smoothBtn');

  let curTool = 'rake';
  let dragging = false;
  let lastPos = null;

  function initSand() {
    ctx.fillStyle = '#EED9B7';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Subtle grain texture
    ctx.fillStyle = 'rgba(120, 53, 15, 0.03)';
    for (let i = 0; i < 4000; i++) {
      ctx.fillRect(Math.random() * canvas.width, Math.random() * canvas.height, 2, 2);
    }
  }

  toolBtns.forEach(b => {
    b.addEventListener('click', () => {
      toolBtns.forEach(x => x.classList.remove('active'));
      b.classList.add('active');
      curTool = b.dataset.tool;
    });
  });

  smoothBtn.addEventListener('click', initSand);

  function getPos(e) {
    const rect = canvas.getBoundingClientRect();
    const cx = e.touches ? e.touches[0].clientX : e.clientX;
    const cy = e.touches ? e.touches[0].clientY : e.clientY;
    return {
      x: (cx - rect.left) * (canvas.width / rect.width),
      y: (cy - rect.top) * (canvas.height / rect.height)
    };
  }

  function drawRake(p1, p2) {
    const offsets = [-10, 0, 10];
    offsets.forEach(off => {
      ctx.beginPath();
      ctx.moveTo(p1.x + off, p1.y);
      ctx.lineTo(p2.x + off, p2.y);
      ctx.strokeStyle = '#D4BC96';
      ctx.lineWidth = 4;
      ctx.lineCap = 'round';
      ctx.stroke();

      // Shadow side
      ctx.beginPath();
      ctx.moveTo(p1.x + off + 1, p1.y + 1);
      ctx.lineTo(p2.x + off + 1, p2.y + 1);
      ctx.strokeStyle = 'rgba(92, 40, 10, 0.15)';
      ctx.lineWidth = 2;
      ctx.stroke();
    });
  }

  function placeStone(p) {
    ctx.save();
    ctx.shadowColor = 'rgba(0, 0, 0, 0.25)';
    ctx.shadowBlur = 10;
    ctx.shadowOffsetX = 3;
    ctx.shadowOffsetY = 4;

    const grad = ctx.createRadialGradient(p.x - 5, p.y - 5, 2, p.x, p.y, 22);
    grad.addColorStop(0, '#57534E');
    grad.addColorStop(1, '#292524');

    ctx.beginPath();
    ctx.ellipse(p.x, p.y, 20 + Math.random()*5, 14 + Math.random()*4, Math.random()*Math.PI, 0, Math.PI * 2);
    ctx.fillStyle = grad;
    ctx.fill();
    ctx.restore();
  }

  function placeSakura(p) {
    ctx.save();
    ctx.fillStyle = '#F472B6';
    ctx.beginPath();
    ctx.ellipse(p.x, p.y, 9, 5, Math.random() * Math.PI, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }

  canvas.addEventListener('mousedown', (e) => {
    dragging = true;
    lastPos = getPos(e);
    if (curTool === 'stone') placeStone(lastPos);
    if (curTool === 'sakura') placeSakura(lastPos);
  });

  canvas.addEventListener('mousemove', (e) => {
    if (!dragging) return;
    const curPos = getPos(e);
    if (curTool === 'rake' && lastPos) {
      drawRake(lastPos, curPos);
    }
    lastPos = curPos;
  });

  canvas.addEventListener('mouseup', () => { dragging = false; lastPos = null; });
  canvas.addEventListener('mouseleave', () => { dragging = false; lastPos = null; });

  canvas.addEventListener('touchstart', (e) => {
    dragging = true;
    lastPos = getPos(e);
    if (curTool === 'stone') placeStone(lastPos);
    if (curTool === 'sakura') placeSakura(lastPos);
    e.preventDefault();
  });
  canvas.addEventListener('touchmove', (e) => {
    if (!dragging) return;
    const curPos = getPos(e);
    if (curTool === 'rake' && lastPos) {
      drawRake(lastPos, curPos);
    }
    lastPos = curPos;
    e.preventDefault();
  });
  canvas.addEventListener('touchend', () => { dragging = false; });

  initSand();
</script>
</body>
</html>
"""

# ==============================================================================
# 7. NEW: STUDENT FORTUNE COOKIE & AFFIRMATION JAR
# ==============================================================================
FORTUNE_COOKIE_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
  body {
    background: linear-gradient(135deg, #FFF1F2 0%, #FFE4E6 50%, #FDF2F8 100%);
    border-radius: 20px;
    padding: 24px;
    text-align: center;
    color: #881337;
  }
  .cookie-box {
    margin: 20px auto;
    width: 140px;
    height: 140px;
    cursor: pointer;
    font-size: 85px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    user-select: none;
  }
  .cookie-box:hover {
    transform: scale(1.12) rotate(4deg);
  }
  .cookie-box:active {
    transform: scale(0.95);
  }
  .slip {
    background: #FFFFFF;
    border: 1px solid #FECDD3;
    border-radius: 14px;
    padding: 16px 20px;
    max-width: 520px;
    margin: 0 auto 16px;
    box-shadow: 0 4px 14px rgba(225, 29, 72, 0.08);
    min-height: 70px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 600;
    color: #9F1239;
    line-height: 1.5;
    transition: all 0.3s ease;
  }
  .counter {
    font-size: 12px;
    color: #BE123C;
    font-weight: 600;
    margin-bottom: 10px;
  }
  .btn {
    background: #E11D48;
    color: white;
    border: none;
    padding: 9px 22px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(225, 29, 72, 0.25);
    transition: all 0.2s;
  }
  .btn:hover { background: #BE123C; }
</style>
</head>
<body>
  <div style="font-weight: 700; font-size: 17px; color: #9F1239;">🥠 Student Affirmation Cookie</div>
  <div class="counter">Tap the cookie to break it open & get your reminder!</div>

  <div class="cookie-box" id="cookieIcon">🥠</div>

  <div class="slip" id="slipText">
    "Click the cookie above to reveal a supportive campus thought."
  </div>

  <button class="btn" id="crackBtn">✨ Crack Another Cookie</button>

<script>
  const cookie = document.getElementById('cookieIcon');
  const slip = document.getElementById('slipText');
  const btn = document.getElementById('crackBtn');

  const affirmations = [
    "Your worth is not defined by a single exam or assignment grade.",
    "Rest is not a reward you earn; it is a basic human necessity to think clearly.",
    "Take it one task at a time. The mountain gets climbed one step per hour.",
    "Everyone else in class looks like they have it together, but they're figuring it out too.",
    "Submitting an 80% effort today is infinitely better than burning out chasing 100%.",
    "Don't trade your physical or mental health for a temporary semester deadline.",
    "Remember: You've made it through every single high-stress week before this one.",
    "Step away from the screen for 5 minutes. Drink water and let your shoulders drop.",
    "A difficult professor or tough exam does not define your intelligence.",
    "It's completely okay to ask a friend or senior for help when you're stuck.",
    "Give yourself credit for simply showing up and trying today."
  ];

  let openedCount = 0;

  function crackCookie() {
    cookie.style.transform = 'scale(0.85) rotate(-15deg)';
    setTimeout(() => {
      cookie.style.transform = 'scale(1.15) rotate(10deg)';
      const randomMsg = affirmations[Math.floor(Math.random() * affirmations.length)];
      slip.style.opacity = '0';
      setTimeout(() => {
        slip.innerText = `"${randomMsg}"`;
        slip.style.opacity = '1';
      }, 150);
      openedCount++;
    }, 120);
    setTimeout(() => {
      cookie.style.transform = 'scale(1) rotate(0deg)';
    }, 300);
  }

  cookie.addEventListener('click', crackCookie);
  btn.addEventListener('click', crackCookie);
</script>
</body>
</html>
"""

# ==============================================================================
# 8. NEW: ZEN WATER RIPPLE & FLOATING LOTUS POND
# ==============================================================================
RIPPLE_POND_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
  body {
    background: linear-gradient(135deg, #042F2E 0%, #0F172A 100%);
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    color: #CCFBF1;
  }
  .header {
    margin-bottom: 12px;
  }
  .title {
    font-size: 16px;
    font-weight: 700;
    color: #5EEAD4;
  }
  .subtitle {
    font-size: 12px;
    color: #99F6E4;
    opacity: 0.8;
  }
  canvas {
    background: radial-gradient(circle at 50% 50%, #115E59, #042F2E);
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4), inset 0 0 40px rgba(94, 234, 212, 0.1);
    cursor: pointer;
    display: block;
    margin: 0 auto;
    touch-action: none;
    border: 2px solid rgba(94, 234, 212, 0.2);
  }
  .hint {
    font-size: 11px;
    color: #5EEAD4;
    margin-top: 10px;
    opacity: 0.7;
  }
</style>
</head>
<body>
  <div class="header">
    <div class="title">🌊 Calming Ripple Pond</div>
    <div class="subtitle">Click or drag across the water surface to generate expanding ripples.</div>
  </div>

  <canvas id="pondCanvas" width="600" height="350"></canvas>
  <div class="hint">Watch the ripples expand and dissolve smoothly into the pond.</div>

<script>
  const canvas = document.getElementById('pondCanvas');
  const ctx = canvas.getContext('2d');

  let ripples = [];
  const lotuses = [
    { x: 140, y: 120, r: 18, angle: 0 },
    { x: 440, y: 220, r: 24, angle: 1.2 },
    { x: 280, y: 260, r: 16, angle: 2.5 }
  ];

  function addRipple(x, y) {
    ripples.push({
      x: x,
      y: y,
      radius: 4,
      maxRadius: 85 + Math.random() * 30,
      alpha: 0.9,
      speed: 1.8
    });
  }

  function getPos(e) {
    const rect = canvas.getBoundingClientRect();
    const cx = e.touches ? e.touches[0].clientX : e.clientX;
    const cy = e.touches ? e.touches[0].clientY : e.clientY;
    return {
      x: (cx - rect.left) * (canvas.width / rect.width),
      y: (cy - rect.top) * (canvas.height / rect.height)
    };
  }

  canvas.addEventListener('mousedown', (e) => {
    const p = getPos(e);
    addRipple(p.x, p.y);
  });

  canvas.addEventListener('mousemove', (e) => {
    if (Math.random() > 0.85) {
      const p = getPos(e);
      addRipple(p.x, p.y);
    }
  });

  canvas.addEventListener('touchstart', (e) => {
    const p = getPos(e);
    addRipple(p.x, p.y);
    e.preventDefault();
  });

  function drawLotus(l) {
    ctx.save();
    ctx.translate(l.x, l.y);
    ctx.rotate(l.angle);

    // Green Lily pad
    ctx.fillStyle = '#065F46';
    ctx.beginPath();
    ctx.arc(0, 0, l.r, 0.2, Math.PI * 1.9);
    ctx.lineTo(0, 0);
    ctx.closePath();
    ctx.fill();

    // Floating pink flower
    ctx.fillStyle = '#F472B6';
    for (let i = 0; i < 6; i++) {
      ctx.rotate((Math.PI * 2) / 6);
      ctx.beginPath();
      ctx.ellipse(l.r * 0.4, 0, 7, 3, 0, 0, Math.PI * 2);
      ctx.fill();
    }
    // Flower center
    ctx.fillStyle = '#FDE047';
    ctx.beginPath();
    ctx.arc(0, 0, 4, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();
  }

  function animate() {
    // Semi-clear trail for dreamy depth
    ctx.fillStyle = 'rgba(4, 47, 46, 0.3)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Update & draw lotuses (gentle drift)
    lotuses.forEach(l => {
      l.angle += 0.003;
      drawLotus(l);
    });

    // Update ripples
    for (let i = ripples.length - 1; i >= 0; i--) {
      const r = ripples[i];
      r.radius += r.speed;
      r.alpha *= 0.965;

      ctx.beginPath();
      ctx.arc(r.x, r.y, r.radius, 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(94, 234, 212, ${r.alpha})`;
      ctx.lineWidth = 2.5;
      ctx.stroke();

      // Secondary echo ripple
      if (r.radius > 16) {
        ctx.beginPath();
        ctx.arc(r.x, r.y, r.radius - 12, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(45, 212, 191, ${r.alpha * 0.5})`;
        ctx.lineWidth = 1.5;
        ctx.stroke();
      }

      if (r.alpha < 0.02 || r.radius > r.maxRadius) {
        ripples.splice(i, 1);
      }
    }

    requestAnimationFrame(animate);
  }

  animate();
</script>
</body>
</html>
"""
