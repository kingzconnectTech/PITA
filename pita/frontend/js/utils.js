/**
 * PITA Utility Functions
 */

/**
 * Format timestamp to readable time
 * @param {Date} date 
 * @returns {string}
 */
export const formatTime = (date = new Date()) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

/**
 * Delay execution for a specified duration
 * @param {number} ms 
 * @returns {Promise}
 */
export const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Generate a random ID
 * @returns {string}
 */
export const generateId = () => Math.random().toString(36).substr(2, 9);

/**
 * DOM query selector shorthand
 * @param {string} selector 
 * @returns {Element}
 */
export const $ = (selector) => document.querySelector(selector);

/**
 * DOM query selector all shorthand
 * @param {string} selector 
 * @returns {NodeList}
 */
export const $$ = (selector) => document.querySelectorAll(selector);
