from http.server import BaseHTTPRequestHandler
import json
import os
import httpx
import asyncio

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Enable CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        try:
            # Run async function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.get_popular())
            loop.close()
            
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            error_response = {"error": str(e)}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    async def get_popular(self):
        api_key = os.environ.get('TMDB_API_KEY')
        base_url = os.environ.get('TMDB_BASE_URL')
        image_base_url = os.environ.get('TMDB_IMAGE_BASE_URL')
        
        async with httpx.AsyncClient() as client:
            # Get popular movies
            movies_response = await client.get(
                f"{base_url}/movie/popular",
                params={"api_key": api_key}
            )
            movies_data = movies_response.json()
            
            # Get popular TV shows
            tv_response = await client.get(
                f"{base_url}/tv/popular", 
                params={"api_key": api_key}
            )
            tv_data = tv_response.json()
            
            results = []
            
            # Process movies
            for movie in movies_data.get("results", [])[:8]:
                formatted = {
                    "id": str(movie.get("id", "")),
                    "title": movie.get("title", "Unknown"),
                    "year": movie.get("release_date", "")[:4],
                    "plot": movie.get("overview", "No plot available"),
                    "poster": f"{image_base_url}{movie.get('poster_path')}" if movie.get('poster_path') else "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300&h=450&fit=crop&crop=faces",
                    "rating": str(movie.get("vote_average", 0)),
                    "genre": "Various",
                    "director": "Unknown",
                    "actors": "Unknown",
                    "type": "movie",
                    "runtime": "Unknown",
                    "country": "Unknown",
                    "language": movie.get("original_language", "").upper()
                }
                results.append(formatted)
            
            # Process TV shows
            for show in tv_data.get("results", [])[:8]:
                formatted = {
                    "id": str(show.get("id", "")),
                    "title": show.get("name", "Unknown"),
                    "year": show.get("first_air_date", "")[:4],
                    "plot": show.get("overview", "No plot available"),
                    "poster": f"{image_base_url}{show.get('poster_path')}" if show.get('poster_path') else "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300&h=450&fit=crop&crop=faces",
                    "rating": str(show.get("vote_average", 0)),
                    "genre": "Various",
                    "director": "Unknown",
                    "actors": "Unknown", 
                    "type": "tv",
                    "runtime": "Unknown",
                    "country": "Unknown",
                    "language": show.get("original_language", "").upper()
                }
                results.append(formatted)
            
            # Sort by rating
            results.sort(key=lambda x: float(x["rating"]), reverse=True)
            
            return {
                "results": results,
                "total": len(results),
                "message": "Popular movies and shows from TMDB"
            }