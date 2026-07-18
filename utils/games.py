"""
games.py
--------
Self-contained HTML/CSS/JS mini-games rendered inside Streamlit via
`st.components.v1.html`. Building these as plain client-side JS (instead of
pure Streamlit widgets) keeps the interactions smooth -- no page rerun on
every click/drag, which matters a lot for a "relaxing" game.
"""

BREATHING_HTML = """
<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
            font-family:'Segoe UI',sans-serif;padding:30px 10px;background:linear-gradient(160deg,#eaf6ff,#f3ecff);
            border-radius:20px;">
  <div id="circle" style="width:140px;height:140px;border-radius:50%;
            background:radial-gradient(circle at 35% 35%, #8ec5fc, #6a89ff);
            box-shadow:0 0 40px rgba(106,137,255,0.5);
            transition: transform 4s ease-in-out; display:flex;align-items:center;justify-content:center;
            color:white;font-size:18px;font-weight:600;text-align:center;">Get Ready</div>
  <p id="label" style="margin-top:28px;font-size:20px;color:#3b3b58;font-weight:600;">Press Start</p>
  <button id="startBtn" style="margin-top:10px;padding:10px 24px;border:none;border-radius:30px;
            background:#6a89ff;color:white;font-size:15px;cursor:pointer;">▶ Start Box Breathing</button>
  <p style="margin-top:16px;color:#666;font-size:13px;">4s in → 4s hold → 4s out → 4s hold (repeats)</p>
</div>
<script>
  const circle = document.getElementById('circle');
  const label = document.getElementById('label');
  const btn = document.getElementById('startBtn');
  let running = false;
  let phaseIndex = 0;
  const phases = [
    {text:'Breathe In...', scale:1.6},
    {text:'Hold...', scale:1.6},
    {text:'Breathe Out...', scale:1.0},
    {text:'Hold...', scale:1.0},
  ];

  function runPhase() {
    if (!running) return;
    const p = phases[phaseIndex % phases.length];
    label.innerText = p.text;
    circle.style.transform = 'scale(' + p.scale + ')';
    circle.innerText = p.text;
    phaseIndex++;
    setTimeout(runPhase, 4000);
  }

  btn.addEventListener('click', () => {
    if (!running) {
      running = true;
      phaseIndex = 0;
      btn.innerText = '⏸ Stop';
      runPhase();
    } else {
      running = false;
      btn.innerText = '▶ Start Box Breathing';
      label.innerText = 'Press Start';
      circle.style.transform = 'scale(1)';
      circle.innerText = 'Get Ready';
    }
  });
</script>
"""


BUBBLE_POP_HTML = """
<div style="font-family:'Segoe UI',sans-serif;text-align:center;padding:20px;
            background:linear-gradient(160deg,#fff3e0,#e0f7fa);border-radius:20px;">
  <h3 style="color:#37474f;margin-bottom:4px;">🫧 Bubble Pop</h3>
  <p style="color:#607d8b;margin-top:0;">Pop all the bubbles to relax. Score: <span id="score">0</span></p>
  <div id="grid" style="display:grid;grid-template-columns:repeat(8, 1fr);gap:10px;max-width:520px;margin:20px auto;"></div>
  <button id="resetBtn" style="padding:10px 22px;border:none;border-radius:30px;background:#26a69a;
            color:white;font-size:14px;cursor:pointer;">🔄 New Sheet</button>
</div>
<script>
  const grid = document.getElementById('grid');
  const scoreEl = document.getElementById('score');
  const resetBtn = document.getElementById('resetBtn');
  let score = 0;
  const colors = ['#ffcdd2','#c8e6c9','#bbdefb','#fff9c4','#e1bee7','#b2ebf2'];

  function buildGrid() {
    grid.innerHTML = '';
    score = 0;
    scoreEl.innerText = score;
    for (let i = 0; i < 32; i++) {
      const bubble = document.createElement('div');
      const color = colors[Math.floor(Math.random()*colors.length)];
      bubble.style.cssText = `
        width:52px;height:52px;border-radius:50%;background:${color};
        box-shadow:inset -4px -4px 8px rgba(0,0,0,0.08), 0 3px 6px rgba(0,0,0,0.15);
        cursor:pointer;transition:transform 0.15s ease;`;
      bubble.addEventListener('click', () => {
        if (bubble.dataset.popped) return;
        bubble.dataset.popped = '1';
        bubble.style.transform = 'scale(0)';
        bubble.style.boxShadow = 'none';
        score++;
        scoreEl.innerText = score;
      });
      grid.appendChild(bubble);
    }
  }
  resetBtn.addEventListener('click', buildGrid);
  buildGrid();
</script>
"""


