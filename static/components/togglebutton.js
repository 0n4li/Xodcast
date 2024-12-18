class ToggleButton {
    constructor(options) {
        this.options = {
            id: 'toggle',
            initialState: false,
            onLabel: 'ON',
            offLabel: 'OFF',
            onChange: null,
            ...options
        };
        this.container = document.getElementById(this.options.id);
        this.state = this.options.initialState;
    }

    render() {
        this.container.innerHTML = '';

        const wrapper = document.createElement('div');
        wrapper.className = 'flex items-center cursor-pointer';

        const offLabel = document.createElement('span');
        offLabel.className = 'text-sm font-medium text-gray-900 dark:text-gray-300';
        offLabel.textContent = this.options.offLabel;
        wrapper.appendChild(offLabel);

        const label = document.createElement('label');
        label.className = 'relative inline-flex items-center mx-4'; // Use mx-4 for spacing
        wrapper.appendChild(label);

        const input = document.createElement('input');
        input.type = 'checkbox';
        input.className = 'sr-only peer';
        input.checked = this.state;
        label.appendChild(input);

        const slider = document.createElement('div');
        slider.className = 'w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[\'\'] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600';
        label.appendChild(slider);

        const onLabel = document.createElement('span');
        onLabel.className = 'text-sm font-medium text-gray-900 dark:text-gray-300';
        onLabel.textContent = this.options.onLabel;
        wrapper.appendChild(onLabel);

        this.container.appendChild(wrapper);

        // Event listener
        input.addEventListener('change', () => {
            this.state = input.checked;
            if (typeof this.options.onChange === 'function') {
                this.options.onChange(this.options.id, this.state);
            }
        });
    }

    getState() {
        return this.state;
    }

    setState(newState) {
        this.state = newState;
        this.render();
    }
}