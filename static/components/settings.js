class SettingsComponent {
    constructor(options) {
        this.options = {
            id: 'settingsComponent',
            config: {
                fields: []
            },
            onChange: null,
            ...options
        };
        this.settings = {}; // Initialize settings as an empty object
        this.container = document.getElementById(this.options.id);
    }

    render() {
        this.container.innerHTML = '';
        const form = document.createElement('form');
        form.className = 'p-4 bg-white rounded shadow-md relative';
        const title = document.createElement('h3');
        title.className = 'text-lg font-bold mb-2';
        title.textContent = 'Settings';
        form.appendChild(title);

        // Add close button
        const closeButton = document.createElement('button');
        closeButton.className = 'absolute top-2 right-2 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded';
        closeButton.textContent = 'Close';
        closeButton.addEventListener('click', (e) => {
            e.preventDefault();
            this.hide()
        });
        form.appendChild(closeButton);

        // Create a map to store created elements
        const elementMap = new Map();

        this.options.config.fields.forEach(field => {
            const div = document.createElement('div');
            div.className = 'mb-2';
            const label = document.createElement('label');
            label.htmlFor = field.id;
            label.textContent = field.label + ':';
            div.appendChild(label);

            let input;
            switch (field.type) {
                case 'text':
                    input = document.createElement('input');
                    input.type = 'text';
                    input.value = field.defaultValue || '';
                    break;
                case 'select':
                    input = document.createElement('select');
                    field.options.forEach(option => {
                        const optionElement = document.createElement('option');
                        optionElement.value = option.value;
                        optionElement.text = option.text;
                        input.appendChild(optionElement);
                    });
                    input.value = field.defaultValue || '';
                    break;
                case 'range':
                    input = document.createElement('input');
                    input.type = 'range';
                    input.min = field.min;
                    input.max = field.max;
                    input.value = field.defaultValue || '';
                    break;
                case 'custom':
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
                    break;
                default:
                    console.error('Unsupported field type:', field.type);
                    return;
            }
            input.id = field.id;
            input.className = 'w-full px-3 py-1 border rounded';

            if (field.readonly) {
                input.disabled = true;
            }

            if (field.type !== 'custom') {
                input.addEventListener('change', () => {
                    this.settings[field.id] = input.value;
                    if (typeof this.options.onChange === 'function') {
                        this.options.onChange(this.settings);
                    }
                });
            }

            div.appendChild(input);
            form.appendChild(div);

            // Store the created element in the map
            elementMap.set(field.id, input);
        });

        this.container.appendChild(form);

        // Call onRender for custom fields after the form is added to the container
        this.options.config.fields.forEach(field => {
            if (field.type === 'custom' && typeof field.onRender === 'function') {
                const element = elementMap.get(field.id);
                if (element) {
                    field.onRender(element, this);
                }
            }
        });
    }

    getSettings() {
        return this.settings;
    }

    setSettings(newSettings) {
        this.settings = { ...newSettings };
        for (let key in this.settings) {
            let element = document.getElementById(key);
            if (element) {
                element.value = this.settings[key];
            }
        }
    }

    show() {
        this.container.classList.remove('hidden');
    }

    hide() {
        this.container.classList.add('hidden');
    }
}
