import json
import requests

def handler(request):
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': ''
        }
    
    # Only allow POST requests
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Parse request body
        if hasattr(request, 'body'):
            body = request.body
        else:
            body = request.get('body', '')
            
        if isinstance(body, bytes):
            body = body.decode('utf-8')
            
        data = json.loads(body)
        query = data.get('query', '').strip()
        
        if not query:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Search query cannot be empty'})
            }
        
        # TMDB API configuration
        api_key = '177b48eb85143a28a9aac14ec0e5a679'
        base_url = 'https://api.themoviedb.org/3'
        image_base_url = 'https://image.tmdb.org/t/p/w500'
        
        # Search TMDB
        response = requests.get(
            f"{base_url}/search/multi",
            params={'api_key': api_key, 'query': query},
            timeout=10
        )
        response.raise_for_status()
        tmdb_data = response.json()
        
        # Format results
        results = []
        for item in tmdb_data.get('results', [])[:15]:
            if item.get('media_type') in ['movie', 'tv']:
                # Get poster URL
                poster_path = item.get('poster_path')
                poster_url = f"{image_base_url}{poster_path}" if poster_path else 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300&h=450&fit=crop&crop=faces'
                
                # Format movie/TV data
                formatted = {
                    'id': str(item.get('id', '')),
                    'title': item.get('title') or item.get('name', 'Unknown Title'),
                    'year': (item.get('release_date') or item.get('first_air_date', ''))[:4] if (item.get('release_date') or item.get('first_air_date')) else 'Unknown',
                    'plot': item.get('overview', 'No plot available')[:200] + ('...' if len(item.get('overview', '')) > 200 else ''),
                    'poster': poster_url,
                    'rating': str(round(item.get('vote_average', 0), 1)),
                    'type': item.get('media_type', 'movie')
                }
                results.append(formatted)
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({
                'query': query,
                'results': results,
                'total': len(results),
                'message': f"Found {len(results)} results for '{query}'"
            })
        }
        
    except requests.RequestException as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'API request failed: {str(e)}'})
        }
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Invalid JSON in request body'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Internal server error: {str(e)}'})
        }