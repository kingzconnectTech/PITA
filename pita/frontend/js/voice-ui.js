/**
 * PITA Voice Interaction UI
 * Controls mic states and interaction animations.
 */

import { State } from './state.js';
import { Api } from './api.js';
import { wsClient } from './websocket.js';

export class VoiceUI {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error(`[VoiceUI] Container with ID "${containerId}" not found.`);
            return;
        }

        this.micButton = null;
        this.micMeter = null;
        this.statusDot = document.getElementById('status-indicator')?.querySelector('.status-dot');
        this.statusText = document.getElementById('status-indicator')?.querySelector('.status-text');
        this.responseText = document.getElementById('response-text');

        this.init();
        this.setupStateListener();
        this.setupWebSocketListener();
    }

    /**
     * Initialize Voice UI elements
     */
    init() {
        console.log('[VoiceUI] Initializing voice interface...');
        
        // Add the mic button to the container
        this.micButton = document.createElement('button');
        this.micButton.className = 'mic-btn';
        this.micButton.innerHTML = `<img src="assets/icons/mic.svg" alt="Mic" onerror="this.src='https://api.iconify.design/material-symbols:mic-rounded.svg?color=white'">`;
        
        // Add Mic Level Meter
        this.micMeter = document.createElement('div');
        this.micMeter.className = 'mic-level-meter';
        this.micMeter.innerHTML = `
            <div class="meter-bar">
                <div class="meter-fill"></div>
            </div>
            <span class="meter-label">MIC</span>
        `;

        this.container.appendChild(this.micButton);
        this.container.appendChild(this.micMeter);

        // Mic Click Event
        this.micButton.addEventListener('click', () => {
            if (State.status === 'idle') {
                this.startListening();
            } else {
                this.stopListening();
            }
        });
    }

    /**
     * Listen for real-time mic levels and state changes from WebSocket
     */
    setupWebSocketListener() {
        wsClient.addListener((data) => {
            // 1. Update Mic Meter
            if (data.type === 'mic_level') {
                this.updateMicMeter(data.value);
            }

            // 2. Sync Global State with Backend
            // We only sync if the backend is NOT in idle (meaning it's actively processing or listening)
            // or if we are currently idle and the backend detects speech.
            if (data.state && data.state !== State.status) {
                console.log(`[VoiceUI] WS Message State: ${data.state} | Current Local State: ${State.status}`);
                State.set({ status: data.state });
            }
        });
    }

    /**
     * Update the visual meter based on RMS value
     * @param {number} rms 
     */
    updateMicMeter(rms) {
        if (!this.micMeter) return;
        
        const fill = this.micMeter.querySelector('.meter-fill');
        if (!fill) return;

        // Map RMS to percentage. RMS 0-200 mapped to 0-100%
        // Using a non-linear mapping (sqrt) to make small sounds more visible
        const maxRms = 200;
        let percentage = Math.min(Math.sqrt(rms / maxRms) * 100, 100);
        
        // Ensure at least a tiny bit is visible if there's any sound
        if (rms > 2 && percentage < 5) percentage = 5;

        fill.style.height = `${percentage}%`;

        // Color coding: Green -> Orange -> Purple/Red
        if (percentage < 60) {
            fill.style.backgroundColor = '#00ff88'; // Green (Listening)
        } else if (percentage < 85) {
            fill.style.backgroundColor = '#ff8800'; // Orange (Processing)
        } else {
            fill.style.backgroundColor = '#7000ff'; // Purple (Speaking/Loud)
        }
    }

    /**
     * Listen for global state changes to update UI
     */
    setupStateListener() {
        State.subscribe((newState, oldState) => {
            if (newState.status !== oldState.status) {
                this.updateUIStatus(newState.status);
            }
        });
    }

    /**
     * Start "listening" mode
     */
    startListening() {
        console.log('[VoiceUI] Microphone activated...');
        State.set({ status: 'listening' });
        // Inform backend if needed, but for now we prioritize local UI feedback
    }

    /**
     * Stop "listening" mode
     */
    stopListening() {
        console.log('[VoiceUI] Microphone deactivated.');
        State.set({ status: 'processing' });
    }

    /**
     * Send simulated query to API
     */
    async processInput() {
        try {
            const response = await Api.sendQuery("Simulated voice input...");
            this.showResponse(response.text);
            
            // Revert to idle after 5 seconds of "speaking"
            setTimeout(() => {
                State.setStatus('idle');
                this.hideResponse();
            }, 5000);
        } catch (error) {
            console.error('[VoiceUI] Error processing input:', error);
            State.setStatus('idle');
        }
    }

    /**
     * Show the text response from PITA
     * @param {string} text 
     */
    showResponse(text) {
        if (this.responseText) {
            this.responseText.querySelector('p').textContent = text;
            this.responseText.classList.remove('hidden');
        }
    }

    /**
     * Hide the text response
     */
    hideResponse() {
        if (this.responseText) {
            this.responseText.classList.add('hidden');
        }
    }

    /**
     * Update visual UI elements based on current status
     * @param {string} status 
     */
    updateUIStatus(status) {
        // Update Indicator
        if (this.statusDot && this.statusText) {
            this.statusText.textContent = status.charAt(0).toUpperCase() + status.slice(1);
            
            // Update color via CSS variables or class
            const colors = {
                'idle': '#00f2ff',      // Blue
                'listening': '#00ff88',  // Green
                'processing': '#ff8800', // Orange
                'speaking': '#7000ff'    // Purple
            };
            this.statusDot.style.backgroundColor = colors[status] || colors.idle;
            this.statusDot.style.boxShadow = `0 0 10px ${colors[status] || colors.idle}`;
        }

        // Update Mic Button
        if (this.micButton) {
            if (status === 'listening') {
                this.micButton.classList.add('active', 'animate-listening');
            } else {
                this.micButton.classList.remove('active', 'animate-listening');
            }
        }
    }
}
