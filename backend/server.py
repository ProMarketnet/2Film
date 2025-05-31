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

# Mock movie data for demonstration (will be replaced with real API later)
MOCK_MOVIES = [
    {
        "title": "The Matrix",
        "year": "1999",
        "plot": "A computer programmer discovers that reality as he knows it is a simulation. Teaming up with a group of rebels, he must fight to free humanity from their digital prison.",
        "poster": "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300&h=450&fit=crop&crop=faces",
        "rating": "8.7",
        "genre": "Action, Sci-Fi",
        "director": "The Wachowskis",
        "actors": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
        "runtime": "136 min",
        "country": "USA",
        "language": "English"
    },
    {
        "title": "Inception",
        "year": "2010",
        "plot": "A thief who enters people's dreams to steal their secrets must plant an idea deep within a target's subconscious in this mind-bending heist thriller.",
        "poster": "https://images.unsplash.com/photo-1518676590629-3dcbd9c5a5c9?w=300&h=450&fit=crop&crop=faces",
        "rating": "8.8",
        "genre": "Action, Drama, Sci-Fi",
        "director": "Christopher Nolan",
        "actors": "Leonardo DiCaprio, Marion Cotillard, Tom Hardy",
        "runtime": "148 min",
        "country": "USA",
        "language": "English"
    },
    {
        "title": "The Dark Knight",
        "year": "2008",
        "plot": "When the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
        "poster": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=300&h=450&fit=crop&crop=faces",
        "rating": "9.0",
        "genre": "Action, Crime, Drama",
        "director": "Christopher Nolan",
        "actors": "Christian Bale, Heath Ledger, Aaron Eckhart",
        "runtime": "152 min",
        "country": "USA",
        "language": "English"
    },
    {
        "title": "Pulp Fiction",
        "year": "1994",
        "plot": "The lives of two mob hitmen, a boxer, a gangster's wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
        "poster": "https://images.unsplash.com/photo-1594909122845-11baa439b7bf?w=300&h=450&fit=crop&crop=faces",
        "rating": "8.9",
        "genre": "Crime, Drama",
        "director": "Quentin Tarantino",
        "actors": "John Travolta, Uma Thurman, Samuel L. Jackson",
        "runtime": "154 min",
        "country": "USA",
        "language": "English"
    },
    {
        "title": "Interstellar",
        "year": "2014",
        "plot": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival when Earth faces environmental collapse.",
        "poster": "https://images.unsplash.com/photo-1446776653964-20c1d3a81b06?w=300&h=450&fit=crop&crop=faces",
        "rating": "8.6",
        "genre": "Adventure, Drama, Sci-Fi",
        "director": "Christopher Nolan",
        "actors": "Matthew McConaughey, Anne Hathaway, Jessica Chastain",
        "runtime": "169 min",
        "country": "USA",
        "language": "English"
    }
]

MOCK_TV_SHOWS = [
    {
        "title": "Breaking Bad",
        "year": "2008-2013",
        "plot": "A high school chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine to secure his family's future.",
        "poster": "https://images.unsplash.com/photo-1616530940355-351fabd9524b?w=300&h=450&fit=crop&crop=faces",
        "rating": "9.5",
        "genre": "Crime, Drama, Thriller",
        "director": "Vince Gilligan",
        "actors": "Bryan Cranston, Aaron Paul, Anna Gunn",
        "type": "tv",
        "runtime": "47 min per episode",
        "country": "USA",
        "language": "English"
    },
    {
        "title": "Stranger Things",
        "year": "2016-2025",
        "plot": "When a young boy disappears, his mother, a police chief and his friends must confront terrifying supernatural forces in order to get him back.",
        "poster": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=450&fit=crop&crop=faces",
        "rating": "8.7",
        "genre": "Drama, Fantasy, Horror",
        "director": "The Duffer Brothers",
        "actors": "Millie Bobby Brown, Finn Wolfhard, Winona Ryder",
        "type": "tv",
        "runtime": "51 min per episode",
        "country": "USA",
        "language": "English"
    }
]

@api_router.get("/")
async def root():
    return {"message": "Film & Movie Agent API - Search for your favorite films and shows!"}

@api_router.post("/movies/search")
async def search_movies(request: MovieSearchRequest):
    """Search for movies and TV shows"""
    try:
        query = request.query.lower().strip()
        
        if not query:
            raise HTTPException(status_code=400, detail="Search query cannot be empty")
        
        # Search in mock data (case-insensitive)
        results = []
        
        # Search movies
        for movie_data in MOCK_MOVIES:
            if (query in movie_data["title"].lower() or 
                query in movie_data["genre"].lower() or 
                query in movie_data["director"].lower() or 
                query in movie_data["actors"].lower() or
                query in movie_data["plot"].lower()):
                
                movie = Movie(**movie_data)
                results.append(movie)
        
        # Search TV shows
        for show_data in MOCK_TV_SHOWS:
            if (query in show_data["title"].lower() or 
                query in show_data["genre"].lower() or 
                query in show_data["director"].lower() or 
                query in show_data["actors"].lower() or
                query in show_data["plot"].lower()):
                
                show = Movie(**show_data)
                results.append(show)
        
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
            "message": f"Found {len(results)} results for '{request.query}'"
        }
        
    except Exception as e:
        logger.error(f"Error searching movies: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while searching")

@api_router.get("/movies/popular")
async def get_popular_movies():
    """Get popular movies"""
    # Return top-rated movies from our mock data
    popular = sorted(MOCK_MOVIES + MOCK_TV_SHOWS, 
                    key=lambda x: float(x["rating"]), reverse=True)[:10]
    
    return {
        "results": [Movie(**item) for item in popular],
        "total": len(popular),
        "message": "Popular movies and shows"
    }

@api_router.get("/movies/genres")
async def get_genres():
    """Get available genres"""
    all_genres = set()
    
    for movie in MOCK_MOVIES + MOCK_TV_SHOWS:
        genres = [g.strip() for g in movie["genre"].split(",")]
        all_genres.update(genres)
    
    return {
        "genres": sorted(list(all_genres)),
        "total": len(all_genres)
    }

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
    """Get detailed information about a specific movie"""
    # For mock data, we'll search by title as ID
    all_content = MOCK_MOVIES + MOCK_TV_SHOWS
    
    for item in all_content:
        if movie_id.lower() in item["title"].lower():
            return Movie(**item)
    
    raise HTTPException(status_code=404, detail="Movie not found")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
