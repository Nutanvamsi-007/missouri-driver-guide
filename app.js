/**
 * Missouri Driver Guide - Interactive Application Engine
 * Pure modern vanilla JS (zero external dependencies, runs offline)
 */

(function () {
  'use strict';

  // Ensure GUIDE_DATA is loaded
  const DATA = window.MISSOURI_GUIDE_DATA;
  if (!DATA) {
    console.error("MISSOURI_GUIDE_DATA not found. Make sure data.js is loaded.");
    return;
  }

  // App State
  const state = {
    currentTab: 'reader',
    currentChapterId: 'chapter-1',
    theme: localStorage.getItem('mo_guide_theme') || 'dark',
    fontSize: parseInt(localStorage.getItem('mo_guide_font_size') || '16', 10),
    bookmarks: JSON.parse(localStorage.getItem('mo_guide_bookmarks') || '[]'),
    readChapters: JSON.parse(localStorage.getItem('mo_guide_read_chapters') || '[]'),
    
    // Exam state
    examMode: 'practice', // 'practice' or 'timed'
    examQuestions: [],
    currentQuestionIdx: 0,
    examUserAnswers: {},
    examSubmitted: false,
    examTimerInterval: null,
    examSecondsLeft: 25 * 60, // 25 mins
    
    // Signs state
    signFilter: 'all',
    
    // Audio Studio State
    audioElement: new Audio(),
    audioTrackId: 'cram',
    audioSpeed: 1.0,
    isPlayingAudio: false,
    isSpeaking: false,
    speechUtterance: null,
    
    // Calculators
    calcSpeed: 55,
    calcRoadCondition: 'dry',
    selectedViolations: []
  };

  // DOM Elements cache
  const el = {
    tabs: document.querySelectorAll('.nav-tab-btn'),
    panes: document.querySelectorAll('.tab-pane'),
    themeToggleBtn: document.getElementById('theme-toggle-btn'),
    searchModal: document.getElementById('search-modal'),
    searchInput: document.getElementById('search-main-input'),
    searchResults: document.getElementById('search-results-list'),
    searchTriggers: document.querySelectorAll('.search-trigger-btn'),
    mirrorModal: document.getElementById('mirror-modal'),
    mirrorImg: document.getElementById('mirror-modal-img'),
    mirrorTitle: document.getElementById('mirror-modal-title'),
    mirrorPageNum: document.getElementById('mirror-modal-page')
  };

  // -------------------------------------------------------------
  // Theme Management
  // -------------------------------------------------------------
  function applyTheme(theme) {
    state.theme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('mo_guide_theme', theme);
    if (el.themeToggleBtn) {
      el.themeToggleBtn.innerHTML = theme === 'dark' 
        ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>'
        : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>';
    }
  }

  // -------------------------------------------------------------
  // Tab Navigation
  // -------------------------------------------------------------
  function switchTab(tabName, updateHash = true) {
    state.currentTab = tabName;
    el.tabs.forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tab === tabName);
    });
    el.panes.forEach(pane => {
      pane.classList.toggle('active', pane.id === `tab-${tabName}`);
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });

    if (updateHash && window.location.hash !== `#${tabName}`) {
      try {
        history.replaceState(null, '', `#${tabName}`);
      } catch (e) {
        window.location.hash = tabName;
      }
    }

    if (tabName === 'reader') {
      renderReaderSidebar();
      renderCurrentChapter();
    } else if (tabName === 'signs') {
      renderSignsAndFlashcards();
    } else if (tabName === 'exam') {
      if (state.examQuestions.length === 0) {
        showExamWelcome();
      }
    } else if (tabName === 'calculators') {
      initCalculators();
    } else if (tabName === 'pdf-mirror') {
      renderPdfMirrorGrid();
    }
  }

  // -------------------------------------------------------------
  // 1. Handbook Reader Engine
  // -------------------------------------------------------------
  function renderReaderSidebar() {
    const listEl = document.getElementById('chapter-nav-list');
    if (!listEl) return;

    listEl.innerHTML = '';
    DATA.chapters.forEach(ch => {
      const isRead = state.readChapters.includes(ch.id);
      const isBookmarked = state.bookmarks.includes(ch.id);
      const isActive = ch.id === state.currentChapterId;

      const li = document.createElement('li');
      li.className = 'chapter-nav-item';
      li.innerHTML = `
        <button class="chapter-nav-btn ${isActive ? 'active' : ''}" data-id="${ch.id}">
          <span style="display:flex; align-items:center; gap:0.5rem; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
            <span class="chapter-num-badge">${ch.number === 0 ? 'Intro' : (ch.number > 16 ? ch.title.split(' ')[0] : 'Ch ' + ch.number)}</span>
            <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${ch.title}</span>
          </span>
          <span style="display:flex; align-items:center; gap:0.35rem;">
            ${isRead ? '<span style="color:var(--mo-green); font-size:0.8rem;">✓</span>' : ''}
            ${isBookmarked ? '<span style="color:var(--mo-gold); font-size:0.8rem;">★</span>' : ''}
          </span>
        </button>
      `;

      li.querySelector('button').addEventListener('click', () => {
        stopAudio();
        state.currentChapterId = ch.id;
        renderReaderSidebar();
        renderCurrentChapter();

        // Collapse mobile chapter drawer if open
        const sidebar = document.getElementById('reader-sidebar');
        const trigger = document.getElementById('mobile-chapter-trigger-btn');
        if (sidebar && window.innerWidth <= 900) {
          sidebar.classList.remove('open');
          if (trigger) trigger.classList.remove('active');
        }

        window.scrollTo({ top: 120, behavior: 'smooth' });
      });

      listEl.appendChild(li);
    });
  }

  function renderCurrentChapter() {
    const ch = DATA.chapters.find(c => c.id === state.currentChapterId) || DATA.chapters[1];
    const container = document.getElementById('reader-chapter-content');
    if (!container) return;

    // Mark as read in state
    if (!state.readChapters.includes(ch.id)) {
      state.readChapters.push(ch.id);
      localStorage.setItem('mo_guide_read_chapters', JSON.stringify(state.readChapters));
    }

    const isBookmarked = state.bookmarks.includes(ch.id);

    // Update mobile chapter title if present
    const mobileChTitle = document.getElementById('mobile-current-chapter-title');
    if (mobileChTitle) {
      mobileChTitle.textContent = `${ch.number === 0 ? 'Intro' : (ch.number > 16 ? 'Reference' : `Chapter ${ch.number}`)}: ${ch.title}`;
    }

    // Build Chapter HTML
    let html = `
      <div class="chapter-header">
        <span class="chapter-number-label">${ch.number === 0 ? 'Introduction' : (ch.number > 16 ? 'Reference' : `Chapter ${ch.number}`)}</span>
        <h1 class="chapter-heading-title">${ch.title}</h1>
        <div class="chapter-meta-bar">
          <span>📖 PDF Pages ${ch.start_page}–${ch.end_page} (Manual pp. ${ch.book_pages})</span>
          <span>⏱ ~${ch.read_minutes} min read</span>
          <button id="reader-bookmark-btn" class="control-btn ${isBookmarked ? 'active' : ''}" style="margin-left:auto;">
            ${isBookmarked ? '★ Bookmarked' : '☆ Bookmark'}
          </button>
        </div>
      </div>

      ${renderAudioStudioMarkup(ch)}
    `;

    // Inline diagrams / figures for this chapter if any
    if (ch.figures && ch.figures.length > 0) {
      html += `
        <h2 style="font-size:1.15rem; margin-top:1.5rem; color:var(--text-accent);">
          Visual Reference & Diagrams (${ch.figures.length})
        </h2>
        <div class="chapter-figures-grid">
      `;
      ch.figures.forEach(fig => {
        html += `
          <div class="figure-card">
            <div class="figure-image-wrap">
              <img src="${fig.image}" alt="${fig.title}" loading="lazy" />
            </div>
            <div class="figure-title">${fig.title}</div>
            <div class="figure-desc">${fig.description}</div>
          </div>
        `;
      });
      html += `</div>`;
    }

    // Body content rendered by page
    html += `<div class="chapter-body" style="font-size:${state.fontSize}px;">`;

    ch.pages.forEach(pg => {
      html += `
        <div class="page-mirror-banner">
          <div>
            <strong>Manual Page ${pg.book_page}</strong>
            <span style="font-size:0.8rem; color:var(--text-secondary); margin-left:0.5rem;">(PDF Page ${pg.page_number})</span>
          </div>
          <button class="control-btn view-mirror-btn" data-page="${pg.page_number}" data-title="${ch.title}">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
            View Official PDF Page
          </button>
        </div>
      `;

      // Render blocks
      pg.blocks.forEach(b => {
        const text = escapeHtml(b.text);
        if (b.is_tip) {
          html += `
            <div class="callout-box tip">
              <div class="callout-title">💡 State Examiner Tip</div>
              <div>${text.replace(/^Tip!\s*/i, '')}</div>
            </div>
          `;
        } else if (b.is_warning) {
          html += `
            <div class="callout-box warning">
              <div class="callout-title">⚠️ Mandatory Rule & Penalty</div>
              <div>${text}</div>
            </div>
          `;
        } else if (b.is_note) {
          html += `
            <div class="callout-box note">
              <div class="callout-title">ℹ️ Important Notice</div>
              <div>${text}</div>
            </div>
          `;
        } else if (b.is_heading) {
          html += `<h3>${escapeHtml(b.first_line)}</h3>`;
          const remainder = b.text.substring(b.first_line.length).trim();
          if (remainder) {
            html += `<p>${formatParagraph(remainder)}</p>`;
          }
        } else {
          html += `<p>${formatParagraph(text)}</p>`;
        }
      });
    });

    html += `</div>`;

    // Chapter Navigation Footer (Prev / Next)
    const currentIdx = DATA.chapters.findIndex(c => c.id === ch.id);
    const prevCh = DATA.chapters[currentIdx - 1];
    const nextCh = DATA.chapters[currentIdx + 1];

    html += `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-top:3rem; padding-top:1.5rem; border-top:1px solid var(--border-color);">
        ${prevCh ? `<button class="btn-secondary" id="prev-chapter-btn" data-id="${prevCh.id}">← ${prevCh.title}</button>` : '<div></div>'}
        ${nextCh ? `<button class="btn-primary" id="next-chapter-btn" data-id="${nextCh.id}">${nextCh.title} →</button>` : '<div></div>'}
      </div>
    `;

    container.innerHTML = html;

    // Attach listeners
    const bkmkBtn = document.getElementById('reader-bookmark-btn');
    if (bkmkBtn) {
      bkmkBtn.addEventListener('click', () => {
        if (state.bookmarks.includes(ch.id)) {
          state.bookmarks = state.bookmarks.filter(id => id !== ch.id);
        } else {
          state.bookmarks.push(ch.id);
        }
        localStorage.setItem('mo_guide_bookmarks', JSON.stringify(state.bookmarks));
        renderReaderSidebar();
        renderCurrentChapter();
      });
    }

    bindAudioStudioControls(ch);

    const prevBtn = document.getElementById('prev-chapter-btn');
    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        stopAudio();
        state.currentChapterId = prevBtn.dataset.id;
        renderReaderSidebar();
        renderCurrentChapter();
        window.scrollTo({ top: 120, behavior: 'smooth' });
      });
    }

    const nextBtn = document.getElementById('next-chapter-btn');
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        stopAudio();
        state.currentChapterId = nextBtn.dataset.id;
        renderReaderSidebar();
        renderCurrentChapter();
        window.scrollTo({ top: 120, behavior: 'smooth' });
      });
    }

    // Mirror page buttons
    container.querySelectorAll('.view-mirror-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        openPdfMirror(parseInt(btn.dataset.page, 10), btn.dataset.title);
      });
    });
  }

  function formatParagraph(text) {
    // Format bullet points
    if (text.includes('•') || text.includes('\x07')) {
      const items = text.split(/[•\x07]/).map(s => s.trim()).filter(Boolean);
      if (items.length > 1) {
        return '<ul>' + items.map(item => `<li>${item}</li>`).join('') + '</ul>';
      }
    }
    return text.replace(/\n\s*\n/g, '</p><p>').replace(/\n/g, ' ');
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  // -------------------------------------------------------------
  // Studio AI Audio Player & Narration Suite
  // -------------------------------------------------------------
  const CHAPTER_AUDIO_TRACKS = {
    'chapter-1': [
      {
        id: 'cram',
        badge: '⚡ High Yield',
        title: '3-Min Exam Cram Podcast',
        voice: 'Guy (AI Neural)',
        src: 'assets/audio/samples/chapter1_cram_podcast_guy.mp3',
        desc: 'Fast-paced review of tested permit ages, curfew & GDL restrictions.'
      },
      {
        id: 'andrew',
        badge: '🎙️ Voice A',
        title: 'Andrew (Conversational Male)',
        voice: 'Andrew (AI Neural)',
        src: 'assets/audio/samples/chapter1_narration_andrew.mp3',
        desc: 'Natural educator narration curated for smooth listening.'
      },
      {
        id: 'jenny',
        badge: '🎙️ Voice B',
        title: 'Jenny (Clear Female)',
        voice: 'Jenny (AI Neural)',
        src: 'assets/audio/samples/chapter1_narration_jenny.mp3',
        desc: 'Warm, articulate teacher narration with natural inflection.'
      },
      {
        id: 'browser',
        badge: '🤖 Fallback',
        title: 'Browser Web Speech (Old)',
        voice: 'Device Synthesizer',
        src: null,
        desc: 'Original browser text-to-speech for side-by-side comparison.'
      }
    ]
  };

  function normalizeTextForSpeech(text) {
    if (!text) return '';
    return text
      .replace(/RSMo/gi, 'Revised Statutes of Missouri')
      .replace(/\bmph\b/gi, 'miles per hour')
      .replace(/\bBAC\b/g, 'Blood Alcohol Concentration')
      .replace(/\bGDL\b/g, 'Graduated Driver License')
      .replace(/\bGVWR\b/g, 'Gross Vehicle Weight Rating')
      .replace(/\bCDL\b/g, 'Commercial Driver License')
      .replace(/\bDUI\b/g, 'Driving Under the Influence')
      .replace(/\bDWI\b/g, 'Driving While Intoxicated')
      .replace(/\bDOT\b/g, 'Department of Transportation')
      .replace(/\bDOR\b/g, 'Department of Revenue')
      .replace(/\bMSHP\b/g, 'Missouri State Highway Patrol')
      .replace(/\. \. \. \. \./g, '')
      .replace(/[•\x07*]/g, ' ')
      .replace(/Page \d+/gi, '')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function getBestSpeechVoice() {
    if (!('speechSynthesis' in window)) return null;
    const voices = window.speechSynthesis.getVoices();
    if (!voices || voices.length === 0) return null;
    
    // Prefer Google, Natural, or premium English voices
    return (
      voices.find(v => v.lang.startsWith('en') && (v.name.includes('Natural') || v.name.includes('Online'))) ||
      voices.find(v => v.lang.startsWith('en') && (v.name.includes('Google') || v.name.includes('Neural'))) ||
      voices.find(v => v.lang.startsWith('en') && (v.name.includes('Samantha') || v.name.includes('Ava') || v.name.includes('Daniel'))) ||
      voices.find(v => v.lang === 'en-US') ||
      voices.find(v => v.lang.startsWith('en')) ||
      voices[0]
    );
  }

  function renderAudioStudioMarkup(ch) {
    const tracks = CHAPTER_AUDIO_TRACKS[ch.id] || [
      {
        id: 'browser',
        badge: '🔊 Audio Narration',
        title: 'Enhanced Chapter Audio',
        voice: 'Smart Web Speech',
        src: null,
        desc: 'Listen to this chapter with text normalization and enhanced pacing.'
      }
    ];

    const currentTrack = tracks.find(t => t.id === state.audioTrackId) || tracks[0];

    return `
      <div class="audio-studio-card" id="audio-studio-card">
        <div class="audio-studio-header">
          <div class="audio-studio-title-group">
            <div class="audio-studio-icon-badge">🎧</div>
            <div>
              <div class="audio-studio-title">Chapter Audio Narration & Exam Cram</div>
              <div class="audio-studio-sub" id="audio-track-desc">${currentTrack.desc}</div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:0.5rem;">
            <div class="audio-equalizer" id="audio-equalizer">
              <span class="eq-bar"></span>
              <span class="eq-bar"></span>
              <span class="eq-bar"></span>
              <span class="eq-bar"></span>
            </div>
            <span class="audio-studio-badge" id="audio-engine-badge">${currentTrack.src ? '✨ AI Neural' : '🤖 Web Speech'}</span>
          </div>
        </div>

        <!-- Track Selection Tabs -->
        <div class="audio-track-tabs" id="audio-track-tabs">
          ${tracks.map(t => `
            <button class="audio-track-btn ${t.id === currentTrack.id ? 'active' : ''}" data-id="${t.id}">
              <span>${t.badge}</span>
              <span>${t.title}</span>
            </button>
          `).join('')}
        </div>

        <!-- Player Controls Bar -->
        <div class="audio-player-controls">
          <button class="audio-main-play-btn" id="audio-main-play-btn" title="Play / Pause Audio" aria-label="Play / Pause">
            <svg id="audio-play-icon" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
            <svg id="audio-pause-icon" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" style="display:none;"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>
          </button>

          <button class="audio-skip-btn" id="audio-skip-back-btn" title="Skip backward 15 seconds">-15s</button>
          <button class="audio-skip-btn" id="audio-skip-fwd-btn" title="Skip forward 15 seconds">+15s</button>

          <div class="audio-timeline-wrap">
            <input type="range" class="audio-progress-bar" id="audio-progress-bar" min="0" max="100" value="0" step="0.1" />
            <div class="audio-time-row">
              <span id="audio-current-time">0:00</span>
              <span id="audio-total-duration">--:--</span>
            </div>
          </div>

          <div class="audio-speed-group">
            <button class="audio-speed-btn ${state.audioSpeed === 1.0 ? 'active' : ''}" data-speed="1.0">1x</button>
            <button class="audio-speed-btn ${state.audioSpeed === 1.25 ? 'active' : ''}" data-speed="1.25">1.25x</button>
            <button class="audio-speed-btn ${state.audioSpeed === 1.5 ? 'active' : ''}" data-speed="1.5">1.5x</button>
          </div>
        </div>
      </div>
    `;
  }

  function formatAudioTime(seconds) {
    if (isNaN(seconds) || seconds < 0) return '0:00';
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  }

  function updateAudioUIState() {
    const playIcon = document.getElementById('audio-play-icon');
    const pauseIcon = document.getElementById('audio-pause-icon');
    const eq = document.getElementById('audio-equalizer');
    const isPlaying = state.isPlayingAudio || state.isSpeaking;

    if (playIcon) playIcon.style.display = isPlaying ? 'none' : 'block';
    if (pauseIcon) pauseIcon.style.display = isPlaying ? 'block' : 'none';
    if (eq) eq.classList.toggle('playing', isPlaying);
  }

  function bindAudioStudioControls(ch) {
    const tracks = CHAPTER_AUDIO_TRACKS[ch.id] || [
      {
        id: 'browser',
        badge: '🔊 Audio Narration',
        title: 'Enhanced Chapter Audio',
        voice: 'Smart Web Speech',
        src: null,
        desc: 'Listen to this chapter with text normalization and enhanced pacing.'
      }
    ];

    let currentTrack = tracks.find(t => t.id === state.audioTrackId) || tracks[0];

    const playBtn = document.getElementById('audio-main-play-btn');
    const skipBackBtn = document.getElementById('audio-skip-back-btn');
    const skipFwdBtn = document.getElementById('audio-skip-fwd-btn');
    const progressBar = document.getElementById('audio-progress-bar');
    const currentTimeEl = document.getElementById('audio-current-time');
    const totalDurationEl = document.getElementById('audio-total-duration');
    const descEl = document.getElementById('audio-track-desc');
    const badgeEl = document.getElementById('audio-engine-badge');

    // Setup Audio Element for MP3
    const audio = state.audioElement;
    if (currentTrack.src) {
      if (audio.src !== window.location.origin + '/' + currentTrack.src) {
        audio.src = currentTrack.src;
        audio.playbackRate = state.audioSpeed;
      }
    }

    // Audio metadata loaded
    audio.onloadedmetadata = () => {
      if (totalDurationEl && !isNaN(audio.duration)) {
        totalDurationEl.textContent = formatAudioTime(audio.duration);
      }
    };

    // Time update
    audio.ontimeupdate = () => {
      if (!audio.duration) return;
      const pct = (audio.currentTime / audio.duration) * 100;
      if (progressBar) progressBar.value = pct;
      if (currentTimeEl) currentTimeEl.textContent = formatAudioTime(audio.currentTime);
      if (totalDurationEl && !isNaN(audio.duration)) totalDurationEl.textContent = formatAudioTime(audio.duration);
    };

    audio.onended = () => {
      state.isPlayingAudio = false;
      updateAudioUIState();
      if (progressBar) progressBar.value = 0;
      if (currentTimeEl) currentTimeEl.textContent = '0:00';
    };

    // Scrubber seek
    if (progressBar) {
      progressBar.addEventListener('input', (e) => {
        if (currentTrack.src && audio.duration) {
          const seekTo = (e.target.value / 100) * audio.duration;
          audio.currentTime = seekTo;
        }
      });
    }

    // Skip Buttons
    if (skipBackBtn) {
      skipBackBtn.addEventListener('click', () => {
        if (currentTrack.src) {
          audio.currentTime = Math.max(0, audio.currentTime - 15);
        }
      });
    }
    if (skipFwdBtn) {
      skipFwdBtn.addEventListener('click', () => {
        if (currentTrack.src && audio.duration) {
          audio.currentTime = Math.min(audio.duration, audio.currentTime + 15);
        }
      });
    }

    // Speed Controls
    document.querySelectorAll('.audio-speed-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const speed = parseFloat(btn.dataset.speed);
        state.audioSpeed = speed;
        audio.playbackRate = speed;
        document.querySelectorAll('.audio-speed-btn').forEach(b => {
          b.classList.toggle('active', parseFloat(b.dataset.speed) === speed);
        });
      });
    });

    // Track Selection Tabs
    document.querySelectorAll('.audio-track-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const trackId = btn.dataset.id;
        state.audioTrackId = trackId;
        stopAudio();

        document.querySelectorAll('.audio-track-btn').forEach(b => {
          b.classList.toggle('active', b.dataset.id === trackId);
        });

        currentTrack = tracks.find(t => t.id === trackId) || tracks[0];
        if (descEl) descEl.textContent = currentTrack.desc;
        if (badgeEl) badgeEl.textContent = currentTrack.src ? '✨ AI Neural' : '🤖 Web Speech';

        if (currentTrack.src) {
          audio.src = currentTrack.src;
          audio.playbackRate = state.audioSpeed;
          audio.currentTime = 0;
          if (progressBar) progressBar.value = 0;
          if (currentTimeEl) currentTimeEl.textContent = '0:00';
          if (totalDurationEl) totalDurationEl.textContent = '--:--';
        } else {
          if (totalDurationEl) totalDurationEl.textContent = `~${ch.read_minutes} min`;
        }
      });
    });

    // Main Play / Pause Button
    if (playBtn) {
      playBtn.addEventListener('click', () => {
        if (currentTrack.src) {
          // Play pre-rendered AI MP3
          if (state.isPlayingAudio) {
            audio.pause();
            state.isPlayingAudio = false;
          } else {
            stopAudio(); // Stop any speech synthesis
            audio.play().then(() => {
              state.isPlayingAudio = true;
              updateAudioUIState();
            }).catch(err => {
              console.warn("Audio play prevented:", err);
            });
          }
          updateAudioUIState();
        } else {
          // Play Web Speech API fallback with enhanced text normalization
          if (state.isSpeaking) {
            stopAudio();
          } else {
            speakEnhancedChapter(ch);
          }
        }
      });
    }

    updateAudioUIState();
  }

  function speakEnhancedChapter(ch) {
    if (!('speechSynthesis' in window)) {
      alert("Text-to-speech is not supported by your browser.");
      return;
    }
    stopAudio();

    const normalized = normalizeTextForSpeech(ch.full_text).substring(0, 5000);
    const textToRead = `${ch.title}. ${ch.summary}. ${normalized}`;
    const utterance = new SpeechSynthesisUtterance(textToRead);

    const bestVoice = getBestSpeechVoice();
    if (bestVoice) utterance.voice = bestVoice;
    utterance.rate = state.audioSpeed || 1.0;
    utterance.pitch = 1.02;

    utterance.onstart = () => {
      state.isSpeaking = true;
      updateAudioUIState();
    };

    utterance.onend = utterance.onerror = () => {
      stopAudio();
    };

    state.speechUtterance = utterance;
    window.speechSynthesis.speak(utterance);
  }

  function stopAudio() {
    if (state.audioElement) {
      state.audioElement.pause();
    }
    if ('speechSynthesis' in window && window.speechSynthesis.speaking) {
      window.speechSynthesis.cancel();
    }
    state.isPlayingAudio = false;
    state.isSpeaking = false;
    updateAudioUIState();
  }

  // -------------------------------------------------------------
  // 2. Practice Exam Simulator Engine
  // -------------------------------------------------------------
  function showExamWelcome() {
    const container = document.getElementById('exam-stage-container');
    if (!container) return;

    container.innerHTML = `
      <div class="exam-welcome-card">
        <div class="exam-badge-icon">📝</div>
        <h2 class="exam-title">Missouri Driver License Exam Simulator</h2>
        <p class="exam-subtitle">Official 25-Question Test Simulation (80% / 20 Correct to Pass)</p>

        <div class="exam-rules-grid">
          <div class="exam-rule-box">
            <strong>25 Questions</strong>
            <p>Drawn from traffic laws, road signs, rules of the road, and safe driving tips.</p>
          </div>
          <div class="exam-rule-box">
            <strong>20 Correct to Pass</strong>
            <p>Requires an 80% passing score, exactly matching the Missouri State Highway Patrol standard.</p>
          </div>
          <div class="exam-rule-box">
            <strong>No Trick Questions</strong>
            <p>Every single question and answer is derived directly from the official Missouri Driver Guide.</p>
          </div>
        </div>

        <div style="display:flex; justify-content:center; gap:1rem; flex-wrap:wrap;">
          <button class="btn-primary" id="start-practice-exam-btn" style="font-size:1.05rem; padding:0.85rem 2rem;">
            ⚡ Start Practice Test (Instant Feedback)
          </button>
          <button class="btn-secondary" id="start-timed-exam-btn" style="font-size:1.05rem; padding:0.85rem 2rem;">
            ⏱ Start Official Timed Exam (25 min)
          </button>
        </div>
      </div>
    `;

    document.getElementById('start-practice-exam-btn').addEventListener('click', () => {
      startExam('practice');
    });
    document.getElementById('start-timed-exam-btn').addEventListener('click', () => {
      startExam('timed');
    });
  }

  function startExam(mode) {
    state.examMode = mode;
    state.examSubmitted = false;
    state.currentQuestionIdx = 0;
    state.examUserAnswers = {};
    state.examSecondsLeft = 25 * 60;

    // Shuffle and pick 25 questions
    const shuffled = [...DATA.questions].sort(() => 0.5 - Math.random());
    state.examQuestions = shuffled.slice(0, 25);

    if (mode === 'timed') {
      if (state.examTimerInterval) clearInterval(state.examTimerInterval);
      state.examTimerInterval = setInterval(() => {
        state.examSecondsLeft--;
        const timerEl = document.getElementById('exam-live-timer');
        if (timerEl) {
          const m = Math.floor(state.examSecondsLeft / 60);
          const s = state.examSecondsLeft % 60;
          timerEl.textContent = `${m}:${s < 10 ? '0' : ''}${s}`;
        }
        if (state.examSecondsLeft <= 0) {
          clearInterval(state.examTimerInterval);
          finishExam();
        }
      }, 1000);
    }

    renderExamQuestion();
  }

  function renderExamQuestion() {
    const container = document.getElementById('exam-stage-container');
    if (!container) return;

    const q = state.examQuestions[state.currentQuestionIdx];
    const total = state.examQuestions.length;
    const answeredCount = Object.keys(state.examUserAnswers).length;
    const progressPct = Math.round((answeredCount / total) * 100);

    const selectedOption = state.examUserAnswers[q.id];
    const isAnswered = selectedOption !== undefined;

    let html = `
      <div class="exam-active-card">
        <div class="exam-header-bar">
          <div class="exam-progress-wrap">
            <div class="exam-progress-text">
              <span>Question ${state.currentQuestionIdx + 1} of ${total}</span>
              <span>${progressPct}% Completed</span>
            </div>
            <div class="progress-bar-bg">
              <div class="progress-bar-fill" style="width:${progressPct}%"></div>
            </div>
          </div>
          ${state.examMode === 'timed' ? `
            <div class="exam-timer" id="exam-live-timer">
              ${Math.floor(state.examSecondsLeft / 60)}:${(state.examSecondsLeft % 60) < 10 ? '0' : ''}${state.examSecondsLeft % 60}
            </div>
          ` : '<span style="font-size:0.85rem; font-weight:700; color:var(--text-accent);">Practice Mode</span>'}
        </div>

        <h3 class="exam-question-text">${q.question}</h3>

        ${q.image ? `
          <div class="exam-question-image">
            <img src="${q.image}" alt="Road Question Graphic" />
          </div>
        ` : ''}

        <div class="exam-options-list">
    `;

    q.options.forEach((opt, idx) => {
      const letters = ['A', 'B', 'C', 'D'];
      let optionClass = '';

      if (isAnswered) {
        if (state.examMode === 'practice') {
          if (idx === q.correctIndex) {
            optionClass = 'correct';
          } else if (idx === selectedOption) {
            optionClass = 'incorrect';
          }
        } else {
          if (idx === selectedOption) {
            optionClass = 'selected';
          }
        }
      }

      html += `
        <div class="exam-option-item ${optionClass}" data-idx="${idx}">
          <div class="exam-option-letter">${letters[idx]}</div>
          <div>${opt}</div>
        </div>
      `;
    });

    html += `</div>`;

    // Feedback in practice mode
    if (isAnswered && state.examMode === 'practice') {
      const isCorrect = selectedOption === q.correctIndex;
      html += `
        <div class="exam-feedback-card ${isCorrect ? 'correct' : 'incorrect'}">
          <strong>${isCorrect ? '✓ Correct!' : '✗ Incorrect!'}</strong>
          <p style="margin-top:0.35rem;">${q.explanation}</p>
          <span style="font-size:0.8rem; opacity:0.8; display:block; margin-top:0.5rem;">📖 Reference: ${q.rule}</span>
        </div>
      `;
    }

    // Action buttons
    html += `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-top:2rem;">
        <button class="btn-secondary" id="exam-prev-btn" ${state.currentQuestionIdx === 0 ? 'disabled style="opacity:0.4; cursor:not-allowed;"' : ''}>
          ← Previous
        </button>
        <div style="display:flex; gap:0.75rem;">
          ${state.currentQuestionIdx < total - 1 ? `
            <button class="btn-primary" id="exam-next-btn">
              Next Question →
            </button>
          ` : `
            <button class="btn-primary" id="exam-finish-btn" style="background:var(--mo-green);">
              Submit & See Results ✓
            </button>
          `}
        </div>
      </div>
    `;

    html += `</div>`;
    container.innerHTML = html;

    // Attach option click listeners
    container.querySelectorAll('.exam-option-item').forEach(item => {
      item.addEventListener('click', () => {
        if (state.examMode === 'practice' && isAnswered) return;
        const chosenIdx = parseInt(item.dataset.idx, 10);
        state.examUserAnswers[q.id] = chosenIdx;
        renderExamQuestion();
      });
    });

    const prevBtn = document.getElementById('exam-prev-btn');
    if (prevBtn && state.currentQuestionIdx > 0) {
      prevBtn.addEventListener('click', () => {
        state.currentQuestionIdx--;
        renderExamQuestion();
      });
    }

    const nextBtn = document.getElementById('exam-next-btn');
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        state.currentQuestionIdx++;
        renderExamQuestion();
      });
    }

    const finishBtn = document.getElementById('exam-finish-btn');
    if (finishBtn) {
      finishBtn.addEventListener('click', finishExam);
    }
  }

  function finishExam() {
    if (state.examTimerInterval) clearInterval(state.examTimerInterval);
    state.examSubmitted = true;

    let score = 0;
    state.examQuestions.forEach(q => {
      if (state.examUserAnswers[q.id] === q.correctIndex) {
        score++;
      }
    });

    const pct = Math.round((score / state.examQuestions.length) * 100);
    const passed = score >= 20;

    const container = document.getElementById('exam-stage-container');
    if (!container) return;

    container.innerHTML = `
      <div class="exam-result-card">
        <div class="result-score-circle ${passed ? 'pass' : 'fail'}">
          ${score}/25
          <span style="font-size:0.9rem; font-weight:700;">${pct}%</span>
        </div>
        <h2 class="result-title">${passed ? '🎉 Congratulations! You Passed!' : 'Needs Review - Keep Practicing!'}</h2>
        <p class="result-subtitle">
          ${passed 
            ? 'You scored 20 or more correct answers, meeting the official Missouri Department of Revenue standard.' 
            : 'You scored below the 80% passing threshold (20 of 25). Review your missed questions below and retake the test!'}
        </p>

        <div style="display:flex; justify-content:center; gap:1rem; flex-wrap:wrap; margin-bottom:2.5rem;">
          <button class="btn-primary" id="retake-exam-btn">Retake Exam</button>
          <button class="btn-secondary" id="study-handbook-btn">Review Handbook</button>
        </div>

        <h3 style="text-align:left; font-size:1.35rem; margin-bottom:1rem; border-bottom:1px solid var(--border-color); padding-bottom:0.5rem;">
          Question Review (${score} Correct, ${25 - score} Missed)
        </h3>
        <div style="display:flex; flex-direction:column; gap:1rem; text-align:left;">
          ${state.examQuestions.map((q, idx) => {
            const userAns = state.examUserAnswers[q.id];
            const isCorrect = userAns === q.correctIndex;
            return `
              <div style="background:var(--bg-elevated); border:1px solid ${isCorrect ? 'rgba(16,185,129,0.3)' : 'rgba(239,68,68,0.3)'}; border-radius:var(--radius-md); padding:1.25rem;">
                <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
                  <strong style="font-size:1.05rem;">Q${idx + 1}: ${q.question}</strong>
                  <span style="font-weight:700; color:${isCorrect ? 'var(--mo-green)' : 'var(--mo-red)'}; font-size:0.9rem;">
                    ${isCorrect ? '✓ Correct' : '✗ Missed'}
                  </span>
                </div>
                ${q.image ? `<img src="${q.image}" style="max-height:80px; margin:0.5rem 0;" />` : ''}
                <div style="font-size:0.9rem; margin-bottom:0.35rem;">
                  Your answer: <strong>${userAns !== undefined ? q.options[userAns] : 'Not answered'}</strong>
                </div>
                ${!isCorrect ? `
                  <div style="font-size:0.9rem; color:var(--mo-green); margin-bottom:0.35rem;">
                    Correct answer: <strong>${q.options[q.correctIndex]}</strong>
                  </div>
                ` : ''}
                <p style="font-size:0.85rem; color:var(--text-secondary); margin-top:0.5rem;">${q.explanation}</p>
                <span style="font-size:0.75rem; color:var(--text-accent); display:block; margin-top:0.35rem;">📖 Reference: ${q.rule}</span>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;

    document.getElementById('retake-exam-btn').addEventListener('click', showExamWelcome);
    document.getElementById('study-handbook-btn').addEventListener('click', () => switchTab('reader'));
  }

  // -------------------------------------------------------------
  // 3. Road Signs & 3D Flashcards
  // -------------------------------------------------------------
  function renderSignsAndFlashcards() {
    const pillsContainer = document.getElementById('signs-category-pills');
    const cardsGrid = document.getElementById('flashcards-grid');
    if (!cardsGrid) return;

    const categories = [
      { id: 'all', label: 'All Signs & Graphics' },
      { id: 'regulatory', label: 'Regulatory Signs' },
      { id: 'warning', label: 'Warning Signs' },
      { id: 'workzone', label: 'Work Zone Signs' },
      { id: 'guide', label: 'Guide & Services' },
      { id: 'shapes', label: 'Sign Shapes' },
      { id: 'diagram', label: 'Driving Maneuver Diagrams' }
    ];

    if (pillsContainer && pillsContainer.children.length === 0) {
      categories.forEach(cat => {
        const btn = document.createElement('button');
        btn.className = `sign-cat-btn ${state.signFilter === cat.id ? 'active' : ''}`;
        btn.textContent = cat.label;
        btn.addEventListener('click', () => {
          state.signFilter = cat.id;
          pillsContainer.querySelectorAll('.sign-cat-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          renderSignsAndFlashcards();
        });
        pillsContainer.appendChild(btn);
      });
    }

    const filtered = state.signFilter === 'all' 
      ? DATA.figures 
      : DATA.figures.filter(f => f.category === state.signFilter);

    cardsGrid.innerHTML = '';
    filtered.forEach(fig => {
      const card = document.createElement('div');
      card.className = 'flip-card';
      card.innerHTML = `
        <div class="flip-card-inner">
          <div class="flip-card-front">
            <div class="flip-card-image-box">
              <img src="${fig.image}?v=2026.2" alt="${fig.title}" loading="lazy" />
            </div>
            <div class="flip-card-title">${fig.title}</div>
            <div class="flip-hint">Click or Tap to Flip ↻</div>
          </div>
          <div class="flip-card-back">
            <div class="flip-back-badge">${fig.category}</div>
            <div class="flip-back-title">${fig.title}</div>
            <div class="flip-back-desc">${fig.description}</div>
            <div class="flip-back-page">📖 Missouri Driver Guide Page ${fig.page}</div>
          </div>
        </div>
      `;

      card.addEventListener('click', () => {
        card.classList.toggle('flipped');
      });

      cardsGrid.appendChild(card);
    });
  }

  // -------------------------------------------------------------
  // 4. Calculators & Simulators
  // -------------------------------------------------------------
  function initCalculators() {
    const slider = document.getElementById('calc-speed-slider');
    const speedNum = document.getElementById('calc-speed-num');
    const roadCond = document.getElementById('calc-road-cond');

    if (slider && speedNum) {
      function updateStoppingDistances() {
        const speed = parseInt(slider.value, 10);
        state.calcSpeed = speed;
        speedNum.textContent = `${speed} mph`;

        // Physics formulas from Missouri Guide (Chapter 8):
        // Reaction time ~ 1.5 seconds -> distance = speed * 1.467 * 1.5
        const reactionDist = Math.round(speed * 1.467 * 1.5);
        // Braking distance ~ speed^2 / (30 * f) where f is friction (~0.7 dry, ~0.4 wet)
        const isWet = roadCond ? roadCond.value === 'wet' : false;
        const friction = isWet ? 0.38 : 0.72;
        const brakingDist = Math.round((speed * speed) / (30 * friction));
        const totalDist = reactionDist + brakingDist;

        // Approximate car lengths (avg car ~15 ft)
        const carLengths = Math.round(totalDist / 15);

        document.getElementById('dist-reaction-val').textContent = `${reactionDist} ft`;
        document.getElementById('dist-braking-val').textContent = `${brakingDist} ft`;
        document.getElementById('dist-total-val').textContent = `${totalDist} ft (~${carLengths} car lengths)`;

        // Max scale ~ 450 ft for 75mph wet
        const maxScale = 500;
        document.getElementById('bar-fill-reaction').style.width = `${Math.min(100, (reactionDist / maxScale) * 100)}%`;
        document.getElementById('bar-fill-braking').style.width = `${Math.min(100, (brakingDist / maxScale) * 100)}%`;
        document.getElementById('bar-fill-total').style.width = `${Math.min(100, (totalDist / maxScale) * 100)}%`;
      }

      slider.addEventListener('input', updateStoppingDistances);
      if (roadCond) roadCond.addEventListener('change', updateStoppingDistances);
      updateStoppingDistances();
    }

    // Points System Calculator
    const pointsList = document.getElementById('points-violations-list');
    if (pointsList && pointsList.children.length === 0) {
      const violations = [
        { id: 'v1', label: 'Speeding 5 to 29 mph over limit (State)', pts: 3 },
        { id: 'v2', label: 'Speeding 5 to 29 mph over limit (Municipal)', pts: 2 },
        { id: 'v3', label: 'Speeding 30+ mph over posted limit', pts: 4 },
        { id: 'v4', label: 'Careless and Imprudent Driving', pts: 4 },
        { id: 'v5', label: 'Failure to Maintain Financial Responsibility', pts: 4 },
        { id: 'v6', label: 'Leaving the Scene of an Accident', pts: 8 },
        { id: 'v7', label: 'Driving While Intoxicated (1st offense)', pts: 8 },
        { id: 'v8', label: 'Driving While Suspended / Revoked', pts: 12 },
        { id: 'v9', label: 'Felony involving a motor vehicle', pts: 12 }
      ];

      violations.forEach(v => {
        const item = document.createElement('div');
        item.className = 'violation-check-item';
        item.innerHTML = `
          <label style="display:flex; align-items:center; gap:0.6rem; cursor:pointer; flex:1;">
            <input type="checkbox" data-pts="${v.pts}" style="width:16px; height:16px; cursor:pointer;" />
            <span>${v.label}</span>
          </label>
          <span class="violation-pts">+${v.pts} pts</span>
        `;

        item.querySelector('input').addEventListener('change', updatePointsGauge);
        pointsList.appendChild(item);
      });
    }
  }

  function updatePointsGauge() {
    const checkboxes = document.querySelectorAll('#points-violations-list input[type="checkbox"]');
    let totalPts = 0;
    checkboxes.forEach(cb => {
      if (cb.checked) totalPts += parseInt(cb.dataset.pts, 10);
    });

    const numEl = document.getElementById('points-total-num');
    const badgeEl = document.getElementById('points-status-badge');
    if (!numEl || !badgeEl) return;

    numEl.textContent = totalPts;

    if (totalPts >= 12) {
      badgeEl.className = 'points-status-badge status-danger';
      badgeEl.textContent = '🚨 1-Year Revocation (12 pts accumulated)';
    } else if (totalPts >= 8) {
      badgeEl.className = 'points-status-badge status-danger';
      badgeEl.textContent = '⛔ License Suspended (8 pts in 18 months)';
    } else if (totalPts >= 4) {
      badgeEl.className = 'points-status-badge status-warning';
      badgeEl.textContent = '⚠️ Official Advisory Warning Letter (4 pts)';
    } else {
      badgeEl.className = 'points-status-badge status-safe';
      badgeEl.textContent = '✓ License in Good Standing';
    }
  }

  // -------------------------------------------------------------
  // 5. PDF Mirror Grid
  // -------------------------------------------------------------
  function renderPdfMirrorGrid() {
    const grid = document.getElementById('pdf-mirror-pages-grid');
    if (!grid) return;

    if (grid.children.length === 0) {
      DATA.pages_meta.forEach(p => {
        const card = document.createElement('div');
        card.style.cssText = `
          background: var(--bg-card);
          border: 1px solid var(--border-color);
          border-radius: var(--radius-md);
          padding: 0.75rem;
          display: flex;
          flex-direction: column;
          align-items: center;
          cursor: pointer;
          transition: transform var(--transition-fast), border-color var(--transition-fast);
        `;
        card.innerHTML = `
          <div style="width:100%; height:180px; overflow:hidden; border-radius:4px; background:#000; margin-bottom:0.5rem;">
            <img src="${p.file}" alt="Page ${p.page_number}" loading="lazy" style="width:100%; height:100%; object-fit:cover;" />
          </div>
          <div style="font-weight:700; font-size:0.85rem;">Page ${p.page_number}</div>
          <div style="font-size:0.75rem; color:var(--text-secondary);">Manual p. ${p.book_page}</div>
        `;

        card.addEventListener('mouseenter', () => { card.style.borderColor = 'var(--primary)'; card.style.transform = 'translateY(-3px)'; });
        card.addEventListener('mouseleave', () => { card.style.borderColor = 'var(--border-color)'; card.style.transform = 'translateY(0)'; });

        card.addEventListener('click', () => {
          openPdfMirror(p.page_number, `Official Manual Page ${p.book_page}`);
        });

        grid.appendChild(card);
      });
    }
  }

  function openPdfMirror(pageNumber, title) {
    if (!el.mirrorModal || !el.mirrorImg) return;
    el.mirrorImg.src = `assets/pages/page_${String(pageNumber).padStart(3, '0')}.webp`;
    if (el.mirrorTitle) el.mirrorTitle.textContent = title || `Missouri Driver Guide`;
    if (el.mirrorPageNum) el.mirrorPageNum.textContent = `Page ${pageNumber} of 102`;
    el.mirrorModal.classList.add('open');
  }

  function closePdfMirror() {
    if (el.mirrorModal) el.mirrorModal.classList.remove('open');
  }

  // -------------------------------------------------------------
  // 6. Global Search (Cmd+K / /)
  // -------------------------------------------------------------
  function openSearchModal() {
    if (!el.searchModal) return;
    el.searchModal.classList.add('open');
    if (el.searchInput) {
      el.searchInput.value = '';
      el.searchInput.focus();
    }
    renderSearchResults('');
  }

  function closeSearchModal() {
    if (el.searchModal) el.searchModal.classList.remove('open');
  }

  function renderSearchResults(query) {
    if (!el.searchResults) return;
    const q = query.trim().toLowerCase();

    if (!q) {
      el.searchResults.innerHTML = `
        <div style="padding:1.5rem; text-align:center; color:var(--text-muted); font-size:0.9rem;">
          Type to search laws, signs, speed limits, points, or chapters...
        </div>
      `;
      return;
    }

    const matches = [];

    // Search signs
    DATA.figures.forEach(fig => {
      if (fig.title.toLowerCase().includes(q) || fig.description.toLowerCase().includes(q)) {
        matches.push({
          type: 'sign',
          title: fig.title,
          subtitle: `Road Sign / Diagram (${fig.category}) - Page ${fig.page}`,
          snippet: fig.description,
          action: () => {
            closeSearchModal();
            switchTab('signs');
          }
        });
      }
    });

    // Search chapters
    DATA.chapters.forEach(ch => {
      if (ch.title.toLowerCase().includes(q) || ch.summary.toLowerCase().includes(q)) {
        matches.push({
          type: 'chapter',
          title: ch.title,
          subtitle: `Chapter ${ch.number} (Pages ${ch.start_page}–${ch.end_page})`,
          snippet: ch.summary,
          action: () => {
            closeSearchModal();
            state.currentChapterId = ch.id;
            switchTab('reader');
          }
        });
      }

      // Search in text blocks
      ch.pages.forEach(pg => {
        pg.blocks.forEach(b => {
          const lower = b.text.toLowerCase();
          const idx = lower.indexOf(q);
          if (idx !== -1 && matches.length < 25) {
            const start = Math.max(0, idx - 40);
            const end = Math.min(b.text.length, idx + q.length + 60);
            let snippet = b.text.substring(start, end).replace(/\n/g, ' ');
            if (start > 0) snippet = '...' + snippet;
            if (end < b.text.length) snippet += '...';

            matches.push({
              type: 'text',
              title: `${ch.title} (Page ${pg.page_number})`,
              subtitle: b.first_line !== b.text ? b.first_line : `Manual page ${pg.book_page}`,
              snippet: snippet,
              query: q,
              action: () => {
                closeSearchModal();
                state.currentChapterId = ch.id;
                switchTab('reader');
              }
            });
          }
        });
      });
    });

    if (matches.length === 0) {
      el.searchResults.innerHTML = `
        <div style="padding:1.5rem; text-align:center; color:var(--text-muted); font-size:0.9rem;">
          No matching results found for "<strong>${escapeHtml(query)}</strong>".
        </div>
      `;
      return;
    }

    el.searchResults.innerHTML = matches.slice(0, 20).map(m => {
      let highlightedSnippet = escapeHtml(m.snippet);
      if (m.query) {
        const regex = new RegExp(`(${escapeRegex(m.query)})`, 'gi');
        highlightedSnippet = highlightedSnippet.replace(regex, '<mark>$1</mark>');
      }

      return `
        <div class="search-result-item" data-id="${m.title}">
          <div class="search-res-title">${escapeHtml(m.title)}</div>
          <div style="font-size:0.75rem; color:var(--text-accent); margin-bottom:0.25rem;">${escapeHtml(m.subtitle)}</div>
          <div class="search-res-snippet">${highlightedSnippet}</div>
        </div>
      `;
    }).join('');

    // Attach click events
    const items = el.searchResults.querySelectorAll('.search-result-item');
    items.forEach((item, idx) => {
      item.addEventListener('click', () => {
        matches[idx].action();
      });
    });
  }

  function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  // -------------------------------------------------------------
  // Initialization & Event Listeners
  // -------------------------------------------------------------
  function init() {
    applyTheme(state.theme);

    // Header tabs
    el.tabs.forEach(btn => {
      btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });

    // Theme toggle
    if (el.themeToggleBtn) {
      el.themeToggleBtn.addEventListener('click', () => {
        applyTheme(state.theme === 'dark' ? 'light' : 'dark');
      });
    }

    // Hero buttons
    const heroReadBtn = document.getElementById('hero-read-btn');
    if (heroReadBtn) heroReadBtn.addEventListener('click', () => switchTab('reader'));

    const heroExamBtn = document.getElementById('hero-exam-btn');
    if (heroExamBtn) heroExamBtn.addEventListener('click', () => switchTab('exam'));

    const heroSignsBtn = document.getElementById('hero-signs-btn');
    if (heroSignsBtn) heroSignsBtn.addEventListener('click', () => switchTab('signs'));

    // Search events
    el.searchTriggers.forEach(btn => btn.addEventListener('click', openSearchModal));
    if (el.searchInput) {
      el.searchInput.addEventListener('input', (e) => renderSearchResults(e.target.value));
    }

    // Keyboard shortcuts
    window.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        openSearchModal();
      } else if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
        e.preventDefault();
        openSearchModal();
      } else if (e.key === 'Escape') {
        closeSearchModal();
        closePdfMirror();
      }
    });

    // Close search modal when clicking backdrop
    if (el.searchModal) {
      el.searchModal.addEventListener('click', (e) => {
        if (e.target === el.searchModal) closeSearchModal();
      });
    }

    const closeSearchBtn = document.getElementById('close-search-btn');
    if (closeSearchBtn) closeSearchBtn.addEventListener('click', closeSearchModal);

    // Close PDF mirror modal
    if (el.mirrorModal) {
      el.mirrorModal.addEventListener('click', (e) => {
        if (e.target === el.mirrorModal) closePdfMirror();
      });
    }
    const closeMirrorBtn = document.getElementById('close-mirror-btn');
    if (closeMirrorBtn) closeMirrorBtn.addEventListener('click', closePdfMirror);

    // Font size controls
    const fontInc = document.getElementById('font-increase-btn');
    const fontDec = document.getElementById('font-decrease-btn');
    if (fontInc) {
      fontInc.addEventListener('click', () => {
        state.fontSize = Math.min(24, state.fontSize + 2);
        localStorage.setItem('mo_guide_font_size', state.fontSize);
        const bodyEl = document.querySelector('.chapter-body');
        if (bodyEl) bodyEl.style.fontSize = `${state.fontSize}px`;
      });
    }
    if (fontDec) {
      fontDec.addEventListener('click', () => {
        state.fontSize = Math.max(13, state.fontSize - 2);
        localStorage.setItem('mo_guide_font_size', state.fontSize);
        const bodyEl = document.querySelector('.chapter-body');
        if (bodyEl) bodyEl.style.fontSize = `${state.fontSize}px`;
      });
    }

    // Mobile chapter menu toggle
    const mobileChTrigger = document.getElementById('mobile-chapter-trigger-btn');
    const readerSidebar = document.getElementById('reader-sidebar');
    if (mobileChTrigger && readerSidebar) {
      mobileChTrigger.addEventListener('click', () => {
        const isOpen = readerSidebar.classList.toggle('open');
        mobileChTrigger.classList.toggle('active', isOpen);
        mobileChTrigger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      });
    }

    // Deep linking & initial tab detection from URL hash
    const validTabs = ['reader', 'exam', 'signs', 'calculators', 'pdf-mirror'];
    const currentHash = (window.location.hash || '').replace('#', '').toLowerCase();
    if (validTabs.includes(currentHash)) {
      switchTab(currentHash, false);
    } else {
      switchTab('reader', false);
    }

    // Listen for browser back/forward or manual hash updates
    window.addEventListener('hashchange', () => {
      const hash = (window.location.hash || '').replace('#', '').toLowerCase();
      if (validTabs.includes(hash) && hash !== state.currentTab) {
        switchTab(hash, false);
      }
    });

    // Register Service Worker for offline PWA capabilities
    if ('serviceWorker' in navigator && (window.location.protocol === 'https:' || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js')
          .then((reg) => {
            console.log('[PWA] Service Worker registered successfully:', reg.scope);
          })
          .catch((err) => {
            console.warn('[PWA] Service Worker registration failed:', err);
          });
      });
    }
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
