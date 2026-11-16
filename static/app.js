/**
 * Koç University ELC INT 07 - Midterm & Speaking Task AI Assistant
 * Client-side Application Logic
 */

// Application State
const state = {
  currentTab: 'midterm', // 'midterm', 'sentence', 'cards', 'speaking', 'tests'
  activeChatId: null,
  chatSessions: [],
  currentAttachment: null, // in-memory { name, mime_type, base64, size }
  
  // Sentence Level Booster
  sentenceFocus: 'Otomatik (Materyale Göre)',
  isUpgradingSentence: false,

  // Flashcards
  flashcards: [],
  currentCardIndex: 0,
  isCardFlipped: false,
  learnedCards: [], // list of learned headwords

  // Interactive Tests & AI Quiz
  tests: [],
  currentQuestionIndex: 0,
  testScore: 0,
  testStreak: 0,
  answeredQuestions: {}, // questionId -> { answered: true, isCorrect: boolean, selected: any }
  quizMode: 'chat', // 'chat' or 'manual'
  quizSelectedChatId: null, // Selected session ID for chat-based quiz
  wrongQuestions: [], // [{ question, topic, explanation }]

  // File Converter
  selectedConvertFile: null,

  // Generation & Abort state
  isGenerating: false,
  chatAbortController: null,

  // Text to Speech
  activeAudioMsgIndex: null,
  isModelAudioPlaying: false,

  // Speaking Task
  speaking: {
    promptId: 1,
    isRecording: false,
    prepTimer: null,
    prepTimeLeft: 60,
    speakTimer: null,
    speakTimeLeft: 120,
    recognition: null,
    transcript: '',
    lastEvaluation: null
  },

  // Chat Voice
  chatRecognition: null,
  isChatRecording: false
};

// Official Speaking Prompts Data
const SPEAKING_PROMPTS = {
  1: {
    id: 1,
    badge: "Task 1 • Official SBS Prompt",
    title: "Restaurant Food & Consumer Decisions",
    text: "Think about the last time you bought food from a restaurant. What kind of food did you buy? Where did you buy it from? Did you eat in a restaurant, did you buy takeout food, or did you have food delivered? How did you choose which item(s) to order? What factors did you consider? Do you think you got a good deal? Why or why not?"
  },
  2: {
    id: 2,
    badge: "Task 2 • Official SBS Prompt",
    title: "Personality Traits (Nature vs. Nurture)",
    text: "Think about the personality of someone you know well, such as a relative, a friend, or yourself. Who is this person? Which of the person's personality traits do you think are genetic? Why do you think that? Which of the person's personality traits do you think are due to their background? Why do you think that? If you think this person's personality has changed, which factors do you think were responsible for the changes?"
  },
  3: {
    id: 3,
    badge: "Task 3 • Official SBS Prompt",
    title: "Relocation & Moving to a New Place",
    text: "Think of a place that you or someone you know would like to move to. Why would you/they want to move there? What advantages would living in this place give you/them? Can you think of any disadvantages? Would you/they like to settle there or just stay for a short time? Explain in detail."
  },
  4: {
    id: 4,
    badge: "Task 4 • Official SBS Prompt",
    title: "Natural Place / Geographical Feature",
    text: "Think about a natural place or geographical feature you know well. Where is it? What does it look like? What impact does it have on people's lives? What is being done to protect the place? What further steps should be taken to preserve it?"
  },
  5: {
    id: 5,
    badge: "Task 5 • Official SBS Prompt",
    title: "Career Aspirations & Perfect Job",
    text: "Think about your perfect job. This could be a first job or a job you have later in your career. What is your perfect job? What interests you about this job? What would you have to do in that job? What education or training do you need for the job? What kind of person would be ideal for the job? Why do you think this would be a good job for you?"
  }
};

// -------------------------------------------------------------
// INITIALIZATION
// -------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
  loadChatSessionsFromStorage();
  initDrawer();
  setupSpeechRecognition();
  setupEventListeners();
  setupConverterDragAndDrop();
  setupKeyboardShortcuts();
  loadInitialFlashcards();
});

// -------------------------------------------------------------
// NAVIGATION TABS
// -------------------------------------------------------------
function switchTab(tabName) {
  state.currentTab = tabName;

  const tabMidterm = document.getElementById('tabContentMidterm');
  const tabSentence = document.getElementById('tabContentSentence');
  const tabCards = document.getElementById('tabContentCards');
  const tabSpeaking = document.getElementById('tabContentSpeaking');
  const tabTests = document.getElementById('tabContentTests');
  const floatingInput = document.getElementById('floatingInputBar');

  const btnMidterm = document.getElementById('navTabMidterm');
  const btnSentence = document.getElementById('navTabSentence');
  const btnCards = document.getElementById('navTabCards');
  const btnSpeaking = document.getElementById('navTabSpeaking');
  const btnTests = document.getElementById('navTabTests');

  // Hide all tabs
  [tabMidterm, tabSentence, tabCards, tabSpeaking, tabTests].forEach(tab => {
    if (tab) tab.classList.add('hidden');
  });

  const activeClasses = ['bg-surface-container-high', 'text-on-surface', 'shadow-[0_2px_12px_rgba(166,25,46,0.35)]', 'ring-1', 'ring-primary/40'];
  const inactiveClasses = ['text-on-surface-variant'];

  [btnMidterm, btnSentence, btnCards, btnSpeaking, btnTests].forEach(btn => {
    if (btn) {
      btn.classList.remove(...activeClasses);
      btn.classList.add(...inactiveClasses);
    }
  });

  if (tabName === 'midterm') {
    tabMidterm.classList.remove('hidden');
    btnMidterm.classList.add(...activeClasses);
    btnMidterm.classList.remove(...inactiveClasses);
    if (floatingInput) floatingInput.classList.remove('hidden');
    renderChatMessages();
  } else if (tabName === 'sentence') {
    tabSentence.classList.remove('hidden');
    btnSentence.classList.add(...activeClasses);
    btnSentence.classList.remove(...inactiveClasses);
    if (floatingInput) floatingInput.classList.add('hidden');
  } else if (tabName === 'cards') {
    tabCards.classList.remove('hidden');
    btnCards.classList.add(...activeClasses);
    btnCards.classList.remove(...inactiveClasses);
    if (floatingInput) floatingInput.classList.add('hidden');
    if (state.flashcards.length === 0) {
      loadInitialFlashcards();
    }
  } else if (tabName === 'speaking') {
    tabSpeaking.classList.remove('hidden');
    btnSpeaking.classList.add(...activeClasses);
    btnSpeaking.classList.remove(...inactiveClasses);
    if (floatingInput) floatingInput.classList.add('hidden');
  } else if (tabName === 'tests') {
    tabTests.classList.remove('hidden');
    btnTests.classList.add(...activeClasses);
    btnTests.classList.remove(...inactiveClasses);
    if (floatingInput) floatingInput.classList.add('hidden');
  }
}

// -------------------------------------------------------------
// CHAT SESSION & DRAWER MANAGEMENT
// -------------------------------------------------------------
function initDrawer() {
  const openBtn = document.getElementById('openDrawerBtn');
  const closeBtn = document.getElementById('closeDrawerBtn');
  const overlay = document.getElementById('drawerOverlay');
  const drawer = document.getElementById('chatDrawer');

  if (openBtn) {
    openBtn.addEventListener('click', () => {
      drawer.classList.remove('-translate-x-full');
      overlay.classList.remove('opacity-0', 'pointer-events-none');
      overlay.classList.add('opacity-100');
      renderDrawerHistoryList();
    });
  }

  function closeDrawer() {
    drawer.classList.add('-translate-x-full');
    overlay.classList.add('opacity-0', 'pointer-events-none');
    overlay.classList.remove('opacity-100');
  }

  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
  if (overlay) overlay.addEventListener('click', closeDrawer);

  const newChatBtn = document.getElementById('newChatBtn');
  if (newChatBtn) {
    newChatBtn.addEventListener('click', () => {
      createNewChatSession();
      closeDrawer();
    });
  }

  const searchInput = document.getElementById('searchHistoryInput');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      renderDrawerHistoryList(e.target.value.toLowerCase());
    });
  }

  const clearAllBtn = document.getElementById('clearAllHistoryBtn');
  if (clearAllBtn) {
    clearAllBtn.addEventListener('click', () => {
      if (confirm('Tüm çalışma sohbetlerini silmek istediğinize emin misiniz?')) {
        state.chatSessions = [];
        saveChatSessionsToStorage();
        createNewChatSession();
        closeDrawer();
      }
    });
  }
}

function loadChatSessionsFromStorage() {
  const saved = localStorage.getItem('elc_chat_sessions');
  if (saved) {
    try {
      state.chatSessions = JSON.parse(saved);
    } catch (e) {
      console.warn('Error reading chat sessions:', e);
      state.chatSessions = [];
    }
  }

  if (!state.chatSessions || !Array.isArray(state.chatSessions) || state.chatSessions.length === 0) {
    createNewChatSession(false);
  } else {
    state.activeChatId = state.chatSessions[0].id;
    renderChatMessages();
    renderDrawerHistoryList();
  }
}

function saveChatSessionsToStorage() {
  try {
    const sanitized = state.chatSessions.map(session => ({
      id: session.id,
      title: session.title,
      createdAt: session.createdAt,
      messages: (session.messages || []).map(m => ({
        role: m.role,
        content: m.content,
        timestamp: m.timestamp,
        attachment: m.attachment ? { name: m.attachment.name, mime_type: m.attachment.mime_type } : null
      }))
    }));
    localStorage.setItem('elc_chat_sessions', JSON.stringify(sanitized));
  } catch (err) {
    console.warn('LocalStorage save quota exceeded, trimming older sessions:', err);
    try {
      state.chatSessions = state.chatSessions.slice(0, 5);
      localStorage.setItem('elc_chat_sessions', JSON.stringify(state.chatSessions));
    } catch (e) {}
  }
}

function createNewChatSession(render = true) {
  const newId = 'session_' + Date.now();
  const newSession = {
    id: newId,
    title: 'Yeni Çalışma Oturumu',
    createdAt: new Date().toISOString(),
    messages: []
  };
  state.chatSessions.unshift(newSession);
  state.activeChatId = newId;
  saveChatSessionsToStorage();

  if (render) {
    switchTab('midterm');
    renderChatMessages();
    renderDrawerHistoryList();
  }
}

