import json
import requests

def handler(request):
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': ''
        }
    
    try:
        # TMDB API configuration
        api_key = '177b48eb85143a28a9aac14ec0e5a679'
        base_url = 'https://api.themoviedb.org/3'
        image_base_url = 'https://image.tmdb.org/t/p/w500'
        
        # Get popular movies
        movies_response = requests.get(
            f"{base_url}/movie/popular",
            params={'api_key': api_key},
            timeout=10
        )
        movies_response.raise_for_status()
        movies_data = movies_response.json()
        
        # Get popular TV shows
        tv_response = requests.get(
            f"{base_url}/tv/popular",
            params={'api_key': api_key},
            timeout=10
        )
        tv_response.raise_for_status()
        tv_data = tv_response.json()
        
        results = []
        
        # Process movies
        for movie in movies_data.get('results', [])[:8]:
            poster_path = movie.get('poster_path')
            poster_url = f"{image_base_url}{poster_path}" if poster_path else 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300&h=450&fit=crop&crop=faces'
            
            formatted = {
                'id': str(movie.get('id', '')),
                'title': movie.get('title', 'Unknown Title'),
                'year': movie.get('release_date', '')[:4] if movie.get('release_date') else 'Unknown',
                'plot': movie.get('overview', 'No plot available')[:200] + ('...' if len(movie.get('overview', '')) > 200 else ''),
                'poster': poster_url,
                'rating': str(round(movie.get('vote_average', 0), 1)),
                'type': 'movie'
            }
            results.append(formatted)
        
        # Process TV shows
        for show in tv_data.get('results', [])[:8]:
            poster_path = show.get('poster_path')
            poster_url = f"{image_base_url}{poster_path}" if poster_path else 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300&h=450&fit=crop&crop=faces'
            
            formatted = {
                'id': str(show.get('id', '')),
                'title': show.get('name', 'Unknown Title'),
                'year': show.get('first_air_date', '')[:4] if show.get('first_air_date') else 'Unknown',
                'plot': show.get('overview', 'No plot available')[:200] + ('...' if len(show.get('overview', '')) > 200 else ''),
                'poster': poster_url,
                'rating': str(round(show.get('vote_average', 0), 1)),
                'type': 'tv'
            }
            results.append(formatted)
        
        # Sort by rating (highest first)
        results.sort(key=lambda x: float(x['rating']), reverse=True)
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({
                'results': results,
                'total': len(results),
                'message': 'Popular movies and shows from TMDB'
            })
        }
        
    except requests.RequestException as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'API request failed: {str(e)}'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Internal server error: {str(e)}'})
        }