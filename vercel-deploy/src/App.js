import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [searchQuery, setSearchQuery] = useState("");
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [popularMovies, setPopularMovies] = useState([]);

  // Fetch popular movies on load
  useEffect(() => {
    fetchPopularMovies();
  }, []);

  const fetchPopularMovies = async () => {
    try {
      const response = await fetch('/api/popular');
      const data = await response.json();
      setPopularMovies(data.results || []);
    } catch (error) {
      console.error("Error fetching popular movies:", error);
    }
  };

  const searchMovies = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setLoading(true);
    setError("");
    setMovies([]);

    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: searchQuery.trim() })
      });
      
      const data = await response.json();
      
      if (data.error) {
        setError(data.error);
      } else {
        setMovies(data.results || []);
        if ((data.results || []).length === 0) {
          setError(`No results found for "${searchQuery}"`);
        }
      }
    } catch (err) {
      setError("Failed to search movies");
    } finally {
      setLoading(false);
    }
  };

  const handleQuickSearch = (query) => {
    setSearchQuery(query);
    setLoading(true);
    setError("");
    setMovies([]);

    fetch('/api/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query })
    })
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          setError(data.error);
        } else {
          setMovies(data.results || []);
          if ((data.results || []).length === 0) {
            setError(`No results found for "${query}"`);
          }
        }
      })
      .catch(err => {
        setError("Failed to search movies");
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const MovieCard = ({ movie }) => (
    <div className="movie-card">
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
                  "🔍"
                )}
              </button>
            </div>
          </form>

          {/* Quick Search Suggestions */}
          <div className="quick-search">
            <span>Try: </span>
            {['Batman', 'Marvel', 'Horror', 'Comedy'].map((suggestion) => (
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
              <MovieCard key={index} movie={movie} />
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
              <MovieCard key={index} movie={movie} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

export default App;