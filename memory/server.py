import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from lookup import find_matching_sentences
from multiprocessing import Pool
import requests

# Load data from 'memory.json' into the memory variable
memory = {}
with open('memory.json', 'r') as file:
    memory = json.load(file)

# Initialize Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for all routes
CORS(app)

def process_entry(entry, expression):
    # Process each entry in the memory dictionary by extracting the filename and data
    filename, data = entry
    
    # Extract the English text from the data
    en_text = data['EN']['text']
    
    # Find matching sentences in the English text based on the given expression
    en_matching_sentences = find_matching_sentences(en_text, expression)
    
    # Return a list of tuples containing the filename and matching sentences
    return [(filename, sentence) for sentence in en_matching_sentences]

@app.route('/search', methods=['GET'])
def search_expression():
    # Get the expression from the query parameters
    expression = request.args.get('expression')
    if not expression:
        # Return an error message if the expression is not provided
        return jsonify({'error': 'Expression not provided.'}), 400

    matching_sentences = []

    with Pool() as pool:
        # Use multiprocessing to parallelize the search process across the memory entries
        # Map the process_entry function to each entry and expression, and store the results in the 'results' list
        results = pool.starmap(process_entry, [(entry, expression) for entry in memory.items()])
        
        # Flatten the results and store the matching sentences in the 'matching_sentences' list
        for result in results:
            matching_sentences += result

    # Create a response dictionary containing the expression and matching sentences
    response = {
        'expression': expression,
        'results': matching_sentences
    }

    # Return the response as JSON with a 200 status code
    return jsonify(response), 200

@app.route('/file', methods=['GET'])
def search_file():
    # Get the filename from the query parameters
    filename = request.args.get('filename')
    
    # Replace the "%231" in the filename with "#"
    filename = filename.replace("%231","#")
    
    if not filename:
        # Return an error message if the filename is not provided
        return jsonify({'error': 'Filename not provided.'}), 400

    # Retrieve the entry corresponding to the filename from the memory dictionary
    entry = memory[filename]

    # Return the entry as JSON with a 200 status code
    return jsonify(entry), 200

@app.route('/linguee', methods=['GET'])
def linguee_api():
    # Get the query from the query parameters
    query = request.args.get('query')
    if not query:
        # Return an error message if the query is not provided
        return jsonify({'error': 'Query not provided.'}), 400

    # Construct the URLs for querying the Linguee API for translations and external sources
    translations_url = f'https://linguee-api.fly.dev/api/v2/translations?query={query}&src=en&dst=fr&guess_direction=true&follow_corrections=always'
    external_sources_url = f'https://linguee-api.fly.dev/api/v2/external_sources?query={query}&src=en&dst=fr&guess_direction=true&follow_corrections=always'

    try:
        # Send GET requests to the Linguee API for translations and external sources
        translations_response = requests.get(translations_url)
        translations_response.raise_for_status()
        translations_api_response = translations_response.json()

        external_sources_response = requests.get(external_sources_url)
        external_sources_response.raise_for_status()
        external_sources_api_response = external_sources_response.json()

        # Return the translations and external sources as JSON with a 200 status code
        return jsonify({
            'translations': translations_api_response,
            'external_sources': external_sources_api_response
        }), 200
    except requests.exceptions.RequestException as e:
        # Return an error message if an exception occurs during the API request
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run the Flask application
    app.run()
