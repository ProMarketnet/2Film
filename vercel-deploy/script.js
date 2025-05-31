// Global variables
let currentMovies = [];
let isLoading = false;

// DOM elements
const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-input');
const searchBtn = document.getElementById('search-btn');
const searchIcon = document.getElementById('search-icon');
const searchSpinner = document.getElementById('search-spinner');
const errorMessage = document.getElementById('error-message');
const loading = document.getElementById('loading');
const searchResults = document.getElementById('search-results');
const resultsTitle = document.getElementById('results-title');
const moviesGrid = document.getElementById('movies-grid');
const popularSection = document.getElementById('popular-section');
const popularGrid = document.getElementById('popular-grid');
const movieModal = document.getElementById('movie-modal');
const modalClose = document.getElementById('modal-close');

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    fetchPopularMovies();
    setupEventListeners();
});

// Event listeners
function setupEventListeners() {
    searchForm.addEventListener('submit', handleSearch);
    modalClose.addEventListener('click', closeModal);
    movieModal.addEventListener('click', function(e) {
        if (e.target === movieModal) {
            closeModal();
        }
    });

    // Quick search buttons
    document.querySelectorAll('.suggestion-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const query = this.getAttribute('data-query');
            searchInput.value = query;
            performSearch(query);
        });
    });

    // Escape key to close modal
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && movieModal.style.display !== 'none') {
            closeModal();
        }
    });
}

// Search functionality
async function handleSearch(e) {
    e.preventDefault();
    const query = searchInput.value.trim();
    if (!query || isLoading) return;
    
    performSearch(query);
}

async function performSearch(query) {
    if (isLoading) return;
    
    setLoading(true);
    hideError();
    hideResults();
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showError(data.error);
        } else {
            currentMovies = data.results || [];
            if (currentMovies.length === 0) {
                showError(`No results found for "${query}"`);
            } else {
                showResults(currentMovies, `Search Results (${currentMovies.length})`);
            }
        }
    } catch (error) {
        console.error('Search error:', error);
        showError('Failed to search movies. Please try again.');
    } finally {
        setLoading(false);
    }
}

// Fetch popular movies
async function fetchPopularMovies() {
    try {
        const response = await fetch('/api/popular');
        const data = await response.json();
        
        if (data.results) {
            displayMovies(data.results, popularGrid);
        }
    } catch (error) {
        console.error('Error fetching popular movies:', error);
    }
}

// Display functions
function displayMovies(movies, container) {
    container.innerHTML = '';
    
    movies.forEach((movie, index) => {
        const movieCard = createMovieCard(movie, index);
        container.appendChild(movieCard);
    });
}

function createMovieCard(movie, index) {
    const card = document.createElement('div');
    card.className = 'movie-card';
    card.style.animationDelay = `${index * 0.1}s`;
    
    card.innerHTML = `
        <div class="movie-poster">
            <img src="${movie.poster}" alt="${movie.title}" onerror="this.src='https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300&h=450&fit=crop&crop=faces'">
            <div class="movie-overlay">
                <div class="movie-rating">⭐ ${movie.rating}</div>
                <div class="movie-type">${movie.type === 'tv' ? 'TV Show' : 'Movie'}</div>
            </div>
        </div>
        <div class="movie-info">
            <h3>${movie.title}</h3>
            <p class="movie-year">${movie.year}</p>
            <p class="movie-plot">${movie.plot}</p>
        </div>
    `;
    
    card.addEventListener('click', () => openModal(movie));
    
    return card;
}

// Modal functions
function openModal(movie) {
    document.getElementById('modal-image').src = movie.poster;
    document.getElementById('modal-title').textContent = `${movie.title} (${movie.year})`;
    document.getElementById('modal-rating').textContent = `⭐ ${movie.rating}/10`;
    document.getElementById('modal-year').textContent = movie.year;
    document.getElementById('modal-type').textContent = movie.type === 'tv' ? 'TV Show' : 'Movie';
    document.getElementById('modal-plot').textContent = movie.plot;
    
    movieModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    movieModal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// UI state functions
function setLoading(loading) {
    isLoading = loading;
    
    if (loading) {
        searchIcon.style.display = 'none';
        searchSpinner.style.display = 'inline';
        searchBtn.disabled = true;
        document.getElementById('loading').style.display = 'block';
        document.querySelectorAll('.suggestion-btn').forEach(btn => btn.disabled = true);
    } else {
        searchIcon.style.display = 'inline';
        searchSpinner.style.display = 'none';
        searchBtn.disabled = false;
        document.getElementById('loading').style.display = 'none';
        document.querySelectorAll('.suggestion-btn').forEach(btn => btn.disabled = false);
    }
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    popularSection.style.display = 'none';
    searchResults.style.display = 'none';
}

function hideError() {
    errorMessage.style.display = 'none';
}

function showResults(movies, title) {
    resultsTitle.textContent = title;
    displayMovies(movies, moviesGrid);
    searchResults.style.display = 'block';
    popularSection.style.display = 'none';
}

function hideResults() {
    searchResults.style.display = 'none';
    popularSection.style.display = 'block';
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}