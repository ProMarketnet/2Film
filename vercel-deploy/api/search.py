from http.server import BaseHTTPRequestHandler
import json
import os
import httpx
import asyncio
from urllib.parse import parse_qs

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Enable CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            query = data.get('query', '').strip()
            if not query:
                response = {"error": "Search query cannot be empty"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Run async search
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.search_movies(query))
            loop.close()
            
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            error_response = {"error": str(e)}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    async def search_movies(self, query):
        api_key = os.environ.get('TMDB_API_KEY')
        base_url = os.environ.get('TMDB_BASE_URL')
        image_base_url = os.environ.get('TMDB_IMAGE_BASE_URL')
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{base_url}/search/multi",
                params={"api_key": api_key, "query": query}
            )
            data = response.json()
            
            results = []
            for item in data.get("results", [])[:10]:
                if item.get("media_type") in ["movie", "tv"]:
                    formatted = {
                        "id": str(item.get("id", "")),
                        "title": item.get("title") or item.get("name", "Unknown"),
                        "year": (item.get("release_date") or item.get("first_air_date", ""))[:4],
                        "plot": item.get("overview", "No plot available"),
                        "poster": f"{image_base_url}{item.get('poster_path')}" if item.get('poster_path') else "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300&h=450&fit=crop&crop=faces",
                        "rating": str(item.get("vote_average", 0)),
                        "genre": "Various",
                        "director": "Unknown",
                        "actors": "Unknown",
                        "type": item.get("media_type", "movie"),
                        "runtime": "Unknown",
                        "country": "Unknown",
                        "language": item.get("original_language", "").upper()
                    }
                    results.append(formatted)
            
            return {
                "query": query,
                "results": results,
                "total": len(results),
                "message": f"Found {len(results)} results for '{query}' from TMDB"
            }