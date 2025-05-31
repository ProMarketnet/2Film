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
            result = loop.run_until_complete(self.get_genres())
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
    
    async def get_genres(self):
        api_key = os.environ.get('TMDB_API_KEY')
        base_url = os.environ.get('TMDB_BASE_URL')
        
        async with httpx.AsyncClient() as client:
            # Get movie genres
            movies_response = await client.get(
                f"{base_url}/genre/movie/list",
                params={"api_key": api_key}
            )
            movies_data = movies_response.json()
            
            # Get TV genres
            tv_response = await client.get(
                f"{base_url}/genre/tv/list",
                params={"api_key": api_key}
            )
            tv_data = tv_response.json()
            
            all_genres = set()
            
            # Combine genres
            for genre in movies_data.get("genres", []):
                all_genres.add(genre["name"])
            
            for genre in tv_data.get("genres", []):
                all_genres.add(genre["name"])
            
            return {
                "genres": sorted(list(all_genres)),
                "total": len(all_genres)
            }