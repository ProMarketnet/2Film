import requests
import json
import unittest
import os
import sys
from dotenv import load_dotenv

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
    
    def test_movie_search_by_title(self):
        """Test searching for movies by title"""
        payload = {"query": "Matrix"}
        response = requests.post(f"{API_URL}/movies/search", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertGreater(len(data["results"]), 0)
        self.assertIn("Matrix", data["results"][0]["title"])
        print(f"✅ Movie search by title test passed: Found {len(data['results'])} results for 'Matrix'")
        
        # Check response format
        movie = data["results"][0]
        required_fields = ["id", "title", "year", "plot", "poster", "rating", "genre", "director", "actors"]
        for field in required_fields:
            self.assertIn(field, movie)
    
    def test_movie_search_by_genre(self):
        """Test searching for movies by genre"""
        payload = {"query": "Action"}
        response = requests.post(f"{API_URL}/movies/search", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertGreater(len(data["results"]), 0)
        # Verify at least one result has Action in its genre
        has_action = False
        for movie in data["results"]:
            if "Action" in movie["genre"]:
                has_action = True
                break
        self.assertTrue(has_action)
        print(f"✅ Movie search by genre test passed: Found {len(data['results'])} results for 'Action'")
    
    def test_movie_search_by_director(self):
        """Test searching for movies by director"""
        payload = {"query": "Nolan"}
        response = requests.post(f"{API_URL}/movies/search", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertGreater(len(data["results"]), 0)
        # Verify at least one result has Nolan as director
        has_nolan = False
        for movie in data["results"]:
            if "Nolan" in movie["director"]:
                has_nolan = True
                break
        self.assertTrue(has_nolan)
        print(f"✅ Movie search by director test passed: Found {len(data['results'])} results for 'Nolan'")
    
    def test_movie_search_by_actor(self):
        """Test searching for movies by actor"""
        payload = {"query": "Leonardo"}
        response = requests.post(f"{API_URL}/movies/search", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertGreater(len(data["results"]), 0)
        # Verify at least one result has Leonardo in actors
        has_leonardo = False
        for movie in data["results"]:
            if "Leonardo" in movie["actors"]:
                has_leonardo = True
                break
        self.assertTrue(has_leonardo)
        print(f"✅ Movie search by actor test passed: Found {len(data['results'])} results for 'Leonardo'")
    
    def test_case_insensitive_search(self):
        """Test case-insensitive search"""
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
        
        # Both should return the same number of results
        self.assertEqual(len(data_lower["results"]), len(data_upper["results"]))
        print(f"✅ Case-insensitive search test passed")
    
    def test_empty_search_query(self):
        """Test empty search query (should return 400 error)"""
        payload = {"query": ""}
        response = requests.post(f"{API_URL}/movies/search", json=payload)
        self.assertEqual(response.status_code, 400)
        print(f"✅ Empty search query test passed: Received 400 error as expected")
    
    def test_popular_movies(self):
        """Test popular movies endpoint"""
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
        
        self.assertTrue(has_movie)
        self.assertTrue(has_tv)
        print(f"✅ Popular movies test passed: Found {len(data['results'])} results sorted by rating")
    
    def test_genres_endpoint(self):
        """Test genres endpoint"""
        response = requests.get(f"{API_URL}/movies/genres")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("genres", data)
        self.assertGreater(len(data["genres"]), 0)
        
        # Verify some expected genres are present
        expected_genres = ["Action", "Drama", "Sci-Fi"]
        for genre in expected_genres:
            self.assertIn(genre, data["genres"])
        
        print(f"✅ Genres endpoint test passed: Found {len(data['genres'])} genres")
    
    def test_search_history(self):
        """Test search history endpoint"""
        # First make a search to ensure there's history
        search_payload = {"query": "test_history_query"}
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
            if item["query"] == "test_history_query":
                found_query = True
                break
        
        self.assertTrue(found_query)
        print(f"✅ Search history test passed: Found {len(data['history'])} history items")
    
    def test_movie_details(self):
        """Test movie details endpoint"""
        # Use "matrix" as the movie ID (the implementation searches by title)
        movie_id = "matrix"
        response = requests.get(f"{API_URL}/movies/{movie_id}")
        self.assertEqual(response.status_code, 200)
        movie = response.json()
        
        # Verify movie details
        self.assertIn("Matrix", movie["title"])
        self.assertEqual(movie["year"], "1999")
        self.assertIn("Keanu Reeves", movie["actors"])
        
        print(f"✅ Movie details test passed: Successfully retrieved details for '{movie['title']}'")
    
    def test_nonexistent_movie(self):
        """Test requesting details for a non-existent movie"""
        movie_id = "nonexistentmovie12345"
        response = requests.get(f"{API_URL}/movies/{movie_id}")
        self.assertEqual(response.status_code, 404)
        print(f"✅ Non-existent movie test passed: Received 404 error as expected")

if __name__ == "__main__":
    # Run the tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)