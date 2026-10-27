/**
 * RETRO FLASH GAMES ARCADE STUDIO
 * Golden-Era Flash & Miniclip Style Web Arcade
 * Features 6 fully interactive HTML5 Canvas games with real-time Web Audio 8-bit sound synthesis.
 */

(function() {
    'use strict';

    // ==========================================
    // 1. RETRO 8-BIT AUDIO SYNTHESIZER
    // ==========================================
    class RetroAudioSynth {
        constructor() {
            this.ctx = null;
            this.muted = false;
        }

        init() {
            if (!this.ctx) {
                const AudioCtx = window.AudioContext || window.webkitAudioContext;
                if (AudioCtx) {
                    this.ctx = new AudioCtx();
                }
            }
            if (this.ctx && this.ctx.state === 'suspended') {
                this.ctx.resume();
            }
        }

        playTone(freq, duration, type = 'square', gainStart = 0.15, gainEnd = 0.001) {
            if (this.muted) return;
            try {
                this.init();
                if (!this.ctx) return;
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();

                osc.type = type;
                osc.frequency.setValueAtTime(freq, this.ctx.currentTime);

                gain.gain.setValueAtTime(gainStart, this.ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(gainEnd, this.ctx.currentTime + duration);

                osc.connect(gain);
                gain.connect(this.ctx.destination);

                osc.start();
                osc.stop(this.ctx.currentTime + duration);
            } catch (e) {
                // AudioContext autoplay restrictions
            }
        }

        playCoin() {
            if (this.muted) return;
            this.playTone(987.77, 0.08, 'sine', 0.2); // B5
            setTimeout(() => this.playTone(1318.51, 0.18, 'sine', 0.2), 80); // E6
        }

        playJump() {
            if (this.muted) return;
            try {
                this.init();
                if (!this.ctx) return;
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(160, this.ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(450, this.ctx.currentTime + 0.12);
                gain.gain.setValueAtTime(0.18, this.ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.12);
                osc.connect(gain);
                gain.connect(this.ctx.destination);
                osc.start();
                osc.stop(this.ctx.currentTime + 0.12);
            } catch (e) {}
        }

        playLaser() {
            if (this.muted) return;
            try {
                this.init();
                if (!this.ctx) return;
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(880, this.ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(110, this.ctx.currentTime + 0.09);
                gain.gain.setValueAtTime(0.15, this.ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.09);
                osc.connect(gain);
                gain.connect(this.ctx.destination);
                osc.start();
                osc.stop(this.ctx.currentTime + 0.09);
            } catch (e) {}
        }

        playHit() {
            if (this.muted) return;
            this.playTone(220, 0.06, 'square', 0.2, 0.01);
        }

        playExplosion() {
            if (this.muted) return;
            try {
                this.init();
                if (!this.ctx) return;
                const bufferSize = this.ctx.sampleRate * 0.25;
                const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
                const data = buffer.getChannelData(0);
                for (let i = 0; i < bufferSize; i++) {
                    data[i] = Math.random() * 2 - 1;
                }
                const noise = this.ctx.createBufferSource();
                noise.buffer = buffer;
                const gain = this.ctx.createGain();
                gain.gain.setValueAtTime(0.3, this.ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.25);
                noise.connect(gain);
                gain.connect(this.ctx.destination);
                noise.start();
            } catch (e) {
                this.playTone(80, 0.25, 'sawtooth', 0.25);
            }
        }

        playGameOver() {
            if (this.muted) return;
            const notes = [330, 293, 261, 196];
            notes.forEach((freq, i) => {
                setTimeout(() => this.playTone(freq, 0.18, 'sawtooth', 0.15), i * 140);
            });
        }

        playVictory() {
            if (this.muted) return;
            const notes = [523.25, 659.25, 783.99, 1046.50];
            notes.forEach((freq, i) => {
                setTimeout(() => this.playTone(freq, 0.15, 'sine', 0.2), i * 110);
            });
        }
    }

    const audio = new RetroAudioSynth();

    // ==========================================
    // 2. GAMES REGISTRY & CONFIGURATION
    // ==========================================
    const GAMES_CATALOG = [
        {
            id: 'snake',
            title: 'Cyber Snake 2099',
            category: 'RETRO',
            category_name: 'Retro Classics',
            icon: '🐍',
            badge: 'NOKIA & FLASH HIT',
            tagline: 'Guide the glowing energy serpent across the cyber grid without crashing into walls or your own tail.',
            difficulty: 'Medium',
            controls: 'Arrow Keys / WASD / D-Pad',
            color: '#10b981',
            accent: '#059669',
            multiplier: '1.5x',
            actionName: 'BOOST'
        },
        {
            id: 'flappy',
            title: 'Motivation Falcon / Flappy Boost',
            category: 'ACTION',
            category_name: 'Action & Reflex',
            icon: '🚀',
            badge: 'MINICLIP REFLEX HIT',
            tagline: 'Fire thrusters to navigate through doubt pillars and collect stoic discipline fuel cores.',
            difficulty: 'Hard',
            controls: 'Spacebar / Click / Tap to Boost',
            color: '#f59e0b',
            accent: '#d97706',
            multiplier: '2.0x',
            actionName: 'BOOST'
        },
        {
            id: 'breakout',
            title: 'Neon Brick Breaker DX',
            category: 'SKILL',
            category_name: 'Skill & Precision',
            icon: '🧱',
            badge: 'ARKANOID DX',
            tagline: 'Deflect the high-velocity energy sphere to shatter rows of multi-colored neon bricks.',
            difficulty: 'Medium',
            controls: 'Mouse Move / Left-Right Arrows / Touch',
            color: '#f43f5e',
            accent: '#e11d48',
            multiplier: '1.8x',
            actionName: 'LAUNCH'
        },
        {
            id: 'matrix2048',
            title: '2048 Cyber Matrix',
            category: 'PUZZLE',
            category_name: 'Puzzle & Logic',
            icon: '🔢',
            badge: 'LOGIC MASTER',
            tagline: 'Slide and merge matching number power cells until you reach the legendary 2048 Core.',
            difficulty: 'Brain Teaser',
            controls: 'Arrow Keys / Swipe / Virtual D-Pad',
            color: '#8b5cf6',
            accent: '#7c3aed',
            multiplier: '1.2x',
            actionName: 'SLIDE'
        },
        {
            id: 'asteroids',
            title: 'Meteor Defender 360',
            category: 'ACTION',
            category_name: 'Action & Reflex',
            icon: '🛸',
            badge: 'VECTOR ARCADE 1982',
            tagline: 'Pilot your vector ship in zero-G, rotate 360° and blast splitting meteors.',
            difficulty: 'Challenging',
            controls: 'Left/Right to Turn, Up/W to Thrust, Space to Shoot',
            color: '#06b6d4',
            accent: '#0891b2',
            multiplier: '2.5x',
            actionName: 'SHOOT'
        },
        {
            id: 'memory',
            title: 'Cyber Hologram Match',
            category: 'PUZZLE',
            category_name: 'Puzzle & Logic',
            icon: '💎',
            badge: 'MIND RETENTION',
            tagline: 'Flip holographic cards, find identical symbol pairs in minimum moves and time.',
            difficulty: 'Relaxing',
            controls: 'Mouse Click / Touch',
            color: '#ec4899',
            accent: '#db2777',
            multiplier: '1.0x',
            actionName: 'FLIP'
        }
    ];

    // ==========================================
    // 3. ARCADE STUDIO MASTER CONTROLLER
    // ==========================================
    class ArcadeStudioManager {
        constructor() {
            this.activeGameId = 'snake';
            this.activeCategory = 'ALL';
            this.canvas = null;
            this.ctx = null;
            this.animFrameId = null;
            this.score = 0;
            this.highScores = {};
            this.gameState = 'START'; // 'START', 'PLAYING', 'PAUSED', 'GAMEOVER'
            this.currentGame = null;
            this.crtActive = true;
            this.theaterActive = false;
        }

        init() {
            this.canvas = document.getElementById('arcadeGameCanvas');
            if (!this.canvas) return;
            this.ctx = this.canvas.getContext('2d');

            this.loadStoredSettings();
            this.fetchHighScores();
            this.renderGameCards();
            this.bindEvents();
            this.loadGame(this.activeGameId);
        }

        loadStoredSettings() {
            const savedCrt = localStorage.getItem('arcade_crt');
            if (savedCrt !== null) {
                this.crtActive = savedCrt === 'true';
            }
            const overlay = document.getElementById('arcadeCrtOverlay');
            if (overlay) {
                overlay.classList.toggle('active', this.crtActive);
            }
            const crtBtn = document.getElementById('arcadeCrtToggleBtn');
            if (crtBtn) crtBtn.textContent = `📺 CRT: ${this.crtActive ? 'ON' : 'OFF'}`;

            const savedMuted = localStorage.getItem('arcade_muted');
            if (savedMuted !== null) {
                audio.muted = savedMuted === 'true';
                const soundBtn = document.getElementById('arcadeSoundToggleBtn');
                if (soundBtn) soundBtn.textContent = `🔊 Sound: ${audio.muted ? 'OFF' : 'ON'}`;
            }

            try {
                const localScores = localStorage.getItem('arcade_high_scores');
                if (localScores) {
                    this.highScores = JSON.parse(localScores);
                }
            } catch (e) {}
        }

        async fetchHighScores() {
            try {
                const res = await fetch('/api/arcade/scores');
                if (res.ok) {
                    const data = await res.json();
                    for (const [gid, record] of Object.entries(data)) {
                        const localVal = this.highScores[gid] || 0;
                        this.highScores[gid] = Math.max(localVal, record.score || 0);
                    }
                    this.updateScoreHud();
                    this.renderGameCards();
                }
            } catch (e) {
                // Offline fallback
            }
        }

        saveHighScore(gameId, newScore) {
            const curr = this.highScores[gameId] || 0;
            if (newScore > curr) {
                this.highScores[gameId] = newScore;
                localStorage.setItem('arcade_high_scores', JSON.stringify(this.highScores));
                this.updateScoreHud();
                this.renderGameCards();

                // Send to backend
                fetch('/api/arcade/scores', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ game_id: gameId, score: newScore, player: 'Gamer' })
                }).catch(() => {});
                return true;
            }
            return false;
        }

        getHighScore(gameId) {
            return this.highScores[gameId] || 0;
        }

        updateScoreHud() {
            const curEl = document.getElementById('arcadeCurrentScore');
            const highEl = document.getElementById('arcadeHighScore');
            if (curEl) curEl.textContent = this.score;
            if (highEl) highEl.textContent = this.getHighScore(this.activeGameId);
        }

        bindEvents() {
            // Category Tabs
            const catTabs = document.querySelectorAll('#arcadeCategoryTabs .arcade-cat-tab');
            catTabs.forEach(tab => {
                tab.addEventListener('click', () => {
                    catTabs.forEach(t => t.classList.remove('active'));
                    tab.classList.add('active');
                    this.activeCategory = tab.getAttribute('data-arcade-cat');
                    this.renderGameCards();
                });
            });

            // Marquee Tools
            const soundBtn = document.getElementById('arcadeSoundToggleBtn');
            if (soundBtn) {
                soundBtn.addEventListener('click', () => {
                    audio.muted = !audio.muted;
                    localStorage.setItem('arcade_muted', audio.muted);
                    soundBtn.textContent = `🔊 Sound: ${audio.muted ? 'OFF' : 'ON'}`;
                });
            }

            const crtBtn = document.getElementById('arcadeCrtToggleBtn');
            if (crtBtn) {
                crtBtn.addEventListener('click', () => {
                    this.crtActive = !this.crtActive;
                    localStorage.setItem('arcade_crt', this.crtActive);
                    const overlay = document.getElementById('arcadeCrtOverlay');
                    if (overlay) overlay.classList.toggle('active', this.crtActive);
                    crtBtn.textContent = `📺 CRT: ${this.crtActive ? 'ON' : 'OFF'}`;
                });
            }

            const pauseBtn = document.getElementById('arcadePauseBtn');
            if (pauseBtn) {
                pauseBtn.addEventListener('click', () => this.togglePause());
            }

            const restartBtn = document.getElementById('arcadeRestartBtn');
            if (restartBtn) {
                restartBtn.addEventListener('click', () => this.restartGame());
            }

            const theaterBtn = document.getElementById('toggleArcadeTheaterBtn');
            if (theaterBtn) {
                theaterBtn.addEventListener('click', () => {
                    this.theaterActive = !this.theaterActive;
                    const container = document.querySelector('.main-container');
                    if (container) {
                        container.classList.toggle('arcade-theater-active', this.theaterActive);
                    }
                    theaterBtn.textContent = this.theaterActive ? '🗗 Standard View' : '⛶ Theater Mode';
                });
            }

            // Overlay Dialog Play Button
            const playBtn = document.getElementById('overlayPlayBtn');
            if (playBtn) {
                playBtn.addEventListener('click', () => {
                    audio.init();
                    if (this.gameState === 'PAUSED') {
                        this.togglePause();
                    } else {
                        this.startGame();
                    }
                });
            }

            // Overlay "Make Reel" Button
            const makeReelBtn = document.getElementById('overlayMakeReelBtn');
            if (makeReelBtn) {
                makeReelBtn.addEventListener('click', () => this.bridgeScoreToReel());
            }

            // Bridge Banner Button
            const bridgeBtn = document.getElementById('bridgeCreateReelBtn');
            if (bridgeBtn) {
                bridgeBtn.addEventListener('click', () => this.bridgeScoreToReel());
            }

            // Keyboard Dispatcher
            window.addEventListener('keydown', (e) => {
                // If focus is in an input or textarea, ignore
                if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) return;

                if (e.key === 'p' || e.key === 'P') {
                    this.togglePause();
                    e.preventDefault();
                    return;
                }
                if (e.key === ' ' || e.code === 'Space') {
                    if (this.gameState === 'START' || this.gameState === 'GAMEOVER') {
                        audio.init();
                        this.startGame();
                        e.preventDefault();
                        return;
                    }
                }
                if (this.currentGame && typeof this.currentGame.onKeyDown === 'function') {
                    this.currentGame.onKeyDown(e);
                }
            });

            window.addEventListener('keyup', (e) => {
                if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) return;
                if (this.currentGame && typeof this.currentGame.onKeyUp === 'function') {
                    this.currentGame.onKeyUp(e);
                }
            });

            // Virtual Controls
            this.bindVirtualControls();
        }

        bindVirtualControls() {
            const sendDir = (dir) => {
                if (this.currentGame && typeof this.currentGame.onDirection === 'function') {
                    this.currentGame.onDirection(dir);
                }
            };
            const btnUp = document.getElementById('vbtnUp');
            const btnDown = document.getElementById('vbtnDown');
            const btnLeft = document.getElementById('vbtnLeft');
            const btnRight = document.getElementById('vbtnRight');
            const btnA = document.getElementById('vbtnActionA');
            const btnB = document.getElementById('vbtnActionB');

            if (btnUp) btnUp.addEventListener('click', () => sendDir('UP'));
            if (btnDown) btnDown.addEventListener('click', () => sendDir('DOWN'));
            if (btnLeft) btnLeft.addEventListener('click', () => sendDir('LEFT'));
            if (btnRight) btnRight.addEventListener('click', () => sendDir('RIGHT'));

            if (btnA) {
                btnA.addEventListener('click', () => {
                    audio.init();
                    if (this.gameState === 'START' || this.gameState === 'GAMEOVER') {
                        this.startGame();
                    } else if (this.currentGame && typeof this.currentGame.onActionA === 'function') {
                        this.currentGame.onActionA();
                    }
                });
            }

            if (btnB) {
                btnB.addEventListener('click', () => {
                    audio.init();
                    if (this.currentGame && typeof this.currentGame.onActionB === 'function') {
                        this.currentGame.onActionB();
                    }
                });
            }

            // Mouse / Touch Drag for Breakout or cards
            this.canvas.addEventListener('mousemove', (e) => {
                if (this.currentGame && typeof this.currentGame.onMouseMove === 'function') {
                    const rect = this.canvas.getBoundingClientRect();
                    const scaleX = this.canvas.width / rect.width;
                    const scaleY = this.canvas.height / rect.height;
                    const x = (e.clientX - rect.left) * scaleX;
                    const y = (e.clientY - rect.top) * scaleY;
                    this.currentGame.onMouseMove(x, y);
                }
            });

            this.canvas.addEventListener('touchmove', (e) => {
                if (this.currentGame && typeof this.currentGame.onMouseMove === 'function' && e.touches.length > 0) {
                    const rect = this.canvas.getBoundingClientRect();
                    const scaleX = this.canvas.width / rect.width;
                    const scaleY = this.canvas.height / rect.height;
                    const x = (e.touches[0].clientX - rect.left) * scaleX;
                    const y = (e.touches[0].clientY - rect.top) * scaleY;
                    this.currentGame.onMouseMove(x, y);
                    e.preventDefault();
                }
            }, { passive: false });

            this.canvas.addEventListener('click', (e) => {
                audio.init();
                if (this.gameState === 'START') {
                    this.startGame();
                    return;
                }
                if (this.currentGame && typeof this.currentGame.onClick === 'function') {
                    const rect = this.canvas.getBoundingClientRect();
                    const scaleX = this.canvas.width / rect.width;
                    const scaleY = this.canvas.height / rect.height;
                    const x = (e.clientX - rect.left) * scaleX;
                    const y = (e.clientY - rect.top) * scaleY;
                    this.currentGame.onClick(x, y);
                }
            });
        }

        renderGameCards() {
            const grid = document.getElementById('arcadeGamesGrid');
            if (!grid) return;
            grid.innerHTML = '';

            const filtered = this.activeCategory === 'ALL'
                ? GAMES_CATALOG
                : GAMES_CATALOG.filter(g => g.category === this.activeCategory);

            filtered.forEach(game => {
                const high = this.getHighScore(game.id);
                const isActive = game.id === this.activeGameId;
                const card = document.createElement('div');
                card.className = `arcade-game-card ${isActive ? 'active-cartridge' : ''}`;
                card.style.setProperty('--card-accent', game.color);

                card.innerHTML = `
                    <div>
                        <div class="card-top-row">
                            <span class="card-game-icon">${game.icon}</span>
                            <span class="card-nostalgia-badge">${game.badge}</span>
                        </div>
                        <h4 class="card-game-title">${game.title}</h4>
                        <p class="card-game-desc">${game.tagline}</p>
                    </div>
                    <div>
                        <div class="card-game-meta">
                            <span class="meta-diff">★ ${game.difficulty}</span>
                            <span class="meta-record">BEST: ${high}</span>
                        </div>
                        <button class="btn-play-cartridge" data-game-id="${game.id}">
                            <span>${isActive ? '▶ Currently Loaded' : '▶ Insert Cartridge'}</span>
                        </button>
                    </div>
                `;

                card.addEventListener('click', (e) => {
                    this.loadGame(game.id);
                    document.getElementById('arcadeCabinetWrapper').scrollIntoView({ behavior: 'smooth' });
                });

                grid.appendChild(card);
            });
        }

        loadGame(gameId) {
            const gameDef = GAMES_CATALOG.find(g => g.id === gameId);
            if (!gameDef) return;

            this.activeGameId = gameId;
            this.score = 0;
            this.gameState = 'START';

            // Update Marquee & Badge
            const titleEl = document.getElementById('cabinetGameTitle');
            const badgeEl = document.getElementById('cabinetNostalgiaBadge');
            const topBadge = document.getElementById('arcadeActiveGameBadge');
            const actionLbl = document.getElementById('vbtnActionLabel');
            const controlsText = document.getElementById('cabinetControlsText');

            if (titleEl) titleEl.textContent = gameDef.title.toUpperCase();
            if (badgeEl) badgeEl.textContent = gameDef.badge;
            if (topBadge) topBadge.textContent = gameDef.title.toUpperCase();
            if (actionLbl) actionLbl.textContent = gameDef.actionName || 'SPACE';
            if (controlsText) controlsText.innerHTML = `Controls: <strong>${gameDef.controls}</strong>. Press <strong>P</strong> to Pause.`;

            this.updateScoreHud();
            this.renderGameCards();

            // Instantiate Engine
            if (this.animFrameId) {
                cancelAnimationFrame(this.animFrameId);
                this.animFrameId = null;
            }

            if (gameId === 'snake') {
                this.currentGame = new SnakeGame(this);
            } else if (gameId === 'flappy') {
                this.currentGame = new FlappyGame(this);
            } else if (gameId === 'breakout') {
                this.currentGame = new BreakoutGame(this);
            } else if (gameId === 'matrix2048') {
                this.currentGame = new Matrix2048Game(this);
            } else if (gameId === 'asteroids') {
                this.currentGame = new AsteroidsGame(this);
            } else if (gameId === 'memory') {
                this.currentGame = new MemoryGame(this);
            }

            this.showOverlay(
                gameDef.icon,
                gameDef.title.toUpperCase(),
                gameDef.tagline,
                'START GAME / INSERT COIN (SPACE)',
                false
            );

            // Draw initial frame
            this.currentGame.draw(this.ctx);
        }

        startGame() {
            this.score = 0;
            this.gameState = 'PLAYING';
            this.hideOverlay();
            this.updateScoreHud();

            if (this.currentGame) {
                this.currentGame.reset();
            }

            const loop = (timestamp) => {
                if (this.gameState === 'PLAYING') {
                    this.currentGame.update();
                    this.currentGame.draw(this.ctx);
                    this.animFrameId = requestAnimationFrame(loop);
                }
            };
            this.animFrameId = requestAnimationFrame(loop);
        }

        togglePause() {
            if (this.gameState === 'PLAYING') {
                this.gameState = 'PAUSED';
                if (this.animFrameId) cancelAnimationFrame(this.animFrameId);
                this.showOverlay('⏸️', 'GAME PAUSED', 'Press P or Click Resume to continue your run.', 'RESUME GAME (P)', false);
            } else if (this.gameState === 'PAUSED') {
                this.gameState = 'PLAYING';
                this.hideOverlay();
                const loop = () => {
                    if (this.gameState === 'PLAYING') {
                        this.currentGame.update();
                        this.currentGame.draw(this.ctx);
                        this.animFrameId = requestAnimationFrame(loop);
                    }
                };
                this.animFrameId = requestAnimationFrame(loop);
            }
        }

        restartGame() {
            audio.init();
            this.startGame();
        }

        gameOver(finalScore) {
            this.score = finalScore;
            this.gameState = 'GAMEOVER';
            if (this.animFrameId) cancelAnimationFrame(this.animFrameId);

            const isNewHigh = this.saveHighScore(this.activeGameId, finalScore);
            audio.playGameOver();

            const gameDef = GAMES_CATALOG.find(g => g.id === this.activeGameId);
            const high = this.getHighScore(this.activeGameId);

            this.showOverlay(
                isNewHigh ? '🏆' : '💀',
                isNewHigh ? 'NEW HIGH SCORE!' : 'GAME OVER',
                isNewHigh ? `Incredible reflex! You conquered the arcade record in ${gameDef.title}!` : `Great run! Every loss is just another step towards mastery.`,
                'INSERT COIN / PLAY AGAIN (SPACE)',
                true,
                finalScore,
                high
            );
        }

        showOverlay(icon, title, subtitle, btnText, showScores = false, finalScore = 0, highScore = 0) {
            const overlay = document.getElementById('arcadeOverlay');
            if (!overlay) return;
            overlay.style.display = 'flex';

            document.getElementById('overlayIcon').textContent = icon;
            document.getElementById('overlayTitle').textContent = title;
            document.getElementById('overlaySubtitle').textContent = subtitle;
            document.getElementById('overlayPlayBtnText').textContent = btnText;

            const scoreBox = document.getElementById('overlayScoreBox');
            const makeReelBtn = document.getElementById('overlayMakeReelBtn');

            if (showScores) {
                scoreBox.style.display = 'flex';
                document.getElementById('overlayFinalScore').textContent = finalScore;
                document.getElementById('overlayHighScore').textContent = highScore;
                makeReelBtn.style.display = 'block';
            } else {
                scoreBox.style.display = 'none';
                makeReelBtn.style.display = 'none';
            }
        }

        hideOverlay() {
            const overlay = document.getElementById('arcadeOverlay');
            if (overlay) overlay.style.display = 'none';
        }

        bridgeScoreToReel() {
            const gameDef = GAMES_CATALOG.find(g => g.id === this.activeGameId);
            const scoreVal = this.score || this.getHighScore(this.activeGameId) || 100;
            const topic = `THE WARRIOR REFLEX: ${gameDef.title.toUpperCase()}`;
            const promptText = `High score achieved in ${gameDef.title} (${scoreVal} points). True mastery in gaming, business, and discipline isn't about avoiding failure—it is about getting back up, hitting restart, and conquering doubt. The real victory is consistency.`;

            if (typeof window.prefillStoryPrompt === 'function') {
                window.prefillStoryPrompt(topic, promptText, 'MOTIVATION');
            } else if (typeof window.switchStudioMode === 'function') {
                window.switchStudioMode('story');
            }
        }

        onPanelOpened() {
            if (this.canvas) {
                // Focus and re-draw current frame
                if (this.currentGame) {
                    this.currentGame.draw(this.ctx);
                }
            }
        }
    }

    // ==========================================
    // 4. GAME 1: CYBER SNAKE 2099
    // ==========================================
    class SnakeGame {
        constructor(manager) {
            this.manager = manager;
            this.grid = 20;
            this.cols = 32;
            this.rows = 24;
            this.reset();
        }

        reset() {
            this.snake = [
                { x: 10, y: 12 },
                { x: 9, y: 12 },
                { x: 8, y: 12 }
            ];
            this.dir = { x: 1, y: 0 };
            this.nextDir = { x: 1, y: 0 };
            this.score = 0;
            this.speed = 95; // ms per tick
            this.lastTick = 0;
            this.particles = [];
            this.spawnFood();
        }

        spawnFood() {
            let valid = false;
            while (!valid) {
                this.food = {
                    x: Math.floor(Math.random() * this.cols),
                    y: Math.floor(Math.random() * this.rows)
                };
                valid = !this.snake.some(s => s.x === this.food.x && s.y === this.food.y);
            }
        }

        onKeyDown(e) {
            if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') {
                if (this.dir.y === 0) this.nextDir = { x: 0, y: -1 };
                e.preventDefault();
            } else if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') {
                if (this.dir.y === 0) this.nextDir = { x: 0, y: 1 };
                e.preventDefault();
            } else if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') {
                if (this.dir.x === 0) this.nextDir = { x: -1, y: 0 };
                e.preventDefault();
            } else if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') {
                if (this.dir.x === 0) this.nextDir = { x: 1, y: 0 };
                e.preventDefault();
            }
        }

        onDirection(dir) {
            if (dir === 'UP' && this.dir.y === 0) this.nextDir = { x: 0, y: -1 };
            if (dir === 'DOWN' && this.dir.y === 0) this.nextDir = { x: 0, y: 1 };
            if (dir === 'LEFT' && this.dir.x === 0) this.nextDir = { x: -1, y: 0 };
            if (dir === 'RIGHT' && this.dir.x === 0) this.nextDir = { x: 1, y: 0 };
        }

        update() {
            const now = performance.now();
            if (now - this.lastTick < this.speed) return;
            this.lastTick = now;

            this.dir = { ...this.nextDir };
            const head = { x: this.snake[0].x + this.dir.x, y: this.snake[0].y + this.dir.y };

            // Wall Collision
            if (head.x < 0 || head.x >= this.cols || head.y < 0 || head.y >= this.rows) {
                audio.playExplosion();
                this.manager.gameOver(this.score);
                return;
            }

            // Self Collision
            if (this.snake.some(s => s.x === head.x && s.y === head.y)) {
                audio.playExplosion();
                this.manager.gameOver(this.score);
                return;
            }

            this.snake.unshift(head);

            // Eat Food
            if (head.x === this.food.x && head.y === this.food.y) {
                this.score += 10;
                this.manager.score = this.score;
                this.manager.updateScoreHud();
                audio.playCoin();
                this.speed = Math.max(50, 95 - Math.floor(this.score / 30) * 4);

                // Spawn Particles
                for (let i = 0; i < 12; i++) {
                    const ang = Math.random() * Math.PI * 2;
                    const spd = Math.random() * 3 + 1;
                    this.particles.push({
                        x: head.x * this.grid + 10,
                        y: head.y * this.grid + 10,
                        vx: Math.cos(ang) * spd,
                        vy: Math.sin(ang) * spd,
                        life: 1,
                        color: '#10b981'
                    });
                }
                this.spawnFood();
            } else {
                this.snake.pop();
            }
        }

        draw(ctx) {
            ctx.fillStyle = '#070a0f';
            ctx.fillRect(0, 0, 640, 480);

            // Subtle Cyber Grid
            ctx.strokeStyle = 'rgba(16, 185, 129, 0.05)';
            ctx.lineWidth = 1;
            for (let x = 0; x < 640; x += this.grid) {
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, 480);
                ctx.stroke();
            }
            for (let y = 0; y < 480; y += this.grid) {
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(640, y);
                ctx.stroke();
            }

            // Food Orb with Pulse
            if (this.food) {
                const fx = this.food.x * this.grid + 10;
                const fy = this.food.y * this.grid + 10;
                const pulse = Math.sin(performance.now() * 0.008) * 2;

                ctx.shadowColor = '#f59e0b';
                ctx.shadowBlur = 12;
                ctx.fillStyle = '#fbbf24';
                ctx.beginPath();
                ctx.arc(fx, fy, 7 + pulse, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = '#fff';
                ctx.beginPath();
                ctx.arc(fx - 2, fy - 2, 2.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.shadowBlur = 0;
            }

            // Snake Body
            this.snake.forEach((seg, idx) => {
                const sx = seg.x * this.grid + 1;
                const sy = seg.y * this.grid + 1;
                const isHead = idx === 0;

                ctx.shadowColor = isHead ? '#34d399' : '#059669';
                ctx.shadowBlur = isHead ? 10 : 4;

                ctx.fillStyle = isHead ? '#10b981' : `hsl(155, 80%, ${Math.max(25, 55 - idx * 1.5)}%)`;
                ctx.beginPath();
                ctx.roundRect(sx, sy, 18, 18, isHead ? 6 : 4);
                ctx.fill();
                ctx.shadowBlur = 0;

                // Eyes on head
                if (isHead) {
                    ctx.fillStyle = '#fff';
                    ctx.beginPath();
                    ctx.arc(sx + 5, sy + 5, 2, 0, Math.PI * 2);
                    ctx.arc(sx + 13, sy + 5, 2, 0, Math.PI * 2);
                    ctx.fill();
                }
            });

            // Particles
            for (let i = this.particles.length - 1; i >= 0; i--) {
                const p = this.particles[i];
                p.x += p.vx;
                p.y += p.vy;
                p.life -= 0.05;
                if (p.life <= 0) {
                    this.particles.splice(i, 1);
                    continue;
                }
                ctx.fillStyle = p.color;
                ctx.globalAlpha = p.life;
                ctx.beginPath();
                ctx.arc(p.x, p.y, 2.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.globalAlpha = 1;
            }
        }
    }

    // ==========================================
    // 5. GAME 2: MOTIVATION FALCON / FLAPPY BOOST
    // ==========================================
    class FlappyGame {
        constructor(manager) {
            this.manager = manager;
            this.reset();
        }

        reset() {
            this.falcon = {
                x: 120,
                y: 220,
                vy: 0,
                gravity: 0.38,
                lift: -6.8,
                width: 32,
                height: 24,
                angle: 0
            };
            this.pipes = [];
            this.pipeTimer = 0;
            this.pipeInterval = 100; // frames
            this.stars = [];
            this.particles = [];
            this.score = 0;
            this.speed = 2.8;
        }

        onKeyDown(e) {
            if (e.key === ' ' || e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') {
                this.boost();
                e.preventDefault();
            }
        }

        onActionA() {
            this.boost();
        }

        onClick() {
            this.boost();
        }

        boost() {
            this.falcon.vy = this.falcon.lift;
            audio.playJump();

            // Thruster fire particles
            for (let i = 0; i < 6; i++) {
                this.particles.push({
                    x: this.falcon.x - 12,
                    y: this.falcon.y + (Math.random() * 8 - 4),
                    vx: -(Math.random() * 3 + 2),
                    vy: Math.random() * 2 - 1,
                    life: 1,
                    color: Math.random() > 0.5 ? '#f59e0b' : '#ef4444'
                });
            }
        }

        update() {
            const f = this.falcon;
            f.vy += f.gravity;
            f.y += f.vy;
            f.angle = Math.min(Math.PI / 4, Math.max(-Math.PI / 4, f.vy * 0.08));

            // Ground & Ceiling
            if (f.y < 0 || f.y + f.height > 480) {
                audio.playExplosion();
                this.manager.gameOver(this.score);
                return;
            }

            // Spawn Pipes
            this.pipeTimer++;
            if (this.pipeTimer >= this.pipeInterval) {
                this.pipeTimer = 0;
                const gap = 135;
                const topH = Math.floor(Math.random() * 200) + 50;
                const bottomY = topH + gap;
                this.pipes.push({
                    x: 640,
                    topH: topH,
                    bottomY: bottomY,
                    width: 55,
                    passed: false
                });

                // Spawn star in gap
                this.stars.push({
                    x: 640 + 27,
                    y: topH + gap / 2,
                    collected: false
                });
            }

            // Update Pipes & Collisions
            for (let i = this.pipes.length - 1; i >= 0; i--) {
                const p = this.pipes[i];
                p.x -= this.speed;

                // Check Falcon Collision
                if (
                    f.x + f.width > p.x &&
                    f.x < p.x + p.width &&
                    (f.y < p.topH || f.y + f.height > p.bottomY)
                ) {
                    audio.playExplosion();
                    this.manager.gameOver(this.score);
                    return;
                }

                // Passed Pipe
                if (!p.passed && p.x + p.width < f.x) {
                    p.passed = true;
                    this.score += 1;
                    this.manager.score = this.score;
                    this.manager.updateScoreHud();
                    audio.playCoin();
                }

                if (p.x + p.width < -10) {
                    this.pipes.splice(i, 1);
                }
            }

            // Collect Stars
            for (let i = this.stars.length - 1; i >= 0; i--) {
                const s = this.stars[i];
                s.x -= this.speed;
                const dx = s.x - (f.x + 16);
                const dy = s.y - (f.y + 12);
                if (!s.collected && Math.hypot(dx, dy) < 26) {
                    s.collected = true;
                    this.score += 2;
                    this.manager.score = this.score;
                    this.manager.updateScoreHud();
                    audio.playVictory();
                }
                if (s.x < -20 || s.collected) {
                    this.stars.splice(i, 1);
                }
            }
        }

        draw(ctx) {
            ctx.fillStyle = '#090d16';
            ctx.fillRect(0, 0, 640, 480);

            // Neon City Silhouette Backdrop
            ctx.fillStyle = 'rgba(255, 255, 255, 0.03)';
            for (let bx = 0; bx < 640; bx += 40) {
                ctx.fillRect(bx, 360 - (bx % 90), 35, 120 + (bx % 90));
            }

            // Pipes (Doubt Pillars)
            this.pipes.forEach(p => {
                ctx.shadowColor = '#06b6d4';
                ctx.shadowBlur = 10;
                ctx.fillStyle = '#0e2333';
                ctx.strokeStyle = '#06b6d4';
                ctx.lineWidth = 2;

                // Top Pipe
                ctx.fillRect(p.x, 0, p.width, p.topH);
                ctx.strokeRect(p.x, 0, p.width, p.topH);
                // Top Cap
                ctx.fillStyle = '#153a54';
                ctx.fillRect(p.x - 4, p.topH - 20, p.width + 8, 20);
                ctx.strokeRect(p.x - 4, p.topH - 20, p.width + 8, 20);

                // Bottom Pipe
                ctx.fillStyle = '#0e2333';
                ctx.fillRect(p.x, p.bottomY, p.width, 480 - p.bottomY);
                ctx.strokeRect(p.x, p.bottomY, p.width, 480 - p.bottomY);
                // Bottom Cap
                ctx.fillStyle = '#153a54';
                ctx.fillRect(p.x - 4, p.bottomY, p.width + 8, 20);
                ctx.strokeRect(p.x - 4, p.bottomY, p.width + 8, 20);

                ctx.shadowBlur = 0;
            });

            // Stars
            this.stars.forEach(s => {
                if (s.collected) return;
                ctx.shadowColor = '#f59e0b';
                ctx.shadowBlur = 12;
                ctx.fillStyle = '#fbbf24';
                ctx.beginPath();
                ctx.arc(s.x, s.y, 8, 0, Math.PI * 2);
                ctx.fill();
                ctx.shadowBlur = 0;
            });

            // Particles (Thruster fire)
            for (let i = this.particles.length - 1; i >= 0; i--) {
                const p = this.particles[i];
                p.x += p.vx;
                p.y += p.vy;
                p.life -= 0.04;
                if (p.life <= 0) {
                    this.particles.splice(i, 1);
                    continue;
                }
                ctx.fillStyle = p.color;
                ctx.globalAlpha = p.life;
                ctx.beginPath();
                ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
                ctx.fill();
                ctx.globalAlpha = 1;
            }

            // Falcon / Rocket Ship
            const f = this.falcon;
            ctx.save();
            ctx.translate(f.x + f.width / 2, f.y + f.height / 2);
            ctx.rotate(f.angle);

            // Rocket Body
            ctx.shadowColor = '#f59e0b';
            ctx.shadowBlur = 10;
            ctx.fillStyle = '#f8fafc';
            ctx.beginPath();
            ctx.ellipse(0, 0, 16, 9, 0, 0, Math.PI * 2);
            ctx.fill();

            // Fins
            ctx.fillStyle = '#ef4444';
            ctx.beginPath();
            ctx.moveTo(-8, -9);
            ctx.lineTo(-15, -14);
            ctx.lineTo(-12, 0);
            ctx.fill();
            ctx.beginPath();
            ctx.moveTo(-8, 9);
            ctx.lineTo(-15, 14);
            ctx.lineTo(-12, 0);
            ctx.fill();

            // Cockpit Window
            ctx.fillStyle = '#06b6d4';
            ctx.beginPath();
            ctx.arc(6, -2, 4, 0, Math.PI * 2);
            ctx.fill();

            ctx.restore();
            ctx.shadowBlur = 0;
        }
    }

    // ==========================================
    // 6. GAME 3: NEON BRICK BREAKER DX
    // ==========================================
    class BreakoutGame {
        constructor(manager) {
            this.manager = manager;
            this.reset();
        }

        reset() {
            this.paddle = {
                x: 270,
                y: 440,
                w: 100,
                h: 14,
                speed: 7
            };
            this.ball = {
                x: 320,
                y: 420,
                vx: 3.5,
                vy: -4.5,
                r: 7
            };
            this.bricks = [];
            this.particles = [];
            this.score = 0;
            this.keys = {};

            // Generate 4 rows of 8 bricks
            const colors = ['#f59e0b', '#f43f5e', '#06b6d4', '#10b981'];
            for (let r = 0; r < 4; r++) {
                for (let c = 0; c < 8; c++) {
                    this.bricks.push({
                        x: 40 + c * 70,
                        y: 50 + r * 28,
                        w: 60,
                        h: 18,
                        color: colors[r],
                        alive: true,
                        points: (4 - r) * 10
                    });
                }
            }
        }

        onKeyDown(e) {
            this.keys[e.key] = true;
            if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') e.preventDefault();
        }

        onKeyUp(e) {
            this.keys[e.key] = false;
        }

        onMouseMove(x) {
            this.paddle.x = Math.max(0, Math.min(640 - this.paddle.w, x - this.paddle.w / 2));
        }

        onDirection(dir) {
            if (dir === 'LEFT') this.paddle.x = Math.max(0, this.paddle.x - 30);
            if (dir === 'RIGHT') this.paddle.x = Math.min(640 - this.paddle.w, this.paddle.x + 30);
        }

        update() {
            // Paddle Movement via Keys
            if (this.keys['ArrowLeft'] || this.keys['a'] || this.keys['A']) {
                this.paddle.x = Math.max(0, this.paddle.x - this.paddle.speed);
            }
            if (this.keys['ArrowRight'] || this.keys['d'] || this.keys['D']) {
                this.paddle.x = Math.min(640 - this.paddle.w, this.paddle.x + this.paddle.speed);
            }

            const b = this.ball;
            b.x += b.vx;
            b.y += b.vy;

            // Wall Collisions
            if (b.x - b.r < 0) {
                b.x = b.r;
                b.vx = -b.vx;
                audio.playHit();
            } else if (b.x + b.r > 640) {
                b.x = 640 - b.r;
                b.vx = -b.vx;
                audio.playHit();
            }
            if (b.y - b.r < 0) {
                b.y = b.r;
                b.vy = -b.vy;
                audio.playHit();
            }

            // Paddle Collision
            const p = this.paddle;
            if (
                b.y + b.r >= p.y &&
                b.y - b.r <= p.y + p.h &&
                b.x >= p.x &&
                b.x <= p.x + p.w
            ) {
                b.vy = -Math.abs(b.vy);
                const hitOffset = (b.x - (p.x + p.w / 2)) / (p.w / 2);
                b.vx = hitOffset * 5.5;
                audio.playHit();
            }

            // Brick Collisions
            let aliveCount = 0;
            this.bricks.forEach(brick => {
                if (!brick.alive) return;
                aliveCount++;
                if (
                    b.x + b.r > brick.x &&
                    b.x - b.r < brick.x + brick.w &&
                    b.y + b.r > brick.y &&
                    b.y - b.r < brick.y + brick.h
                ) {
                    brick.alive = false;
                    b.vy = -b.vy;
                    this.score += brick.points;
                    this.manager.score = this.score;
                    this.manager.updateScoreHud();
                    audio.playCoin();

                    // Brick shatter particles
                    for (let i = 0; i < 10; i++) {
                        this.particles.push({
                            x: brick.x + brick.w / 2,
                            y: brick.y + brick.h / 2,
                            vx: (Math.random() - 0.5) * 5,
                            vy: (Math.random() - 0.5) * 5,
                            life: 1,
                            color: brick.color
                        });
                    }
                }
            });

            // Stage Clear Win Condition
            if (aliveCount === 0) {
                audio.playVictory();
                this.manager.gameOver(this.score + 500);
                return;
            }

            // Ball Out of Bounds Bottom
            if (b.y > 480) {
                audio.playExplosion();
                this.manager.gameOver(this.score);
            }
        }

        draw(ctx) {
            ctx.fillStyle = '#090a10';
            ctx.fillRect(0, 0, 640, 480);

            // Draw Bricks
            this.bricks.forEach(brick => {
                if (!brick.alive) return;
                ctx.shadowColor = brick.color;
                ctx.shadowBlur = 8;
                ctx.fillStyle = brick.color;
                ctx.beginPath();
                ctx.roundRect(brick.x, brick.y, brick.w, brick.h, 4);
                ctx.fill();
                ctx.shadowBlur = 0;
            });

            // Draw Paddle
            const p = this.paddle;
            ctx.shadowColor = '#f43f5e';
            ctx.shadowBlur = 12;
            ctx.fillStyle = '#f43f5e';
            ctx.beginPath();
            ctx.roundRect(p.x, p.y, p.w, p.h, 6);
            ctx.fill();

            // Inner Paddle Accent
            ctx.fillStyle = '#fff';
            ctx.beginPath();
            ctx.roundRect(p.x + p.w * 0.25, p.y + 3, p.w * 0.5, 3, 2);
            ctx.fill();
            ctx.shadowBlur = 0;

            // Draw Ball with Glow Trail
            const b = this.ball;
            ctx.shadowColor = '#06b6d4';
            ctx.shadowBlur = 12;
            ctx.fillStyle = '#22d3ee';
            ctx.beginPath();
            ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
            ctx.fill();
            ctx.shadowBlur = 0;

            // Particles
            for (let i = this.particles.length - 1; i >= 0; i--) {
                const part = this.particles[i];
                part.x += part.vx;
                part.y += part.vy;
                part.life -= 0.04;
                if (part.life <= 0) {
                    this.particles.splice(i, 1);
                    continue;
                }
                ctx.fillStyle = part.color;
                ctx.globalAlpha = part.life;
                ctx.fillRect(part.x, part.y, 4, 4);
                ctx.globalAlpha = 1;
            }
        }
    }

    // ==========================================
    // 7. GAME 4: 2048 CYBER MATRIX
    // ==========================================
    class Matrix2048Game {
        constructor(manager) {
            this.manager = manager;
            this.reset();
        }

        reset() {
            this.grid = [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ];
            this.score = 0;
            this.addRandomTile();
            this.addRandomTile();
        }

        addRandomTile() {
            const empty = [];
            for (let r = 0; r < 4; r++) {
                for (let c = 0; c < 4; c++) {
                    if (this.grid[r][c] === 0) empty.push({ r, c });
                }
            }
            if (empty.length > 0) {
                const spot = empty[Math.floor(Math.random() * empty.length)];
                this.grid[spot.r][spot.c] = Math.random() < 0.9 ? 2 : 4;
            }
        }

        onKeyDown(e) {
            if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') {
                this.move('UP');
                e.preventDefault();
            } else if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') {
                this.move('DOWN');
                e.preventDefault();
            } else if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') {
                this.move('LEFT');
                e.preventDefault();
            } else if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') {
                this.move('RIGHT');
                e.preventDefault();
            }
        }

        onDirection(dir) {
            this.move(dir);
        }

        move(dir) {
            let moved = false;
            const slide = (row) => {
                let arr = row.filter(val => val !== 0);
                for (let i = 0; i < arr.length - 1; i++) {
                    if (arr[i] === arr[i + 1]) {
                        arr[i] *= 2;
                        this.score += arr[i];
                        this.manager.score = this.score;
                        this.manager.updateScoreHud();
                        audio.playCoin();
                        arr.splice(i + 1, 1);
                        moved = true;
                    }
                }
                while (arr.length < 4) arr.push(0);
                return arr;
            };

            const oldGrid = JSON.stringify(this.grid);

            if (dir === 'LEFT') {
                for (let r = 0; r < 4; r++) {
                    this.grid[r] = slide(this.grid[r]);
                }
            } else if (dir === 'RIGHT') {
                for (let r = 0; r < 4; r++) {
                    this.grid[r] = slide(this.grid[r].reverse()).reverse();
                }
            } else if (dir === 'UP') {
                for (let c = 0; c < 4; c++) {
                    let col = [this.grid[0][c], this.grid[1][c], this.grid[2][c], this.grid[3][c]];
                    col = slide(col);
                    for (let r = 0; r < 4; r++) this.grid[r][c] = col[r];
                }
            } else if (dir === 'DOWN') {
                for (let c = 0; c < 4; c++) {
                    let col = [this.grid[3][c], this.grid[2][c], this.grid[1][c], this.grid[0][c]];
                    col = slide(col);
                    for (let r = 0; r < 4; r++) this.grid[r][c] = col[3 - r];
                }
            }

            if (JSON.stringify(this.grid) !== oldGrid) {
                audio.playLaser();
                this.addRandomTile();

                // Check Game Over
                if (this.isGameOver()) {
                    this.manager.gameOver(this.score);
                }
            }
        }

        isGameOver() {
            for (let r = 0; r < 4; r++) {
                for (let c = 0; c < 4; c++) {
                    if (this.grid[r][c] === 0) return false;
                    if (c < 3 && this.grid[r][c] === this.grid[r][c + 1]) return false;
                    if (r < 3 && this.grid[r][c] === this.grid[r + 1][c]) return false;
                }
            }
            return true;
        }

        update() {
            // Static board, updates on key events
        }

        draw(ctx) {
            ctx.fillStyle = '#080c14';
            ctx.fillRect(0, 0, 640, 480);

            // Matrix Board Container
            const boardSize = 380;
            const startX = (640 - boardSize) / 2;
            const startY = 50;

            ctx.fillStyle = '#101725';
            ctx.strokeStyle = 'rgba(139, 92, 246, 0.4)';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.roundRect(startX, startY, boardSize, boardSize, 12);
            ctx.fill();
            ctx.stroke();

            const tileSize = (boardSize - 50) / 4;
            const colors = {
                2: { bg: '#1e293b', txt: '#94a3b8' },
                4: { bg: '#0f3a4c', txt: '#38bdf8' },
                8: { bg: '#064e3b', txt: '#34d399' },
                16: { bg: '#78350f', txt: '#fbbf24' },
                32: { bg: '#831843', txt: '#f472b6' },
                64: { bg: '#881337', txt: '#fda4af' },
                128: { bg: '#4c1d95', txt: '#c084fc' },
                256: { bg: '#312e81', txt: '#818cf8' },
                512: { bg: '#1e1b4b', txt: '#a5b4fc' },
                1024: { bg: '#b45309', txt: '#fff' },
                2048: { bg: '#e11d48', txt: '#fff' }
            };

            for (let r = 0; r < 4; r++) {
                for (let c = 0; c < 4; c++) {
                    const val = this.grid[r][c];
                    const tx = startX + 10 + c * (tileSize + 10);
                    const ty = startY + 10 + r * (tileSize + 10);

                    const style = colors[val] || { bg: '#161e2e', txt: '#64748b' };
                    ctx.fillStyle = style.bg;
                    ctx.beginPath();
                    ctx.roundRect(tx, ty, tileSize, tileSize, 8);
                    ctx.fill();

                    if (val > 0) {
                        ctx.fillStyle = style.txt;
                        ctx.font = `bold ${val > 512 ? 22 : 28}px 'Space Grotesk', sans-serif`;
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillText(val, tx + tileSize / 2, ty + tileSize / 2);
                    }
                }
            }
        }
    }

    // ==========================================
    // 8. GAME 5: METEOR DEFENDER 360
    // ==========================================
    class AsteroidsGame {
        constructor(manager) {
            this.manager = manager;
            this.reset();
        }

        reset() {
            this.ship = {
                x: 320,
                y: 240,
                r: 12,
                angle: -Math.PI / 2,
                rotSpeed: 0,
                vx: 0,
                vy: 0,
                thrust: false
            };
            this.lasers = [];
            this.meteors = [];
            this.particles = [];
            this.score = 0;
            this.keys = {};

            // Spawn 5 large meteors
            for (let i = 0; i < 5; i++) {
                this.spawnMeteor(3);
            }
        }

        spawnMeteor(size, x, y) {
            let mx = x !== undefined ? x : Math.random() * 640;
            let my = y !== undefined ? y : Math.random() * 480;

            // Keep away from ship on spawn
            if (x === undefined && Math.hypot(mx - this.ship.x, my - this.ship.y) < 100) {
                mx += 150;
            }

            const rad = size === 3 ? 32 : size === 2 ? 20 : 12;
            const points = [];
            const numVerts = 8;
            for (let v = 0; v < numVerts; v++) {
                const a = (v / numVerts) * Math.PI * 2;
                const d = rad + (Math.random() * 8 - 4);
                points.push({ x: Math.cos(a) * d, y: Math.sin(a) * d });
            }

            this.meteors.push({
                x: mx,
                y: my,
                vx: (Math.random() - 0.5) * (4 - size),
                vy: (Math.random() - 0.5) * (4 - size),
                size: size,
                rad: rad,
                points: points,
                rotAngle: 0,
                rotSpeed: (Math.random() - 0.5) * 0.04
            });
        }

        onKeyDown(e) {
            this.keys[e.key] = true;
            if (e.key === ' ' || e.code === 'Space') {
                this.fireLaser();
                e.preventDefault();
            }
            if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
                e.preventDefault();
            }
        }

        onKeyUp(e) {
            this.keys[e.key] = false;
        }

        onDirection(dir) {
            if (dir === 'UP') this.applyThrust();
            if (dir === 'LEFT') this.ship.angle -= 0.35;
            if (dir === 'RIGHT') this.ship.angle += 0.35;
        }

        onActionA() {
            this.fireLaser();
        }

        fireLaser() {
            audio.playLaser();
            this.lasers.push({
                x: this.ship.x + Math.cos(this.ship.angle) * 16,
                y: this.ship.y + Math.sin(this.ship.angle) * 16,
                vx: Math.cos(this.ship.angle) * 8 + this.ship.vx,
                vy: Math.sin(this.ship.angle) * 8 + this.ship.vy,
                life: 45
            });
        }

        applyThrust() {
            this.ship.vx += Math.cos(this.ship.angle) * 0.45;
            this.ship.vy += Math.sin(this.ship.angle) * 0.45;
            audio.playJump();
        }

        update() {
            const s = this.ship;

            // Rotation
            if (this.keys['ArrowLeft'] || this.keys['a'] || this.keys['A']) s.angle -= 0.08;
            if (this.keys['ArrowRight'] || this.keys['d'] || this.keys['D']) s.angle += 0.08;

            // Thrust
            s.thrust = Boolean(this.keys['ArrowUp'] || this.keys['w'] || this.keys['W']);
            if (s.thrust) {
                this.applyThrust();
                // Particles
                this.particles.push({
                    x: s.x - Math.cos(s.angle) * 14,
                    y: s.y - Math.sin(s.angle) * 14,
                    vx: -Math.cos(s.angle) * 3 + (Math.random() - 0.5),
                    vy: -Math.sin(s.angle) * 3 + (Math.random() - 0.5),
                    life: 0.8,
                    color: '#06b6d4'
                });
            }

            // Ship movement & friction
            s.vx *= 0.985;
            s.vy *= 0.985;
            s.x = (s.x + s.vx + 640) % 640;
            s.y = (s.y + s.vy + 480) % 480;

            // Lasers
            for (let i = this.lasers.length - 1; i >= 0; i--) {
                const l = this.lasers[i];
                l.x = (l.x + l.vx + 640) % 640;
                l.y = (l.y + l.vy + 480) % 480;
                l.life--;
                if (l.life <= 0) {
                    this.lasers.splice(i, 1);
                }
            }

            // Meteors update & laser collision
            for (let mIdx = this.meteors.length - 1; mIdx >= 0; mIdx--) {
                const m = this.meteors[mIdx];
                m.x = (m.x + m.vx + 640) % 640;
                m.y = (m.y + m.vy + 480) % 480;
                m.rotAngle += m.rotSpeed;

                // Ship collision
                if (Math.hypot(m.x - s.x, m.y - s.y) < m.rad + s.r) {
                    audio.playExplosion();
                    this.manager.gameOver(this.score);
                    return;
                }

                // Laser collision
                for (let lIdx = this.lasers.length - 1; lIdx >= 0; lIdx--) {
                    const l = this.lasers[lIdx];
                    if (Math.hypot(m.x - l.x, m.y - l.y) < m.rad) {
                        this.lasers.splice(lIdx, 1);
                        audio.playExplosion();

                        // Score
                        this.score += m.size * 25;
                        this.manager.score = this.score;
                        this.manager.updateScoreHud();

                        // Particles
                        for (let p = 0; p < 10; p++) {
                            this.particles.push({
                                x: m.x,
                                y: m.y,
                                vx: (Math.random() - 0.5) * 6,
                                vy: (Math.random() - 0.5) * 6,
                                life: 1,
                                color: '#38bdf8'
                            });
                        }

                        // Split meteor
                        if (m.size > 1) {
                            this.spawnMeteor(m.size - 1, m.x, m.y);
                            this.spawnMeteor(m.size - 1, m.x, m.y);
                        }
                        this.meteors.splice(mIdx, 1);
                        break;
                    }
                }
            }

            // Respawn meteors if empty
            if (this.meteors.length === 0) {
                audio.playVictory();
                for (let i = 0; i < 6; i++) {
                    this.spawnMeteor(3);
                }
            }
        }

        draw(ctx) {
            ctx.fillStyle = '#05070d';
            ctx.fillRect(0, 0, 640, 480);

            // Vector Stars
            ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
            for (let st = 0; st < 30; st++) {
                ctx.fillRect((st * 47) % 640, (st * 79) % 480, 1.5, 1.5);
            }

            // Lasers
            ctx.shadowColor = '#06b6d4';
            ctx.shadowBlur = 8;
            ctx.fillStyle = '#38bdf8';
            this.lasers.forEach(l => {
                ctx.beginPath();
                ctx.arc(l.x, l.y, 3, 0, Math.PI * 2);
                ctx.fill();
            });

            // Meteors
            ctx.strokeStyle = '#38bdf8';
            ctx.lineWidth = 1.8;
            this.meteors.forEach(m => {
                ctx.save();
                ctx.translate(m.x, m.y);
                ctx.rotate(m.rotAngle);
                ctx.beginPath();
                m.points.forEach((pt, idx) => {
                    if (idx === 0) ctx.moveTo(pt.x, pt.y);
                    else ctx.lineTo(pt.x, pt.y);
                });
                ctx.closePath();
                ctx.stroke();
                ctx.restore();
            });

            // Ship (Vector Triangle)
            const s = this.ship;
            ctx.save();
            ctx.translate(s.x, s.y);
            ctx.rotate(s.angle);

            ctx.shadowColor = '#06b6d4';
            ctx.shadowBlur = 12;
            ctx.strokeStyle = '#fff';
            ctx.fillStyle = '#0f172a';
            ctx.lineWidth = 2;

            ctx.beginPath();
            ctx.moveTo(18, 0);
            ctx.lineTo(-12, -10);
            ctx.lineTo(-8, 0);
            ctx.lineTo(-12, 10);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();

            // Thruster fire
            if (s.thrust) {
                ctx.strokeStyle = '#f59e0b';
                ctx.beginPath();
                ctx.moveTo(-9, -5);
                ctx.lineTo(-18 - Math.random() * 6, 0);
                ctx.lineTo(-9, 5);
                ctx.stroke();
            }

            ctx.restore();
            ctx.shadowBlur = 0;

            // Particles
            for (let i = this.particles.length - 1; i >= 0; i--) {
                const p = this.particles[i];
                p.x += p.vx;
                p.y += p.vy;
                p.life -= 0.05;
                if (p.life <= 0) {
                    this.particles.splice(i, 1);
                    continue;
                }
                ctx.fillStyle = p.color;
                ctx.globalAlpha = p.life;
                ctx.fillRect(p.x, p.y, 2.5, 2.5);
                ctx.globalAlpha = 1;
            }
        }
    }

    // ==========================================
    // 9. GAME 6: CYBER HOLOGRAM MATCH
    // ==========================================
    class MemoryGame {
        constructor(manager) {
            this.manager = manager;
            this.reset();
        }

        reset() {
            const symbols = ['⚡', '🏔️', '🌹', '⏳', '🌌', '🎬', '🚀', '💎'];
            const deck = [...symbols, ...symbols].sort(() => Math.random() - 0.5);

            this.cards = deck.map((sym, i) => ({
                id: i,
                symbol: sym,
                flipped: false,
                matched: false
            }));

            this.selected = [];
            this.moves = 0;
            this.matches = 0;
            this.score = 0;
            this.canFlip = true;
            this.particles = [];
        }

        onClick(x, y) {
            if (!this.canFlip) return;
            const startX = 140;
            const startY = 60;
            const cardW = 80;
            const cardH = 85;
            const gap = 12;

            for (let r = 0; r < 4; r++) {
                for (let c = 0; c < 4; c++) {
                    const idx = r * 4 + c;
                    const card = this.cards[idx];
                    const cx = startX + c * (cardW + gap);
                    const cy = startY + r * (cardH + gap);

                    if (x >= cx && x <= cx + cardW && y >= cy && y <= cy + cardH) {
                        this.flipCard(card);
                        return;
                    }
                }
            }
        }

        flipCard(card) {
            if (card.flipped || card.matched || this.selected.length >= 2) return;

            card.flipped = true;
            this.selected.push(card);
            audio.playLaser();

            if (this.selected.length === 2) {
                this.moves++;
                const [c1, c2] = this.selected;
                if (c1.symbol === c2.symbol) {
                    c1.matched = true;
                    c2.matched = true;
                    this.matches++;
                    this.score += 50;
                    this.manager.score = this.score;
                    this.manager.updateScoreHud();
                    audio.playCoin();
                    this.selected = [];

                    // Confetti particles
                    for (let i = 0; i < 20; i++) {
                        this.particles.push({
                            x: 320,
                            y: 240,
                            vx: (Math.random() - 0.5) * 8,
                            vy: (Math.random() - 0.5) * 8,
                            life: 1,
                            color: ['#ec4899', '#f59e0b', '#10b981', '#06b6d4'][Math.floor(Math.random() * 4)]
                        });
                    }

                    if (this.matches === 8) {
                        const bonus = Math.max(0, 300 - this.moves * 10);
                        audio.playVictory();
                        this.manager.gameOver(this.score + bonus);
                    }
                } else {
                    this.canFlip = false;
                    setTimeout(() => {
                        c1.flipped = false;
                        c2.flipped = false;
                        this.selected = [];
                        this.canFlip = true;
                    }, 800);
                }
            }
        }

        update() {}

        draw(ctx) {
            ctx.fillStyle = '#0c0e18';
            ctx.fillRect(0, 0, 640, 480);

            const startX = 140;
            const startY = 60;
            const cardW = 80;
            const cardH = 85;
            const gap = 12;

            for (let r = 0; r < 4; r++) {
                for (let c = 0; c < 4; c++) {
                    const idx = r * 4 + c;
                    const card = this.cards[idx];
                    const cx = startX + c * (cardW + gap);
                    const cy = startY + r * (cardH + gap);

                    if (card.matched) {
                        ctx.fillStyle = 'rgba(16, 185, 129, 0.2)';
                        ctx.strokeStyle = '#10b981';
                        ctx.lineWidth = 1.5;
                        ctx.beginPath();
                        ctx.roundRect(cx, cy, cardW, cardH, 8);
                        ctx.fill();
                        ctx.stroke();

                        ctx.font = '32px sans-serif';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillText(card.symbol, cx + cardW / 2, cy + cardH / 2);
                    } else if (card.flipped) {
                        ctx.fillStyle = '#1e1b4b';
                        ctx.strokeStyle = '#ec4899';
                        ctx.lineWidth = 2;
                        ctx.beginPath();
                        ctx.roundRect(cx, cy, cardW, cardH, 8);
                        ctx.fill();
                        ctx.stroke();

                        ctx.font = '32px sans-serif';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillText(card.symbol, cx + cardW / 2, cy + cardH / 2);
                    } else {
                        // Card Back
                        ctx.fillStyle = '#161b2e';
                        ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
                        ctx.lineWidth = 1;
                        ctx.beginPath();
                        ctx.roundRect(cx, cy, cardW, cardH, 8);
                        ctx.fill();
                        ctx.stroke();

                        ctx.fillStyle = '#ec4899';
                        ctx.font = 'bold 20px monospace';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillText('👾', cx + cardW / 2, cy + cardH / 2);
                    }
                }
            }

            // Stats top text
            ctx.fillStyle = '#94a3b8';
            ctx.font = '14px monospace';
            ctx.textAlign = 'center';
            ctx.fillText(`MOVES: ${this.moves}  |  PAIRS: ${this.matches} / 8`, 320, 35);

            // Particles
            for (let i = this.particles.length - 1; i >= 0; i--) {
                const p = this.particles[i];
                p.x += p.vx;
                p.y += p.vy;
                p.life -= 0.03;
                if (p.life <= 0) {
                    this.particles.splice(i, 1);
                    continue;
                }
                ctx.fillStyle = p.color;
                ctx.globalAlpha = p.life;
                ctx.fillRect(p.x, p.y, 4, 4);
                ctx.globalAlpha = 1;
            }
        }
    }

    // ==========================================
    // 10. BOOTSTRAP ON DOM READY
    // ==========================================
    window.ArcadeStudio = new ArcadeStudioManager();

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => window.ArcadeStudio.init());
    } else {
        window.ArcadeStudio.init();
    }
})();
