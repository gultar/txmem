# Python Server README

This is a Python server that receives search queries and performs fuzzy matching in a translation memory file. It provides an API for searching and retrieving data from the memory file.

## Getting Started

To use the server, follow the instructions below:

1. Clone the repository or download the source code files.
2. Ensure you have Python installed on your system (version 3.6 or higher).
3. Install the required dependencies by running the following command:

```bash
pip install flask flask_cors requests
```

4. Place your translation memory file named `memory.json` in the same directory as the server file.
   - Ensure that the memory file is properly formatted and contains the necessary data for searching.

## Running the Server

To start the server, run the following command in the terminal:

```bash
python server.py
```

Once the server is running, it will listen for incoming requests on `http://localhost:5000`.

## Endpoints

The server provides the following endpoints:

### 1. Search Endpoint (`/search`)

- **Method:** GET
- **Parameters:**
  - `expression`: The search query or expression.
- **Response:**
  - Returns a JSON response with the matching sentences found in the translation memory file.

Example usage:

```
GET http://localhost:5000/search?expression=example
```

### 2. File Endpoint (`/file`)

- **Method:** GET
- **Parameters:**
  - `filename`: The name of the file to retrieve from the translation memory.
- **Response:**
  - Returns a JSON response with the data corresponding to the requested file from the translation memory.

Example usage:

```
GET http://localhost:5000/file?filename=my_file.json
```

### 3. Linguee Endpoint (`/linguee`)

- **Method:** GET
- **Parameters:**
  - `query`: The query to search for translations and external sources using the Linguee API.
- **Response:**
  - Returns a JSON response with translations and external sources retrieved from the Linguee API.

Example usage:

```
GET http://localhost:5000/linguee?query=example
```

## Translation Memory

The translation memory file (`memory.json`) is used for fuzzy matching against search queries. Ensure that the memory file is in the correct format and contains the necessary data for searching.

If the server fails to load your `memory.json` file, make sure to use `pair.py` to align your documents and translations correctly.

## Dependencies

The server utilizes the following dependencies:

- Flask: A lightweight web framework for creating APIs.
- Flask-CORS: A Flask extension for handling Cross-Origin Resource Sharing.
- Requests: A library for making HTTP requests.

## Contributions

Contributions to the server are welcome. If you find any issues or want to add new features, please submit a pull request or open an issue on the project repository.

## License

This server is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Acknowledgements

The server utilizes an unofficial Linguee API for translations and external sources. Special thanks to https://linguee-api.fly.dev/ for providing the API.

