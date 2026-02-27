/**
 * PITA Loader Component
 */

export class Loader {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.warn(`[Loader] Container with ID "${containerId}" not found.`);
            return;
        }

        this.loaderEl = null;
        this.init();
    }

    init() {
        this.loaderEl = document.createElement('div');
        this.loaderEl.id = 'pita-loader';
        this.loaderEl.style.cssText = `
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: #0a0a0f;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            z-index: 9999;
            transition: opacity 0.5s ease;
        `;

        this.loaderEl.innerHTML = `
            <div class="spinner" style="
                width: 60px; height: 60px;
                border: 4px solid rgba(0, 242, 255, 0.1);
                border-top: 4px solid #00f2ff;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            "></div>
            <p id="loader-text" style="
                margin-top: 20px; color: #00f2ff;
                font-family: monospace; letter-spacing: 2px;
            ">Initializing...</p>
            <style>
                @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            </style>
        `;

        this.container.appendChild(this.loaderEl);
    }

    show(text = 'Initializing...') {
        if (this.loaderEl) {
            this.loaderEl.style.display = 'flex';
            this.loaderEl.style.opacity = '1';
            const textEl = this.loaderEl.querySelector('#loader-text');
            if (textEl) textEl.textContent = text;
        }
    }

    hide() {
        if (this.loaderEl) {
            this.loaderEl.style.opacity = '0';
            setTimeout(() => {
                this.loaderEl.style.display = 'none';
            }, 500);
        }
    }
}