function getActiveChat() {
  let session = state.chatSessions.find(s => s.id === state.activeChatId);
  if (!session && state.chatSessions.length > 0) {
    session = state.chatSessions[0];
    state.activeChatId = session.id;
  }
  return session;
}

function renderDrawerHistoryList(filter = '') {
  const listContainer = document.getElementById('drawerHistoryList');
  if (!listContainer) return;

  const filtered = (state.chatSessions || []).filter(s => (s.title || '').toLowerCase().includes(filter));

  if (filtered.length === 0) {
    listContainer.innerHTML = `
      <div class="text-center py-8 text-on-surface-variant text-xs">
        <span class="material-symbols-outlined text-[28px] opacity-40">history_edu</span>
        <p class="mt-1">Kayıtlı sohbet bulunamadı.</p>
      </div>
    `;
    return;
  }

  listContainer.innerHTML = filtered.map(s => {
    const isActive = s.id === state.activeChatId;
    const msgCount = (s.messages || []).length;
    const timeStr = new Date(s.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    return `
      <div onclick="selectChatSession('${s.id}')" class="p-2.5 rounded-xl transition-all cursor-pointer flex items-center justify-between group ${isActive ? 'bg-primary-container/20 border border-primary/30 text-white' : 'bg-surface-container hover:bg-surface-container-high text-on-surface'}">
        <div class="flex items-center gap-2 overflow-hidden">
          <span class="material-symbols-outlined text-[18px] ${isActive ? 'text-primary' : 'text-on-surface-variant'}">chat</span>
          <div class="truncate text-xs font-semibold">
            <span class="truncate block">${escapeHtml(s.title || 'Adsız Sohbet')}</span>
            <span class="text-[10px] text-on-surface-variant font-normal">${msgCount} mesaj • ${timeStr}</span>
          </div>
        </div>
        <button onclick="event.stopPropagation(); deleteChatSession('${s.id}')" class="opacity-0 group-hover:opacity-100 hover:text-error transition-opacity p-1">
          <span class="material-symbols-outlined text-[16px]">delete</span>
        </button>
      </div>
    `;
  }).join('');
}

function selectChatSession(sessionId) {
  state.activeChatId = sessionId;
  switchTab('midterm');
  renderChatMessages();
  renderDrawerHistoryList();
  const drawer = document.getElementById('chatDrawer');
  const overlay = document.getElementById('drawerOverlay');
  if (drawer) drawer.classList.add('-translate-x-full');
  if (overlay) {
    overlay.classList.add('opacity-0', 'pointer-events-none');
    overlay.classList.remove('opacity-100');
  }
}

function deleteChatSession(sessionId) {
  state.chatSessions = state.chatSessions.filter(s => s.id !== sessionId);
  if (state.chatSessions.length === 0) {
    createNewChatSession(false);
  } else if (state.activeChatId === sessionId) {
    state.activeChatId = state.chatSessions[0].id;
  }
  if (state.quizSelectedChatId === sessionId) {
    state.quizSelectedChatId = state.activeChatId;
  }
  saveChatSessionsToStorage();
  renderChatMessages();
  renderDrawerHistoryList();
}

function renderChatMessages() {
  const container = document.getElementById('chatStream');
  if (!container) return;

  const session = getActiveChat();
  if (!session || !session.messages || session.messages.length === 0) {
    container.innerHTML = `
      <div class="flex flex-col items-center justify-center text-center p-8 space-y-3">
        <div class="w-14 h-14 rounded-2xl bg-primary-container/30 text-primary flex items-center justify-center ring-1 ring-primary/40 shadow-inner">
          <span class="material-symbols-outlined text-[32px]">school</span>
        </div>
        <div class="space-y-1">
          <h2 class="text-base font-bold text-on-surface">Koç ELC INT 07 Akademik Çalışma Alanı</h2>
          <p class="text-xs text-on-surface-variant max-w-sm">
            Midterm sınavı, Pathways 3 kelimeleri, gramer yapıları ve speaking konuları hakkında her şeyi sorabilir; ders notlarınızı veya taslak kompozisyonlarınızı yükleyebilirsiniz.
          </p>
        </div>
        <div class="flex flex-wrap gap-2 justify-center max-w-md pt-2">
          <button onclick="sendQuickPrompt('Midterm için Cause & Effect kompozisyonu yazarken dikkat etmem gereken 3 altın kural nedir?')" class="text-[11px] px-3 py-1.5 rounded-full bg-surface-container-high hover:bg-surface-bright text-on-surface active:scale-95 transition-all border border-white/5">
            ✍️ Cause & Effect 3 Altın Kural
          </button>
          <button onclick="sendQuickPrompt('Pathways 3 Unit 1 ve 2deki en kritik edat ve collocation kalıplarını listele.')" class="text-[11px] px-3 py-1.5 rounded-full bg-surface-container-high hover:bg-surface-bright text-on-surface active:scale-95 transition-all border border-white/5">
            📚 Unit 1-2 Edat & Kalıplar
          </button>
        </div>
      </div>
    `;
    return;
  }

  container.innerHTML = session.messages.map((m, idx) => {
    const isUser = m.role === 'user';
    const parsedHtml = isUser ? escapeHtml(m.content) : marked.parse(m.content || '');

    return `
      <div class="flex ${isUser ? 'justify-end' : 'justify-start'} w-full animate-fadeIn">
        <div class="max-w-[88%] sm:max-w-[80%] rounded-2xl p-4 ${isUser ? 'bg-gradient-to-br from-primary-container to-inverse-primary text-white shadow-md rounded-br-none' : 'bg-surface-container/90 backdrop-blur-xl text-on-surface border border-white/5 shadow-lg rounded-bl-none prose-ai'}">
          ${m.attachment ? `
            <div class="mb-2 flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-black/25 text-[11px] font-mono text-secondary">
              <span class="material-symbols-outlined text-[15px]">attachment</span>
              <span class="truncate">${escapeHtml(m.attachment.name)}</span>
            </div>
          ` : ''}
          <div class="text-xs sm:text-sm leading-relaxed">${parsedHtml}</div>
          <div class="flex items-center justify-between gap-3 mt-2 pt-1 border-t border-white/10 text-[10px] ${isUser ? 'text-white/70' : 'text-on-surface-variant'}">
            <span>${m.timestamp || ''}</span>
            ${!isUser ? `
              <div class="flex items-center gap-1.5">
                <button onclick="copyMessageText(${idx})" title="Metni Kopyala" class="hover:text-primary transition-colors">
                  <span class="material-symbols-outlined text-[14px]">content_copy</span>
                </button>
                <button onclick="speakMessageText(${idx})" title="Sesli Oku" class="hover:text-secondary transition-colors">
                  <span class="material-symbols-outlined text-[14px]">volume_up</span>
                </button>
              </div>
            ` : ''}
          </div>
        </div>
      </div>
    `;
  }).join('');

  container.scrollTop = container.scrollHeight;
}

function sendQuickPrompt(promptText) {
  const input = document.getElementById('chatPromptInput');
  if (input) {
    input.value = promptText;
    handleChatSubmit();
  }
}

function handleChatSubmit() {
  if (state.isGenerating) {
    stopChatGeneration();
  } else {
    sendChatMessage();
  }
}

function stopChatGeneration() {
  if (state.chatAbortController) {
    state.chatAbortController.abort();
    state.chatAbortController = null;
  }
  state.isGenerating = false;
  removeChatTypingIndicator();
  updateSendButtonUI(false);

  const session = getActiveChat();
  if (session) {
    session.messages.push({
      role: 'assistant',
      content: '*(Yanıt kullanıcı tarafından durduruldu)*',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    });
    renderChatMessages();
    saveChatSessionsToStorage();
  }
}

function updateSendButtonUI(generating) {
  const btn = document.getElementById('chatSendBtn');
  const icon = document.getElementById('chatSendIcon');
  const input = document.getElementById('chatPromptInput');

  if (!btn || !icon) return;

  if (generating) {
    btn.classList.remove('bg-gradient-to-br', 'from-primary-container', 'to-[#8B0000]');
    btn.classList.add('bg-red-600', 'hover:bg-red-700', 'shadow-[0_0_16px_rgba(220,38,38,0.7)]');
    icon.textContent = 'stop';
    btn.title = 'Yanıtı Durdur (Stop Generation)';
    if (input) input.placeholder = 'AI yanıt üretiyor... Durdurmak için kareye basın.';
  } else {
    btn.classList.remove('bg-red-600', 'hover:bg-red-700', 'shadow-[0_0_16px_rgba(220,38,38,0.7)]');
    btn.classList.add('bg-gradient-to-br', 'from-primary-container', 'to-[#8B0000]');
    icon.textContent = 'arrow_upward';
    btn.title = 'Gönder (Send Prompt)';
    if (input) {
      input.placeholder = 'Ask ELC 07 AI or upload notes/prompts...';
      input.disabled = false;
    }
  }
}

async function sendChatMessage() {
  if (state.isGenerating) return;

  const input = document.getElementById('chatPromptInput');
  const userText = input ? input.value.trim() : '';

  if (!userText && !state.currentAttachment) return;

  const session = getActiveChat();
  const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  if (session.messages.length === 0) {
    session.title = userText ? (userText.slice(0, 32) + (userText.length > 32 ? '...' : '')) : (state.currentAttachment ? state.currentAttachment.name : 'Ders Notu İnceleme');
  }

  const userMsg = {
    role: 'user',
    content: userText || 'Lütfen eklediğim bu belgeyi/görseli detaylıca analiz et.',
    attachment: state.currentAttachment ? { name: state.currentAttachment.name, mime_type: state.currentAttachment.mime_type } : null,
    timestamp: timeStr
  };
  session.messages.push(userMsg);
  if (input) input.value = '';

  const attachmentToSend = state.currentAttachment;
  removeAttachment();

  renderChatMessages();
  saveChatSessionsToStorage();
  renderDrawerHistoryList();

  state.isGenerating = true;
  state.chatAbortController = new AbortController();
  updateSendButtonUI(true);
  showChatTypingIndicator();

  try {
    const historyPayload = session.messages.slice(0, -1).map(m => ({
      role: m.role,
      content: m.content
    }));

    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: userText,
        history: historyPayload,
        file_attachment: attachmentToSend
      }),
      signal: state.chatAbortController.signal
    });

    removeChatTypingIndicator();

    if (response.ok) {
      const data = await response.json();
      session.messages.push({
        role: 'assistant',
        content: data.reply || 'Cevap alınamadı.',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      });
    } else {
      session.messages.push({
        role: 'assistant',
        content: '⚠️ AI servisiyle bağlantı sağlanamadı. Durum kodu: ' + response.status,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      });
    }
  } catch (err) {
    removeChatTypingIndicator();
    if (err.name === 'AbortError') return;
    session.messages.push({
      role: 'assistant',
      content: '⚠️ Bağlantı hatası: ' + err.message,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    });
  } finally {
    state.isGenerating = false;
    state.chatAbortController = null;
    updateSendButtonUI(false);
    renderChatMessages();
    saveChatSessionsToStorage();
  }
}

