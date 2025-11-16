/**
 * Color-code profit/loss values in the portfolio table.
 * Adds 'g' class for positive values (green) and 'r' class for negative values (red).
 */
(function() {
    'use strict';
    
    const numElements = document.getElementsByClassName('num');
    
    for (let i = 0; i < numElements.length; i++) {
        const element = numElements[i];
        const text = element.innerHTML || element.textContent || '';
        
        // Match numbers (including negative) in the text
        const matches = text.match(/(-?\d+\.?\d*)/g);
        
        if (matches && matches.length > 0) {
            try {
                const value = parseFloat(matches[0]);
                
                if (!isNaN(value)) {
                    if (value > 0) {
                        element.classList.add('g');
                    } else if (value < 0) {
                        element.classList.add('r');
                    }
                }
            } catch (e) {
                // Silently skip elements that can't be parsed
                console.debug('Could not parse value for element:', e);
            }
        }
    }
})();
