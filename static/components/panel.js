class Panel {
    constructor(options) {
        this.options = {
            id: 'panel', // ID of the panel container (required)
            ...options
        };

        this.panelContainer = document.getElementById(this.options.id);
        this.slots = {};

        this.extractSlots();
    }

    extractSlots() {
        // Create a copy of the children to avoid modifying the original HTMLCollection
        const children = Array.from(this.panelContainer.children);

        for (let i = 0; i < children.length; i++) {
            const child = children[i];
            const slotName = child.dataset.slot;

            if (slotName) {
                this.slots[slotName] = child.cloneNode(true); // Clone the node
                // Remove the original node to avoid recursion when rendering
                this.panelContainer.removeChild(child); 
            }
        }
    }

    render() {
        // Left View
        this.leftView = document.createElement('div');
        this.leftView.className = 'flex-1 flex flex-col';
        this.renderSlots('left', this.leftView);

        // Right View
        this.rightView = document.createElement('div');
        this.rightView.className = 'flex-1 flex flex-col';
        this.renderSlots('right', this.rightView);

        const flexContainer = document.createElement('div');
        flexContainer.className = 'flex h-full gap-4';

        flexContainer.appendChild(this.leftView);
        flexContainer.appendChild(this.rightView);

        this.panelContainer.innerHTML = ''; // Clear previous content
        this.panelContainer.className = 'panel h-full'; // Add Tailwind CSS classes
        this.panelContainer.appendChild(flexContainer);
    }

    renderSlots(view, container) {
        let slot = this.slots[view];
        if (slot) {
            let panelComponent = new PanelComponent(slot);
            panelComponent.render();
            container.appendChild(panelComponent.getComponent()); // Append the rendered component
        }
    }
}

class PanelComponent {
    constructor(slotView) {
        this.slotView = slotView;
        this.slots = {};
        this.isRendered = false; // Flag to prevent re-rendering
        this.component = document.createElement('div'); // Container for the rendered component
        this.extractSlots();
    }

    extractSlots() {
        const children = Array.from(this.slotView.children); 
        
        for (let i = 0; i < children.length; i++) {
            const child = children[i];
            const slotName = child.dataset.slot;

            if (slotName) {
                this.slots[slotName] = child.cloneNode(true); // Clone the node
            }
        }
    }

    render() {
        this.header = document.createElement('div');
        this.header.className = 'flex justify-between items-center mb-4';

        if (this.slots.title) {
            let titleElement = document.createElement('h1');
            titleElement.className = 'text-3xl font-bold text-gray-800';
            titleElement.textContent = this.slots.title.textContent;
            this.header.appendChild(titleElement);
            this.slots.title.remove(); // remove the element after using its content
        } else {
            let placeholder = document.createElement('p');
            placeholder.className = 'text-gray-600';
            placeholder.textContent = '_';
            this.header.appendChild(placeholder);
        }

        if (this.slots.actions) {
            this.header.appendChild(this.slots.actions);
        }

        this.card = document.createElement('div');
        this.card.className = 'flex-1 bg-white h-full rounded-lg shadow-lg p-6 flex flex-col overflow-hidden';

        if (this.slots.content) {
            this.card.appendChild(this.slots.content);
        } else {
            let placeholder = document.createElement('p');
            placeholder.className = 'text-gray-600';
            placeholder.textContent = 'No content available';
            this.card.appendChild(placeholder);
        }
        
        if (this.slots.footer) {
            this.slots.footer.className = 'mt-auto';
            this.card.appendChild(this.slots.footer);
        }
        
        this.component.className = 'flex-1 flex flex-col h-full';
        this.component.appendChild(this.header);
        this.component.appendChild(this.card);
    }

    getComponent() {
        return this.component;
    }
}