function showChatTypingIndicator() {
  const container = document.getElementById('chatStream');
  if (!container) return;
  const indicator = document.createElement('div');
  indicator.id = 'chatTypingIndicator';
  indicator.className = 'flex justify-start w-full';
  indicator.innerHTML = `
    <div class="bg-surface-container/80 backdrop-blur-md rounded-2xl p-3.5 border border-white/5 flex items-center gap-2">
      <span class="w-2 h-2 rounded-full bg-primary animate-ping"></span>
      <span class="text-xs text-on-surface-variant font-medium">ELC 07 AI hazırlanıyor...</span>
    </div>
  `;
  container.appendChild(indicator);
  container.scrollTop = container.scrollHeight;
}

function removeChatTypingIndicator() {
  const ind = document.getElementById('chatTypingIndicator');
  if (ind) ind.remove();
}

function copyMessageText(index) {
  const session = getActiveChat();
  if (!session || !session.messages[index]) return;
  const text = session.messages[index].content || '';
  navigator.clipboard.writeText(text).then(() => {
    alert('Yanıt kopyalandı.');
  });
}

function speakMessageText(index) {
  const session = getActiveChat();
  if (!session || !session.messages[index]) return;
  const text = session.messages[index].content || '';
  if (!text) return;

  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const cleanText = text.replace(/[*#`_]/g, '');
    const utter = new SpeechSynthesisUtterance(cleanText);
    utter.lang = 'en-US';
    utter.rate = 0.95;
    window.speechSynthesis.speak(utter);
  }
}

// -------------------------------------------------------------
// ATTACHMENT HANDLING
// -------------------------------------------------------------
function handleFileUpload(event) {
  const file = event.target.files ? event.target.files[0] : null;
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    state.currentAttachment = {
      name: file.name,
      mime_type: file.type || 'application/octet-stream',
      size: file.size,
      base64: e.target.result
    };

    const preview = document.getElementById('attachmentPreview');
    const nameEl = document.getElementById('attachmentName');
    if (preview && nameEl) {
      nameEl.textContent = file.name;
      preview.classList.remove('hidden');
    }
  };
  reader.readAsDataURL(file);
}

function removeAttachment() {
  state.currentAttachment = null;
  const preview = document.getElementById('attachmentPreview');
  const fileInput = document.getElementById('fileUploadInput');
  if (preview) preview.classList.add('hidden');
  if (fileInput) fileInput.value = '';
}

// -------------------------------------------------------------
// MODULE 1: CÜMLE SEVİYE YÜKSELTİCİ
// -------------------------------------------------------------
function setSentenceFocus(focus) {
  state.sentenceFocus = focus;
  document.querySelectorAll('.sentence-focus-chip').forEach(chip => {
    const txt = chip.textContent.trim();
    if (txt.startsWith(focus) || txt === focus) {
      chip.className = 'sentence-focus-chip shrink-0 px-3 py-1.5 rounded-full text-xs font-semibold transition-all bg-primary-container text-white ring-1 ring-primary/40 shadow-sm';
    } else {
      chip.className = 'sentence-focus-chip shrink-0 px-3 py-1.5 rounded-full text-xs font-semibold transition-all bg-surface-container-high text-on-surface-variant hover:text-on-surface';
    }
  });
}

async function handleSentenceUpgrade() {
  const input = document.getElementById('sentenceInput');
  const sentence = input ? input.value.trim() : '';

  if (!sentence) {
    alert('Lütfen seviyesini yükseltmek istediğiniz basit bir cümle girin.\nÖrnek: Technology helps students learn better.');
    if (input) input.focus();
    return;
  }

  const btn = document.getElementById('upgradeSentenceBtn');
  const btnText = document.getElementById('upgradeSentenceBtnText');
  const resultsSec = document.getElementById('sentenceResultsSection');

  btn.disabled = true;
  btnText.textContent = 'Yükseltiliyor...';

  try {
    const res = await fetch('/api/upgrade-sentence', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        sentence: sentence,
        focus: state.sentenceFocus
      })
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || `Sunucu hatası (${res.status})`);
    }

    const data = await res.json();
    renderSentenceUpgradeResults(data);
    resultsSec.classList.remove('hidden');
    resultsSec.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  } catch (err) {
    alert('Cümle yükseltme hatası: ' + err.message);
  } finally {
    btn.disabled = false;
    btnText.textContent = 'Seviye Yükselt';
  }
}

function renderSentenceUpgradeResults(data) {
  // 1. Grammar Card
  const g = data.dilbilgisi_versiyonu || {};
  const gSentenceEl = document.getElementById('grammarSentenceText');
  if (gSentenceEl) {
    let formatted = escapeHtml(g.cumle || '');
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<span class="bg-indigo-500/25 text-indigo-300 font-bold px-1.5 py-0.5 rounded ring-1 ring-indigo-500/40">$1</span>');
    gSentenceEl.innerHTML = formatted;
  }
  document.getElementById('grammarPill').textContent = g.vurgulanan_yapi || 'Hedef Dilbilgisi Yapısı';
  document.getElementById('grammarExplanationText').textContent = g.turkce_aciklama || 'Sınavda daha yüksek dilbilgisi puanı getirir.';

  // 2. Vocab Card
  const v = data.kelime_versiyonu || {};
  const vSentenceEl = document.getElementById('vocabSentenceText');
  if (vSentenceEl) {
    let formatted = escapeHtml(v.cumle || '');
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<span class="bg-emerald-500/25 text-emerald-300 font-bold px-1.5 py-0.5 rounded ring-1 ring-emerald-500/40">$1</span>');
    vSentenceEl.innerHTML = formatted;
  }
  const pillsContainer = document.getElementById('vocabPills');
  if (pillsContainer) {
    const words = v.hedef_kelimeler || [];
    pillsContainer.innerHTML = words.map(w => `<span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-[10px] font-bold">${escapeHtml(w)}</span>`).join('');
  }
  document.getElementById('vocabExplanationText').textContent = v.turkce_aciklama || 'ELC Intermediate kelime listesi ve edat kalıpları leksikal puanı artırır.';

  // 3. Speaking Card
  const s = data.konusma_versiyonu || {};
  const sSentenceEl = document.getElementById('speakingSentenceText');
  if (sSentenceEl) {
    let formatted = escapeHtml(s.cumle || '');
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<span class="bg-secondary/25 text-secondary font-bold px-1.5 py-0.5 rounded ring-1 ring-secondary/40">$1</span>');
    sSentenceEl.innerHTML = formatted;
  }
  document.getElementById('speakingPill').textContent = s.anahtar_kalip || 'Doğal Geçiş Kalıbı';
  document.getElementById('speakingExplanationText').textContent = s.turkce_aciklama || 'Speaking sınavında akıcılık ve doğallık sağlar.';
}

function copyCardContent(elementId, btn) {
  const el = document.getElementById(elementId);
  if (!el) return;
  const text = el.innerText || el.textContent;
  navigator.clipboard.writeText(text).then(() => {
    const originalHtml = btn.innerHTML;
    btn.innerHTML = `<span class="material-symbols-outlined text-[15px] text-emerald-400">check</span><span class="text-emerald-400">Kopyalandı!</span>`;
    setTimeout(() => {
      btn.innerHTML = originalHtml;
    }, 2000);
  }).catch(() => {
    alert('Metin kopyalanamadı.');
  });
}

function speakSentenceText(elementId) {
  const el = document.getElementById(elementId);
  if (!el) return;
  const text = el.innerText || el.textContent;
  if (!text) return;

  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = 'en-US';
    utter.rate = 0.95;
    window.speechSynthesis.speak(utter);
  }
}

// -------------------------------------------------------------
// MODULE 2: AKILLI KELİME KARTLARI (FLASHCARDS)
// -------------------------------------------------------------
function setupKeyboardShortcuts() {
  document.addEventListener('keydown', (e) => {
    if (state.currentTab === 'cards') {
      const tag = (document.activeElement && document.activeElement.tagName) ? document.activeElement.tagName.toLowerCase() : '';
      if (tag === 'input' || tag === 'textarea') return;

      if (e.code === 'Space') {
        e.preventDefault();
        flipFlashcard();
      } else if (e.code === 'ArrowLeft') {
        e.preventDefault();
        prevFlashcard();
      } else if (e.code === 'ArrowRight') {
        e.preventDefault();
        nextFlashcard();
      }
    }
  });
}

function loadInitialFlashcards() {
  const saved = localStorage.getItem('elc_flashcards_deck');
  const savedLearned = localStorage.getItem('elc_flashcards_learned');
  if (savedLearned) {
    try { state.learnedCards = JSON.parse(savedLearned); } catch (e) { state.learnedCards = []; }
  }
  updateLearnedCountLabel();

  if (saved) {
    try {
      state.flashcards = JSON.parse(saved);
      if (state.flashcards.length > 0) {
        state.currentCardIndex = 0;
        renderCurrentFlashcard();
        return;
      }
    } catch (e) {}
  }
  generateFlashcardsFromCurriculum();
}

function updateLearnedCountLabel() {
  const label = document.getElementById('learnedCountLabel');
  if (label) {
    label.textContent = `Öğrenilen: ${state.learnedCards.length}`;
  }
}

