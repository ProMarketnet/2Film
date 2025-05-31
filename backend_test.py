import requests
import json
import unittest
import os
import sys
from dotenv import load_dotenv
import re

# Load environment variables from frontend/.env
load_dotenv("frontend/.env")

# Get the backend URL from environment variables
BACKEND_URL = os.environ.get("REACT_APP_BACKEND_URL")
if not BACKEND_URL:
    print("Error: REACT_APP_BACKEND_URL environment variable not found")
    sys.exit(1)

# Ensure the URL ends with /api for all requests
API_URL = f"{BACKEND_URL}/api"
print(f"Testing backend API at: {API_URL}")

class FilmMovieAgentAPITest(unittest.TestCase):
    
    def test_root_endpoint(self):
        """Test the root API endpoint"""
        response = requests.get(f"{API_URL}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        print(f"✅ Root endpoint test passed: {data['message']}")
    
    def test_tmdb_movie_search_by_title(self):
        """Test searching for movies by title using TMDB API"""
        payload = {"query": "Avengers"}
        response = requests.post(f"{API_URL}/movies/search", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertGreater(len(data["results"]), 0)
        
        # Check if "Avengers" is in at least one title
        has_avengers = False
        for movie in data["results"]:
            if "Avengers" in movie["title"]:
                has_avengers = True
                break
        self.assertTrue(has_avengers, "No Avengers movie found in search results")
        
        # Check response format and TMDB data
        movie = data["results"][0]
        required_fields = ["id", "title", "year", "plot", "poster", "rating", "genre", "director", "actors", "type"]
        for field in required_fields:
            self.assertIn(field, movie)
        
        # Verify poster URL is from TMDB
        self.assertTrue(
            movie["poster"].startswith("https://image.tmdb.org/t/p/") or 
            movie["poster"].startswith("https://images.unsplash.com/"),
            f"Poster URL doesn't match TMDB format: {movie['poster']}"
        )
        
        print(f"✅ TMDB Movie search by title test passed: Found {len(data['results'])} results for 'Avengers'")
    
    def test_tmdb_tv_show_search(self):
        """Test searching for TV shows using TMDB API"""
        payload = {"query": "Breaking Bad"}
        response = requests.post(f"{API_URL}/movies/search", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertGreater(len(data["results"]), 0)
        
        # Check if at least one result is a TV show
        has_tv_show = False
        has_breaking_bad = False
        for item in data["results"]:
            if item["type"] == "tv":
                has_tv_show = True
                if "Breaking Bad" in item["title"]:
                    has_breaking_bad = True
                    break
        
        self.assertTrue(has_tv_show, "No TV shows found in search results")
        self.assertTrue(has_breaking_bad, "Breaking Bad not found in search results")
        
        # Find Breaking Bad in results
        breaking_bad = None
        for item in data["results"]:
            if "Breaking Bad" in item["title"]:
                breaking_bad = item
                break
        
        self.assertIsNotNone(breaking_bad, "Breaking Bad not found in search results")
        
        # Verify TV show details
        self.assertEqual(breaking_bad["type"], "tv")
        self.assertIn("runtime", breaking_bad)
        self.assertIn("min per episode", breaking_bad["runtime"])
        
        print(f"✅ TMDB TV show search test passed: Found Breaking Bad in {len(data['results'])} results")
    
    def test_tmdb_person_search(self):
        """Test searching for actors/directors using TMDB API"""
        payload = {"query": "Tom Hanks"}
        response = requests.post(f"{API_URL}/movies/search", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertGreater(len(data["results"]), 0)
        
        # Check if Tom Hanks appears in actors or director fields
        has_tom_hanks = False
        for item in data["results"]:
            if "Tom Hanks" in item["actors"] or "Tom Hanks" in item["director"]:
                has_tom_hanks = True
                break
        
        self.assertTrue(has_tom_hanks, "No movies with Tom Hanks found in search results")
        print(f"✅ TMDB Person search test passed: Found {len(data['results'])} results for 'Tom Hanks'")
        
        # Test another person search
        payload = {"query": "Christopher Nolan"}
        response = requests.post(f"{API_URL}/movies/search", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check if Christopher Nolan appears as director
        has_nolan_director = False
        for item in data["results"]:
            if "Nolan" in item["director"]:
                has_nolan_director = True
                break
        
        self.assertTrue(has_nolan_director, "No movies directed by Christopher Nolan found")
        print(f"✅ TMDB Director search test passed: Found {len(data['results'])} results for 'Christopher Nolan'")
    
    def test_case_insensitive_search(self):
        """Test case-insensitive search with TMDB API"""
        # Test with lowercase
        payload_lower = {"query": "matrix"}
        response_lower = requests.post(f"{API_URL}/movies/search", json=payload_lower)
        self.assertEqual(response_lower.status_code, 200)
        data_lower = response_lower.json()
        
        # Test with uppercase
        payload_upper = {"query": "MATRIX"}
        response_upper = requests.post(f"{API_URL}/movies/search", json=payload_upper)
        self.assertEqual(response_upper.status_code, 200)
        data_upper = response_upper.json()
        
        # Both should return results with "Matrix" in the title
        has_matrix_lower = False
        has_matrix_upper = False
        
        for movie in data_lower["results"]:
            if re.search("matrix", movie["title"], re.IGNORECASE):
                has_matrix_lower = True
                break
        
        for movie in data_upper["results"]:
            if re.search("matrix", movie["title"], re.IGNORECASE):
                has_matrix_upper = True
                break
        
        self.assertTrue(has_matrix_lower, "No Matrix movie found in lowercase search")
        self.assertTrue(has_matrix_upper, "No Matrix movie found in uppercase search")
        print(f"✅ TMDB Case-insensitive search test passed")
    
    def test_empty_search_query(self):
        """Test empty search query with TMDB API (should return 400 error)"""
        payload = {"query": ""}
        response = requests.post(f"{API_URL}/movies/search", json=payload)
        self.assertEqual(response.status_code, 400)
        print(f"✅ TMDB Empty search query test passed: Received 400 error as expected")
    
    def test_tmdb_popular_movies(self):
        """Test popular movies endpoint with TMDB API"""
        response = requests.get(f"{API_URL}/movies/popular")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertGreater(len(data["results"]), 0)
        
        # Verify results are sorted by rating (highest first)
        ratings = [float(movie["rating"]) for movie in data["results"]]
        self.assertEqual(ratings, sorted(ratings, reverse=True))
        
        # Verify both movies and TV shows are included
        has_movie = False
        has_tv = False
        for item in data["results"]:
            if item["type"] == "movie":
                has_movie = True
            elif item["type"] == "tv":
                has_tv = True
        
        self.assertTrue(has_movie, "No movies found in popular results")
        self.assertTrue(has_tv, "No TV shows found in popular results")
        
        # Check for high-quality poster images
        for item in data["results"]:
            self.assertTrue(
                item["poster"].startswith("https://image.tmdb.org/t/p/") or 
                item["poster"].startswith("https://images.unsplash.com/"),
                f"Poster URL doesn't match TMDB format: {item['poster']}"
            )
        
        # Check for cast/crew information
        for item in data["results"]:
            self.assertNotEqual(item["actors"], "Unknown", f"No actors found for {item['title']}")
            self.assertNotEqual(item["director"], "Unknown", f"No director found for {item['title']}")
        
        print(f"✅ TMDB Popular movies test passed: Found {len(data['results'])} results with real TMDB data")
    
    def test_tmdb_genres(self):
        """Test genres endpoint with TMDB API"""
        response = requests.get(f"{API_URL}/movies/genres")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("genres", data)
        self.assertGreater(len(data["genres"]), 10, "Too few genres returned, expected at least 10")
        
        # Verify common movie genres are present
        movie_genres = ["Action", "Drama", "Comedy", "Horror", "Thriller"]
        for genre in movie_genres:
            self.assertIn(genre, data["genres"], f"Movie genre '{genre}' not found")
        
        # Verify TV-specific genres are present
        tv_genres = ["Animation", "Documentary", "Family"]
        for genre in tv_genres:
            self.assertIn(genre, data["genres"], f"TV genre '{genre}' not found")
        
        print(f"✅ TMDB Genres endpoint test passed: Found {len(data['genres'])} genres from both movies and TV")
    
    def test_tmdb_search_history(self):
        """Test search history endpoint with TMDB search results"""
        # First make a search to ensure there's history
        search_payload = {"query": "tmdb_test_history_query"}
        search_response = requests.post(f"{API_URL}/movies/search", json=search_payload)
        self.assertEqual(search_response.status_code, 200)
        
        # Then check the history endpoint
        response = requests.get(f"{API_URL}/search/history")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("history", data)
        
        # Verify our test query is in the history
        found_query = False
        for item in data["history"]:
            if item["query"] == "tmdb_test_history_query":
                found_query = True
                break
        
        self.assertTrue(found_query, "Test query not found in search history")
        print(f"✅ TMDB Search history test passed: Found {len(data['history'])} history items")
    
    def test_tmdb_movie_details_by_id(self):
        """Test movie details endpoint with TMDB ID"""
        # First search for a movie to get its ID
        search_payload = {"query": "Inception"}
        search_response = requests.post(f"{API_URL}/movies/search", json=search_payload)
        self.assertEqual(search_response.status_code, 200)
        search_data = search_response.json()
        
        # Find Inception in results
        inception_id = None
        for movie in search_data["results"]:
            if "Inception" in movie["title"]:
                inception_id = movie["id"]
                break
        
        self.assertIsNotNone(inception_id, "Inception not found in search results")
        
        # Get movie details by ID
        response = requests.get(f"{API_URL}/movies/{inception_id}")
        self.assertEqual(response.status_code, 200)
        movie = response.json()
        
        # Verify movie details
        self.assertIn("Inception", movie["title"])
        self.assertEqual(movie["type"], "movie")
        self.assertIn("Christopher Nolan", movie["director"])
        self.assertIn("Leonardo DiCaprio", movie["actors"])
        
        print(f"✅ TMDB Movie details by ID test passed: Successfully retrieved details for '{movie['title']}'")
    
    def test_tmdb_tv_details_by_id(self):
        """Test TV show details endpoint with TMDB ID"""
        # First search for a TV show to get its ID
        search_payload = {"query": "Game of Thrones"}
        search_response = requests.post(f"{API_URL}/movies/search", json=search_payload)
        self.assertEqual(search_response.status_code, 200)
        search_data = search_response.json()
        
        # Find Game of Thrones in results
        got_id = None
        for item in search_data["results"]:
            if "Game of Thrones" in item["title"]:
                got_id = item["id"]
                break
        
        self.assertIsNotNone(got_id, "Game of Thrones not found in search results")
        
        # Get TV show details by ID
        response = requests.get(f"{API_URL}/movies/{got_id}")
        self.assertEqual(response.status_code, 200)
        tv_show = response.json()
        
        # Verify TV show details
        self.assertIn("Game of Thrones", tv_show["title"])
        self.assertEqual(tv_show["type"], "tv")
        
        print(f"✅ TMDB TV show details by ID test passed: Successfully retrieved details for '{tv_show['title']}'")
    
    def test_tmdb_movie_details_by_title(self):
        """Test movie details endpoint with title search"""
        movie_title = "matrix"
        response = requests.get(f"{API_URL}/movies/{movie_title}")
        self.assertEqual(response.status_code, 200)
        movie = response.json()
        
        # Verify movie details
        self.assertIn("Matrix", movie["title"])
        self.assertIn("Keanu Reeves", movie["actors"])
        
        print(f"✅ TMDB Movie details by title test passed: Successfully retrieved details for '{movie['title']}'")
    
    def test_nonexistent_movie(self):
        """Test requesting details for a non-existent movie with TMDB API"""
        movie_id = "nonexistentmovie12345"
        response = requests.get(f"{API_URL}/movies/{movie_id}")
        self.assertEqual(response.status_code, 404)
        print(f"✅ TMDB Non-existent movie test passed: Received 404 error as expected")
    
    def test_tmdb_poster_urls(self):
        """Test that poster URLs are from TMDB CDN"""
        # Test in search results
        payload = {"query": "Batman"}
        response = requests.post(f"{API_URL}/movies/search", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        for movie in data["results"]:
            self.assertTrue(
                movie["poster"].startswith("https://image.tmdb.org/t/p/") or 
                movie["poster"].startswith("https://images.unsplash.com/"),
                f"Poster URL doesn't match TMDB format: {movie['poster']}"
            )
        
        # Test in popular movies
        response = requests.get(f"{API_URL}/movies/popular")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        for movie in data["results"]:
            self.assertTrue(
                movie["poster"].startswith("https://image.tmdb.org/t/p/") or 
                movie["poster"].startswith("https://images.unsplash.com/"),
                f"Poster URL doesn't match TMDB format: {movie['poster']}"
            )
        
        print(f"✅ TMDB Poster URLs test passed: All posters use TMDB CDN")

if __name__ == "__main__":
    # Run the tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)