class SettingsComponent {
    constructor(options) {
        this.options = {
            id: 'settingsComponent',
            config: {
                fields: []
            },
            onChange: null,
            onClose: null,
            ...options
        };
        this.settings = {};
        this.container = document.getElementById(this.options.id);
        this.initializeSettings();
        window.addEventListener('resize', this.adjustHeight.bind(this));
    }

    adjustHeight() {
        const form = this.container.querySelector('form');
        const title = this.container.querySelector('h3');
        const closeButton = this.container.querySelector('.top-2');
        let otherElementsHeight = 0;
        if (title) {
            otherElementsHeight += title.offsetHeight;
        }
        if (closeButton) {
            otherElementsHeight += closeButton.offsetHeight;
        }
        const maxHeight = window.innerHeight - otherElementsHeight - 20; // 20px margin
        form.style.maxHeight = `${maxHeight}px`;
        form.style.overflowY = 'auto';
    }

    initializeSettings() {
        this.options.config.fields.forEach(field => {
            this.settings[field.id] = field.defaultValue;
        });
    }

    render() {
        this.container.innerHTML = '';
        const form = document.createElement('form');
        form.className = 'bg-white rounded-lg shadow-xl max-w-md w-full relative'; // Added 'relative' for absolute positioning inside

        // Create a header div for title and close button
        const headerDiv = document.createElement('div');
        headerDiv.className = 'flex items-center justify-between sticky px-8 pt-4 top-0 bg-white z-10';

        const title = document.createElement('h3');
        title.className = 'text-xl font-bold text-gray-800';
        title.textContent = 'Settings';
        headerDiv.appendChild(title);

        // Add close button
        const closeButton = document.createElement('button');
        closeButton.type = 'button';
        closeButton.className = 'bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-lg focus:outline-none focus:shadow-outline';
        closeButton.textContent = 'Close';
        closeButton.addEventListener('click', () => {
            this.hide();
            if (typeof this.options.onClose === 'function') {
                this.options.onClose(this.getSettings());
            }
        });
        headerDiv.appendChild(closeButton);

        // Append the header div to the form
        form.appendChild(headerDiv);

        // Add a submit listener to prevent default form submission
        form.addEventListener('submit', (event) => {
            event.preventDefault();
        });

        // Create a container for the form fields
        const fieldsContainer = document.createElement('div');
        fieldsContainer.className = 'overflow-y-auto px-8 py-4';

        // Create a map to store created elements
        const elementMap = new Map();

        this.options.config.fields.forEach(field => {
            const div = document.createElement('div');
            div.className = 'mb-4';
            const label = document.createElement('label');
            label.className = 'block text-gray-700 text-sm font-bold mb-2';
            label.htmlFor = field.id;
            label.textContent = field.label + ':';
            div.appendChild(label);

            let input;
            if (field.type === 'checkbox') {
                input = document.createElement('input');
                input.type = 'checkbox';
                input.className = 'form-checkbox h-5 w-5 text-blue-600';
                input.checked = field.defaultValue || false;
            } else if (field.type === 'number') {
                input = document.createElement('input');
                input.type = 'number';
                input.className = 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline';
                input.min = field.min || 0;
                input.max = field.max || 99;
                input.value = field.defaultValue || 0;
            } else if (field.type === 'text') {
                input = document.createElement('input');
                input.type = 'text';
                input.className = 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline';
                input.value = field.defaultValue || '';
            } else if (field.type === 'select') {
                input = document.createElement('select');
                input.className = 'block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline';
                field.options.forEach(option => {
                    const optionElement = document.createElement('option');
                    optionElement.value = option.value;
                    optionElement.text = option.text;
                    input.appendChild(optionElement);
                });
                input.value = field.defaultValue || '';
            } else if (field.type === 'range') {
                input = document.createElement('input');
                input.type = 'range';
                input.className = 'w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer';
                input.min = field.min;
                input.max = field.max;
                input.value = field.defaultValue || '';
            } else if (field.type === 'custom') {
                input = document.createElement(field.tag);
                for (const attr in field.attributes) {
                    input.setAttribute(attr, field.attributes[attr]);
                }
                if (field.text) {
                    input.textContent = field.text;
                }
                if (field.events) {
                    for (const event in field.events) {
                        input.addEventListener(event, field.events[event]);
                    }
                }
            } else {
                console.error('Unsupported field type:', field.type);
                return;
            }
            input.id = field.id;

            if (field.readonly) {
                input.disabled = true;
            }

            if (field.type !== 'custom') {
                input.addEventListener('change', () => {
                    this.settings[field.id] = field.type === 'checkbox' ? input.checked : input.value;
                    if (typeof this.options.onChange === 'function') {
                        this.options.onChange(this.settings);
                    }
                });
            }

            div.appendChild(input);
            fieldsContainer.appendChild(div); // Append to the fields container

            // Store the created element in the map
            elementMap.set(field.id, input);
        });

        // Append the fields container to the form
        form.appendChild(fieldsContainer);

        this.container.appendChild(form);

        // Call onRender for custom fields after the form is added to the container
        this.options.config.fields.forEach(field => {
            if (field.type === 'custom' && typeof field.onRender === 'function') {
                const element = elementMap.get(field.id);
                if (element) {
                    field.onRender(element, this, field.defaultValue);
                }
            }
        });
    }

    getSettings() {
        return this.settings;
    }

    setSettings(newSettings) {
        // Merge default settings with the loaded settings
        this.options.config.fields.forEach(field => {
            if (field.type !== 'custom' && !(field.id in newSettings)) {
                newSettings[field.id] = field.defaultValue;
            }
        });

        this.settings = { ...newSettings };
        for (let key in this.settings) {
            let element = document.getElementById(key);
            if (element) {
                const field = this.options.config.fields.find(f => f.id === key);
                if (field && field.type === 'number') {
                    this.settings[key] = Number(this.settings[key]);
                    element.value = this.settings[key];
                } else {
                    element.value = this.settings[key];
                }
            }
        }
    }

    show() {
        this.container.classList.remove('hidden');
        setTimeout(() => {
            this.adjustHeight();
        }, 0);
    }

    hide() {
        this.container.classList.add('hidden');
    }
}
