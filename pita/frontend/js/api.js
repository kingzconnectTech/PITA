/**
 * PITA API Client
 * Handles communication with the Python backend.
 */

import { State } from './state.js';

const API_BASE_URL = 'http://localhost:8000/api';

export const Api = {
    /**
     * Send a text query to the backend
     * @param {string} text 
     * @returns {Promise<Object>}
     */
    async sendQuery(text) {
        console.log(`[API] Sending query: ${text}`);
        State.setStatus('processing');
        
        try {
            // Placeholder for real backend call
            // const response = await fetch(`${API_BASE_URL}/query`, {
            //     method: 'POST',
            //     headers: { 'Content-Type': 'application/json' },
            //     body: JSON.stringify({ query: text })
            // });
            // return await response.json();

            // Mock response
            return new Promise(resolve => {
                setTimeout(() => {
                    State.setStatus('speaking');
                    resolve({
                        text: "I've processed your request. How else can I help?",
                        action: null
                    });
                }, 1500);
            });
        } catch (error) {
            console.error('[API] Error sending query:', error);
            State.set({ errors: [...State.errors, error.message] });
            State.setStatus('idle');
            throw error;
        }
    },

    /**
     * Send audio blob to backend for transcription/processing
     * @param {Blob} audioBlob 
     */
    async sendAudio(audioBlob) {
        console.log(`[API] Sending audio data...`);
        State.setStatus('processing');
        
        // Placeholder for WebSocket or Multipart upload
        return new Promise(resolve => {
            setTimeout(() => {
                State.setStatus('speaking');
                resolve({ text: "I heard you clearly." });
            }, 1000);
        });
    }
};
