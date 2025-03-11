// API utility functions for teacher-portfolio
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000'  // For local development
    : '/api';  // For Docker deployment - will be proxied through nginx

// Function to fetch prices from the backend
async function fetchPrices() {
    try {
        const response = await fetch(`${API_BASE_URL}/prices/`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const prices = await response.json();
        return prices;
    } catch (error) {
        console.error('Error fetching prices:', error);
        return [];
    }
}

// Function to update the pricing cards with data from the backend
async function updatePricingCards() {
    try {
        const prices = await fetchPrices();
        
        if (prices.length === 0) {
            console.warn('No pricing data available');
            return;
        }
        
        const pricingCardContainer = document.querySelector('.pricing-card-container');
        
        // Clear existing cards
        pricingCardContainer.innerHTML = '';
        
        // Create a card for each price level
        prices.forEach(price => {
            // Map difficulty levels to readable names
            const difficultyMap = {
                '1': 'רמה בסיסית',
                '2': 'רמה בינונית',
                '3': 'רמה מתקדמת'
            };
            
            const difficultyName = difficultyMap[price.difficulty] || `רמה ${price.difficulty}`;
            
            // Create a new pricing card
            const card = document.createElement('div');
            card.className = 'pricing-card';
            
            card.innerHTML = `
                <h4>${difficultyName}</h4>
                <div class="card-price-row">
                    <h2>₪${price.hourly_wage}</h2>
                    <a href="#book">
                        <i class="fa-solid fa-arrow-left"></i>
                    </a>
                </div>
                <div>
                    <h5 class="card-inc">כלול בחבילה:</h5>
                    <ul class="card-list">
                        <li>שיעור פרטי אישי</li>
                        <li>חומרי לימוד</li>
                        <li>תרגילים ופתרונות</li>
                        <li>תמיכה בין השיעורים</li>
                    </ul>
                </div>
            `;
            
            pricingCardContainer.appendChild(card);
        });
        
    } catch (error) {
        console.error('Error updating pricing cards:', error);
    }
}

// Export functions for use in other scripts
window.teacherPortfolioAPI = {
    fetchPrices,
    updatePricingCards
};
