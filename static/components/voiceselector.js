class VoiceSelector {
    constructor(options) {
        this.options = {
            id: 'voiceSelector',
            voices: {},
            defaultHostVoice: null,
            defaultGuestVoice: null,
            soundsPath: 'static/sounds/', // Default path
            ...options
        };

        this.hostVoice = this.options.defaultHostVoice;
        this.guestVoice = this.options.defaultGuestVoice;
        this.audioPlayer = null;
        this.container = null;

        // Assume multiSpeakerVoices is available globally (you might need to adjust this)
        this.voices = this.options.voices;
        this.changeListeners = [];
    }

    addChangeListener(listener) {
        this.changeListeners.push(listener);
    }
    render() {
        this.container = document.getElementById(this.options.id);
        if (!this.container) {
            console.error("Container element not found:", this.options.id);
            return; // Exit if container is not found
        }
        console.log("Rendering Voice Selector");
        this.container.innerHTML = '';

        const title = document.createElement('h3');
        title.className = 'text-lg font-bold mb-2';
        title.textContent = 'Select Voices';
        this.container.appendChild(title);

        const hostRow = this.createVoiceRow('Host');
        const guestRow = this.createVoiceRow('Guest');

        this.container.appendChild(hostRow);
        this.container.appendChild(guestRow);

        // Create a container for the AudioPlayer and add it to the DOM
        const audioPlayerContainer = document.createElement('div');
        audioPlayerContainer.id = 'voicePreviewPlayer';
        this.container.appendChild(audioPlayerContainer);

        // Create the AudioPlayer instance
        this.audioPlayer = new AudioPlayer({
            id: 'voicePreviewPlayer',
            showTime: false,
            showProgressBar: false,
            playText: "Preview",
            pauseText: "Stop",
        });
        this.audioPlayer.render();

        // Update audio player if voices are already set
        if (this.hostVoice && this.guestVoice) {
            this.updateAudioPlayer();
        }
    }

    createVoiceRow(type) {
        const row = document.createElement('div');
        row.className = 'flex flex-col items-center mb-4';

        const label = document.createElement('h4');
        label.className = 'font-bold mb-2';
        label.textContent = type;
        row.appendChild(label);

        const avatarsContainer = document.createElement('div');
        avatarsContainer.className = 'flex gap-4';

        for (const voiceKey in this.voices) {
            const voice = this.voices[voiceKey];
            const avatarButton = document.createElement('button');
            avatarButton.className = 'rounded-full w-16 h-16 flex items-center justify-center text-white font-bold text-lg';
            avatarButton.style.backgroundColor = this.stringToColor(voice.Name);
            avatarButton.textContent = voice.Name[0];
            avatarButton.addEventListener('click', (event) => {
                event.preventDefault(); // Prevent form submission

                if (type === 'Host') {
                    if (this.guestVoice === voiceKey) return;
                    this.hostVoice = this.hostVoice === voiceKey ? null : voiceKey;
                } else {
                    if (this.hostVoice === voiceKey) return;
                    this.guestVoice = this.guestVoice === voiceKey ? null : voiceKey;
                }
                this.render();
                this.updateAudioPlayer();

                // Notify change listeners
                this.changeListeners.forEach(listener => listener());
            });

            // Disable button if the voice is selected for the other type
            if ((type === 'Host' && this.guestVoice === voiceKey) || (type === 'Guest' && this.hostVoice === voiceKey)) {
                avatarButton.disabled = true;
                avatarButton.classList.add('opacity-50', 'cursor-not-allowed'); // Add Tailwind CSS classes for disabled state
            } else {
                avatarButton.disabled = false;
                avatarButton.classList.remove('opacity-50', 'cursor-not-allowed');
            }

            // Highlight if selected
            if ((type === 'Host' && this.hostVoice === voiceKey) || (type === 'Guest' && this.guestVoice === voiceKey)) {
                avatarButton.classList.add('ring-4', 'ring-blue-500');
            } else {
                avatarButton.classList.remove('ring-4', 'ring-blue-500');
            }

            const nameLabel = document.createElement('p');
            nameLabel.className = 'text-center mt-1';
            nameLabel.textContent = voice.Name;

            const avatarContainer = document.createElement('div');
            avatarContainer.className = 'flex flex-col items-center';
            avatarContainer.appendChild(avatarButton);
            avatarContainer.appendChild(nameLabel);

            avatarsContainer.appendChild(avatarContainer);
        }

        row.appendChild(avatarsContainer);
        return row;
    }

    updateAudioPlayer() {
        console.log("Updating Audio Player");
        console.log(this.hostVoice);
        console.log(this.guestVoice);
        if (this.hostVoice && this.guestVoice) {
            const hostVoiceKey = this.hostVoice.split('-').pop();
            const guestVoiceKey = this.guestVoice.split('-').pop();
            const audioSrc = `${this.options.soundsPath}output-${hostVoiceKey}-${guestVoiceKey}.wav`;
            this.audioPlayer.setAudioSource(audioSrc);
            console.log(audioSrc);
        } else {
            this.audioPlayer.setAudioSource('');
        }
    }

    // Helper function to generate a color from a string
    stringToColor(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = str.charCodeAt(i) + ((hash << 5) - hash);
        }
        let color = '#';
        for (let i = 0; i < 3; i++) {
            const value = (hash >> (i * 8)) & 0xFF;
            color += ('00' + value.toString(16)).substr(-2);
        }
        return color;
    }

    setVoices(hostVoice, guestVoice) {
        this.hostVoice = hostVoice;
        this.guestVoice = guestVoice;
        this.render();
        this.updateAudioPlayer();
    }

    getSelectedVoices() {
        return {
            hostVoice: this.hostVoice,
            guestVoice: this.guestVoice
        };
    }
}