function flipFlashcard() {
  const inner = document.getElementById('flashcardInner');
  if (!inner) return;
  state.isCardFlipped = !state.isCardFlipped;
  if (state.isCardFlipped) {
    inner.classList.add('is-flipped');
  } else {
    inner.classList.remove('is-flipped');
  }
}

function renderCurrentFlashcard() {
  if (!state.flashcards || state.flashcards.length === 0) return;
  if (state.currentCardIndex >= state.flashcards.length) {
    state.currentCardIndex = 0;
  }

  const card = state.flashcards[state.currentCardIndex];
  if (!card) return;

  state.isCardFlipped = false;
  const inner = document.getElementById('flashcardInner');
  if (inner) inner.classList.remove('is-flipped');

  document.getElementById('flashcardCounter').textContent = `${state.currentCardIndex + 1} / ${state.flashcards.length}`;

  // Front elements
  document.getElementById('cardHeadword').textContent = card.kelime || '';
  document.getElementById('cardPosBadge').textContent = card.tur || 'Kelime';
  document.getElementById('cardEnglishDef').textContent = card.ingilizce_tanim || '';

  // Back elements
  document.getElementById('cardTurkishMeaning').textContent = card.turkce_anlam || '';

  // Collocations & prepositions
  const colContainer = document.getElementById('cardCollocationsList');
  if (colContainer) {
    const list = card.kalip_ve_edatlar || [];
    colContainer.innerHTML = list.map(c => {
      let formatted = escapeHtml(c).replace(/\*\*(.*?)\*\*/g, '<strong class="text-secondary">$1</strong>');
      return `<span class="px-2.5 py-1 rounded-lg bg-surface-container-lowest border border-white/10 shadow-sm">${formatted}</span>`;
    }).join('');
  }

  // Word family
  const famContainer = document.getElementById('cardWordFamilyGrid');
  if (famContainer) {
    const fam = card.kelime_ailesi || {};
    const items = [
      { label: 'İsim', val: fam.isim },
      { label: 'Fiil', val: fam.fiil },
      { label: 'Sıfat', val: fam.sifat },
      { label: 'Zarf', val: fam.zarf }
    ].filter(i => i.val && i.val.trim());

    if (items.length > 0) {
      famContainer.innerHTML = items.map(i => `
        <div class="flex items-center justify-between px-2 py-1 rounded bg-surface-container/60">
          <span class="font-bold text-tertiary">${i.label}:</span>
          <span class="font-mono text-on-surface font-semibold">${escapeHtml(i.val)}</span>
        </div>
      `).join('');
    } else {
      famContainer.innerHTML = '<span class="text-on-surface-variant/50 text-[10px] italic col-span-2">Ek türev kaydı bulunmuyor</span>';
    }
  }

  // Example sentence
  const exEl = document.getElementById('cardExampleSentence');
  if (exEl) {
    let formatted = escapeHtml(card.ornek_cumle || '');
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong class="text-amber-300">$1</strong>');
    exEl.innerHTML = formatted;
  }
}

function nextFlashcard() {
  if (state.flashcards.length === 0) return;
  state.currentCardIndex = (state.currentCardIndex + 1) % state.flashcards.length;
  renderCurrentFlashcard();
}

function prevFlashcard() {
  if (state.flashcards.length === 0) return;
  state.currentCardIndex = (state.currentCardIndex - 1 + state.flashcards.length) % state.flashcards.length;
  renderCurrentFlashcard();
}

function markCardLearned() {
  if (state.flashcards.length === 0) return;
  const currentCard = state.flashcards[state.currentCardIndex];
  if (!currentCard) return;

  const word = (currentCard.kelime || '').toLowerCase();
  if (!state.learnedCards.includes(word)) {
    state.learnedCards.push(word);
    localStorage.setItem('elc_flashcards_learned', JSON.stringify(state.learnedCards));
    updateLearnedCountLabel();
  }

  state.flashcards.splice(state.currentCardIndex, 1);
  localStorage.setItem('elc_flashcards_deck', JSON.stringify(state.flashcards));

  if (state.flashcards.length === 0) {
    alert('🎉 Harika! Bu destedeki tüm kelimeleri öğrendiniz. Yeni kartlar yüklemek için "Yüklü Materyalden Üret" butonuna basın.');
    generateFlashcardsFromCurriculum();
  } else {
    if (state.currentCardIndex >= state.flashcards.length) {
      state.currentCardIndex = 0;
    }
    renderCurrentFlashcard();
  }
}

function speakCardWord() {
  const card = state.flashcards[state.currentCardIndex];
  if (!card || !card.kelime) return;
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(card.kelime);
    utter.lang = 'en-US';
    utter.rate = 0.9;
    window.speechSynthesis.speak(utter);
  }
}

function speakCardExample() {
  const card = state.flashcards[state.currentCardIndex];
  if (!card || !card.ornek_cumle) return;
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(card.ornek_cumle);
    utter.lang = 'en-US';
    utter.rate = 0.95;
    window.speechSynthesis.speak(utter);
  }
}

function toggleCustomTextInput() {
  const panel = document.getElementById('customTextCardPanel');
  if (panel) panel.classList.toggle('hidden');
}

async function generateFlashcardsFromCurriculum() {
  const unitSelect = document.getElementById('flashcardUnitSelect');
  const unit = unitSelect ? unitSelect.value : '';

  try {
    const res = await fetch('/api/generate-flashcards', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        source: 'curriculum',
        unit: unit,
        count: 10
      })
    });

    if (res.ok) {
      const data = await res.json();
      if (data.cards && data.cards.length > 0) {
        state.flashcards = data.cards;
        state.currentCardIndex = 0;
        localStorage.setItem('elc_flashcards_deck', JSON.stringify(state.flashcards));
        renderCurrentFlashcard();
      }
    } else {
      alert('Kartlar üretilirken hata oluştu.');
    }
  } catch (err) {
    console.error('Flashcard error:', err);
    alert('Bağlantı hatası: ' + err.message);
  }
}

async function generateFlashcardsFromCustomText() {
  const textInput = document.getElementById('customFlashcardText');
  const text = textInput ? textInput.value.trim() : '';

  if (!text) {
    alert('Lütfen kelime çıkarılmasını istediğiniz bir okuma parçası veya kelime listesi yapıştırın.');
    return;
  }

  try {
    const res = await fetch('/api/generate-flashcards', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        source: 'text',
        text: text,
        count: 10
      })
    });

    if (res.ok) {
      const data = await res.json();
      if (data.cards && data.cards.length > 0) {
        state.flashcards = data.cards;
        state.currentCardIndex = 0;
        localStorage.setItem('elc_flashcards_deck', JSON.stringify(state.flashcards));
        renderCurrentFlashcard();
        const panel = document.getElementById('customTextCardPanel');
        if (panel) panel.classList.add('hidden');
        alert(`${data.cards.length} adet akıllı kelime kartı başarıyla üretildi!`);
      }
    } else {
      alert('Kart üretilirken hata oluştu.');
    }
  } catch (err) {
    alert('Bağlantı hatası: ' + err.message);
  }
}

// -------------------------------------------------------------
// DOSYA CONVERTER (FILE CONVERTER MODAL)
// -------------------------------------------------------------
function openFileConverterModal() {
  const modal = document.getElementById('fileConverterModal');
  if (modal) {
    modal.classList.remove('hidden');
    modal.classList.add('flex');
  }
}

function closeFileConverterModal() {
  const modal = document.getElementById('fileConverterModal');
  if (modal) {
    modal.classList.add('hidden');
    modal.classList.remove('flex');
  }
}

function setupConverterDragAndDrop() {
  const dropZone = document.getElementById('converterDropZone');
  if (!dropZone) return;

  ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropZone.classList.add('border-primary', 'bg-primary-container/10');
    });
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropZone.classList.remove('border-primary', 'bg-primary-container/10');
    });
  });

  dropZone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const file = dt.files ? dt.files[0] : null;
    if (file) setupConverterFile(file);
  });
}

function handleConverterFileSelected(event) {
  const file = event.target.files ? event.target.files[0] : null;
  if (!file) return;
  setupConverterFile(file);
}

