class LoadingIndicator {
    constructor(options) {
        this.options = {
            id: 'loadingIndicator',
            message: 'Loading...',
            ...options
        };
        this.component = document.getElementById(this.options.id);
    }

    render() {
        this.component.innerHTML = `
            <div class="flex-1 flex flex-col items-center justify-center text-center w-full h-full">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p class="mt-4 text-lg">${this.options.message}</p>
            </div>
        `;
    }

    show() {
        this.component.classList.remove('hidden');
    }

    hide() {
        this.component.classList.add('hidden');
    }

    getElement() {
        return this.component;
    }

}