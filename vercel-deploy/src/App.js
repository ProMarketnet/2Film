import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || window.location.origin;
const API = `${BACKEND_URL}/api`;

function App() {
  const [searchQuery, setSearchQuery] = useState("");
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [popularMovies, setPopularMovies] = useState([]);
  const [genres, setGenres] = useState([]);
  const [searchHistory, setSearchHistory] = useState([]);

  // Fetch popular movies on load
  useEffect(() => {
    fetchPopularMovies();
    fetchGenres();
    fetchSearchHistory();
  }, []);

  const fetchPopularMovies = async () => {
    try {
      const response = await axios.get(`${API}/movies/popular`);
      setPopularMovies(response.data.results);
    } catch (error) {
      console.error("Error fetching popular movies:", error);
    }
  };

  const fetchGenres = async () => {
    try {
      const response = await axios.get(`${API}/movies/genres`);
      setGenres(response.data.genres);
    } catch (error) {
      console.error("Error fetching genres:", error);
    }
  };

  const fetchSearchHistory = async () => {
    try {
      const response = await axios.get(`${API}/search/history`);
      setSearchHistory(response.data.history);
    } catch (error) {
      console.error("Error fetching search history:", error);
    }
  };

  const searchMovies = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setLoading(true);
    setError("");
    setMovies([]);

    try {
      const response = await axios.post(`${API}/movies/search`, {
        query: searchQuery.trim()
      });
      
      setMovies(response.data.results);
      if (response.data.results.length === 0) {
        setError(`No results found for "${searchQuery}"`);
      }
      
      // Refresh search history
      fetchSearchHistory();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to search movies");
    } finally {
      setLoading(false);
    }
  };

  const handleQuickSearch = (query) => {
    setSearchQuery(query);
    setLoading(true);
    setError("");
    setMovies([]);

    axios.post(`${API}/movies/search`, { query })
      .then(response => {
        setMovies(response.data.results);
        if (response.data.results.length === 0) {
          setError(`No results found for "${query}"`);
        }
        fetchSearchHistory();
      })
      .catch(err => {
        setError(err.response?.data?.detail || "Failed to search movies");
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const openMovieDetails = (movie) => {
    setSelectedMovie(movie);
  };

  const closeMovieDetails = () => {
    setSelectedMovie(null);
  };

  const MovieCard = ({ movie, onClick }) => (
    <div className="movie-card" onClick={() => onClick(movie)}>
      <div className="movie-poster">
        <img src={movie.poster} alt={movie.title} />
        <div className="movie-overlay">
          <div className="movie-rating">⭐ {movie.rating}</div>
          <div className="movie-type">{movie.type === 'tv' ? 'TV Show' : 'Movie'}</div>
        </div>
      </div>
      <div className="movie-info">
        <h3>{movie.title}</h3>
        <p className="movie-year">{movie.year}</p>
        <p className="movie-genre">{movie.genre}</p>
      </div>
    </div>
  );

  const MovieModal = ({ movie, onClose }) => (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>×</button>
        <div className="modal-body">
          <div className="modal-poster">
            <img src={movie.poster} alt={movie.title} />
          </div>
          <div className="modal-details">
            <h2>{movie.title} ({movie.year})</h2>
            <div className="movie-meta">
              <span className="rating">⭐ {movie.rating}/10</span>
              <span className="runtime">{movie.runtime}</span>
              <span className="type">{movie.type === 'tv' ? 'TV Show' : 'Movie'}</span>
            </div>
            <div className="movie-genres">
              {movie.genre.split(',').map((genre, index) => (
                <span key={index} className="genre-tag">{genre.trim()}</span>
              ))}
            </div>
            <div className="movie-plot">
              <h3>Plot</h3>
              <p>{movie.plot}</p>
            </div>
            <div className="movie-cast">
              <div className="cast-item">
                <strong>Director:</strong> {movie.director}
              </div>
              <div className="cast-item">
                <strong>Cast:</strong> {movie.actors}
              </div>
              <div className="cast-item">
                <strong>Country:</strong> {movie.country}
              </div>
              <div className="cast-item">
                <strong>Language:</strong> {movie.language}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="App">
      {/* Hero Section */}
      <div className="hero-section">
        <div className="hero-content">
          <h1>Film & Movie Agent</h1>
          <p>Discover your favorite films and shows with detailed information</p>
          
          <form onSubmit={searchMovies} className="search-form">
            <div className="search-container">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search for movies, TV shows, actors, directors..."
                className="search-input"
                disabled={loading}
              />
              <button type="submit" disabled={loading || !searchQuery.trim()} className="search-button">
                {loading ? (
                  <div className="spinner"></div>
                ) : (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
                  </svg>
                )}
              </button>
            </div>
          </form>

          {/* Quick Search Suggestions */}
          <div className="quick-search">
            <span>Try: </span>
            {['Matrix', 'Nolan', 'Action', 'Drama', 'Breaking Bad'].map((suggestion) => (
              <button 
                key={suggestion}
                onClick={() => handleQuickSearch(suggestion)}
                className="suggestion-button"
                disabled={loading}
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Search Results */}
      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      {movies.length > 0 && (
        <section className="results-section">
          <h2>Search Results ({movies.length})</h2>
          <div className="movies-grid">
            {movies.map((movie, index) => (
              <MovieCard key={index} movie={movie} onClick={openMovieDetails} />
            ))}
          </div>
        </section>
      )}

      {/* Popular Movies Section */}
      {movies.length === 0 && !loading && (
        <section className="popular-section">
          <h2>Popular Movies & Shows</h2>
          <div className="movies-grid">
            {popularMovies.map((movie, index) => (
              <MovieCard key={index} movie={movie} onClick={openMovieDetails} />
            ))}
          </div>
        </section>
      )}

      {/* Sidebar with Genres and History */}
      <div className="sidebar">
        {/* Genres */}
        <div className="sidebar-section">
          <h3>Genres</h3>
          <div className="genre-list">
            {genres.slice(0, 10).map((genre, index) => (
              <button 
                key={index}
                onClick={() => handleQuickSearch(genre)}
                className="genre-button"
                disabled={loading}
              >
                {genre}
              </button>
            ))}
          </div>
        </div>

        {/* Recent Searches */}
        {searchHistory.length > 0 && (
          <div className="sidebar-section">
            <h3>Recent Searches</h3>
            <div className="search-history">
              {searchHistory.slice(0, 5).map((search, index) => (
                <button 
                  key={index}
                  onClick={() => handleQuickSearch(search.query)}
                  className="history-button"
                  disabled={loading}
                >
                  {search.query} ({search.results_count})
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Movie Details Modal */}
      {selectedMovie && (
        <MovieModal movie={selectedMovie} onClose={closeMovieDetails} />
      )}
    </div>
  );
}

export default App;