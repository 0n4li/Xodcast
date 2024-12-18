class AceViewer {
    constructor(options = {}) {
        this.options = {
            id: 'aceViewer',
            theme: 'ace/theme/dawn',
            mode: 'ace/mode/json',
            selectionStyle: 'text',
            showPrintMargin: false,
            showGutter: true,
            showInvisibles: false,
            showLineNumbers: true,
            readOnly: false,
            ...options, // Allow overriding default options
        };

        this.editor = null; // Will hold the CodeMirror instance
    }

    render() {
        // Create the Ace instance
        this.editor = ace.edit(this.options.id);
        this.editor.setTheme(this.options.theme);
        this.editor.session.setMode(this.options.mode);
        this.editor.setOptions(this.options);
        var beautify = ace.require("ace/ext/beautify"); // Use the correct path
        if (beautify) {
            console.log("Beautify extension loaded.");
        }
        var mode = ace.require(this.options.mode); // Use the correct path, e.g., "ace/mode/json");
        if (mode) {
            console.log(`${this.options.mode} mode loaded.`);
        }
        this.editor.resize();
    }

    setValue(jsonString) {
        if (this.editor) {
            this.editor.setValue(jsonString, -1);
        }
    }

    getValue() {
        if (this.editor) {
            return this.editor.getValue();
        }
        return null;
    }

    setTheme(theme) {
        if (this.editor) {
            this.editor.setTheme(theme);
        }
    }

    setMode(mode) {
        if (this.editor) {
            this.editor.session.setMode(mode);
        }
    }

    setReadOnly(readOnly) {
        if (this.editor) {
            this.editor.setReadOnly(readOnly);
        }
    }

    // Add more methods as needed (e.g., for theming, events, etc.)
}