function setupConverterFile(file) {
  state.selectedConvertFile = file;
  const detailsBox = document.getElementById('converterFileDetails');
  const resultBox = document.getElementById('converterResultBox');
  const startBtn = document.getElementById('startConvertBtn');
  const nameEl = document.getElementById('detectedFileName');
  const badgeEl = document.getElementById('detectedFileBadge');
  const selectEl = document.getElementById('converterTargetFormatSelect');

  if (resultBox) resultBox.classList.add('hidden');
  if (detailsBox) detailsBox.classList.remove('hidden');
  if (startBtn) startBtn.disabled = false;

  const ext = file.name.includes('.') ? file.name.split('.').pop().toLowerCase() : '';
  if (nameEl) nameEl.textContent = file.name;

  const EXT_LABELS = {
    'docx': 'Word Belgesi (.docx)',
    'doc': 'Word Belgesi (.doc)',
    'pdf': 'PDF Belgesi (.pdf)',
    'xlsx': 'Excel Tablosu (.xlsx)',
    'xls': 'Excel Tablosu (.xls)',
    'csv': 'CSV Verisi (.csv)',
    'pptx': 'PowerPoint (.pptx)',
    'png': 'PNG Görsel (.png)',
    'jpg': 'JPG Görsel (.jpg)',
    'jpeg': 'JPEG Görsel (.jpeg)',
    'webp': 'WebP Görsel (.webp)',
    'bmp': 'BMP Görsel (.bmp)',
    'txt': 'Düz Metin (.txt)',
    'md': 'Markdown Belgesi (.md)'
  };

  if (badgeEl) badgeEl.textContent = EXT_LABELS[ext] || `.${ext.toUpperCase()} Dosyası`;

  const TARGET_OPTIONS = {
    'docx': [['pdf', 'PDF Belgesi (.pdf)'], ['txt', 'Düz Metin (.txt)'], ['html', 'Web Sayfası (.html)']],
    'doc': [['pdf', 'PDF Belgesi (.pdf)'], ['txt', 'Düz Metin (.txt)'], ['html', 'Web Sayfası (.html)']],
    'pdf': [['docx', 'Word Belgesi (.docx)'], ['txt', 'Düz Metin (.txt)'], ['html', 'Web Sayfası (.html)']],
    'xlsx': [['csv', 'CSV Verisi (.csv)'], ['pdf', 'PDF Belgesi (.pdf)'], ['html', 'Web Sayfası (.html)'], ['txt', 'Düz Metin (.txt)']],
    'xls': [['csv', 'CSV Verisi (.csv)'], ['xlsx', 'Excel Tablosu (.xlsx)'], ['txt', 'Düz Metin (.txt)']],
    'csv': [['xlsx', 'Excel Tablosu (.xlsx)'], ['pdf', 'PDF Belgesi (.pdf)'], ['txt', 'Düz Metin (.txt)'], ['html', 'Web Sayfası (.html)']],
    'pptx': [['pdf', 'PDF Belgesi (.pdf)'], ['docx', 'Word Belgesi (.docx)'], ['txt', 'Düz Metin (.txt)'], ['html', 'Web Sayfası (.html)']],
    'png': [['jpg', 'JPG Görsel (.jpg)'], ['webp', 'WebP Görsel (.webp)'], ['pdf', 'PDF Belgesi (.pdf)']],
    'jpg': [['png', 'PNG Görsel (.png)'], ['webp', 'WebP Görsel (.webp)'], ['pdf', 'PDF Belgesi (.pdf)']],
    'jpeg': [['png', 'PNG Görsel (.png)'], ['webp', 'WebP Görsel (.webp)'], ['pdf', 'PDF Belgesi (.pdf)']],
    'webp': [['png', 'PNG Görsel (.png)'], ['jpg', 'JPG Görsel (.jpg)'], ['pdf', 'PDF Belgesi (.pdf)']],
    'txt': [['pdf', 'PDF Belgesi (.pdf)'], ['docx', 'Word Belgesi (.docx)'], ['html', 'Web Sayfası (.html)']],
    'md': [['pdf', 'PDF Belgesi (.pdf)'], ['docx', 'Word Belgesi (.docx)'], ['html', 'Web Sayfası (.html)'], ['txt', 'Düz Metin (.txt)']]
  };

  const defaultList = [
    ['pdf', 'PDF Belgesi (.pdf)'],
    ['docx', 'Word Belgesi (.docx)'],
    ['txt', 'Düz Metin (.txt)'],
    ['xlsx', 'Excel Tablosu (.xlsx)'],
    ['csv', 'CSV Verisi (.csv)'],
    ['png', 'PNG Görsel (.png)'],
    ['jpg', 'JPG Görsel (.jpg)']
  ];

  const opts = TARGET_OPTIONS[ext] || defaultList;
  if (selectEl) {
    selectEl.innerHTML = opts.map(([val, label]) => `<option value="${val}">${label}</option>`).join('');
  }
}

async function startFileConversion() {
  if (!state.selectedConvertFile) return;

  const file = state.selectedConvertFile;
  const formatSelect = document.getElementById('converterTargetFormatSelect');
  const targetFormat = formatSelect ? formatSelect.value : 'pdf';
  const startBtn = document.getElementById('startConvertBtn');
  const startBtnText = document.getElementById('startConvertBtnText');
  const resultBox = document.getElementById('converterResultBox');
  const detailMsg = document.getElementById('converterSuccessDetail');
  const dlBtn = document.getElementById('converterDownloadBtn');
  const dlLabel = document.getElementById('converterDownloadBtnLabel');

  startBtn.disabled = true;
  startBtnText.textContent = 'Dönüştürülüyor...';
  if (resultBox) resultBox.classList.add('hidden');

  const formData = new FormData();
  formData.append('file', file);
  formData.append('target_format', targetFormat);

  try {
    const res = await fetch('/api/convert-file', {
      method: 'POST',
      body: formData
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `Dönüştürme hatası (${res.status})`);
    }

    let outFilename = '';
    const disposition = res.headers.get('Content-Disposition') || '';
    if (disposition.includes('filename=')) {
      outFilename = disposition.split('filename=')[1].replace(/["']/g, '').trim();
    }
    if (!outFilename) {
      const baseName = file.name.includes('.') ? file.name.substring(0, file.name.lastIndexOf('.')) : file.name;
      outFilename = `${baseName}_convertedelcai07.${targetFormat}`;
    }

    const blob = await res.blob();
    const downloadUrl = URL.createObjectURL(blob);

    // Auto-download converted file
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = outFilename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    // Show result box with download button
    if (resultBox) resultBox.classList.remove('hidden');
    if (detailMsg) detailMsg.textContent = `"${outFilename}" başarıyla dönüştürüldü ve indirildi.`;
    if (dlLabel) dlLabel.textContent = `Tekrar İndir (${outFilename})`;
    if (dlBtn) {
      dlBtn.onclick = () => {
        const a2 = document.createElement('a');
        a2.href = downloadUrl;
        a2.download = outFilename;
        document.body.appendChild(a2);
        a2.click();
        document.body.removeChild(a2);
      };
    }
  } catch (err) {
    alert('Dosya dönüştürme hatası: ' + err.message);
  } finally {
    startBtn.disabled = false;
    startBtnText.textContent = 'Dönüştür';
  }
}

// -------------------------------------------------------------
// SPEAKING TASK ENGINE
// -------------------------------------------------------------
function changeSpeakingTopic() {
  const select = document.getElementById('speakingTopicSelect');
  const topicId = parseInt(select.value, 10);
  state.speaking.promptId = topicId;

  const promptData = SPEAKING_PROMPTS[topicId];
  if (promptData) {
    document.getElementById('speakingTaskBadge').textContent = promptData.badge;
    document.getElementById('currentPromptTitle').textContent = promptData.title;
    document.getElementById('currentPromptText').textContent = promptData.text;
  }
  resetSpeakingSession();
}

function startPrepTimer() {
  clearInterval(state.speaking.prepTimer);
  state.speaking.prepTimeLeft = 60;
  updatePrepTimerDisplay();

  state.speaking.prepTimer = setInterval(() => {
    state.speaking.prepTimeLeft--;
    updatePrepTimerDisplay();
    if (state.speaking.prepTimeLeft <= 0) {
      clearInterval(state.speaking.prepTimer);
      alert('⏰ 1 dakikalık hazırlık süreniz doldu! Şimdi konuşma kaydını başlatabilirsiniz.');
    }
  }, 1000);
}

function updatePrepTimerDisplay() {
  const display = document.getElementById('speakingTimerDisplay');
  const mins = Math.floor(state.speaking.prepTimeLeft / 60);
  const secs = state.speaking.prepTimeLeft % 60;
  if (display) {
    display.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  }
}

function setupSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    console.warn('Web Speech API not supported in this browser.');
    return;
  }

  // Speaking Task Recognition
  const recog = new SpeechRecognition();
  recog.continuous = true;
  recog.interimResults = true;
  recog.lang = 'en-US';

  recog.onresult = (event) => {
    let finalTrans = '';
    for (let i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        state.speaking.transcript += event.results[i][0].transcript + ' ';
      } else {
        finalTrans += event.results[i][0].transcript;
      }
    }
    const fullText = (state.speaking.transcript + finalTrans).trim();
    const box = document.getElementById('speakingTranscriptBox');
    if (box) box.textContent = fullText || 'Dinleniyor...';

    const wordCount = fullText ? fullText.split(/\s+/).filter(Boolean).length : 0;
    const countEl = document.getElementById('speakingWordCount');
    if (countEl) countEl.textContent = `${wordCount} words`;
  };

  recog.onerror = (e) => {
    console.warn('Speech recognition notice:', e.error);
  };

  recog.onend = () => {
    if (state.speaking.isRecording) {
      try { recog.start(); } catch (err) {}
    }
  };

  state.speaking.recognition = recog;

  // Chat Voice Recognition
  const chatRecog = new SpeechRecognition();
  chatRecog.continuous = false;
  chatRecog.interimResults = false;
  chatRecog.lang = 'en-US';

  chatRecog.onresult = (event) => {
    const text = event.results[0][0].transcript;
    const input = document.getElementById('chatPromptInput');
    if (input) {
      input.value = (input.value + ' ' + text).trim();
    }
  };

  chatRecog.onend = () => {
    state.isChatRecording = false;
    const ring = document.getElementById('micRecordingRing');
    if (ring) ring.classList.add('hidden');
  };

  state.chatRecognition = chatRecog;
}

function toggleSpeakingRecording() {
  if (state.speaking.isRecording) {
    stopSpeakingRecording();
  } else {
    startSpeakingRecording();
  }
}

function startSpeakingRecording() {
  if (!state.speaking.recognition) {
    alert('Tarayıcınız Web Speech API sesli kayıt özelliğini desteklemiyor (Chrome/Edge önerilir).');
    return;
  }

  state.speaking.isRecording = true;
  state.speaking.speakTimeLeft = 120;
  state.speaking.transcript = '';

  const label = document.getElementById('speakingStatusLabel');
  if (label) label.textContent = '🔴 Konuşmanız dinleniyor... Lütfen promptu yanıtlayın (2 Dakika).';

  const micIcon = document.getElementById('speakingMicIcon');
  if (micIcon) micIcon.textContent = 'stop';

  const wave = document.getElementById('audioWaveform');
  if (wave) wave.classList.remove('hidden');

  const p1 = document.getElementById('micOrbPulse1');
  const p2 = document.getElementById('micOrbPulse2');
  if (p1) p1.classList.remove('opacity-0');
  if (p2) p2.classList.remove('opacity-0');

  try {
    state.speaking.recognition.start();
  } catch (e) {}

  clearInterval(state.speaking.speakTimer);
  state.speaking.speakTimer = setInterval(() => {
    state.speaking.speakTimeLeft--;
    if (state.speaking.speakTimeLeft <= 0) {
      stopSpeakingRecording();
      alert('⏰ 2 dakikalık konuşma süreniz doldu! Şimdi "Analyze" butonuna basarak değerlendirmenizi alabilirsiniz.');
    }
  }, 1000);
}

