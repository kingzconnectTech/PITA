/**
 * PITA State Management
 * Centralized store for the application state.
 */

export const State = {
    // Current application mode: 'assistant' or 'dashboard'
    mode: 'assistant',
    
    // Voice interaction status: 'idle', 'listening', 'processing', 'speaking'
    status: 'idle',
    
    // User information (placeholder)
    user: {
        name: 'User',
        preferences: {}
    },
    
    // Error tracking
    errors: [],
    
    // Connection state
    wsConnected: false,
    
    // Listeners for state changes
    listeners: [],

    /**
     * Update state and notify listeners
     * @param {Object} newState 
     */
    set(newState) {
        const oldState = { ...this };
        Object.assign(this, newState);
        
        console.log(`[State Update]`, newState);
        
        this.listeners.forEach(callback => callback(this, oldState));
    },

    /**
     * Add a listener for state changes
     * @param {Function} callback 
     */
    subscribe(callback) {
        this.listeners.push(callback);
        return () => {
            this.listeners = this.listeners.filter(l => l !== callback);
        };
    },

    /**
     * Convenience method to update status
     * @param {string} status 
     */
    setStatus(status) {
        this.set({ status });
    }
};
