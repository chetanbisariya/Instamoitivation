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
    let optionsData = null;

    // Category Presets
    const CATEGORY_TOPICS = {
        "MOTIVATION": ["DAILY DISCIPLINE", "RELENTLESS FOCUS", "THE POWER OF SILENCE", "STAND FIRM", "UNSHAKABLE MIND"],
        "ADVENTURE": ["INTO THE UNKNOWN", "THE WHISPERING CANYON", "SUMMIT OF THE GODS", "ANCIENT PASSAGE", "THE WILD FRONTIER"],
        "ROMANTIC": ["MIDNIGHT CONFESSIONS", "THE UNSPOKEN TRUTH", "TIMELESS CONNECTION", "STARS ALIGNED", "TWILIGHT LETTERS"],
        "THRILLER": ["THE 3 AM KNOCK", "THE FORBIDDEN TAPE", "VANISHED AT DAWN", "SHADOW ON THE WALL", "LOCKED ELEVATOR"],
        "WISDOM": ["THE ART OF LETTING GO", "THE RIPPLE EFFECT", "STILLNESS IN CHAOS", "TIMELESS PERSPECTIVE", "THE QUIET MIND"]
    };

    // Elements
    const reelVideoPlayer = document.getElementById("reelVideoPlayer");
    const videoSource = document.getElementById("videoSource");
    const currentFileName = document.getElementById("currentFileName");
    const currentGenreBadge = document.getElementById("currentGenreBadge");
    const currentVoiceProvider = document.getElementById("currentVoiceProvider");
    const downloadReelBtn = document.getElementById("downloadReelBtn");
    const categoryTaglineBadge = document.getElementById("categoryTaglineBadge");

    const categoryTabs = document.querySelectorAll("#categoryTabsContainer .cat-tab");
    const avatarCards = document.querySelectorAll("#avatarsPickerContainer .avatar-card");
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
    const dispatchFeedback = document.getElementById("dispatchFeedback");

    const reelsGrid = document.getElementById("reelsGrid");
    const refreshLibraryBtn = document.getElementById("refreshLibraryBtn");

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
    const cfgElevenKey = document.getElementById("cfgElevenKey");
    const cfgGeminiKey = document.getElementById("cfgGeminiKey");
    const cfgBufferToken = document.getElementById("cfgBufferToken");
    const cfgBufferProfileId = document.getElementById("cfgBufferProfileId");
    const cfgWebhookUrl = document.getElementById("cfgWebhookUrl");

    // 1. Category Switcher
    function setCategory(catKey) {
        selectedCategory = catKey;
        categoryTabs.forEach(t => {
            t.classList.toggle("active", t.getAttribute("data-cat") === catKey);
        });

        // Update Tagline
        const taglines = {
            "MOTIVATION": "DAILY DISCIPLINE & STOICISM",
            "ADVENTURE": "STORYTELLING & ADVENTURE",
            "ROMANTIC": "ROMANTIC & POETIC",
            "THRILLER": "THRILLER & SUSPENSE",
            "WISDOM": "LIFE WISDOM & PARABLES"
        };
        categoryTaglineBadge.textContent = taglines[catKey] || catKey;

        // Populate Topic Chips
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

        // Suggest best default voice and avatar for the category
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

    // 2. Avatar Selection
    function setAvatar(avKey) {
        selectedAvatar = avKey;
        avatarCards.forEach(c => {
            c.classList.toggle("active", c.getAttribute("data-avatar") === avKey);
        });
    }

    avatarCards.forEach(card => {
        card.addEventListener("click", () => {
            setAvatar(card.getAttribute("data-avatar"));
        });
    });

    // 3. Voice Selection
    voiceSelect.addEventListener("change", (e) => {
        selectedVoice = e.target.value;
    });

    // 4. Load Initial Config & Options
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

    // 5. Load Reels Library
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

        captionTextArea.value = reel.caption || "";
        currentPublishStatus.textContent = reel.status || "SAVED_LOCALLY";

        document.querySelectorAll(".reel-card").forEach(c => c.classList.remove("active"));
        renderReelsGrid(currentReels);
    }

    // 6. Generate Story Reel Action
    generateReelBtn.addEventListener("click", async () => {
        generateReelBtn.disabled = true;
        generationProgressBox.style.display = "block";
        progressStepTitle.textContent = `Crafting ${selectedCategory} Story Reel...`;
        progressStepDesc.textContent = `Generating story prose, synthesizing voice (${selectedVoice}), pulsing avatar aura, and rendering 1080x1920 MP4...`;

        const payload = {
            category: selectedCategory,
            voice: selectedVoice,
            avatar: selectedAvatar,
            topic: selectedTopic,
            prompt: customPromptInput.value.trim()
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
            progressStepDesc.textContent = "1080x1920 MP4 ready for preview and publishing.";
            
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

    // 7. Copy Caption
    copyCaptionBtn.addEventListener("click", () => {
        if (!captionTextArea.value) return;
        navigator.clipboard.writeText(captionTextArea.value).then(() => {
            const originalText = copyCaptionBtn.textContent;
            copyCaptionBtn.textContent = "✅ Copied!";
            setTimeout(() => copyCaptionBtn.textContent = originalText, 2000);
        });
    });

    // 8. Queue to Buffer / Trigger Webhook
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

    // Initialize Default
    setCategory("ROMANTIC");
    loadConfig();
    loadReels();
});
