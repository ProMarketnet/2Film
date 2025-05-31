import React, { useState, useEffect } from 'react';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [popularMovies, setPopularMovies] = useState([]);

  useEffect(() => {
    fetchPopularMovies();
  }, []);

  const fetchPopularMovies = async () => {
    try {
      const response = await fetch('/api/popular');
      if (response.ok) {
        const data = await response.json();
        setPopularMovies(data.results || []);
      }
    } catch (error) {
      console.error('Error fetching popular movies:', error);
    }
  };

  const searchMovies = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setLoading(true);
    setError('');
    setMovies([]);

    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
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
      setError('Failed to search movies');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickSearch = (query) => {
    setSearchQuery(query);
    setLoading(true);
    setError('');
    setMovies([]);

    fetch('/api/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
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
      .catch(() => setError('Failed to search movies'))
      .finally(() => setLoading(false));
  };

  return (
    <div className="app">
      <div className="hero">
        <h1>🎬 Film & Movie Agent</h1>
        <p>Discover your favorite films and shows</p>
        
        <form onSubmit={searchMovies} className="search-form">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search movies, TV shows, actors..."
            disabled={loading}
            className="search-input"
          />
          <button type="submit" disabled={loading || !searchQuery.trim()} className="search-btn">
            {loading ? '⏳' : '🔍'}
          </button>
        </form>

        <div className="quick-search">
          <span>Try: </span>
          {['Batman', 'Marvel', 'Horror', 'Comedy'].map((suggestion) => (
            <button 
              key={suggestion}
              onClick={() => handleQuickSearch(suggestion)}
              disabled={loading}
              className="suggestion-btn"
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      {movies.length > 0 && (
        <div className="results">
          <h2>Search Results ({movies.length})</h2>
          <div className="movie-grid">
            {movies.map((movie, index) => (
              <div key={index} className="movie-card">
                <img src={movie.poster} alt={movie.title} className="movie-poster" />
                <div className="movie-info">
                  <h3>{movie.title}</h3>
                  <p>{movie.year} • ⭐ {movie.rating}</p>
                  <p className="movie-plot">{movie.plot}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {movies.length === 0 && !loading && (
        <div className="popular">
          <h2>Popular Movies & Shows</h2>
          <div className="movie-grid">
            {popularMovies.map((movie, index) => (
              <div key={index} className="movie-card">
                <img src={movie.poster} alt={movie.title} className="movie-poster" />
                <div className="movie-info">
                  <h3>{movie.title}</h3>
                  <p>{movie.year} • ⭐ {movie.rating}</p>
                  <p className="movie-plot">{movie.plot}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;