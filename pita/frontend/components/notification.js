/**
 * PITA Notification Component
 */

export class Notification {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.warn(`[Notification] Container with ID "${containerId}" not found.`);
            return;
        }

        this.notificationEl = null;
        this.init();
    }

    init() {
        this.notificationEl = document.createElement('div');
        this.notificationEl.id = 'pita-notification';
        this.notificationEl.style.cssText = `
            position: fixed;
            bottom: 20px; right: 20px;
            padding: 1rem 2rem;
            background: rgba(0, 242, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 242, 255, 0.3);
            border-radius: 8px;
            color: #fff;
            font-size: 0.9rem;
            z-index: 1000;
            transform: translateX(120%);
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
        `;

        this.container.appendChild(this.notificationEl);
    }

    show(message, type = 'info', duration = 3000) {
        if (!this.notificationEl) return;

        this.notificationEl.textContent = message;
        
        // Update color based on type
        const colors = {
            'info': 'rgba(0, 242, 255, 0.3)',
            'error': 'rgba(255, 0, 85, 0.3)',
            'warning': 'rgba(255, 204, 0, 0.3)'
        };
        this.notificationEl.style.borderColor = colors[type] || colors.info;
        
        // Show
        this.notificationEl.style.transform = 'translateX(0)';

        // Hide after duration
        setTimeout(() => {
            this.hide();
        }, duration);
    }

    hide() {
        if (this.notificationEl) {
            this.notificationEl.style.transform = 'translateX(120%)';
        }
    }
}
