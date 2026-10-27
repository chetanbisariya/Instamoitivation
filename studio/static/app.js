// ========================================================
// INSTAGRAM STORY & MOTIVATION AGENT - STUDIO CLIENT
// ========================================================

document.addEventListener("DOMContentLoaded", () => {
    // State
    let currentReels = [];
    let selectedReel = null;
    let selectedCategory = "ROMANTIC";
    let selectedAvatar = "female_innocent";
    let selectedVoice = "ava_female";
    let selectedTopic = "MIDNIGHT CONFESSIONS";
    let optionsData = { avatars: {}, voices: {}, categories: {} };

    // Category Presets
    const CATEGORY_TOPICS = {
        "MOTIVATION": ["DAILY DISCIPLINE", "RELENTLESS FOCUS", "THE POWER OF SILENCE", "STAND FIRM", "UNSHAKABLE MIND"],
        "ADVENTURE": ["INTO THE UNKNOWN", "THE WHISPERING CANYON", "SUMMIT OF THE GODS", "ANCIENT PASSAGE", "THE WILD FRONTIER"],
        "ROMANTIC": ["MIDNIGHT CONFESSIONS", "THE UNSPOKEN TRUTH", "TIMELESS CONNECTION", "STARS ALIGNED", "TWILIGHT LETTERS"],
        "THRILLER": ["THE 3 AM KNOCK", "THE FORBIDDEN TAPE", "VANISHED AT DAWN", "SHADOW ON THE WALL", "LOCKED ELEVATOR"],
        "WISDOM": ["THE ART OF LETTING GO", "THE RIPPLE EFFECT", "STILLNESS IN CHAOS", "TIMELESS PERSPECTIVE", "THE QUIET MIND"]
    };

    // Cinema Keyword Presets
    const KEYWORD_TRIOS = [
        { k1: "Midnight", k2: "Lighthouse", k3: "Key", genre: "THRILLER" },
        { k1: "Eclipse", k2: "Observatory", k3: "Signal", genre: "SCI-FI" },
        { k1: "Blizzard", k2: "Altar", k3: "Sanctuary", genre: "ADVENTURE" },
        { k1: "Rain", k2: "Cobblestone", k3: "Farewell", genre: "ROMANTIC" },
        { k1: "Fog", k2: "Warehouse", k3: "Revolver", genre: "NOIR" },
        { k1: "Clocktower", k2: "Attic", k3: "Reflection", genre: "THRILLER" },
        { k1: "Shipwreck", k2: "Jungle", k3: "Amulet", genre: "ADVENTURE" },
        { k1: "Quantum", k2: "Drone", k3: "Paradox", genre: "SCI-FI" },
        { k1: "Neon", k2: "Alley", k3: "Cipher", genre: "NOIR" },
        { k1: "Letter", k2: "Lavender", k3: "Vow", genre: "ROMANTIC" }
    ];

    let selectedCinemaGenre = "THRILLER";

    // Mode Switcher Elements
    const modeStoryReelTab = document.getElementById("modeStoryReelTab");
    const modeCinemaTab = document.getElementById("modeCinemaTab");
    const storyDirectorPanel = document.getElementById("storyDirectorPanel");
    const cinemaDirectorPanel = document.getElementById("cinemaDirectorPanel");

    // Cinema Elements
    const kw1Input = document.getElementById("kw1Input");
    const kw2Input = document.getElementById("kw2Input");
    const kw3Input = document.getElementById("kw3Input");
    const randomizeKeywordsBtn = document.getElementById("randomizeKeywordsBtn");
    const cinemaGenreTabs = document.querySelectorAll("#cinemaGenreTabs .cinema-tab");
    const cinemaGenreBadge = document.getElementById("cinemaGenreBadge");
    const cinemaAvatarSelect = document.getElementById("cinemaAvatarSelect");
    const cinemaVoiceSelect = document.getElementById("cinemaVoiceSelect");
    const generateMovieBtn = document.getElementById("generateMovieBtn");
    const movieProgressBox = document.getElementById("movieProgressBox");
    const movieProgressTitle = document.getElementById("movieProgressTitle");
    const movieProgressDesc = document.getElementById("movieProgressDesc");

    // Elements
    const reelVideoPlayer = document.getElementById("reelVideoPlayer");
    const videoSource = document.getElementById("videoSource");
    const currentFileName = document.getElementById("currentFileName");
    const currentGenreBadge = document.getElementById("currentGenreBadge");
    const currentVoiceProvider = document.getElementById("currentVoiceProvider");
    const downloadReelBtn = document.getElementById("downloadReelBtn");
    const downloadThumbnailBtn = document.getElementById("downloadThumbnailBtn");
    const categoryTaglineBadge = document.getElementById("categoryTaglineBadge");

    const categoryTabs = document.querySelectorAll("#categoryTabsContainer .cat-tab");
    const avatarsPickerContainer = document.getElementById("avatarsPickerContainer");
    const reelLanguageSelect = document.getElementById("reelLanguageSelect");
    const cinemaLanguageSelect = document.getElementById("cinemaLanguageSelect");
    const voiceSelect = document.getElementById("voiceSelect");
    const topicChipsContainer = document.getElementById("topicChipsContainer");
    const customPromptInput = document.getElementById("customPromptInput");

    const generateReelBtn = document.getElementById("generateReelBtn");
    const generationProgressBox = document.getElementById("generationProgressBox");
    const progressStepTitle = document.getElementById("progressStepTitle");
    const progressStepDesc = document.getElementById("progressStepDesc");

    const captionTextArea = document.getElementById("captionTextArea");
    const copyCaptionBtn = document.getElementById("copyCaptionBtn");
    const currentPublishStatus = document.getElementById("currentPublishStatus");
    const dispatchBufferBtn = document.getElementById("dispatchBufferBtn");
    const dispatchWebhookBtn = document.getElementById("dispatchWebhookBtn");
    const dispatchInstagramDirectBtn = document.getElementById("dispatchInstagramDirectBtn");
    const dispatchYouTubeShortsBtn = document.getElementById("dispatchYouTubeShortsBtn");
    const dispatchFeedback = document.getElementById("dispatchFeedback");

    const reelsGrid = document.getElementById("reelsGrid");
    const refreshLibraryBtn = document.getElementById("refreshLibraryBtn");

    // Creator Lab Elements
    const openCreatorLabBtn = document.getElementById("openCreatorLabBtn");
    const closeCreatorLabBtn = document.getElementById("closeCreatorLabBtn");
    const creatorLabModal = document.getElementById("creatorLabModal");
    const quickAddAvatarBtn = document.getElementById("quickAddAvatarBtn");
    const quickAddVoiceBtn = document.getElementById("quickAddVoiceBtn");
    const labTabs = document.querySelectorAll(".modal-tab");
    const labTabContents = document.querySelectorAll(".lab-tab-content");

    const avatarDropzone = document.getElementById("avatarDropzone");
    const avatarFileInput = document.getElementById("avatarFileInput");
    const avatarDropzoneContent = document.getElementById("avatarDropzoneContent");
    const avatarPreviewContainer = document.getElementById("avatarPreviewContainer");
    const avatarPreviewImg = document.getElementById("avatarPreviewImg");
    const avatarUploadForm = document.getElementById("avatarUploadForm");
    const customAvatarName = document.getElementById("customAvatarName");
    const customAvatarRole = document.getElementById("customAvatarRole");
    const avatarUploadMsg = document.getElementById("avatarUploadMsg");

    const voiceUploadForm = document.getElementById("voiceUploadForm");
    const voiceFileInput = document.getElementById("voiceFileInput");
    const customVoiceName = document.getElementById("customVoiceName");
    const cloneInElevenLabs = document.getElementById("cloneInElevenLabs");
    const voiceUploadMsg = document.getElementById("voiceUploadMsg");

    const directAudioForm = document.getElementById("directAudioForm");
    const directAudioFile = document.getElementById("directAudioFile");
    const directAudioScript = document.getElementById("directAudioScript");
    const directAudioCategory = document.getElementById("directAudioCategory");
    const directAudioTopic = document.getElementById("directAudioTopic");
    const directAudioMsg = document.getElementById("directAudioMsg");

    // Live Mic Studio Elements
    const startMicBtn = document.getElementById("startMicBtn");
    const stopMicBtn = document.getElementById("stopMicBtn");
    const resetMicBtn = document.getElementById("resetMicBtn");
    const liveMicCanvas = document.getElementById("liveMicCanvas");
    const micTimerTag = document.getElementById("micTimerTag");
    const micStatusBadge = document.getElementById("micStatusBadge");
    const recordedAudioPreview = document.getElementById("recordedAudioPreview");
    const micPostRecordOptions = document.getElementById("micPostRecordOptions");
    const micScriptWordsInput = document.getElementById("micScriptWordsInput");
    const micCategorySelect = document.getElementById("micCategorySelect");
    const micAvatarSelect = document.getElementById("micAvatarSelect");
    const renderMicReelBtn = document.getElementById("renderMicReelBtn");
    const saveMicAsVoiceBtn = document.getElementById("saveMicAsVoiceBtn");
    const micFeedbackMsg = document.getElementById("micFeedbackMsg");

    // Live Mic Studio State
    let mediaRecorder = null;
    let audioChunks = [];
    let recordedAudioBlob = null;
    let micTimerInterval = null;
    let micElapsedSeconds = 0;
    let micAudioCtx = null;
    let micAnalyser = null;
    let micStream = null;
    let micAnimFrame = null;

    // Settings Modal Elements
    const openSettingsBtn = document.getElementById("openSettingsBtn");
    const closeSettingsBtn = document.getElementById("closeSettingsBtn");
    const cancelSettingsBtn = document.getElementById("cancelSettingsBtn");
    const saveSettingsBtn = document.getElementById("saveSettingsBtn");
    const settingsModal = document.getElementById("settingsModal");

    const cfgInstaHandle = document.getElementById("cfgInstaHandle");
    const cfgScheduleTime = document.getElementById("cfgScheduleTime");
    const cfgCategoryRotation = document.getElementById("cfgCategoryRotation");
    const cfgShowAvatar = document.getElementById("cfgShowAvatar");
    const cfgInstaDirectId = document.getElementById("cfgInstaDirectId");
    const cfgInstaDirectToken = document.getElementById("cfgInstaDirectToken");
    const cfgYouTubeKey = document.getElementById("cfgYouTubeKey");
    const cfgElevenKey = document.getElementById("cfgElevenKey");
    const cfgGeminiKey = document.getElementById("cfgGeminiKey");
    const cfgBufferToken = document.getElementById("cfgBufferToken");
    const cfgBufferProfileId = document.getElementById("cfgBufferProfileId");
    const cfgWebhookUrl = document.getElementById("cfgWebhookUrl");

    // 1. Fetch Options (Avatars, Voices, Categories, Languages)
    async function loadOptions() {
        try {
            const res = await fetch("/api/options");
            optionsData = await res.json();
            renderAvatarsPicker(optionsData.avatars);
            renderVoiceDropdown(optionsData.voices, reelLanguageSelect ? reelLanguageSelect.value : "en");
            renderCinemaCastOptions(optionsData.avatars, optionsData.voices, cinemaLanguageSelect ? cinemaLanguageSelect.value : "en");
            
            // Populate Mic Avatar select
            if (micAvatarSelect) {
                micAvatarSelect.innerHTML = "";
                Object.entries(optionsData.avatars).forEach(([avKey, avInfo]) => {
                    const opt = document.createElement("option");
                    opt.value = avKey;
                    opt.textContent = `${avInfo.name} (${avInfo.gender || 'Narrator'})`;
                    if (avKey === selectedAvatar) opt.selected = true;
                    micAvatarSelect.appendChild(opt);
                });
            }
        } catch (err) {
            console.error("Options fetch error:", err);
        }
    }

    if (reelLanguageSelect) {
        reelLanguageSelect.addEventListener("change", (e) => {
            renderVoiceDropdown(optionsData.voices, e.target.value);
        });
    }

    if (cinemaLanguageSelect) {
        cinemaLanguageSelect.addEventListener("change", (e) => {
            renderCinemaCastOptions(optionsData.avatars, optionsData.voices, e.target.value);
        });
    }

    function renderCinemaCastOptions(avatars, voices, filterLang = "en") {
        cinemaAvatarSelect.innerHTML = "";
        cinemaVoiceSelect.innerHTML = "";

        Object.entries(avatars).forEach(([avKey, avInfo]) => {
            const opt = document.createElement("option");
            opt.value = avKey;
            opt.textContent = `${avInfo.name} (${avInfo.description ? avInfo.description.split(' ')[0] : 'Narrator'})`;
            if (avKey === "female_innocent") opt.selected = true;
            cinemaAvatarSelect.appendChild(opt);
        });

        const noneOpt = document.createElement("option");
        noneOpt.value = "none";
        noneOpt.textContent = "None (Minimal / Waveform Only)";
        cinemaAvatarSelect.appendChild(noneOpt);

        let firstMatchKey = null;
        Object.entries(voices).forEach(([vKey, vInfo]) => {
            const vLang = vInfo.lang || "en";
            const opt = document.createElement("option");
            opt.value = vKey;
            opt.textContent = `${vInfo.name} (${vInfo.gender})${vLang !== 'en' ? ' [' + vLang.toUpperCase() + ']' : ''}`;
            if (vLang === filterLang && !firstMatchKey) {
                firstMatchKey = vKey;
            }
            cinemaVoiceSelect.appendChild(opt);
        });

        if (firstMatchKey) {
            cinemaVoiceSelect.value = firstMatchKey;
        } else if (cinemaVoiceSelect.options.length > 0) {
            cinemaVoiceSelect.selectedIndex = 0;
        }
    }

    // Studio Mode Switcher
    modeStoryReelTab.addEventListener("click", () => {
        modeStoryReelTab.classList.add("active");
        modeCinemaTab.classList.remove("active");
        storyDirectorPanel.style.display = "block";
        cinemaDirectorPanel.style.display = "none";
    });

    modeCinemaTab.addEventListener("click", () => {
        modeCinemaTab.classList.add("active");
        modeStoryReelTab.classList.remove("active");
        cinemaDirectorPanel.style.display = "block";
        storyDirectorPanel.style.display = "none";
    });

    // Randomize Keywords
    randomizeKeywordsBtn.addEventListener("click", () => {
        const randomTrio = KEYWORD_TRIOS[Math.floor(Math.random() * KEYWORD_TRIOS.length)];
        kw1Input.value = randomTrio.k1;
        kw2Input.value = randomTrio.k2;
        kw3Input.value = randomTrio.k3;
        setCinemaGenre(randomTrio.genre);
    });

    // Cinema Genre Selector
    cinemaGenreTabs.forEach(tab => {
        tab.addEventListener("click", () => {
            setCinemaGenre(tab.getAttribute("data-genre"));
        });
    });

    function setCinemaGenre(genre) {
        selectedCinemaGenre = genre;
        cinemaGenreTabs.forEach(t => t.classList.toggle("active", t.getAttribute("data-genre") === genre));
        const labels = {
            "THRILLER": "SUSPENSE THRILLER",
            "SCI-FI": "SCI-FI CINEMA",
            "ADVENTURE": "EPIC ADVENTURE",
            "ROMANTIC": "ROMANTIC CINEMA",
            "NOIR": "NEO-NOIR MYSTERY"
        };
        cinemaGenreBadge.textContent = labels[genre] || genre;
    }

    function renderAvatarsPicker(avatars) {
        avatarsPickerContainer.innerHTML = "";
        
        Object.entries(avatars).forEach(([avKey, avInfo]) => {
            const card = document.createElement("div");
            card.className = `avatar-card ${selectedAvatar === avKey ? 'active' : ''}`;
            card.setAttribute("data-avatar", avKey);
            
            const isCustom = avInfo.custom;
            card.innerHTML = `
                ${isCustom ? '<span class="avatar-custom-badge">CUSTOM</span>' : ''}
                <img src="/avatars/${avInfo.file}" alt="${escapeHtml(avInfo.name)}" class="avatar-thumb" onerror="this.src='/avatars/female_innocent.jpg'">
                <div class="avatar-info">
                    <span class="avatar-name">${escapeHtml(avInfo.name)}</span>
                    <span class="avatar-desc">${escapeHtml(avInfo.description ? avInfo.description.split(' ')[0] : 'Narrator')}</span>
                </div>
            `;
            card.addEventListener("click", () => setAvatar(avKey));
            avatarsPickerContainer.appendChild(card);
        });

        // Add None / Minimal card
        const noneCard = document.createElement("div");
        noneCard.className = `avatar-card ${selectedAvatar === 'none' ? 'active' : ''}`;
        noneCard.setAttribute("data-avatar", "none");
        noneCard.innerHTML = `
            <div class="avatar-thumb avatar-none-thumb">🚫</div>
            <div class="avatar-info">
                <span class="avatar-name">Minimal</span>
                <span class="avatar-desc">Waveform Only</span>
            </div>
        `;
        noneCard.addEventListener("click", () => setAvatar("none"));
        avatarsPickerContainer.appendChild(noneCard);
    }

    function renderVoiceDropdown(voices, filterLang = "en") {
        voiceSelect.innerHTML = "";
        
        const langGroup = document.createElement("optgroup");
        langGroup.label = `Native ${filterLang.toUpperCase()} Voices`;

        const femaleGroup = document.createElement("optgroup");
        femaleGroup.label = "Girl / Female Voices";

        const maleGroup = document.createElement("optgroup");
        maleGroup.label = "Male Voices";

        const customGroup = document.createElement("optgroup");
        customGroup.label = "Custom & Cloned Voices";

        let firstLangVoiceKey = null;

        Object.entries(voices).forEach(([vKey, vInfo]) => {
            const vLang = vInfo.lang || "en";
            const opt = document.createElement("option");
            opt.value = vKey;
            opt.textContent = `${vInfo.name} — ${vInfo.description}`;

            if (vLang === filterLang && !firstLangVoiceKey) {
                firstLangVoiceKey = vKey;
            }

            if (vInfo.custom) {
                customGroup.appendChild(opt);
            } else if (filterLang !== "en" && vLang === filterLang) {
                langGroup.appendChild(opt);
            } else if (vInfo.gender === "Female") {
                femaleGroup.appendChild(opt);
            } else {
                maleGroup.appendChild(opt);
            }
        });

        if (langGroup.children.length > 0) voiceSelect.appendChild(langGroup);
        if (customGroup.children.length > 0) voiceSelect.appendChild(customGroup);
        voiceSelect.appendChild(femaleGroup);
        voiceSelect.appendChild(maleGroup);

        if (firstLangVoiceKey) {
            voiceSelect.value = firstLangVoiceKey;
            selectedVoice = firstLangVoiceKey;
        } else if (voiceSelect.options.length > 0) {
            voiceSelect.selectedIndex = 0;
            selectedVoice = voiceSelect.value;
        }
    }

    function setAvatar(avKey) {
        selectedAvatar = avKey;
        document.querySelectorAll("#avatarsPickerContainer .avatar-card").forEach(c => {
            c.classList.toggle("active", c.getAttribute("data-avatar") === avKey);
        });
    }

    voiceSelect.addEventListener("change", (e) => {
        selectedVoice = e.target.value;
    });

    // 2. Category Switcher
    function setCategory(catKey) {
        selectedCategory = catKey;
        categoryTabs.forEach(t => {
            t.classList.toggle("active", t.getAttribute("data-cat") === catKey);
        });

        const taglines = {
            "MOTIVATION": "DAILY DISCIPLINE & STOICISM",
            "ADVENTURE": "STORYTELLING & ADVENTURE",
            "ROMANTIC": "ROMANTIC & POETIC",
            "THRILLER": "THRILLER & SUSPENSE",
            "WISDOM": "LIFE WISDOM & PARABLES"
        };
        categoryTaglineBadge.textContent = taglines[catKey] || catKey;

        const topics = CATEGORY_TOPICS[catKey] || CATEGORY_TOPICS["MOTIVATION"];
        topicChipsContainer.innerHTML = "";
        topics.forEach((t, i) => {
            const chip = document.createElement("button");
            chip.className = `chip ${i === 0 ? 'active' : ''}`;
            chip.textContent = t;
            chip.addEventListener("click", () => {
                document.querySelectorAll("#topicChipsContainer .chip").forEach(c => c.classList.remove("active"));
                chip.classList.add("active");
                selectedTopic = t;
            });
            topicChipsContainer.appendChild(chip);
        });
        selectedTopic = topics[0];

        // Recommend default avatar & voice pairing
        if (catKey === "ROMANTIC") {
            setAvatar("female_innocent");
            voiceSelect.value = "ava_female";
            selectedVoice = "ava_female";
        } else if (catKey === "ADVENTURE") {
            setAvatar("male_adventurer");
            voiceSelect.value = "andrew_male";
            selectedVoice = "andrew_male";
        } else if (catKey === "THRILLER") {
            setAvatar("female_innocent");
            voiceSelect.value = "christopher_male";
            selectedVoice = "christopher_male";
        } else if (catKey === "WISDOM") {
            setAvatar("male_innocent");
            voiceSelect.value = "brian_male";
            selectedVoice = "brian_male";
        } else {
            setAvatar("male_innocent");
            voiceSelect.value = "christopher_male";
            selectedVoice = "christopher_male";
        }
    }

    categoryTabs.forEach(tab => {
        tab.addEventListener("click", () => {
            setCategory(tab.getAttribute("data-cat"));
        });
    });

    // 3. Creator Lab (Custom Character & Voice Upload)
    openCreatorLabBtn.addEventListener("click", () => {
        creatorLabModal.style.display = "flex";
        switchLabTab("uploadAvatarTab");
    });
    quickAddAvatarBtn.addEventListener("click", () => {
        creatorLabModal.style.display = "flex";
        switchLabTab("uploadAvatarTab");
    });
    quickAddVoiceBtn.addEventListener("click", () => {
        creatorLabModal.style.display = "flex";
        switchLabTab("uploadVoiceTab");
    });
    closeCreatorLabBtn.addEventListener("click", () => creatorLabModal.style.display = "none");

    function switchLabTab(tabId) {
        labTabs.forEach(t => t.classList.toggle("active", t.getAttribute("data-tab") === tabId));
        labTabContents.forEach(c => c.classList.toggle("active", c.id === tabId));
    }

    labTabs.forEach(tab => {
        tab.addEventListener("click", () => switchLabTab(tab.getAttribute("data-tab")));
    });

    // Avatar Dropzone Handlers
    avatarDropzone.addEventListener("click", () => avatarFileInput.click());
    avatarFileInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (re) => {
                avatarPreviewImg.src = re.target.result;
                avatarDropzoneContent.style.display = "none";
                avatarPreviewContainer.style.display = "flex";
            };
            reader.readAsDataURL(file);
        }
    });

    // Upload Avatar Form
    avatarUploadForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const file = avatarFileInput.files[0];
        if (!file) {
            alert("Please select a character image first.");
            return;
        }

        const formData = new FormData();
        formData.append("avatar_file", file);
        formData.append("name", customAvatarName.value.trim());
        formData.append("description", customAvatarRole.value.trim());

        avatarUploadMsg.style.color = "var(--primary-gold)";
        avatarUploadMsg.textContent = "Uploading & processing character portrait...";

        try {
            const res = await fetch("/api/upload/avatar", { method: "POST", body: formData });
            const data = await res.json();
            if (data.success) {
                avatarUploadMsg.style.color = "var(--accent-emerald)";
                avatarUploadMsg.textContent = `✅ ${data.message}`;
                await loadOptions();
                setAvatar(data.avatar_id);
                setTimeout(() => creatorLabModal.style.display = "none", 1500);
            } else {
                throw new Error(data.detail || "Upload failed");
            }
        } catch (err) {
            avatarUploadMsg.style.color = "var(--accent-rose)";
            avatarUploadMsg.textContent = `Error: ${err.message}`;
        }
    });

    // Upload Voice Form
    voiceUploadForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const file = voiceFileInput.files[0];
        if (!file) {
            alert("Please select an audio file first.");
            return;
        }

        const formData = new FormData();
        formData.append("audio_file", file);
        formData.append("name", customVoiceName.value.trim());
        formData.append("clone_mode", cloneInElevenLabs.checked);

        voiceUploadMsg.style.color = "var(--primary-gold)";
        voiceUploadMsg.textContent = "Uploading & registering voice...";

        try {
            const res = await fetch("/api/upload/voice", { method: "POST", body: formData });
            const data = await res.json();
            if (data.success) {
                voiceUploadMsg.style.color = "var(--accent-emerald)";
                voiceUploadMsg.textContent = `✅ ${data.message}`;
                await loadOptions();
                selectedVoice = data.voice_id;
                voiceSelect.value = data.voice_id;
                setTimeout(() => creatorLabModal.style.display = "none", 1500);
            } else {
                throw new Error(data.detail || "Upload failed");
            }
        } catch (err) {
            voiceUploadMsg.style.color = "var(--accent-rose)";
            voiceUploadMsg.textContent = `Error: ${err.message}`;
        }
    });

    // Direct Spoken Voice Form
    directAudioForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const file = directAudioFile.files[0];
        if (!file) {
            alert("Please select your voice recording file.");
            return;
        }

        const formData = new FormData();
        formData.append("audio_file", file);
        formData.append("script", directAudioScript.value.trim());
        formData.append("category", directAudioCategory.value);
        formData.append("avatar", selectedAvatar);
        formData.append("topic", directAudioTopic.value.trim() || "MY SPOKEN STORY");

        directAudioMsg.style.color = "var(--primary-gold)";
        directAudioMsg.textContent = "Rendering 1080x1920 reel with your voice recording...";

        try {
            const res = await fetch("/api/generate-with-audio", { method: "POST", body: formData });
            const data = await res.json();
            if (data.success) {
                directAudioMsg.style.color = "var(--accent-emerald)";
                directAudioMsg.textContent = "✅ Spoken story reel rendered successfully!";
                creatorLabModal.style.display = "none";
                await loadReels();
                if (data.reel) {
                    selectReel(data.reel);
                    reelVideoPlayer.play().catch(() => {});
                }
            } else {
                throw new Error(data.detail || "Rendering failed");
            }
        } catch (err) {
            directAudioMsg.style.color = "var(--accent-rose)";
            directAudioMsg.textContent = `Error: ${err.message}`;
        }
    });

    // 4. Load Config & Reels
    async function loadConfig() {
        try {
            const res = await fetch("/api/config");
            const data = await res.json();
            
            cfgInstaHandle.value = data.instagram_handle || "";
            cfgScheduleTime.value = data.schedule_time || "09:00";
            cfgCategoryRotation.checked = data.schedule_category_rotation !== false;
            cfgShowAvatar.checked = data.show_avatar !== false;
            cfgWebhookUrl.value = data.webhook_url || "";
            
            const statusText = document.getElementById("agentStatusText");
            const mode = data.schedule_category_rotation ? "Auto-Rotate Daily" : data.default_category;
            statusText.textContent = `Daily Scheduler Ready (${mode} @ ${data.schedule_time})`;
        } catch (err) {
            console.error("Config fetch error:", err);
        }
    }

    async function loadReels() {
        try {
            const res = await fetch("/api/reels");
            const reels = await res.json();
            currentReels = reels;
            renderReelsGrid(reels);

            if (reels.length > 0 && !selectedReel) {
                selectReel(reels[0]);
            }
        } catch (err) {
            console.error("Reels fetch error:", err);
        }
    }

    function renderReelsGrid(reels) {
        reelsGrid.innerHTML = "";
        if (reels.length === 0) {
            reelsGrid.innerHTML = `<p style="color: var(--text-muted); grid-column: 1 / -1;">No reels generated yet. Create your first reel above!</p>`;
            return;
        }

        reels.forEach(reel => {
            const card = document.createElement("div");
            card.className = `reel-card ${selectedReel && selectedReel.filename === reel.filename ? 'active' : ''}`;
            
            const cat = reel.category || "MOTIVATION";
            const catColors = {
                "MOTIVATION": "var(--primary-gold)",
                "ADVENTURE": "var(--genre-adventure)",
                "ROMANTIC": "var(--genre-romantic)",
                "THRILLER": "var(--genre-thriller)",
                "WISDOM": "var(--genre-wisdom)"
            };
            const col = catColors[cat] || "var(--primary-gold)";

            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.375rem;">
                    <span class="reel-card-topic" style="color: ${col};">${escapeHtml(cat)}</span>
                    <span style="font-size: 0.6875rem; color: var(--text-muted);">${escapeHtml(reel.topic || '')}</span>
                </div>
                <div class="reel-card-quote">"${escapeHtml(reel.script || reel.topic)}"</div>
                <div class="reel-card-footer">
                    <span>${reel.duration ? reel.duration.toFixed(1) + 's' : ''} • ${reel.size_mb || 0} MB</span>
                    <span>${reel.voice_name || 'Neural'}</span>
                </div>
            `;
            card.addEventListener("click", () => selectReel(reel));
            reelsGrid.appendChild(card);
        });
    }

    function selectReel(reel) {
        selectedReel = reel;
        
        videoSource.src = reel.url;
        reelVideoPlayer.load();
        
        currentFileName.textContent = reel.filename;
        currentGenreBadge.textContent = reel.category || "MOTIVATION";
        currentVoiceProvider.textContent = reel.voice_name || reel.voice_provider || "Neural Voice";
        downloadReelBtn.href = reel.url;
        downloadReelBtn.setAttribute("download", reel.filename);

        // Thumbnail Cover Image Handler
        const thumbUrl = reel.thumbnail_url || `/media/cover_${reel.filename.replace('.mp4', '')}.jpg`;
        if (downloadThumbnailBtn) {
            downloadThumbnailBtn.href = thumbUrl;
            downloadThumbnailBtn.setAttribute("download", `cover_${reel.filename.replace('.mp4', '')}.jpg`);
            downloadThumbnailBtn.style.display = "inline-flex";
        }

        captionTextArea.value = reel.caption || "";
        currentPublishStatus.textContent = reel.status || "SAVED_LOCALLY";

        document.querySelectorAll(".reel-card").forEach(c => c.classList.remove("active"));
        renderReelsGrid(currentReels);
    }

    // 5. Generate Story Reel Action
    generateReelBtn.addEventListener("click", async () => {
        generateReelBtn.disabled = true;
        generationProgressBox.style.display = "block";
        const selectedLang = reelLanguageSelect ? reelLanguageSelect.value : "en";
        progressStepTitle.textContent = `Crafting ${selectedCategory} Story Reel (${selectedLang.toUpperCase()})...`;
        progressStepDesc.textContent = `Generating story prose, synthesizing voice (${selectedVoice}), pulsing avatar aura, and rendering 1080x1920 MP4...`;

        const payload = {
            category: selectedCategory,
            voice: selectedVoice,
            avatar: selectedAvatar,
            topic: selectedTopic,
            prompt: customPromptInput.value.trim(),
            language: selectedLang
        };

        try {
            const res = await fetch("/api/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const data = await res.json();
            if (!res.ok) {
                throw new Error(data.detail || "Generation failed");
            }

            progressStepTitle.textContent = "Story Reel Rendered Successfully!";
            progressStepDesc.textContent = "1080x1920 MP4 and High-Retention Cover Thumbnail ready for preview & publishing.";
            
            await loadReels();
            if (data.reel) {
                selectReel(data.reel);
                reelVideoPlayer.play().catch(() => {});
            }

            setTimeout(() => {
                generationProgressBox.style.display = "none";
            }, 3000);

        } catch (err) {
            alert(`Error: ${err.message}`);
            generationProgressBox.style.display = "none";
        } finally {
            generateReelBtn.disabled = false;
        }
    });

    // 5B. Generate 3-Keyword Short Movie Action
    generateMovieBtn.addEventListener("click", async () => {
        const k1 = kw1Input.value.trim() || "Midnight";
        const k2 = kw2Input.value.trim() || "Lighthouse";
        const k3 = kw3Input.value.trim() || "Key";
        const cinemaLang = cinemaLanguageSelect ? cinemaLanguageSelect.value : "en";

        generateMovieBtn.disabled = true;
        movieProgressBox.style.display = "block";
        movieProgressTitle.textContent = `Directing 3-Act ${selectedCinemaGenre} Short Film (${cinemaLang.toUpperCase()})...`;
        movieProgressDesc.textContent = `Keywords: [${k1}, ${k2}, ${k3}] • Writing screenplay, synthesizing voice, adding SFX risers, and rendering 3-act widescreen film...`;

        try {
            const payload = {
                keyword1: k1,
                keyword2: k2,
                keyword3: k3,
                genre: selectedCinemaGenre,
                voice: cinemaVoiceSelect.value,
                avatar: cinemaAvatarSelect.value,
                language: cinemaLang
            };

            const res = await fetch("/api/movie/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const data = await res.json();
            if (!res.ok) {
                throw new Error(data.detail || "Movie generation failed");
            }

            movieProgressTitle.textContent = "🎬 Short Movie Rendered Successfully!";
            movieProgressDesc.textContent = `"${data.movie.title}" is ready! 3-Act film + SFX audio + Cover thumbnail ready.`;

            await loadReels();
            if (data.movie) {
                selectReel({
                    filename: data.movie.filename,
                    url: data.movie.url,
                    thumbnail_url: data.movie.thumbnail_url,
                    category: `MOVIE (${data.movie.genre})`,
                    topic: data.movie.title,
                    script: data.movie.script,
                    caption: data.movie.caption,
                    duration: data.movie.duration,
                    voice_name: data.movie.voice_name,
                    status: data.movie.status
                });
                reelVideoPlayer.play().catch(() => {});
            }

            setTimeout(() => {
                movieProgressBox.style.display = "none";
            }, 3500);

        } catch (err) {
            alert(`Movie Generation Error: ${err.message}`);
            movieProgressBox.style.display = "none";
        } finally {
            generateMovieBtn.disabled = false;
        }
    });

    // 6. Copy Caption
    copyCaptionBtn.addEventListener("click", () => {
        if (!captionTextArea.value) return;
        navigator.clipboard.writeText(captionTextArea.value).then(() => {
            const originalText = copyCaptionBtn.textContent;
            copyCaptionBtn.textContent = "✅ Copied!";
            setTimeout(() => copyCaptionBtn.textContent = originalText, 2000);
        });
    });

    // 7. Queue to Buffer / Trigger Webhook
    async function handlePublish(target) {
        if (!selectedReel) {
            alert("Please select or generate a reel first.");
            return;
        }

        dispatchFeedback.style.color = "var(--primary-gold)";
        dispatchFeedback.textContent = `Dispatching to ${target}...`;

        try {
            const res = await fetch(`/api/publish/${selectedReel.filename}`, {
                method: "POST"
            });
            const data = await res.json();

            if (data.status === "QUEUED_TO_BUFFER") {
                dispatchFeedback.style.color = "var(--accent-emerald)";
                dispatchFeedback.textContent = "✅ Successfully queued to Buffer for Instagram!";
                currentPublishStatus.textContent = "QUEUED_TO_BUFFER";
            } else if (data.status === "DISPATCHED_TO_WEBHOOK") {
                dispatchFeedback.style.color = "var(--accent-emerald)";
                dispatchFeedback.textContent = "✅ Dispatched to Webhook successfully!";
                currentPublishStatus.textContent = "DISPATCHED_TO_WEBHOOK";
            } else {
                dispatchFeedback.style.color = "var(--accent-rose)";
                dispatchFeedback.textContent = `Notice: ${data.buffer?.message || data.webhook?.message || "Saved locally. Configure keys in Settings to auto-publish."}`;
            }
        } catch (err) {
            dispatchFeedback.style.color = "var(--accent-rose)";
            dispatchFeedback.textContent = `Error: ${err.message}`;
        }
    }

    dispatchBufferBtn.addEventListener("click", () => handlePublish("Buffer"));
    dispatchWebhookBtn.addEventListener("click", () => handlePublish("Webhook"));

    // Direct Instagram Graph API Publisher
    if (dispatchInstagramDirectBtn) {
        dispatchInstagramDirectBtn.addEventListener("click", async () => {
            if (!selectedReel) {
                alert("Please select or generate a reel first.");
                return;
            }
            dispatchFeedback.style.color = "var(--primary-gold)";
            dispatchFeedback.textContent = "Publishing directly to Instagram via Meta Graph API...";

            try {
                const res = await fetch(`/api/publish/instagram-direct/${selectedReel.filename}`, { method: "POST" });
                const data = await res.json();
                if (data.success) {
                    dispatchFeedback.style.color = "var(--accent-emerald)";
                    dispatchFeedback.textContent = `✅ Published Live! Media ID: ${data.media_id}`;
                    currentPublishStatus.textContent = "PUBLISHED_INSTAGRAM_DIRECT";
                } else {
                    dispatchFeedback.style.color = "var(--accent-rose)";
                    dispatchFeedback.textContent = `Instagram Notice: ${data.error || data.message || "Configure Instagram Account ID & Token in Settings"}`;
                }
            } catch (err) {
                dispatchFeedback.style.color = "var(--accent-rose)";
                dispatchFeedback.textContent = `Publish Error: ${err.message}`;
            }
        });
    }

    // YouTube Shorts Manifest Packager
    if (dispatchYouTubeShortsBtn) {
        dispatchYouTubeShortsBtn.addEventListener("click", async () => {
            if (!selectedReel) {
                alert("Please select or generate a reel first.");
                return;
            }
            dispatchFeedback.style.color = "var(--primary-gold)";
            dispatchFeedback.textContent = "Packaging YouTube Shorts metadata manifest...";

            try {
                const res = await fetch(`/api/publish/youtube-shorts/${selectedReel.filename}`, { method: "POST" });
                const data = await res.json();
                if (data.success) {
                    dispatchFeedback.style.color = "var(--accent-emerald)";
                    dispatchFeedback.textContent = `✅ ${data.message} Ready for YouTube Studio & Data API!`;
                } else {
                    dispatchFeedback.style.color = "var(--accent-rose)";
                    dispatchFeedback.textContent = `Notice: ${data.message}`;
                }
            } catch (err) {
                dispatchFeedback.style.color = "var(--accent-rose)";
                dispatchFeedback.textContent = `Error: ${err.message}`;
            }
        });
    }

    // 8. Live Microphone Studio Logic
    function drawIdleMicCanvas() {
        if (!liveMicCanvas) return;
        const ctx = liveMicCanvas.getContext("2d");
        const w = liveMicCanvas.width;
        const h = liveMicCanvas.height;
        ctx.clearRect(0, 0, w, h);
        ctx.fillStyle = "#090d16";
        ctx.fillRect(0, 0, w, h);
        ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(0, h / 2);
        ctx.lineTo(w, h / 2);
        ctx.stroke();
    }
    drawIdleMicCanvas();

    function formatTime(secs) {
        const m = Math.floor(secs / 60).toString().padStart(2, '0');
        const s = (secs % 60).toString().padStart(2, '0');
        return `${m}:${s}`;
    }

    function stopRecording() {
        if (micTimerInterval) {
            clearInterval(micTimerInterval);
            micTimerInterval = null;
        }
        if (mediaRecorder && mediaRecorder.state !== "inactive") {
            mediaRecorder.stop();
        }
    }

    if (startMicBtn) {
        startMicBtn.addEventListener("click", async () => {
            try {
                audioChunks = [];
                recordedAudioBlob = null;
                micFeedbackMsg.textContent = "";

                micStream = await navigator.mediaDevices.getUserMedia({ audio: true });

                // Web Audio Analyser for live dancing waveform
                micAudioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const source = micAudioCtx.createMediaStreamSource(micStream);
                micAnalyser = micAudioCtx.createAnalyser();
                micAnalyser.fftSize = 64;
                source.connect(micAnalyser);

                const bufferLength = micAnalyser.frequencyBinCount;
                const dataArray = new Uint8Array(bufferLength);
                const canvasCtx = liveMicCanvas.getContext("2d");
                const w = liveMicCanvas.width;
                const h = liveMicCanvas.height;

                function renderLiveWaveform() {
                    micAnimFrame = requestAnimationFrame(renderLiveWaveform);
                    micAnalyser.getByteFrequencyData(dataArray);

                    canvasCtx.fillStyle = "#090d16";
                    canvasCtx.fillRect(0, 0, w, h);

                    const barWidth = (w / bufferLength) * 1.8;
                    let x = 0;

                    for (let i = 0; i < bufferLength; i++) {
                        const barHeight = (dataArray[i] / 255) * h * 0.9;
                        const grad = canvasCtx.createLinearGradient(0, h, 0, 0);
                        grad.addColorStop(0, "#f59e0b");
                        grad.addColorStop(0.6, "#ef4444");
                        grad.addColorStop(1, "#ec4899");
                        canvasCtx.fillStyle = grad;

                        canvasCtx.fillRect(x, h - barHeight, barWidth - 3, barHeight);
                        x += barWidth;
                    }
                }
                renderLiveWaveform();

                // MediaRecorder Setup
                const mimeType = MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
                    ? "audio/webm;codecs=opus"
                    : (MediaRecorder.isTypeSupported("audio/mp4") ? "audio/mp4" : "");

                mediaRecorder = mimeType ? new MediaRecorder(micStream, { mimeType }) : new MediaRecorder(micStream);

                mediaRecorder.ondataavailable = (e) => {
                    if (e.data && e.data.size > 0) {
                        audioChunks.push(e.data);
                    }
                };

                mediaRecorder.onstop = () => {
                    recordedAudioBlob = new Blob(audioChunks, { type: mediaRecorder.mimeType || "audio/webm" });
                    const audioUrl = URL.createObjectURL(recordedAudioBlob);
                    recordedAudioPreview.src = audioUrl;
                    recordedAudioPreview.style.display = "block";
                    micPostRecordOptions.style.display = "block";
                    resetMicBtn.style.display = "inline-flex";
                    stopMicBtn.style.display = "none";
                    startMicBtn.style.display = "none";
                    micStatusBadge.textContent = `Recorded (${micElapsedSeconds}s)`;
                    micStatusBadge.classList.remove("recording");

                    if (micAnimFrame) cancelAnimationFrame(micAnimFrame);
                    if (micStream) micStream.getTracks().forEach(t => t.stop());
                    if (micAudioCtx) micAudioCtx.close().catch(() => {});
                    drawIdleMicCanvas();
                };

                mediaRecorder.start(200);
                micElapsedSeconds = 0;
                micTimerTag.textContent = "00:00 / 01:00";
                micStatusBadge.textContent = "Recording Live";
                micStatusBadge.classList.add("recording");

                startMicBtn.style.display = "none";
                stopMicBtn.style.display = "inline-flex";
                resetMicBtn.style.display = "none";
                recordedAudioPreview.style.display = "none";
                micPostRecordOptions.style.display = "none";

                micTimerInterval = setInterval(() => {
                    micElapsedSeconds++;
                    micTimerTag.textContent = `${formatTime(micElapsedSeconds)} / 01:00`;
                    if (micElapsedSeconds >= 60) {
                        stopRecording();
                    }
                }, 1000);

            } catch (err) {
                console.error("Mic access error:", err);
                micFeedbackMsg.style.color = "var(--accent-rose)";
                micFeedbackMsg.textContent = `Microphone access error: ${err.message}. Please allow mic permissions in browser.`;
            }
        });
    }

    if (stopMicBtn) stopMicBtn.addEventListener("click", stopRecording);

    if (resetMicBtn) {
        resetMicBtn.addEventListener("click", () => {
            stopRecording();
            audioChunks = [];
            recordedAudioBlob = null;
            micElapsedSeconds = 0;
            micTimerTag.textContent = "00:00 / 01:00";
            micStatusBadge.textContent = "Ready";
            micStatusBadge.classList.remove("recording");
            recordedAudioPreview.style.display = "none";
            recordedAudioPreview.src = "";
            micPostRecordOptions.style.display = "none";
            startMicBtn.style.display = "inline-flex";
            stopMicBtn.style.display = "none";
            resetMicBtn.style.display = "none";
            micFeedbackMsg.textContent = "";
            drawIdleMicCanvas();
        });
    }

    if (renderMicReelBtn) {
        renderMicReelBtn.addEventListener("click", async () => {
            if (!recordedAudioBlob) {
                alert("Please record audio before rendering.");
                return;
            }
            const words = micScriptWordsInput.value.trim() || "Spoken story recorded with studio microphone.";
            const cat = micCategorySelect ? micCategorySelect.value : "ROMANTIC";
            const av = micAvatarSelect ? micAvatarSelect.value : selectedAvatar;

            const formData = new FormData();
            formData.append("audio_file", recordedAudioBlob, "mic_voice.webm");
            formData.append("script", words);
            formData.append("category", cat);
            formData.append("avatar", av);
            formData.append("topic", "MICROPHONE STORY");
            formData.append("author", "Creator");

            micFeedbackMsg.style.color = "var(--primary-gold)";
            micFeedbackMsg.textContent = "Rendering 1080x1920 reel with your microphone audio...";

            try {
                const res = await fetch("/api/generate-with-audio", { method: "POST", body: formData });
                const data = await res.json();
                if (data.success) {
                    micFeedbackMsg.style.color = "var(--accent-emerald)";
                    micFeedbackMsg.textContent = "✅ Reel rendered successfully!";
                    creatorLabModal.style.display = "none";
                    await loadReels();
                    if (data.reel) {
                        selectReel(data.reel);
                        reelVideoPlayer.play().catch(() => {});
                    }
                } else {
                    throw new Error(data.detail || "Render failed");
                }
            } catch (err) {
                micFeedbackMsg.style.color = "var(--accent-rose)";
                micFeedbackMsg.textContent = `Error: ${err.message}`;
            }
        });
    }

    if (saveMicAsVoiceBtn) {
        saveMicAsVoiceBtn.addEventListener("click", async () => {
            if (!recordedAudioBlob) {
                alert("Please record audio before saving.");
                return;
            }
            const voiceName = prompt("Enter a name for this custom voice:", "My Studio Voice");
            if (!voiceName) return;

            const formData = new FormData();
            formData.append("audio_file", recordedAudioBlob, "my_mic_voice.webm");
            formData.append("name", voiceName.trim());
            formData.append("clone_mode", false);
            formData.append("description", "Recorded in-browser with live studio microphone");

            micFeedbackMsg.style.color = "var(--primary-gold)";
            micFeedbackMsg.textContent = "Registering custom voice...";

            try {
                const res = await fetch("/api/upload/voice", { method: "POST", body: formData });
                const data = await res.json();
                if (data.success) {
                    micFeedbackMsg.style.color = "var(--accent-emerald)";
                    micFeedbackMsg.textContent = `✅ ${data.message}`;
                    await loadOptions();
                    selectedVoice = data.voice_id;
                    voiceSelect.value = data.voice_id;
                    setTimeout(() => creatorLabModal.style.display = "none", 1500);
                } else {
                    throw new Error(data.detail || "Upload failed");
                }
            } catch (err) {
                micFeedbackMsg.style.color = "var(--accent-rose)";
                micFeedbackMsg.textContent = `Error: ${err.message}`;
            }
        });
    }

    // 9. Settings Modal
    openSettingsBtn.addEventListener("click", () => settingsModal.style.display = "flex");
    closeSettingsBtn.addEventListener("click", () => settingsModal.style.display = "none");
    cancelSettingsBtn.addEventListener("click", () => settingsModal.style.display = "none");

    saveSettingsBtn.addEventListener("click", async () => {
        const updatePayload = {
            instagram_handle: cfgInstaHandle.value.trim(),
            schedule_time: cfgScheduleTime.value.trim(),
            schedule_category_rotation: cfgCategoryRotation.checked,
            show_avatar: cfgShowAvatar.checked,
            instagram_account_id: cfgInstaDirectId ? cfgInstaDirectId.value.trim() : "",
            instagram_access_token: cfgInstaDirectToken ? cfgInstaDirectToken.value.trim() : "",
            youtube_api_key: cfgYouTubeKey ? cfgYouTubeKey.value.trim() : "",
            elevenlabs_api_key: cfgElevenKey.value.trim(),
            gemini_api_key: cfgGeminiKey.value.trim(),
            buffer_access_token: cfgBufferToken.value.trim(),
            buffer_profile_id: cfgBufferProfileId.value.trim(),
            webhook_url: cfgWebhookUrl.value.trim()
        };

        try {
            const res = await fetch("/api/config", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(updatePayload)
            });
            const data = await res.json();
            if (data.success) {
                alert("Settings saved successfully!");
                settingsModal.style.display = "none";
                loadConfig();
            }
        } catch (err) {
            alert(`Failed to save settings: ${err.message}`);
        }
    });

    refreshLibraryBtn.addEventListener("click", loadReels);

    function escapeHtml(text) {
        if (!text) return "";
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // Initialize
    loadOptions().then(() => {
        setCategory("ROMANTIC");
    });
    loadConfig();
    loadReels();
});
