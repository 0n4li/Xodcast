class AudioPlayer {
    constructor(options) {
        this.options = {
            id: 'audioPlayer',
            audioSrc: null,
            showTime: true,
            showProgressBar: true,
            playText: "Play",
            pauseText: "Pause",
            autoPlay: false,
            onended: (taskId) => { console.log('Audio playback ended for taskId:', taskId); },
            ...options
        };

        this.container = document.getElementById(this.options.id);

        this.audio = null;
        this.isPlaying = false;
        this.progressBar = null;
        this.playPauseButton = null;
        this.currentTimeDisplay = null;
        this.durationDisplay = null;
        this.autoPlay = this.options.autoPlay;

        this.mediaSource = null;
        this.sourceBuffer = null;
        this.audioQueue = [];
        this.isAppending = false;
        this.isStreaming = false;
        this.lastChunkEndTime = 0;
        this.isStreamFinished = false;
        this.taskId = null;

        this.initialized = false;
    }

    render() {
        if (this.initialized) {
            return;
        }

        // Use a document fragment for efficient DOM updates
        const fragment = document.createDocumentFragment();

        this.container.className = 'flex items-center flex-col gap-4 justify-center align-center p-4 h-full';

        // Create elements
        if (this.options.showProgressBar) {
            this.progressBar = this.createProgressBar();
            fragment.appendChild(this.progressBar);
        }

        if (this.options.showTime) {
            const { timeHolder, currentTimeDisplay, durationDisplay } = this.createTimeDisplay();
            this.timeHolder = timeHolder;
            this.currentTimeDisplay = currentTimeDisplay;
            this.durationDisplay = durationDisplay;
            fragment.appendChild(this.timeHolder);
        }

        this.playPauseButton = this.createPlayPauseButton();
        fragment.appendChild(this.playPauseButton);

        // Append the fragment to the container
        this.container.innerHTML = '';
        this.container.appendChild(fragment);

        // Add event listeners
        this.addEventListeners();

        // Set initial audio source
        this.setAudioSource(this.audioSrc);

        this.initialized = true;
    }

    createProgressBar() {
        const progressBar = document.createElement('progress');
        progressBar.className = 'w-full h-2 bg-gray-200 rounded';
        progressBar.value = 0;
        progressBar.max = 100;
        return progressBar;
    }

    createTimeDisplay() {
        const timeHolder = document.createElement('div');
        timeHolder.className = 'flex justify-between w-full';

        const currentTimeDisplay = document.createElement('span');
        currentTimeDisplay.textContent = '0:00';

        const durationDisplay = document.createElement('span');
        durationDisplay.textContent = '0:00';

        timeHolder.appendChild(currentTimeDisplay);
        timeHolder.appendChild(durationDisplay);

        return { timeHolder, currentTimeDisplay, durationDisplay };
    }

    createPlayPauseButton() {
        const playPauseButton = document.createElement('button');
        playPauseButton.className = 'play-pause-button bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white py-2 px-4 rounded';
        playPauseButton.textContent = this.options.playText;
        playPauseButton.disabled = true; // Disable until audio source is set
        return playPauseButton;
    }

    addEventListeners() {
        this.playPauseButton.addEventListener('click', (event) => {
            event.preventDefault();
            this.togglePlayPause();
        });
    }

    setAudioSource(audioSrc, isStreaming = false, taskId = null, supportedType = null) {
        console.log('setAudioSource called with audioSrc:', audioSrc, 'isStreaming:', isStreaming, 'taskId:', taskId, 'supportedType:', supportedType);
        this.audioSrc = audioSrc;
        this.taskId = taskId;
        this.isStreaming = isStreaming;

        if (isStreaming) {
            this.handleStreamingSource(audioSrc, taskId, supportedType);
        } else if (this.audioSrc) {
            this.handleNonStreamingSource(audioSrc);
        } else {
            this.resetAudioState();
        }
    }

    handleNonStreamingSource(audioSrc) {
        if (!this.audio) {
            this.audio = document.createElement('audio');
            this.audio.preload = 'metadata';
            this.container.appendChild(this.audio);
            this.audio.addEventListener('error', (e) => {
                console.error('Audio element error:', e);
            });
        }
        try {
            this.audio.src = audioSrc;
            this.audio.load();
            console.log('Non-streaming Audio source set:', audioSrc);
        } catch (error) {
            console.error('Error setting audio source:', error);
        }

        this.updateAudioEventListeners();
    }

    handleStreamingSource(streamUrl, taskId, supportedType) {
        console.log('handleStreamingSource called with taskId:', taskId);

        if (this.audio) {
            this.resetAudioState();
        }

        this.isStreamFinished = false;
        this.taskId = taskId;
        this.audio = document.createElement('audio');
        this.mediaSource = new MediaSource();
        this.audio.src = URL.createObjectURL(this.mediaSource);
        this.container.appendChild(this.audio);
        this.isAppending = false;

        this.mediaSource.addEventListener('sourceopen', this.onSourceOpen.bind(this, streamUrl, supportedType));

        this.updateAudioEventListeners();
    }

    onSourceOpen(streamUrl, supportedType) {
        console.log('onSourceOpen called with streamUrl:', streamUrl, 'supportedType:', supportedType);
        this.sourceBuffer = this.mediaSource.addSourceBuffer(supportedType);
        this.sourceBuffer.mode = 'sequence';
        this.sourceBuffer.addEventListener('updateend', this.onUpdateEnd.bind(this));
        this.fetchStream(streamUrl);
    }

    onUpdateEnd() {
        this.isAppending = false;
        if (this.audioQueue.length > 0 && !this.sourceBuffer.updating) {
            this.appendNextChunk();
        } else if (this.isStreamFinished && this.audioQueue.length === 0) {
            if (this.mediaSource.readyState === 'open') {
                try {
                    this.mediaSource.endOfStream();
                    console.log('Stream ended');
                } catch (error) {
                    console.error('Error ending media source:', error);
                }
            }
        }

        this.updateDurationDisplay();
    }

    appendNextChunk() {
        if (this.audioQueue.length === 0 || this.isAppending) return;

        this.isAppending = true;

        const chunk = this.audioQueue.shift();
        try {
            if (!this.sourceBuffer.isUpdating) {
                if (this.audio.buffered.length > 0) {
                    this.sourceBuffer.appendWindowStart = this.audio.buffered.end(this.audio.buffered.length - 1);
                } else {
                    this.sourceBuffer.appendWindowStart = 0;
                }
            }
            this.sourceBuffer.appendWindowEnd = Infinity;
            this.sourceBuffer.appendBuffer(chunk);
            console.log("Next chunk appended");

            console.log("Append Window Start:", this.sourceBuffer.appendWindowStart);
            console.log("Append Window End:", this.sourceBuffer.appendWindowEnd);

            if (this.audio.buffered.length > 0) {
                this.lastChunkEndTime = this.audio.buffered.end(this.audio.buffered.length - 1);
            }
        } catch (error) {
            console.error('Error appending buffer:', error);
            this.audioQueue.unshift(chunk);
            this.isAppending = false;
        }
    }

    fetchStream(streamUrl) {
        console.log('Fetching stream:', streamUrl);
        fetch(streamUrl)
            .then(response => {
                const reader = response.body.getReader();
                const read = () => {
                    if (this.isAppending && this.audioQueue.length > 0) {
                        setTimeout(read, 100);
                        return;
                    }
                    reader.read().then(({ done, value }) => {
                        if (done) {
                            console.log("Stream finished");
                            this.isStreamFinished = true;
                            this.onUpdateEnd();
                            return;
                        }

                        this.audioQueue.push(value);
                        if (!this.isAppending) {
                            this.appendNextChunk();
                        }
                        read();
                    }).catch(error => {
                        console.error('Error in reader.read():', error);
                        this.cleanupMediaSource();
                    });
                };
                read();
            })
            .catch(error => {
                console.error('Error fetching stream:', error);
                this.cleanupMediaSource();
            });
    }

    cleanupMediaSource() {
        if (this.sourceBuffer) {
            try {
                if (this.sourceBuffer.updating) {
                    this.sourceBuffer.abort();
                }
            } catch (error) {
                console.error('Error aborting source buffer:', error);
            }
            this.sourceBuffer = null;
        }
        if (this.mediaSource && this.mediaSource.readyState === 'open') {
            try {
                this.mediaSource.endOfStream();
            } catch (error) {
                console.error('Error ending media source:', error);
            }
            this.mediaSource = null;
        }
    }

    updateAudioEventListeners() {
        console.log('updateAudioEventListeners called');
        // Remove existing listeners if any
        this.removeAudioEventListeners();

        if (this.audio) {
            this.audio.addEventListener('loadedmetadata', this.handleLoadedMetadata);
            this.audio.addEventListener('timeupdate', this.handleTimeUpdate);
            this.audio.addEventListener('ended', this.handleEnded);
            this.audio.addEventListener('canplay', this.handleCanPlay);
            this.audio.addEventListener('error', this.handleAudioError);
            this.audio.addEventListener('seeked', this.handleSeeked);

            if (this.progressBar && !this.mediaSource) {
                this.progressBar.addEventListener('click', this.handleProgressBarClick);
            }
        }

    }

    handleSeeked = () => {  
        this.updateDurationDisplay();
    }

    handleAudioError = (e) => {
        console.error('Audio element error:', e);
        this.cleanupMediaSource();
        this.resetAudioState();
    }

    removeAudioEventListeners() {
        if (!this.audio) return;

        this.audio.removeEventListener('loadedmetadata', this.handleLoadedMetadata);
        this.audio.removeEventListener('timeupdate', this.handleTimeUpdate);
        this.audio.removeEventListener('ended', this.handleEnded);
        this.audio.removeEventListener('canplay', this.handleCanPlay);
        this.audio.removeEventListener('error', this.handleAudioError);

        if (this.progressBar) {
            this.progressBar.removeEventListener('click', this.handleProgressBarClick);
        }
    }

    handleLoadedMetadata = () => {
        console.log('Audio loaded');
        if (this.durationDisplay) {
            try {
                this.durationDisplay.textContent = this.formatTime(this.audio.duration);
            } catch (error) {
                console.error('Error formatting duration:', error);
            }
        }
        this.playPauseButton.disabled = false; // Enable play/pause button
    }

    handleTimeUpdate = () => {
        this.updateProgressBar();
        if (this.currentTimeDisplay) {
            try {
                this.currentTimeDisplay.textContent = this.formatTime(this.audio.currentTime);
                if (this.isStreaming) {
                    this.updateDurationDisplay();
                }
            } catch (error) {
                console.error('Error formatting current time:', error);
            }
        }
    }

    updateDurationDisplay() {
        if (!this.durationDisplay) return;

        if (this.isStreaming) {
            this.durationDisplay.textContent = this.formatTime(this.lastChunkEndTime);
        } else {
            this.durationDisplay.textContent = this.formatTime(this.audio.duration);
        }
    }

    handleEnded = () => {
        this.isPlaying = false;
        this.playPauseButton.textContent = this.options.playText;
        if (this.progressBar) {
            this.progressBar.value = 0;
        }
        if (this.currentTimeDisplay) {
            this.currentTimeDisplay.textContent = '0:00';
        }
        this.options.onended(this.taskId);
    }

    handleProgressBarClick = (event) => {
        const rect = this.progressBar.getBoundingClientRect();
        const clickX = event.clientX - rect.left;
        const percentage = clickX / this.progressBar.offsetWidth;
        const newTime = percentage * this.audio.duration;
        this.audio.currentTime = newTime;
    }

    handleCanPlay = () => {
        // Play the audio when it's ready to play
        if (this.autoPlay && this.mediaSource && this.mediaSource.readyState === 'open') {
            this.play();
        }
    }

    resetAudioState() {
        console.log('resetAudioState called');
        if (this.audio) {
            this.audio.pause();
            if (this.audio.parentNode === this.container) {
                this.container.removeChild(this.audio);
            }
            this.audio = null;
            this.isPlaying = false;
            this.playPauseButton.textContent = this.options.playText;
            this.mediaSource = null;
            this.sourceBuffer = null;
            this.removeAudioEventListeners();
        }

        if (this.durationDisplay) {
            this.durationDisplay.textContent = '0:00';
        }
        if (this.progressBar) {
            this.progressBar.value = 0;
        }
        if (this.currentTimeDisplay) {
            this.currentTimeDisplay.textContent = '0:00';
        }
        this.playPauseButton.disabled = true;
        this.lastChunkEndTime = 0;
        this.isStreaming = false;
    }

    getAudioSource() {
        return this.audioSrc;
    }

    async togglePlayPause() {
        if (!this.audio) return; // Do nothing if no audio is loaded

        try {
            if (this.isPlaying) {
                this.audio.pause();
                this.playPauseButton.textContent = this.options.playText;
            } else {
                await this.audio.play(); // Handle potential play() exceptions
                this.playPauseButton.textContent = this.options.pauseText;
            }
            this.isPlaying = !this.isPlaying;
        } catch (error) {
            console.error('Error toggling play/pause:', error);
            // Handle error gracefully, e.g., display an error message to the user
        }
    }

    async play() {
        if (!this.audio || this.isPlaying) return;

        try {
            await this.audio.play();
            this.isPlaying = true;
            this.playPauseButton.textContent = this.options.pauseText;
        } catch (error) {
            console.error('Error playing audio:', error);
        }
    }

    updateProgressBar() {
        if (!this.audio) return; // Do nothing if no audio is loaded

        if (isNaN(this.audio.duration) || isNaN(this.audio.currentTime)) {
            return;
        }

        const percentage = (this.audio.currentTime / this.audio.duration) * 100;
        if (this.progressBar) {
            this.progressBar.value = percentage;
        }
    }

    formatTime(seconds) {
        if (isNaN(seconds)) {
            return '0:00';
        }
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }

    resolveUrl(url) {
        // If the URL is already absolute, return it directly
        if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('//')) {
            return url;
        }

        // Otherwise, resolve it relative to the current document's base URL
        const a = document.createElement('a');
        a.href = url;
        return a.href;
    }

    show() {
        this.container.classList.remove('hidden');
    }

    hide() {
        this.container.classList.add('hidden');
    }
}

function resolveRelativeUrl(url) {
    // If the URL is already absolute, return it directly
    if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('//')) {
        return url;
    }

    // Otherwise, resolve it relative to the current document's base URL
    const a = document.createElement('a');
    a.href = url;
    return a.href;
}
