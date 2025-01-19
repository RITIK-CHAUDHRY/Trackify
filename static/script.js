// script.js

const coinContainer = document.querySelector('.coin-container');
const splashScreen = document.querySelector('.splash-screen');
const piggyBank = document.querySelector('.piggy-bank');
const welcomeSection = document.querySelector('.welcome-section');

// Function to create coins
function createCoin() {
    const coin = document.createElement('div');
    coin.classList.add('coin');
    coin.style.left = `${Math.random() * 80}%`; // Random horizontal position within container
    coinContainer.appendChild(coin);

    // Remove coin after animation
    setTimeout(() => {
        coinContainer.removeChild(coin);
    }, 2000);
}

// Generate coins every 100ms for 2 seconds
const coinInterval = setInterval(createCoin, 100);
setTimeout(() => {
    clearInterval(coinInterval); // Stop generating coins after 2 seconds
}, 2000);

// Fade out piggy bank and splash screen after 2 seconds
setTimeout(() => {
    piggyBank.style.opacity = '0'; // Gradual fade-out of piggy bank
    splashScreen.style.opacity = '0'; // Fade out the entire splash screen

    setTimeout(() => {
        splashScreen.style.display = 'none'; // Hide splash screen completely
        welcomeSection.classList.add('visible'); // Show welcome section
    }, 2000);
}, 2000);
