/**
 * PITA Microphone Button Component
 * (Optional: Used for more complex mic UI logic)
 */

export class MicrophoneButton {
    static create() {
        const btn = document.createElement('button');
        btn.className = 'mic-btn';
        btn.innerHTML = `
            <img src="assets/icons/mic.svg" alt="Mic" onerror="this.src='https://api.iconify.design/material-symbols:mic-rounded.svg?color=white'">
        `;
        return btn;
    }
}
