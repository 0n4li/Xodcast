class JsonViewer {
    constructor(options) {
        this.options = {
            id: 'json-viewer',
            ...options
        };
        this.container = document.getElementById(this.options.id);
        this.mode = 'visual';
        this.visualView = null;
        this.jsonView = null;
        this.aceJsonViewer = null;
        this.setJson('{}');
        this.initialized = false;
    }

    render() {
        this.container.innerHTML = '';

        this.errorDiv = document.createElement('div');
        this.errorDiv.className = 'text-red-500 hidden';
        this.errorDiv.textContent = '';
        this.container.appendChild(this.errorDiv);

        this.visualView = document.createElement('div');
        this.visualView.className = 'visual-view overflow-y-auto relative'; 
        this.container.appendChild(this.visualView);

        this.jsonView = document.createElement('div');
        this.jsonView.id = `${this.options.id}-json-view-ace`;
        this.jsonView.className = 'json-view hidden w-full px-3 py-2 border border-gray-300 rounded-md resize-none font-mono';
        this.container.appendChild(this.jsonView);
        this.aceJsonViewer = new AceViewer({
            id: this.jsonView.id,
            readOnly: false,
            value: this.getJson(),
            onChange: (jsonString) => {
                this.setJson(jsonString);
            },
        });
        this.aceJsonViewer.render();

        this.initialized = true;
        this.renderContent();
    }

    switchMode(mode) {
        this.mode = mode;
        if (this.initialized) {
            this.renderContent();
        }
    }

    renderContent() {
        if (this.mode === 'visual') {
            this.visualView.classList.remove('hidden');
            this.visualView.classList.add('flex-1');
            this.jsonView.classList.add('hidden');
            this.jsonView.classList.remove('flex-1');
            this.renderVisualView();
        } else {
            this.jsonView.classList.remove('hidden');
            this.jsonView.classList.add('flex-1');
            this.visualView.classList.add('hidden');
            this.visualView.classList.remove('flex-1');
            this.renderJsonView();
        }
    }

    renderVisualView() {
        this.visualView.innerHTML = '';
        this.errorDiv.classList.add('hidden');

        if (this.isValidJson(this.data)) {
            const fragment = document.createDocumentFragment();

            const titleDiv = document.createElement('div');
            titleDiv.className = 'bg-gray-50 p-4 rounded-lg mb-4 relative';
            const titleH3 = document.createElement('h3');
            titleH3.className = 'font-bold text-lg mb-2';
            titleH3.contentEditable = 'true';
            titleH3.textContent = this.data.title;
            titleDiv.appendChild(titleH3);

            const hostDiv = document.createElement('div');
            hostDiv.className = 'flex items-center relative';
            const hostP1 = document.createElement('p');
            hostP1.className = 'text-sm text-gray-600 font-bold mr-2';
            hostP1.textContent = 'Host:';
            const hostP2 = document.createElement('p');
            hostP2.className = 'text-sm text-gray-600';
            hostP2.contentEditable = 'true';
            hostP2.textContent = this.data.host_name;
            hostDiv.appendChild(hostP1);
            hostDiv.appendChild(hostP2);

            const guestDiv = document.createElement('div');
            guestDiv.className = 'flex items-center relative';
            const guestP1 = document.createElement('p');
            guestP1.className = 'text-sm text-gray-600 font-bold mr-2';
            guestP1.textContent = 'Guest:';
            const guestP2 = document.createElement('p');
            guestP2.className = 'text-sm text-gray-600';
            guestP2.contentEditable = 'true';
            guestP2.textContent = this.data.guest_name;
            guestDiv.appendChild(guestP1);
            guestDiv.appendChild(guestP2);

            const titleDivInner = document.createElement('div');
            titleDivInner.className = 'flex justify-between items-center';
            titleDivInner.style.marginTop = '10px';
            titleDivInner.appendChild(hostDiv);
            titleDivInner.appendChild(guestDiv);
            titleDiv.appendChild(titleDivInner);

            fragment.appendChild(titleDiv);

            const conversationDiv = document.createElement('div');
            conversationDiv.className = 'flex flex-col';
            fragment.appendChild(conversationDiv);

            this.data.conversation.forEach((entry, index) => {
                const messageDiv = document.createElement('div');
                messageDiv.className = 'p-3 rounded-lg mb-2 relative ' + (entry.speaker === 'Host' ? 'bg-blue-50' : 'bg-green-50');
                const speakerDiv = document.createElement('div');
                speakerDiv.className = 'font-semibold';
                speakerDiv.textContent = entry.speaker;
                const messageTextDiv = document.createElement('div');
                messageTextDiv.className = 'message-text';
                messageTextDiv.contentEditable = 'true';
                messageTextDiv.textContent = entry.text;
                const deleteButton = document.createElement('button');
                deleteButton.className = 'delete-button absolute top-2 right-2 bg-red-300 hover:bg-red-500 text-white font-bold pb-1 px-2 rounded-full';
                deleteButton.textContent = 'x';
                deleteButton.style.fontSize = '0.8em'; // Reduced font size
                deleteButton.style.padding = '0.2em 0.5em'; // Added padding
                deleteButton.onclick = () => this.deleteMessage(index);
                messageDiv.appendChild(speakerDiv);
                messageDiv.appendChild(messageTextDiv);
                messageDiv.appendChild(deleteButton);
                this.createAddButtons(messageDiv, index);
                conversationDiv.appendChild(messageDiv);
            });

            this.visualView.appendChild(fragment);

        } else {
            if (this.getJson() === '{}') {
                this.setError('');
            } else {
                this.setError('Invalid JSON data.');
            }
            this.switchMode('json');
        }
    }

    createAddButtons(element, index = null) {
        const addButtonContainerAbove = this.createButtonSet(index, true);
        const addButtonContainerBelow = this.createButtonSet(index, false);
        element.appendChild(addButtonContainerAbove);
        element.appendChild(addButtonContainerBelow);

        element.addEventListener('mouseover', () => {
            addButtonContainerAbove.style.display = 'block';
            addButtonContainerBelow.style.display = 'block';
        });
        element.addEventListener('mouseout', () => {
            addButtonContainerAbove.style.display = 'none';
            addButtonContainerBelow.style.display = 'none';
        });

    }

    createButtonSet(index, above) {
        const addButtonContainer = document.createElement('div');
        addButtonContainer.className = 'add-button-container relative w-full z-50';
        addButtonContainer.innerHTML = `
            <div class="add-button-wrapper w-full flex justify-center gap-2">
                <button class="add-button btn rounded-full add-host w-200 bg-blue-300 hover:bg-blue-700 text-white font-bold py-1 px-2 rounded flex items-center">
                    <span class="material-icons-outlined mr-1">+ Host</span>
                </button>
                <button class="add-button btn rounded-full add-guest w-200 bg-green-300 hover:bg-green-700 text-white font-bold py-1 px-2 rounded flex items-center">
                    <span class="material-icons-outlined mr-1">+ Guest</span>
                </button>
            </div>
        `;
        const addHostButton = addButtonContainer.querySelector('.add-host');
        const addGuestButton = addButtonContainer.querySelector('.add-guest');

        addHostButton.onclick = () => this.addSection('Host', index, above);
        addGuestButton.onclick = () => this.addSection('Guest', index, above);

        addButtonContainer.style.position = 'absolute';
        addButtonContainer.style.transform = 'translateY(-40%)';
        addButtonContainer.style.display = 'none';
        if (above) {
            addButtonContainer.style.top = '-8px'; 
        } else {
            addButtonContainer.style.bottom = '-32px'; 
        }
        return addButtonContainer;
    }

    addSection(speaker, index = null, above = false) {
        const newSection = { speaker: speaker, text: '' };
        if (index === null) {
            this.data.conversation.push(newSection);
        } else {
            if (above) {
                this.data.conversation.splice(index, 0, newSection);
            } else {
                this.data.conversation.splice(index + 1, 0, newSection);
            }
        }
        this.renderContent();
    }

    deleteMessage(index) {
        this.data.conversation.splice(index, 1);
        this.renderContent();
    }

    isValidJson(data) {
        if (!data) {
            data = this.data;
        }

        if (typeof data !== 'object' || data === null) {
            return false;
        }

        if (
            typeof data.title !== 'string' ||
            typeof data.host_name !== 'string' ||
            typeof data.guest_name !== 'string' ||
            !Array.isArray(data.conversation)
        ) {
            return false;
        }

        for (const entry of data.conversation) {
            if (
                typeof entry !== 'object' ||
                typeof entry.speaker !== 'string' ||
                typeof entry.text !== 'string'
            ) {
                return false;
            }
        }

        return true;
    }

    renderJsonView() {
        this.aceJsonViewer.setValue(this.getJson());
    }

    setJson(jsonString) {
        try {
            this.data = JSON.parse(jsonString);
            this.switchMode(this.mode);
        } catch (error) {
            this.setError('Invalid JSON');
        }
    }

    getJson() {
        return JSON.stringify(this.data, null, 2);
    }

    hide() {
        this.container.classList.add('hidden');
    }

    show() {
        this.container.classList.remove('hidden');
    }

    setError(error) {
        this.errorDiv.textContent = error;
        this.errorDiv.classList.remove('hidden');
    }

    clearError() {
        this.errorDiv.textContent = '';
        this.errorDiv.classList.add('hidden');
    }

    clear() {
        this.data = {};
        this.clearError();
        this.switchMode(this.mode);
    }
}
