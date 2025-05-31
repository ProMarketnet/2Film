import json
import os
import requests

def handler(request):
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
    
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        data = json.loads(request.body)
        query = data.get('query', '').strip()
        
        if not query:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Search query cannot be empty'})
            }
        
        api_key = '177b48eb85143a28a9aac14ec0e5a679'
        base_url = 'https://api.themoviedb.org/3'
        image_base_url = 'https://image.tmdb.org/t/p/w500'
        
        response = requests.get(
            f"{base_url}/search/multi",
            params={'api_key': api_key, 'query': query}
        )
        tmdb_data = response.json()
        
        results = []
        for item in tmdb_data.get('results', [])[:10]:
            if item.get('media_type') in ['movie', 'tv']:
                poster_url = f"{image_base_url}{item.get('poster_path')}" if item.get('poster_path') else 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300&h=450&fit=crop'
                
                formatted = {
                    'id': str(item.get('id', '')),
                    'title': item.get('title') or item.get('name', 'Unknown'),
                    'year': (item.get('release_date') or item.get('first_air_date', ''))[:4],
                    'plot': item.get('overview', 'No plot available'),
                    'poster': poster_url,
                    'rating': str(item.get('vote_average', 0)),
                    'genre': 'Various',
                    'type': item.get('media_type', 'movie')
                }
                results.append(formatted)
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'query': query,
                'results': results,
                'total': len(results),
                'message': f"Found {len(results)} results for '{query}'"
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }