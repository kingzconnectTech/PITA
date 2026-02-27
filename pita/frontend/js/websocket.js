/**
 * PITA WebSocket Client
 * Manages real-time connection with the backend.
 */

import { State } from './state.js';

class WebSocketClient {
    constructor(url = 'ws://127.0.0.1:8005') {
        this.url = url;
        this.socket = null;
        this.listeners = new Set();
        this.reconnectInterval = 3000;
        this.connect();
    }

    connect() {
        console.log(`[WS] Connecting to ${this.url}...`);
        this.socket = new WebSocket(this.url);

        this.socket.onopen = () => {
            console.log('%c[WS] Connected to PITA Backend', 'color: #00ff88; font-weight: bold;');
            State.set({ wsConnected: true });
        };

        this.socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                if (data.type !== 'mic_level') {
                    console.log('[WS] Received:', data);
                }
                this.notifyListeners(data);
            } catch (error) {
                console.error('[WS] Error parsing message:', error);
            }
        };

        this.socket.onclose = () => {
            console.warn('[WS] Connection closed. Retrying in 3s...');
            State.set({ wsConnected: false });
            setTimeout(() => this.connect(), this.reconnectInterval);
        };

        this.socket.onerror = (error) => {
            console.error('[WS] WebSocket error:', error);
            this.socket.close();
        };
    }

    send(data) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify(data));
        } else {
            console.error('[WS] Cannot send: Socket not open.');
        }
    }

    addListener(callback) {
        this.listeners.add(callback);
    }

    removeListener(callback) {
        this.listeners.delete(callback);
    }

    notifyListeners(data) {
        this.listeners.forEach(callback => callback(data));
    }
}

export const wsClient = new WebSocketClient();