function stopSpeakingRecording() {
  state.speaking.isRecording = false;
  clearInterval(state.speaking.speakTimer);

  const label = document.getElementById('speakingStatusLabel');
  if (label) label.textContent = 'Kayıt tamamlandı. Değerlendirme için "Analyze" butonuna basın.';

  const micIcon = document.getElementById('speakingMicIcon');
  if (micIcon) micIcon.textContent = 'mic';

  const wave = document.getElementById('audioWaveform');
  if (wave) wave.classList.add('hidden');

  const p1 = document.getElementById('micOrbPulse1');
  const p2 = document.getElementById('micOrbPulse2');
  if (p1) p1.classList.add('opacity-0');
  if (p2) p2.classList.add('opacity-0');

  if (state.speaking.recognition) {
    try { state.speaking.recognition.stop(); } catch (e) {}
  }
}

function resetSpeakingSession() {
  stopSpeakingRecording();
  clearInterval(state.speaking.prepTimer);
  state.speaking.prepTimeLeft = 60;
  updatePrepTimerDisplay();
  state.speaking.transcript = '';

  const box = document.getElementById('speakingTranscriptBox');
  if (box) box.textContent = 'Your spoken words will appear here in real time as you speak...';

  const countEl = document.getElementById('speakingWordCount');
  if (countEl) countEl.textContent = '0 words';

  const resSec = document.getElementById('speakingResultSection');
  if (resSec) resSec.classList.add('hidden');
}

