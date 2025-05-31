# 🚀 Deployment Guide for Film & Movie Agent

## Quick Deployment to Vercel

### Option 1: Deploy Frontend + Backend Together (Recommended)

1. **Fork this repository** to your GitHub account

2. **Connect to Vercel:**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will auto-detect the configuration

3. **Configure Environment Variables in Vercel:**
   - Go to Project Settings → Environment Variables
   - Add these variables:
     ```
     TMDB_API_KEY = 177b48eb85143a28a9aac14ec0e5a679
     TMDB_BASE_URL = https://api.themoviedb.org/3
     TMDB_IMAGE_BASE_URL = https://image.tmdb.org/t/p/w500
     MONGO_URL = mongodb+srv://username:password@cluster.mongodb.net/movie_agent
     DB_NAME = movie_agent
     ```

4. **Deploy:**
   - Vercel will automatically build and deploy
   - Your app will be available at `https://your-app-name.vercel.app`

### Option 2: Deploy Frontend Only (Using External Backend)

If you want to deploy just the frontend and use an external backend:

1. **Update Frontend Environment:**
   ```bash
   # In frontend/.env.production
   REACT_APP_BACKEND_URL=https://your-backend-url.com/api
   ```

2. **Deploy to Vercel:**
   - Import your repository
   - Vercel will build only the frontend
   - Configure the environment variable above

### Option 3: Deploy Backend Only

If you want to deploy just the backend API:

1. **Create a new Vercel project**
2. **Point it to the `/backend` folder**
3. **Add environment variables:**
   ```
   TMDB_API_KEY = your_tmdb_api_key
   TMDB_BASE_URL = https://api.themoviedb.org/3
   TMDB_IMAGE_BASE_URL = https://image.tmdb.org/t/p/w500
   MONGO_URL = your_mongodb_connection_string
   DB_NAME = movie_agent
   ```

## Database Setup

### Option 1: MongoDB Atlas (Recommended for Production)

1. **Create MongoDB Atlas Account:**
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create a free cluster

2. **Get Connection String:**
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your database user password

3. **Use in Vercel:**
   ```
   MONGO_URL = mongodb+srv://username:password@cluster.mongodb.net/movie_agent
   ```

### Option 2: Local Development

For local development, use:
```
MONGO_URL = mongodb://localhost:27017/
```

## Environment Variables Reference

### Required for Backend:
- `TMDB_API_KEY`: Your TMDB API key
- `TMDB_BASE_URL`: https://api.themoviedb.org/3
- `TMDB_IMAGE_BASE_URL`: https://image.tmdb.org/t/p/w500
- `MONGO_URL`: MongoDB connection string
- `DB_NAME`: Database name (e.g., movie_agent)

### Required for Frontend:
- `REACT_APP_BACKEND_URL`: Backend API URL (automatically set in Vercel)

## Troubleshooting

### Common Issues:

1. **TMDB API Errors:**
   - Verify your TMDB API key is correct
   - Check TMDB API rate limits

2. **Database Connection Issues:**
   - Verify MongoDB connection string
   - Check database user permissions
   - Ensure network access is allowed

3. **Build Failures:**
   - Check Node.js version compatibility
   - Verify all dependencies are installed
   - Check for syntax errors in code

4. **CORS Issues:**
   - Ensure backend CORS is configured for your frontend domain
   - Check environment variable configuration

### Support:

If you encounter issues:
1. Check Vercel deployment logs
2. Verify all environment variables are set
3. Test API endpoints individually
4. Check browser console for frontend errors

## Post-Deployment Checklist

✅ Frontend loads correctly  
✅ Search functionality works  
✅ Movie details display properly  
✅ Images load from TMDB  
✅ Responsive design works on mobile  
✅ API endpoints respond correctly  
✅ Database operations work  
✅ Error handling displays properly  

## Performance Optimization

For production deployment:

1. **Enable caching** for movie posters
2. **Implement lazy loading** for images
3. **Add search debouncing** to reduce API calls
4. **Enable gzip compression**
5. **Use CDN** for static assets

Your Film & Movie Agent is now ready for the world! 🎬✨