DOODLE_PAD_HTML = """
<div style="font-family:'Segoe UI',sans-serif;text-align:center;padding:20px;
            background:linear-gradient(160deg,#f3e5f5,#e8f5e9);border-radius:20px;">
  <h3 style="color:#37474f;margin-bottom:10px;">🎨 Doodle Pad</h3>
  <div style="margin-bottom:12px;">
    <input type="color" id="colorPicker" value="#6a4cff" style="vertical-align:middle;">
    <input type="range" id="brush" min="1" max="30" value="5" style="vertical-align:middle;">
    <button id="clearBtn" style="padding:6px 16px;border:none;border-radius:20px;background:#ef5350;color:white;cursor:pointer;">Clear</button>
    <button id="downloadBtn" style="padding:6px 16px;border:none;border-radius:20px;background:#42a5f5;color:white;cursor:pointer;">Download PNG</button>
  </div>
  <canvas id="canvas" width="600" height="360" style="border-radius:14px;background:white;
            box-shadow:0 4px 14px rgba(0,0,0,0.12);cursor:crosshair;touch-action:none;"></canvas>
</div>
<script>
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');
  const colorPicker = document.getElementById('colorPicker');
  const brush = document.getElementById('brush');
  let drawing = false;

  function pos(e) {
    const rect = canvas.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    return {
      x: (clientX - rect.left) * (canvas.width / rect.width),
      y: (clientY - rect.top) * (canvas.height / rect.height)
    };
  }

  function start(e) {
    drawing = true;
    const p = pos(e);
    ctx.beginPath();
    ctx.moveTo(p.x, p.y);
    e.preventDefault();
  }
  function draw(e) {
    if (!drawing) return;
    const p = pos(e);
    ctx.lineTo(p.x, p.y);
    ctx.strokeStyle = colorPicker.value;
    ctx.lineWidth = brush.value;
    ctx.lineCap = 'round';
    ctx.stroke();
    e.preventDefault();
  }
  function stop() { drawing = false; }

  canvas.addEventListener('mousedown', start);
  canvas.addEventListener('mousemove', draw);
  canvas.addEventListener('mouseup', stop);
  canvas.addEventListener('mouseleave', stop);
  canvas.addEventListener('touchstart', start);
  canvas.addEventListener('touchmove', draw);
  canvas.addEventListener('touchend', stop);

  document.getElementById('clearBtn').addEventListener('click', () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  });
  document.getElementById('downloadBtn').addEventListener('click', () => {
    const link = document.createElement('a');
    link.download = 'my-doodle.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
  });
</script>
"""


MEMORY_GAME_HTML = """
<div style="font-family:'Segoe UI',sans-serif;text-align:center;padding:20px;
            background:linear-gradient(160deg,#e8f0fe,#fce4ec);border-radius:20px;">
  <h3 style="color:#37474f;margin-bottom:4px;">🧩 Memory Match</h3>
  <p style="color:#607d8b;margin-top:0;">Moves: <span id="moves">0</span> | Matches: <span id="matches">0</span>/8</p>
  <div id="board" style="display:grid;grid-template-columns:repeat(4, 70px);gap:10px;justify-content:center;margin:18px auto;"></div>
  <p id="winMsg" style="color:#2e7d32;font-weight:700;font-size:16px;height:20px;"></p>
  <button id="restartBtn" style="padding:10px 22px;border:none;border-radius:30px;background:#7e57c2;
            color:white;font-size:14px;cursor:pointer;">🔄 Restart</button>
</div>
<script>
  const board = document.getElementById('board');
  const movesEl = document.getElementById('moves');
  const matchesEl = document.getElementById('matches');
  const winMsg = document.getElementById('winMsg');
  const emojis = ['🌸','🌈','⭐','🍀','🌙','☀️','🎈','🦋'];

  let cards = [], flipped = [], matched = [], moves = 0, lock = false;

  function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  function buildBoard() {
    board.innerHTML = '';
    cards = shuffle([...emojis, ...emojis]);
    flipped = []; matched = []; moves = 0; lock = false;
    movesEl.innerText = moves;
    matchesEl.innerText = 0;
    winMsg.innerText = '';

    cards.forEach((emoji, idx) => {
      const card = document.createElement('div');
      card.dataset.emoji = emoji;
      card.dataset.idx = idx;
      card.style.cssText = `
        width:70px;height:70px;border-radius:12px;background:#5c6bc0;color:transparent;
        display:flex;align-items:center;justify-content:center;font-size:30px;cursor:pointer;
        box-shadow:0 3px 6px rgba(0,0,0,0.15);transition:transform 0.2s, background 0.2s;user-select:none;`;
      card.innerText = emoji;
      card.addEventListener('click', () => flipCard(card));
      board.appendChild(card);
    });
  }

  function flipCard(card) {
    if (lock || card.classList.contains('matched') || flipped.includes(card)) return;
    card.style.color = '#fff';
    card.style.background = '#26a69a';
    flipped.push(card);

    if (flipped.length === 2) {
      lock = true;
      moves++;
      movesEl.innerText = moves;
      const [a, b] = flipped;
      if (a.dataset.emoji === b.dataset.emoji) {
        a.classList.add('matched');
        b.classList.add('matched');
        a.style.background = '#66bb6a';
        b.style.background = '#66bb6a';
        matched.push(a, b);
        matchesEl.innerText = matched.length / 2;
        flipped = [];
        lock = false;
        if (matched.length === cards.length) {
          winMsg.innerText = '🎉 You matched them all in ' + moves + ' moves!';
        }
      } else {
        setTimeout(() => {
          a.style.color = 'transparent';
          b.style.color = 'transparent';
          a.style.background = '#5c6bc0';
          b.style.background = '#5c6bc0';
          flipped = [];
          lock = false;
        }, 700);
      }
    }
  }

  document.getElementById('restartBtn').addEventListener('click', buildBoard);
  buildBoard();
</script>
"""
