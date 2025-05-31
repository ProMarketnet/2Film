import json
import requests

def handler(request):
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
        api_key = '177b48eb85143a28a9aac14ec0e5a679'
        base_url = 'https://api.themoviedb.org/3'
        image_base_url = 'https://image.tmdb.org/t/p/w500'
        
        # Get popular movies
        movies_response = requests.get(
            f"{base_url}/movie/popular",
            params={'api_key': api_key}
        )
        movies_data = movies_response.json()
        
        # Get popular TV shows
        tv_response = requests.get(
            f"{base_url}/tv/popular",
            params={'api_key': api_key}
        )
        tv_data = tv_response.json()
        
        results = []
        
        # Process movies
        for movie in movies_data.get('results', [])[:8]:
            poster_url = f"{image_base_url}{movie.get('poster_path')}" if movie.get('poster_path') else 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300&h=450&fit=crop'
            
            formatted = {
                'id': str(movie.get('id', '')),
                'title': movie.get('title', 'Unknown'),
                'year': movie.get('release_date', '')[:4],
                'plot': movie.get('overview', 'No plot available'),
                'poster': poster_url,
                'rating': str(movie.get('vote_average', 0)),
                'genre': 'Various',
                'type': 'movie'
            }
            results.append(formatted)
        
        # Process TV shows
        for show in tv_data.get('results', [])[:8]:
            poster_url = f"{image_base_url}{show.get('poster_path')}" if show.get('poster_path') else 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300&h=450&fit=crop'
            
            formatted = {
                'id': str(show.get('id', '')),
                'title': show.get('name', 'Unknown'),
                'year': show.get('first_air_date', '')[:4],
                'plot': show.get('overview', 'No plot available'),
                'poster': poster_url,
                'rating': str(show.get('vote_average', 0)),
                'genre': 'Various',
                'type': 'tv'
            }
            results.append(formatted)
        
        # Sort by rating
        results.sort(key=lambda x: float(x['rating']), reverse=True)
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'results': results,
                'total': len(results),
                'message': 'Popular movies and shows'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }