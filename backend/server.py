from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
import httpx
import asyncio

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# TMDB Service Class
class TMDBService:
    def __init__(self):
        self.api_key = os.environ.get('TMDB_API_KEY')
        self.base_url = os.environ.get('TMDB_BASE_URL')
        self.image_base_url = os.environ.get('TMDB_IMAGE_BASE_URL')
        
    async def _make_request(self, endpoint: str, params: dict = None) -> dict:
        """Make authenticated request to TMDB API"""
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}{endpoint}", params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"TMDB API HTTP error: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=500, detail=f"TMDB API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"TMDB API error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"TMDB API error: {str(e)}")
    
    async def search_multi(self, query: str, page: int = 1) -> dict:
        """Search for movies, TV shows, and people"""
        return await self._make_request("/search/multi", {"query": query, "page": page})
    
    async def search_movies(self, query: str, page: int = 1) -> dict:
        """Search for movies by title"""
        return await self._make_request("/search/movie", {"query": query, "page": page})
    
    async def search_tv_shows(self, query: str, page: int = 1) -> dict:
        """Search for TV shows by title"""
        return await self._make_request("/search/tv", {"query": query, "page": page})
    
    async def search_person(self, query: str, page: int = 1) -> dict:
        """Search for actors/directors"""
        return await self._make_request("/search/person", {"query": query, "page": page})
    
    async def get_popular_movies(self, page: int = 1) -> dict:
        """Get popular movies"""
        return await self._make_request("/movie/popular", {"page": page})
    
    async def get_popular_tv_shows(self, page: int = 1) -> dict:
        """Get popular TV shows"""
        return await self._make_request("/tv/popular", {"page": page})
    
    async def get_movie_details(self, movie_id: int) -> dict:
        """Get detailed movie information"""
        return await self._make_request(f"/movie/{movie_id}", {"append_to_response": "credits,videos"})
    
    async def get_tv_details(self, tv_id: int) -> dict:
        """Get detailed TV show information"""
        return await self._make_request(f"/tv/{tv_id}", {"append_to_response": "credits,videos"})
    
    async def get_movie_genres(self) -> dict:
        """Get list of movie genres"""
        return await self._make_request("/genre/movie/list")
    
    async def get_tv_genres(self) -> dict:
        """Get list of TV genres"""
        return await self._make_request("/genre/tv/list")
    
    async def discover_by_genre(self, genre_id: int, content_type: str = "movie", page: int = 1) -> dict:
        """Discover movies or TV shows by genre"""
        endpoint = f"/discover/{content_type}"
        return await self._make_request(endpoint, {"with_genres": genre_id, "page": page})
    
    def get_full_image_url(self, image_path: str) -> str:
        """Convert relative image path to full URL"""
        if not image_path:
            return "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300&h=450&fit=crop&crop=faces"
        return f"{self.image_base_url}{image_path}"
    
    def format_movie_for_frontend(self, tmdb_movie: dict) -> dict:
        """Convert TMDB movie format to frontend format"""
        return {
            "id": str(tmdb_movie.get("id", "")),
            "title": tmdb_movie.get("title", "Unknown Title"),
            "year": tmdb_movie.get("release_date", "")[:4] if tmdb_movie.get("release_date") else "Unknown",
            "plot": tmdb_movie.get("overview", "No plot available"),
            "poster": self.get_full_image_url(tmdb_movie.get("poster_path")),
            "rating": str(tmdb_movie.get("vote_average", 0)),
            "genre": self.get_genre_names(tmdb_movie.get("genre_ids", []), tmdb_movie.get("genres", [])),
            "director": self.get_director_from_credits(tmdb_movie.get("credits", {})),
            "actors": self.get_actors_from_credits(tmdb_movie.get("credits", {})),
            "type": "movie",
            "runtime": f"{tmdb_movie.get('runtime', 'Unknown')} min" if tmdb_movie.get('runtime') else "Unknown",
            "country": self.get_countries(tmdb_movie.get("production_countries", [])),
            "language": tmdb_movie.get("original_language", "").upper()
        }
    
    def format_tv_for_frontend(self, tmdb_tv: dict) -> dict:
        """Convert TMDB TV show format to frontend format"""
        first_air = tmdb_tv.get('first_air_date', '')[:4] if tmdb_tv.get('first_air_date') else ''
        last_air = tmdb_tv.get('last_air_date', '')[:4] if tmdb_tv.get('last_air_date') else ''
        year_range = f"{first_air}-{last_air}" if first_air and last_air and first_air != last_air else first_air
        
        return {
            "id": str(tmdb_tv.get("id", "")),
            "title": tmdb_tv.get("name", "Unknown Title"),
            "year": year_range or "Unknown",
            "plot": tmdb_tv.get("overview", "No plot available"),
            "poster": self.get_full_image_url(tmdb_tv.get("poster_path")),
            "rating": str(tmdb_tv.get("vote_average", 0)),
            "genre": self.get_genre_names(tmdb_tv.get("genre_ids", []), tmdb_tv.get("genres", [])),
            "director": self.get_creator_from_tv(tmdb_tv.get("created_by", [])),
            "actors": self.get_actors_from_credits(tmdb_tv.get("credits", {})),
            "type": "tv",
            "runtime": f"{tmdb_tv.get('episode_run_time', [45])[0] if tmdb_tv.get('episode_run_time') else 45} min per episode",
            "country": self.get_countries(tmdb_tv.get("production_countries", [])),
            "language": tmdb_tv.get("original_language", "").upper()
        }
    
    def get_genre_names(self, genre_ids: list, genres: list = None) -> str:
        """Convert genre IDs to genre names"""
        # If we have genre objects directly, use them
        if genres:
            genre_names = [genre["name"] for genre in genres[:3]]
            return ", ".join(genre_names) if genre_names else "Unknown"
        
        # Otherwise use genre ID mapping
        genre_map = {
            28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy", 80: "Crime",
            99: "Documentary", 18: "Drama", 10751: "Family", 14: "Fantasy", 36: "History",
            27: "Horror", 10402: "Music", 9648: "Mystery", 10749: "Romance", 878: "Sci-Fi",
            10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western", 10759: "Action & Adventure",
            10762: "Kids", 10763: "News", 10764: "Reality", 10765: "Sci-Fi & Fantasy",
            10766: "Soap", 10767: "Talk", 10768: "War & Politics"
        }
        genre_names = [genre_map.get(gid, f"Genre{gid}") for gid in genre_ids[:3]]
        return ", ".join(genre_names) if genre_names else "Unknown"
    
    def get_director_from_credits(self, credits: dict) -> str:
        """Extract director from movie credits"""
        crew = credits.get("crew", [])
        directors = [person["name"] for person in crew if person.get("job") == "Director"]
        return ", ".join(directors[:2]) if directors else "Unknown"
    
    def get_creator_from_tv(self, creators: list) -> str:
        """Extract creator from TV show"""
        creator_names = [creator["name"] for creator in creators[:2]]
        return ", ".join(creator_names) if creator_names else "Unknown"
    
    def get_actors_from_credits(self, credits: dict) -> str:
        """Extract main actors from credits"""
        cast = credits.get("cast", [])
        actors = [person["name"] for person in cast[:4]]
        return ", ".join(actors) if actors else "Unknown"
    
    def get_countries(self, countries: list) -> str:
        """Extract production countries"""
        country_names = [country["name"] for country in countries[:2]]
        return ", ".join(country_names) if country_names else "Unknown"

# Initialize TMDB service
tmdb_service = TMDBService()

# Models
class MovieSearchRequest(BaseModel):
    query: str

class Movie(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    year: str
    plot: str
    poster: str
    rating: str
    genre: str
    director: str
    actors: str
    type: str = "movie"  # "movie" or "tv"
    runtime: str = ""
    country: str = ""
    language: str = ""

class SearchHistory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    results_count: int

@api_router.get("/")
async def root():
    return {"message": "Film & Movie Agent API - Search for your favorite films and shows with real TMDB data!"}

@api_router.post("/movies/search")
async def search_movies(request: MovieSearchRequest):
    """Search for movies and TV shows using TMDB API"""
    try:
        query = request.query.strip()
        
        if not query:
            raise HTTPException(status_code=400, detail="Search query cannot be empty")
        
        # Search using TMDB multi search to get movies, TV shows, and people
        tmdb_results = await tmdb_service.search_multi(query)
        
        results = []
        
        # Process TMDB results
        for item in tmdb_results.get("results", [])[:15]:  # Limit to 15 results
            try:
                if item.get("media_type") == "movie":
                    # Get detailed movie info with credits
                    try:
                        detailed_movie = await tmdb_service.get_movie_details(item["id"])
                        formatted_movie = tmdb_service.format_movie_for_frontend(detailed_movie)
                        results.append(formatted_movie)
                    except Exception as e:
                        logger.warning(f"Failed to get movie details for {item.get('title', 'Unknown')}: {e}")
                        # Use basic info if detailed request fails
                        formatted_movie = tmdb_service.format_movie_for_frontend(item)
                        results.append(formatted_movie)
                        
                elif item.get("media_type") == "tv":
                    # Get detailed TV show info with credits
                    try:
                        detailed_tv = await tmdb_service.get_tv_details(item["id"])
                        formatted_tv = tmdb_service.format_tv_for_frontend(detailed_tv)
                        results.append(formatted_tv)
                    except Exception as e:
                        logger.warning(f"Failed to get TV details for {item.get('name', 'Unknown')}: {e}")
                        # Use basic info if detailed request fails
                        formatted_tv = tmdb_service.format_tv_for_frontend(item)
                        results.append(formatted_tv)
                        
                elif item.get("media_type") == "person":
                    # If searching for a person, get their popular movies/TV shows
                    try:
                        person_credits = await tmdb_service._make_request(f"/person/{item['id']}/combined_credits")
                        # Add top-rated movies/shows from this person
                        cast_credits = person_credits.get("cast", [])
                        crew_credits = person_credits.get("crew", [])
                        
                        # Combine and sort by popularity
                        all_credits = cast_credits + crew_credits
                        all_credits.sort(key=lambda x: x.get("popularity", 0), reverse=True)
                        
                        # Add top 3 works from this person
                        for credit in all_credits[:3]:
                            if credit.get("media_type") == "movie":
                                formatted_movie = tmdb_service.format_movie_for_frontend(credit)
                                results.append(formatted_movie)
                            elif credit.get("media_type") == "tv":
                                formatted_tv = tmdb_service.format_tv_for_frontend(credit)
                                results.append(formatted_tv)
                                
                    except Exception as e:
                        logger.warning(f"Failed to get person credits for {item.get('name', 'Unknown')}: {e}")
                        
            except Exception as e:
                logger.warning(f"Error processing search result: {e}")
                continue
        
        # Save search to history
        search_record = SearchHistory(
            query=request.query,
            results_count=len(results)
        )
        await db.search_history.insert_one(search_record.dict())
        
        return {
            "query": request.query,
            "results": results,
            "total": len(results),
            "message": f"Found {len(results)} results for '{request.query}' from TMDB"
        }
        
    except Exception as e:
        logger.error(f"Error searching movies: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while searching")

@api_router.get("/movies/popular")
async def get_popular_movies():
    """Get popular movies and TV shows from TMDB"""
    try:
        # Get popular movies and TV shows
        popular_movies_data = await tmdb_service.get_popular_movies()
        popular_tv_data = await tmdb_service.get_popular_tv_shows()
        
        results = []
        
        # Format movies
        for movie in popular_movies_data.get("results", [])[:8]:
            try:
                detailed_movie = await tmdb_service.get_movie_details(movie["id"])
                formatted_movie = tmdb_service.format_movie_for_frontend(detailed_movie)
                results.append(formatted_movie)
            except Exception as e:
                logger.warning(f"Failed to get popular movie details: {e}")
                formatted_movie = tmdb_service.format_movie_for_frontend(movie)
                results.append(formatted_movie)
        
        # Format TV shows
        for tv_show in popular_tv_data.get("results", [])[:8]:
            try:
                detailed_tv = await tmdb_service.get_tv_details(tv_show["id"])
                formatted_tv = tmdb_service.format_tv_for_frontend(detailed_tv)
                results.append(formatted_tv)
            except Exception as e:
                logger.warning(f"Failed to get popular TV details: {e}")
                formatted_tv = tmdb_service.format_tv_for_frontend(tv_show)
                results.append(formatted_tv)
        
        # Sort by rating
        results.sort(key=lambda x: float(x["rating"]), reverse=True)
        
        return {
            "results": results,
            "total": len(results),
            "message": "Popular movies and shows from TMDB"
        }
        
    except Exception as e:
        logger.error(f"Error getting popular content: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching popular content")

@api_router.get("/movies/genres")
async def get_genres():
    """Get available genres from TMDB"""
    try:
        # Get both movie and TV genres
        movie_genres = await tmdb_service.get_movie_genres()
        tv_genres = await tmdb_service.get_tv_genres()
        
        all_genres = set()
        
        # Combine genres from both movies and TV
        for genre in movie_genres.get("genres", []):
            all_genres.add(genre["name"])
        
        for genre in tv_genres.get("genres", []):
            all_genres.add(genre["name"])
        
        return {
            "genres": sorted(list(all_genres)),
            "total": len(all_genres)
        }
        
    except Exception as e:
        logger.error(f"Error fetching genres: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching genres")

@api_router.get("/search/history")
async def get_search_history():
    """Get recent search history"""
    try:
        history = await db.search_history.find().sort("timestamp", -1).limit(10).to_list(10)
        return {
            "history": [SearchHistory(**item) for item in history],
            "total": len(history)
        }
    except Exception as e:
        logger.error(f"Error fetching search history: {str(e)}")
        return {"history": [], "total": 0}

@api_router.get("/movies/{movie_id}")
async def get_movie_details(movie_id: str):
    """Get detailed information about a specific movie or TV show"""
    try:
        # Try to parse as integer for TMDB ID
        try:
            tmdb_id = int(movie_id)
            # Try movie first
            try:
                movie_data = await tmdb_service.get_movie_details(tmdb_id)
                return tmdb_service.format_movie_for_frontend(movie_data)
            except:
                # If movie fails, try TV show
                tv_data = await tmdb_service.get_tv_details(tmdb_id)
                return tmdb_service.format_tv_for_frontend(tv_data)
        except ValueError:
            # If not a valid integer, search by title
            search_results = await tmdb_service.search_multi(movie_id)
            
            for item in search_results.get("results", []):
                if (item.get("media_type") == "movie" and 
                    movie_id.lower() in item.get("title", "").lower()):
                    
                    detailed_movie = await tmdb_service.get_movie_details(item["id"])
                    return tmdb_service.format_movie_for_frontend(detailed_movie)
                    
                elif (item.get("media_type") == "tv" and 
                      movie_id.lower() in item.get("name", "").lower()):
                    
                    detailed_tv = await tmdb_service.get_tv_details(item["id"])
                    return tmdb_service.format_tv_for_frontend(detailed_tv)
            
            raise HTTPException(status_code=404, detail="Movie or TV show not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching movie details: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching movie details")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
