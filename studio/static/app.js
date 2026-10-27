// ========================================================
// INSTAGRAM MOTIVATION AGENT - STUDIO CLIENT LOGIC
// ========================================================

document.addEventListener("DOMContentLoaded", () => {
    // State
    let currentReels = [];
    let selectedReel = null;
    let selectedTopic = "DAILY DISCIPLINE";

    // Elements
    const reelVideoPlayer = document.getElementById("reelVideoPlayer");
    const videoSource = document.getElementById("videoSource");
    const currentFileName = document.getElementById("currentFileName");
    const currentVoiceProvider = document.getElementById("currentVoiceProvider");
    const downloadReelBtn = document.getElementById("downloadReelBtn");
    
    const topicChips = document.querySelectorAll("#topicChipsContainer .chip");
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
    const cfgElevenKey = document.getElementById("cfgElevenKey");
    const cfgVoiceId = document.getElementById("cfgVoiceId");
    const cfgGeminiKey = document.getElementById("cfgGeminiKey");
    const cfgBufferToken = document.getElementById("cfgBufferToken");
    const cfgBufferProfileId = document.getElementById("cfgBufferProfileId");
    const cfgWebhookUrl = document.getElementById("cfgWebhookUrl");
    const cfgScheduleTime = document.getElementById("cfgScheduleTime");

    // 1. Topic Selection
    topicChips.forEach(chip => {
        chip.addEventListener("click", () => {
            topicChips.forEach(c => c.classList.remove("active"));
            chip.classList.add("active");
            selectedTopic = chip.getAttribute("data-topic");
        });
    });

    // 2. Load Config
    async function loadConfig() {
        try {
            const res = await fetch("/api/config");
            const data = await res.json();
            
            cfgInstaHandle.value = data.instagram_handle || "";
            cfgVoiceId.value = data.elevenlabs_voice_id || "";
            cfgScheduleTime.value = data.schedule_time || "09:00";
            cfgWebhookUrl.value = data.webhook_url || "";
            
            const statusText = document.getElementById("agentStatusText");
            if (data.elevenlabs_configured) {
                statusText.textContent = `ElevenLabs Voice Active (${data.schedule_time})`;
            } else {
                statusText.textContent = `Edge-TTS Neural Active (${data.schedule_time})`;
            }
        } catch (err) {
            console.error("Failed to load config:", err);
        }
    }

    // 3. Load Reels Library
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
            console.error("Failed to load reels:", err);
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
            card.innerHTML = `
                <div class="reel-card-topic">${escapeHtml(reel.topic || 'MOTIVATION')}</div>
                <div class="reel-card-quote">"${escapeHtml(reel.script || reel.topic)}"</div>
                <div class="reel-card-footer">
                    <span>${reel.duration ? reel.duration.toFixed(1) + 's' : ''} • ${reel.size_mb || 0} MB</span>
                    <span>${reel.created_at ? reel.created_at.split(' ')[0] : ''}</span>
                </div>
            `;
            card.addEventListener("click", () => selectReel(reel));
            reelsGrid.appendChild(card);
        });
    }

    function selectReel(reel) {
        selectedReel = reel;
        
        // Update Video Player
        videoSource.src = reel.url;
        reelVideoPlayer.load();
        
        // Update Info
        currentFileName.textContent = reel.filename;
        currentVoiceProvider.textContent = reel.voice_provider || (reel.filename.includes('sample') ? 'Edge-TTS (Christopher)' : 'Neural Voice');
        downloadReelBtn.href = reel.url;
        downloadReelBtn.setAttribute("download", reel.filename);

        // Update Caption & Status
        captionTextArea.value = reel.caption || "";
        currentPublishStatus.textContent = reel.status || "SAVED_LOCALLY";

        // Highlight active in grid
        document.querySelectorAll(".reel-card").forEach(c => c.classList.remove("active"));
        renderReelsGrid(currentReels);
    }

    // 4. Generate Reel Action
    generateReelBtn.addEventListener("click", async () => {
        generateReelBtn.disabled = true;
        generationProgressBox.style.display = "block";
        progressStepTitle.textContent = "Initiating Video Pipeline...";
        progressStepDesc.textContent = "Generating script, synthesizing neural voiceover, and analyzing audio spectrum...";

        const payload = {
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

            // Success
            progressStepTitle.textContent = "Reel Rendered Successfully!";
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

    // 5. Copy Caption
    copyCaptionBtn.addEventListener("click", () => {
        if (!captionTextArea.value) return;
        navigator.clipboard.writeText(captionTextArea.value).then(() => {
            const originalText = copyCaptionBtn.textContent;
            copyCaptionBtn.textContent = "✅ Copied!";
            setTimeout(() => copyCaptionBtn.textContent = originalText, 2000);
        });
    });

    // 6. Queue to Buffer / Trigger Webhook
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

    // 7. Settings Modal
    openSettingsBtn.addEventListener("click", () => settingsModal.style.display = "flex");
    closeSettingsBtn.addEventListener("click", () => settingsModal.style.display = "none");
    cancelSettingsBtn.addEventListener("click", () => settingsModal.style.display = "none");

    saveSettingsBtn.addEventListener("click", async () => {
        const updatePayload = {
            instagram_handle: cfgInstaHandle.value.trim(),
            elevenlabs_api_key: cfgElevenKey.value.trim(),
            elevenlabs_voice_id: cfgVoiceId.value.trim(),
            gemini_api_key: cfgGeminiKey.value.trim(),
            buffer_access_token: cfgBufferToken.value.trim(),
            buffer_profile_id: cfgBufferProfileId.value.trim(),
            webhook_url: cfgWebhookUrl.value.trim(),
            schedule_time: cfgScheduleTime.value.trim()
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
    loadConfig();
    loadReels();
});