async function analyzeSpokenSpeech() {
  const transcript = state.speaking.transcript.trim();
  if (!transcript || transcript.split(/\s+/).length < 5) {
    alert('Lütfen analiz için mikrofona en az birkaç cümle konuşun.');
    return;
  }

  const btn = document.getElementById('analyzeSpeechBtn');
  btn.disabled = true;
  btn.innerHTML = `<span class="material-symbols-outlined text-[18px] animate-spin mb-0.5">sync</span><span>Analyzing...</span>`;

  const promptData = SPEAKING_PROMPTS[state.speaking.promptId] || SPEAKING_PROMPTS[1];

  try {
    const res = await fetch('/api/speaking-evaluate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt_id: state.speaking.promptId,
        prompt_title: promptData.title,
        prompt_text: promptData.text,
        transcript: transcript
      })
    });

    if (res.ok) {
      const evalData = await res.json();
      state.speaking.lastEvaluation = evalData;
      renderSpeakingEvaluation(evalData);
    } else {
      alert('Speaking değerlendirmesi yapılırken hata oluştu.');
    }
  } catch (err) {
    alert('Bağlantı hatası: ' + err.message);
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<span class="material-symbols-outlined text-[18px] mb-0.5">analytics</span><span>Analyze</span>`;
  }
}

function renderSpeakingEvaluation(ev) {
  const sec = document.getElementById('speakingResultSection');
  if (!sec) return;

  sec.classList.remove('hidden');

  document.getElementById('evalOverallScore').textContent = `${ev.overall_score || 85}/100 (${ev.cefr_band || 'B2+'})`;
  document.getElementById('evalSummary').textContent = ev.summary || '';

  const metricsGrid = document.getElementById('evalMetricsGrid');
  if (metricsGrid && ev.metrics) {
    metricsGrid.innerHTML = `
      <div class="p-2.5 rounded-xl bg-surface-container-lowest/80 border border-white/5 space-y-1">
        <div class="flex items-center justify-between text-xs font-bold text-on-surface">
          <span>🗣️ Fluency & Coherence</span>
          <span class="font-mono text-secondary">${ev.metrics.fluency?.score || 84}/100</span>
        </div>
        <p class="text-[11px] text-on-surface-variant leading-tight">${escapeHtml(ev.metrics.fluency?.comment || '')}</p>
      </div>
      <div class="p-2.5 rounded-xl bg-surface-container-lowest/80 border border-white/5 space-y-1">
        <div class="flex items-center justify-between text-xs font-bold text-on-surface">
          <span>📚 Lexical Resource</span>
          <span class="font-mono text-emerald-400">${ev.metrics.lexical_resource?.score || 86}/100</span>
        </div>
        <p class="text-[11px] text-on-surface-variant leading-tight">${escapeHtml(ev.metrics.lexical_resource?.comment || '')}</p>
      </div>
      <div class="p-2.5 rounded-xl bg-surface-container-lowest/80 border border-white/5 space-y-1">
        <div class="flex items-center justify-between text-xs font-bold text-on-surface">
          <span>⚖️ Grammar Range & Accuracy</span>
          <span class="font-mono text-amber-400">${ev.metrics.grammar_accuracy?.score || 82}/100</span>
        </div>
        <p class="text-[11px] text-on-surface-variant leading-tight">${escapeHtml(ev.metrics.grammar_accuracy?.comment || '')}</p>
      </div>
      <div class="p-2.5 rounded-xl bg-surface-container-lowest/80 border border-white/5 space-y-1">
        <div class="flex items-center justify-between text-xs font-bold text-on-surface">
          <span>🎯 Task Fulfillment</span>
          <span class="font-mono text-primary">${ev.metrics.task_fulfillment?.score || 88}/100</span>
        </div>
        <p class="text-[11px] text-on-surface-variant leading-tight">${escapeHtml(ev.metrics.task_fulfillment?.comment || '')}</p>
      </div>
    `;
  }

  const strList = document.getElementById('evalStrengthsList');
  if (strList) {
    strList.innerHTML = (ev.strengths || []).map(s => `<li>${escapeHtml(s)}</li>`).join('');
  }

  const impList = document.getElementById('evalImprovementsList');
  if (impList) {
    impList.innerHTML = (ev.improvements || []).map(i => `<li>${escapeHtml(i)}</li>`).join('');
  }

  document.getElementById('evalModelResponse').textContent = ev.model_response || '';
  sec.scrollIntoView({ behavior: 'smooth' });
}

function toggleModelAudio() {
  const icon = document.getElementById('modelListenIcon');
  const label = document.getElementById('modelListenLabel');
  const text = (state.speaking.lastEvaluation && state.speaking.lastEvaluation.model_response) || '';

  if (!text || !('speechSynthesis' in window)) return;

  if (state.isModelAudioPlaying) {
    window.speechSynthesis.cancel();
    state.isModelAudioPlaying = false;
    if (icon) icon.textContent = 'volume_up';
    if (label) label.textContent = 'Listen';
  } else {
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = 'en-US';
    utter.rate = 0.95;

    state.isModelAudioPlaying = true;
    if (icon) icon.textContent = 'stop_circle';
    if (label) label.textContent = 'Stop';

    utter.onend = () => {
      state.isModelAudioPlaying = false;
      if (icon) icon.textContent = 'volume_up';
      if (label) label.textContent = 'Listen';
    };

    utter.onerror = () => {
      state.isModelAudioPlaying = false;
      if (icon) icon.textContent = 'volume_up';
      if (label) label.textContent = 'Listen';
    };

    window.speechSynthesis.speak(utter);
  }
}

function toggleChatVoice() {
  if (!state.chatRecognition) {
    alert('Tarayıcınız ses tanıma desteği sunmuyor.');
    return;
  }
  const ring = document.getElementById('micRecordingRing');
  if (state.isChatRecording) {
    state.chatRecognition.stop();
    state.isChatRecording = false;
    if (ring) ring.classList.add('hidden');
  } else {
    try {
      state.chatRecognition.start();
      state.isChatRecording = true;
      if (ring) ring.classList.remove('hidden');
    } catch (e) {}
  }
}

// -------------------------------------------------------------
// INTERACTIVE TESTS & CUSTOM AI QUIZ GENERATOR
// -------------------------------------------------------------
function selectQuizMode(mode) {
  state.quizMode = mode;
  const chatBtn = document.getElementById('quizModeChatBtn');
  const manualBtn = document.getElementById('quizModeManualBtn');
  const chatPanel = document.getElementById('quizChatModePanel');
  const manualPanel = document.getElementById('quizManualModePanel');

  if (mode === 'chat') {
    chatBtn.className = 'py-2 rounded-lg text-xs font-bold transition-all bg-primary-container text-white shadow';
    manualBtn.className = 'py-2 rounded-lg text-xs font-semibold text-on-surface-variant hover:text-on-surface transition-all';
    chatPanel.classList.remove('hidden');
    manualPanel.classList.add('hidden');
    renderQuizChatSelector();
  } else {
    manualBtn.className = 'py-2 rounded-lg text-xs font-bold transition-all bg-primary-container text-white shadow';
    chatBtn.className = 'py-2 rounded-lg text-xs font-semibold text-on-surface-variant hover:text-on-surface transition-all';
    chatPanel.classList.add('hidden');
    manualPanel.classList.remove('hidden');
  }
}

function renderQuizChatSelector() {
  const container = document.getElementById('quizChatSessionList');
  const countBadge = document.getElementById('quizChatCountBadge');
  if (!container) return;

  const sessions = state.chatSessions || [];
  if (countBadge) {
    countBadge.textContent = `${sessions.length} Sohbet`;
  }

  if (sessions.length === 0) {
    container.innerHTML = `
      <div class="p-3 rounded-xl bg-surface-container-lowest text-center text-on-surface-variant text-xs space-y-1">
        <span class="material-symbols-outlined text-[24px] opacity-40">history_edu</span>
        <p class="font-medium">Henüz kayıtlı bir sohbetiniz bulunmuyor.</p>
        <p class="text-[10px] text-on-surface-variant/70">"Midterm" sekmesinde soru sorabilir veya "✏️ Manuel Oluştur" seçeneğini kullanabilirsiniz.</p>
      </div>
    `;
    return;
  }

  if (!state.quizSelectedChatId || !sessions.some(s => s.id === state.quizSelectedChatId)) {
    state.quizSelectedChatId = state.activeChatId || sessions[0].id;
  }

  container.innerHTML = sessions.map(s => {
    const isSelected = s.id === state.quizSelectedChatId;
    const msgCount = (s.messages || []).length;
    const timeStr = s.createdAt ? new Date(s.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';
    const dateStr = s.createdAt ? new Date(s.createdAt).toLocaleDateString([], { day: 'numeric', month: 'short' }) : '';

    return `
      <div onclick="selectQuizChatSession('${s.id}')" class="p-2.5 rounded-xl transition-all cursor-pointer flex items-center justify-between border ${isSelected ? 'bg-primary-container/20 border-primary/50 ring-1 ring-primary/40 text-white shadow-sm' : 'bg-surface-container-lowest hover:bg-surface-container-high border-white/5 text-on-surface'}">
        <div class="flex items-center gap-2.5 overflow-hidden">
          <div class="w-7 h-7 rounded-lg flex items-center justify-center shrink-0 ${isSelected ? 'bg-primary-container text-white' : 'bg-surface-container-high text-on-surface-variant'}">
            <span class="material-symbols-outlined text-[16px]">${isSelected ? 'check_circle' : 'chat'}</span>
          </div>
          <div class="truncate text-xs font-semibold">
            <span class="truncate block text-on-surface">${escapeHtml(s.title || 'Adsız Sohbet')}</span>
            <span class="text-[10px] text-on-surface-variant font-normal block">${msgCount} mesaj • ${dateStr} ${timeStr}</span>
          </div>
        </div>
        ${isSelected ? '<span class="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-primary-container text-white shrink-0">Seçildi</span>' : ''}
      </div>
    `;
  }).join('');
}

function selectQuizChatSession(sessionId) {
  state.quizSelectedChatId = sessionId;
  renderQuizChatSelector();
}

function openCustomQuizModal() {
  const modal = document.getElementById('customQuizModal');
  if (modal) {
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    renderQuizChatSelector();
  }
}

function closeCustomQuizModal() {
  const modal = document.getElementById('customQuizModal');
  if (modal) {
    modal.classList.add('hidden');
    modal.classList.remove('flex');
  }
}

async function submitGenerateQuiz() {
  const countSelect = document.getElementById('quizCountSelect');
  const typeSelect = document.getElementById('quizTypeSelect');
  const submitBtn = document.getElementById('generateQuizSubmitBtn');
  const count = parseInt(countSelect.value, 10) || 5;
  const quizType = typeSelect.value || 'mixed';

  let topic = 'ELC Intermediate Skills';
  let chatHistoryPayload = [];

  if (state.quizMode === 'chat') {
    let session = (state.chatSessions || []).find(s => s.id === state.quizSelectedChatId);
    if (!session) {
      session = getActiveChat();
    }
    if (!session || !session.messages || session.messages.length === 0) {
      alert('Seçilen sohbette henüz mesaj bulunmuyor!\nLütfen mesaj içeren bir sohbet seçin veya "Manuel Oluştur" seçeneğini kullanın.');
      return;
    }
    chatHistoryPayload = session.messages.map(m => ({ role: m.role, content: m.content }));
    topic = session.title || 'ELC Intermediate Chat Topic';
  } else {
    const topicInput = document.getElementById('quizTopicInput');
    topic = (topicInput ? topicInput.value.trim() : '') || 'ELC Intermediate Midterm Skills';
  }

  submitBtn.disabled = true;
  submitBtn.textContent = 'Üretiliyor...';

  try {
    const res = await fetch('/api/generate-quiz', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        mode: state.quizMode,
        topic: topic,
        chat_history: chatHistoryPayload,
        count: count,
        quiz_type: quizType
      })
    });

    if (res.ok) {
      const data = await res.json();
      if (data.questions && data.questions.length > 0) {
        state.tests = data.questions;
        state.currentQuestionIndex = 0;
        state.testScore = 0;
        state.testStreak = 0;
        state.answeredQuestions = {};
        state.wrongQuestions = [];

        closeCustomQuizModal();

        document.getElementById('quizStarterCard').classList.add('hidden');
        document.getElementById('quizSummaryCard').classList.add('hidden');
        document.getElementById('activeQuizWrapper').classList.remove('hidden');

        renderCurrentQuestion();
      } else {
        alert('Bu konu için soru üretilemedi. Lütfen tekrar deneyiniz.');
      }
    } else {
      alert('Soru üretilirken hata oluştu. Durum: ' + res.status);
    }
  } catch (err) {
    alert('Bağlantı hatası: ' + err.message);
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Quizi Başlat';
  }
}

function renderCurrentQuestion() {
  if (!state.tests || state.tests.length === 0) return;

  const q = state.tests[state.currentQuestionIndex];
  if (!q) return;

  // Header & progress
  document.getElementById('testQuestionIndex').textContent = `Q ${state.currentQuestionIndex + 1} / ${state.tests.length}`;
  const pct = Math.round(((state.currentQuestionIndex + 1) / state.tests.length) * 100);
  document.getElementById('testProgressBar').style.width = pct + '%';

  // Badges
  document.getElementById('testScoreBadge').textContent = `🎯 Score: ${state.testScore}/${Object.keys(state.answeredQuestions).length} Correct`;
  document.getElementById('testStreakBadge').textContent = `🔥 Streak: ${state.testStreak}`;

  // Card Content
  document.getElementById('quizCardUnit').textContent = q.unit || 'Skill Building Set Practice';
  document.getElementById('quizQuestionText').textContent = q.question;

  const isGapFill = q.type === 'gap_fill';
  const optionsContainer = document.getElementById('quizOptionsContainer');
  const gapFillContainer = document.getElementById('quizGapFillContainer');
  const explanationCard = document.getElementById('quizExplanationCard');

  explanationCard.classList.add('hidden');

  const answerState = state.answeredQuestions[q.id || `q_${state.currentQuestionIndex}`];

  if (isGapFill) {
    optionsContainer.classList.add('hidden');
    gapFillContainer.classList.remove('hidden');
    document.getElementById('quizInstructionText').textContent = 'Provide the exact academic word or nominalized phrase:';
    
    const input = document.getElementById('gapFillInput');
    input.value = answerState ? answerState.selected : '';
    input.disabled = !!answerState;

    if (answerState) {
      showExplanation(q, answerState.isCorrect);
    }
  } else {
    gapFillContainer.classList.add('hidden');
    optionsContainer.classList.remove('hidden');
    document.getElementById('quizInstructionText').textContent = 'Select the most accurate option:';

    optionsContainer.innerHTML = (q.options || []).map((opt, i) => {
      const char = String.fromCharCode(65 + i);
      let btnClasses = 'bg-surface-container-high/50 hover:bg-surface-container-high';
      let icon = 'radio_button_unchecked';
      let iconClass = 'text-surface-variant';
      let statusBadge = '';

      if (answerState) {
        if (i === q.correct) {
          btnClasses = 'bg-emerald-500/20 ring-1 ring-emerald-500 shadow-[0_0_16px_rgba(16,185,129,0.3)]';
          icon = 'check_circle';
          iconClass = 'text-emerald-400';
          statusBadge = `<span class="text-[11px] font-bold text-emerald-400 uppercase tracking-wider">Correct!</span>`;
        } else if (answerState.selected === i && !answerState.isCorrect) {
          btnClasses = 'bg-red-500/20 ring-1 ring-red-500';
          icon = 'cancel';
          iconClass = 'text-red-400';
          statusBadge = `<span class="text-[11px] font-bold text-red-400 uppercase tracking-wider">Incorrect</span>`;
        }
      }

      return `
        <button onclick="selectMultipleChoiceOption(${i})" ${answerState ? 'disabled' : ''} class="w-full flex items-center justify-between p-3.5 rounded-xl ${btnClasses} text-left transition-all active:scale-[0.99] border border-white/5">
          <div class="flex items-center gap-3">
            <span class="w-7 h-7 rounded-full flex items-center justify-center font-mono text-xs font-bold bg-surface-container text-on-surface-variant">${char}</span>
            <span class="text-xs sm:text-sm font-medium text-on-surface">${escapeHtml(opt)}</span>
          </div>
          <div class="flex items-center gap-1.5">
            ${statusBadge}
            <span class="material-symbols-outlined text-[20px] ${iconClass}">${icon}</span>
          </div>
        </button>
      `;
    }).join('');

    if (answerState) {
      showExplanation(q, answerState.isCorrect);
    }
  }
}

function selectMultipleChoiceOption(optionIndex) {
  const qId = state.tests[state.currentQuestionIndex]?.id || `q_${state.currentQuestionIndex}`;
  const q = state.tests[state.currentQuestionIndex];
  if (!q || state.answeredQuestions[qId]) return;

  const isCorrect = optionIndex === q.correct;
  if (isCorrect) {
    state.testScore++;
    state.testStreak++;
  } else {
    state.testStreak = 0;
    state.wrongQuestions.push({
      question: q.question,
      topic: q.topic || q.unit || 'Dilbilgisi / Kelime',
      explanation: q.explanation || 'Bu soru üzerinde tekrar çalışılması önerilir.'
    });
  }

  state.answeredQuestions[qId] = {
    answered: true,
    isCorrect: isCorrect,
    selected: optionIndex
  };

  renderCurrentQuestion();
}

function checkGapFillAnswer() {
  const qId = state.tests[state.currentQuestionIndex]?.id || `q_${state.currentQuestionIndex}`;
  const q = state.tests[state.currentQuestionIndex];
  if (!q || state.answeredQuestions[qId]) return;

  const input = document.getElementById('gapFillInput');
  const val = (input ? input.value : '').trim().toLowerCase();
  if (!val) return;

  const accepted = (q.accepted_answers || [q.correct_answer || '']).map(a => a.toLowerCase().trim());
  const isCorrect = accepted.includes(val);

  if (isCorrect) {
    state.testScore++;
    state.testStreak++;
  } else {
    state.testStreak = 0;
    state.wrongQuestions.push({
      question: q.question,
      topic: q.topic || q.unit || 'Boşluk Doldurma',
      explanation: q.explanation || 'Bu kelime ve türevi üzerinde tekrar çalışılması önerilir.'
    });
  }

  state.answeredQuestions[qId] = {
    answered: true,
    isCorrect: isCorrect,
    selected: val
  };

  renderCurrentQuestion();
}

function showExplanation(q, isCorrect) {
  const card = document.getElementById('quizExplanationCard');
  if (!card) return;
  card.classList.remove('hidden');

  document.getElementById('quizExplanationText').innerHTML = `
    <strong>${isCorrect ? '✅ Doğru Yanıt!' : '❌ Yanlış.'}</strong> ${escapeHtml(q.explanation || '')}
  `;

  const synRow = document.getElementById('quizSynonymsRow');
  const colRow = document.getElementById('quizCollocationsRow');

  if (q.synonyms) {
    synRow.classList.remove('hidden');
    document.getElementById('quizSynonymsText').textContent = q.synonyms;
  } else {
    synRow.classList.add('hidden');
  }

  if (q.collocation) {
    colRow.classList.remove('hidden');
    document.getElementById('quizCollocationsText').textContent = q.collocation;
  } else {
    colRow.classList.add('hidden');
  }
}

function prevQuestion() {
  if (state.currentQuestionIndex > 0) {
    state.currentQuestionIndex--;
    renderCurrentQuestion();
  }
}

function nextQuestion() {
  if (state.currentQuestionIndex < state.tests.length - 1) {
    state.currentQuestionIndex++;
    renderCurrentQuestion();
  } else {
    showQuizSummary();
  }
}

function showQuizSummary() {
  document.getElementById('activeQuizWrapper').classList.add('hidden');
  const summaryCard = document.getElementById('quizSummaryCard');
  if (!summaryCard) return;

  summaryCard.classList.remove('hidden');

  const total = state.tests.length;
  const score = state.testScore;
  const pct = Math.round((score / total) * 100);

  document.getElementById('finalScoreBadge').textContent = `${score}/${total} Doğru (%${pct})`;

  let msg = '';
  if (pct >= 85) {
    msg = `🎉 Mükemmel Başarı! ELC Intermediate standartlarında konuya son derece hakimsiniz. En yüksek seri: ${state.testStreak}`;
  } else if (pct >= 60) {
    msg = `👍 Başarılı! Çoğu soruyu doğru yanıtladınız ancak sınav öncesi aşağıdaki eksik olduğunuz konuları gözden geçirmeniz tavsiye edilir.`;
  } else {
    msg = `⚠️ Bu konuyu biraz daha pekiştirmeniz gerekiyor. Aşağıdaki analizde belirtilen konuları Skill Building Set ve kelime listesinden tekrar çalışın.`;
  }
  document.getElementById('finalScoreMsg').textContent = msg;

  const listEl = document.getElementById('weakTopicsList');
  if (listEl) {
    if (state.wrongQuestions.length === 0) {
      listEl.innerHTML = `<li class="text-emerald-400 font-semibold">Tüm soruları doğru bildiniz! Harika bir sınav performansı bekliyoruz.</li>`;
    } else {
      const topicsMap = {};
      state.wrongQuestions.forEach(wq => {
        const top = wq.topic || 'Genel Konu';
        if (!topicsMap[top]) topicsMap[top] = [];
        topicsMap[top].push(wq);
      });

      listEl.innerHTML = Object.entries(topicsMap).map(([topicName, items]) => `
        <li class="space-y-0.5">
          <strong class="text-amber-300 font-bold">${escapeHtml(topicName)}:</strong>
          <span class="text-on-surface-variant block text-[11px] leading-relaxed">
            ${items.map(i => `• ${escapeHtml(i.explanation || '')}`).join('<br/>')}
          </span>
        </li>
      `).join('');
    }
  }
}

function restartCurrentQuiz() {
  state.currentQuestionIndex = 0;
  state.testScore = 0;
  state.testStreak = 0;
  state.answeredQuestions = {};
  state.wrongQuestions = [];
  document.getElementById('quizSummaryCard').classList.add('hidden');
  document.getElementById('activeQuizWrapper').classList.remove('hidden');
  renderCurrentQuestion();
}

// -------------------------------------------------------------
// PDF EXPORT ENGINE
// -------------------------------------------------------------
async function exportStudyGuidePdf() {
  const printArea = document.getElementById('pdfExportContainer');
  if (!printArea) return;

  const session = getActiveChat();
  const dateStr = new Date().toLocaleDateString('tr-TR', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' });

  let contentHtml = `
    <div style="font-family: Arial, sans-serif; color: #1a1d26; line-height: 1.5; font-size: 12px;">
      
      <!-- HEADER -->
      <div class="pdf-avoid-break" style="border-bottom: 3px solid #a6192e; padding-bottom: 12px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center;">
        <div>
          <h1 style="color: #a6192e; margin: 0; font-size: 22px; font-weight: bold; letter-spacing: -0.5px;">KOÇ UNIVERSITY ELC</h1>
          <h2 style="color: #333; margin: 4px 0 0; font-size: 15px; font-weight: 600;">Intermediate 07 • Midterm & Speaking Task Study Guide</h2>
        </div>
        <div style="text-align: right; font-size: 11px; color: #666;">
          <div><strong>Tarih:</strong> ${dateStr}</div>
          <div><strong>Hedef:</strong> Midterm Sprint & Speaking Prep</div>
        </div>
      </div>
  `;

  if (session && session.messages && session.messages.length > 0) {
    contentHtml += `
      <div style="margin-bottom: 20px;">
        <h3 class="pdf-avoid-break" style="background-color: #f3f4f8; padding: 8px 12px; border-left: 4px solid #a6192e; font-size: 14px; margin: 0 0 10px 0; color: #1a1d26;">
          1. Midterm Çalışma Notları ve Soru-Cevap Analizleri
        </h3>
        <div>
    `;
    session.messages.forEach(m => {
      const isUser = m.role === 'user';
      contentHtml += `
        <div class="pdf-avoid-break" style="margin-bottom: 10px; padding: 10px; border-radius: 6px; background-color: ${isUser ? '#f0f4ff' : '#f9f9f9'}; border: 1px solid #e5e7eb;">
          <div style="font-weight: bold; color: ${isUser ? '#00424e' : '#a6192e'}; margin-bottom: 4px; font-size: 11px;">
            ${isUser ? 'Öğrenci (Student)' : 'ELC 07 AI Assistant'} (${m.timestamp || ''}):
          </div>
          <div style="font-size: 12px;">${isUser ? escapeHtml(m.content) : marked.parse(m.content || '')}</div>
        </div>
      `;
    });
    contentHtml += `</div></div>`;
  }

  if (state.speaking.lastEvaluation) {
    const ev = state.speaking.lastEvaluation;
    contentHtml += `
      <div class="pdf-avoid-break" style="margin-bottom: 20px;">
        <h3 style="background-color: #f3f4f8; padding: 8px 12px; border-left: 4px solid #03b5d3; font-size: 14px; margin: 0 0 10px 0; color: #1a1d26;">
          2. Speaking Task Değerlendirme Raporu (CEFR B2+)
        </h3>
        <div style="font-size: 12px;">
          <div style="margin-bottom: 6px;"><strong>Soru:</strong> ${escapeHtml(SPEAKING_PROMPTS[state.speaking.promptId]?.text || '')}</div>
          <div style="margin-bottom: 6px; background-color: #f5f5f5; padding: 8px; border-radius: 4px;">
            <strong>Konuşma Transkripti:</strong> <em>"${escapeHtml(state.speaking.transcript)}"</em>
          </div>
          <div style="margin-bottom: 6px;"><strong>Puan:</strong> <span style="color: #a6192e; font-weight: bold;">${ev.overall_score}/100 (${ev.cefr_band})</span> - ${escapeHtml(ev.summary || '')}</div>
          <div style="margin-bottom: 6px;">
            <strong>Model B2+ Yanıt Metni:</strong>
            <p style="background-color: #fcfcfc; padding: 8px; border-left: 3px solid #10b981; margin: 4px 0 0;">${escapeHtml(ev.model_response || '')}</p>
          </div>
        </div>
      </div>
    `;
  }

  const answeredKeys = Object.keys(state.answeredQuestions);
  if (answeredKeys.length > 0) {
    contentHtml += `
      <div style="margin-bottom: 20px;">
        <h3 class="pdf-avoid-break" style="background-color: #f3f4f8; padding: 8px 12px; border-left: 4px solid #632ecd; font-size: 14px; margin: 0 0 10px 0; color: #1a1d26;">
          3. Çözülen Test Soruları ve Kural Açıklamaları (${state.testScore}/${answeredKeys.length} Doğru)
        </h3>
        <div>
    `;

    answeredKeys.forEach((qid, idx) => {
      const q = state.tests.find(item => item.id === qid) || state.tests[idx];
      const ans = state.answeredQuestions[qid];
      if (!q) return;

      contentHtml += `
        <div class="pdf-avoid-break" style="margin-bottom: 10px; padding: 10px; border: 1px solid #e5e7eb; border-radius: 6px; background-color: #ffffff;">
          <div style="font-weight: bold; margin-bottom: 4px;">Soru ${idx + 1} (${escapeHtml(q.unit || '')}): ${escapeHtml(q.question)}</div>
          <div style="margin-bottom: 4px; color: ${ans.isCorrect ? '#10b981' : '#dc2626'}; font-weight: bold;">
            ${ans.isCorrect ? '✔ Doğru Cevap' : '✘ Yanlış Cevap'} (Verilen Cevap: ${escapeHtml(String(ans.selected))})
          </div>
          <div style="color: #555; font-size: 11px;">
            <strong>Kural & Açıklama:</strong> ${escapeHtml(q.explanation || '')}
            ${q.synonyms ? `<br/><strong>Eş Anlamlılar:</strong> ${escapeHtml(q.synonyms)}` : ''}
            ${q.collocation ? `<br/><strong>Birlikte Kullanım (Collocation):</strong> ${escapeHtml(q.collocation)}` : ''}
          </div>
        </div>
      `;
    });

    contentHtml += `</div></div>`;
  }

  contentHtml += `
      <div class="pdf-avoid-break" style="border-top: 1px solid #ddd; padding-top: 10px; font-size: 10px; color: #888; text-align: center;">
        Koç University ELC Intermediate 07 • Skill Building Set Academic Assistant
      </div>
    </div>
  `;

  printArea.innerHTML = contentHtml;
  printArea.classList.remove('hidden');

  const opt = {
    margin: [10, 10, 10, 10],
    filename: `Koc_ELC_INT07_Study_Guide_${Date.now()}.pdf`,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2, useCORS: true, letterRendering: true, logging: false },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
    pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
  };

  try {
    await html2pdf().set(opt).from(printArea).save();
  } catch (err) {
    console.error('PDF generation error:', err);
    window.print();
  } finally {
    printArea.classList.add('hidden');
  }
}

// -------------------------------------------------------------
// EVENT LISTENERS & HELPERS
// -------------------------------------------------------------
function setupEventListeners() {
  const exportBtn = document.getElementById('exportPdfBtn');
  if (exportBtn) {
    exportBtn.addEventListener('click', exportStudyGuidePdf);
  }

  setInterval(() => {
    fetch('/api/status').catch(() => {});
  }, 5 * 60 * 1000);
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
