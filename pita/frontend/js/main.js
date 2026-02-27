/**
 * PITA Main Entry Point
 * Initializes all modules and sets up the application.
 */

import { State } from './state.js';
import { AvatarRenderer } from './avatar.js';
import { VoiceUI } from './voice-ui.js';
import { Notification } from '../components/notification.js';
import { Loader } from '../components/loader.js';

class PitaApp {
    constructor() {
        console.log('--- PITA Assistant Initializing ---');
        
        this.loader = new Loader('loader-container');
        this.notification = new Notification('notification-container');
        this.avatar = null;
        this.voiceUI = null;
        
        this.init();
    }

    async init() {
        try {
            // 1. Show loader
            this.loader.show('Calibrating AI Core...');
            
            // 2. Initialize Avatar (Three.js)
            this.avatar = new AvatarRenderer('avatar-canvas');
            
            // 3. Initialize Voice UI
            this.voiceUI = new VoiceUI('mic-container');
            
            // 4. Bind Dashboard Toggle
            this.setupDashboardToggle();
            
            // 5. Hide loader after a brief delay
            setTimeout(() => {
                this.loader.hide();
                this.notification.show('PITA Online. Systems Nominal.', 'info');
                console.log('--- PITA Assistant Ready ---');
            }, 2000);

        } catch (error) {
            console.error('Initialization failed:', error);
            this.notification.show('Critical error during initialization.', 'error');
        }
    }

    setupDashboardToggle() {
        const toggleBtn = document.getElementById('dashboard-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                window.location.href = 'dashboard.html';
            });
        }
    }
}

// Start application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new PitaApp();
});
