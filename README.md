# 🎬 Film & Movie Agent

A comprehensive movie and TV show search application powered by The Movie Database (TMDB) API.

## Features

🔍 **Smart Search**
- Search for movies, TV shows, actors, and directors
- Real-time search with comprehensive results
- Case-insensitive search functionality

🎥 **Rich Content**
- High-quality poster images from TMDB
- Detailed movie/TV information including cast, crew, plot, ratings
- Popular movies and TV shows
- Genre-based browsing

📱 **Modern UI**
- Responsive design for all devices
- Dark theme with cinematic aesthetics
- Smooth animations and hover effects
- Detailed modal popups

🔧 **Advanced Features**
- Search history tracking
- Quick genre navigation
- Popular content discovery
- MongoDB integration for data persistence

## Tech Stack

**Frontend:**
- React.js
- Modern CSS with Tailwind-inspired styling
- Responsive design
- Axios for API calls

**Backend:**
- FastAPI (Python)
- TMDB API integration
- MongoDB for search history
- Real-time data processing

**Database:**
- MongoDB for search history and user data

## Live Demo

[Deploy to Vercel](https://vercel.com/deploy)

## Local Development

### Prerequisites
- Node.js 18+
- Python 3.11+
- MongoDB

### Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd film-movie-agent
```

2. **Frontend Setup**
```bash
cd frontend
npm install
```

3. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
```

4. **Environment Variables**

Create `.env` files:

**frontend/.env:**
```
REACT_APP_BACKEND_URL=http://localhost:8001
```

**backend/.env:**
```
MONGO_URL=mongodb://localhost:27017/
DB_NAME=movie_agent
TMDB_API_KEY=your_tmdb_api_key_here
TMDB_BASE_URL=https://api.themoviedb.org/3
TMDB_IMAGE_BASE_URL=https://image.tmdb.org/t/p/w500
```

5. **Get TMDB API Key**
- Visit [TMDB](https://www.themoviedb.org/)
- Create a free account
- Go to Settings → API → Create API Key
- Copy your API Key to the backend `.env` file

6. **Run the Application**

Start MongoDB, then:

```bash
# Terminal 1 - Backend
cd backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload

# Terminal 2 - Frontend
cd frontend
npm start
```

## Deployment to Vercel

1. **Fork/Clone this repository**

2. **Connect to Vercel**
   - Go to [Vercel](https://vercel.com/)
   - Import your GitHub repository
   - Vercel will automatically detect the configuration

3. **Set Environment Variables in Vercel**
   - Go to your project settings in Vercel
   - Add environment variables:
     - `TMDB_API_KEY`: Your TMDB API key
     - `TMDB_BASE_URL`: https://api.themoviedb.org/3
     - `TMDB_IMAGE_BASE_URL`: https://image.tmdb.org/t/p/w500

4. **Deploy**
   - Vercel will automatically deploy your application
   - Both frontend and backend will be deployed together

## API Endpoints

### Movies & TV Shows
- `POST /api/movies/search` - Search for movies, TV shows, and people
- `GET /api/movies/popular` - Get popular movies and TV shows
- `GET /api/movies/genres` - Get available genres
- `GET /api/movies/{movie_id}` - Get detailed movie/TV information

### User Data
- `GET /api/search/history` - Get recent search history

## Features in Detail

### Search Functionality
- **Multi-type Search**: Search across movies, TV shows, and people
- **Smart Results**: When searching for actors/directors, shows their popular works
- **Comprehensive Data**: Full cast, crew, plot, ratings, and metadata

### Movie Information
- **High-Quality Images**: Real poster images from TMDB's CDN
- **Detailed Metadata**: Runtime, country, language, release dates
- **Cast & Crew**: Complete information about actors, directors, and creators
- **Ratings**: Real user ratings from TMDB

### User Experience
- **Responsive Design**: Optimized for desktop, tablet, and mobile
- **Dark Theme**: Cinematic experience with modern aesthetics
- **Quick Navigation**: Genre buttons and search history for easy browsing
- **Smooth Interactions**: Hover effects, animations, and modal popups

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [The Movie Database (TMDB)](https://www.themoviedb.org/) for providing the comprehensive movie and TV data
- [Vercel](https://vercel.com/) for hosting and deployment platform
- [React](https://reactjs.org/) for the frontend framework
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework

---

**Made with ❤️ for movie and TV show enthusiasts**