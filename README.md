# Translation Memory Interface

This is a React application that serves as a user interface for a translation memory system. It connects to a local Python API that provides translation segments and related files. The application allows users to search for translation segments, view search results, and access additional information from Linguee.

## Features

The translation memory interface includes the following features:

- Search Form: Users can enter a query to search for translation segments.
- Navigation: The navigation bar provides a convenient way to submit search queries.
- Search Results: Displays the search results obtained from the Python API.
- Active Text: Shows the selected source and target texts, with a highlighted segment.
- Linguee Integration: Retrieves additional information from Linguee related to the search query.

## Getting Started

To use the translation memory interface, follow these steps:

1. Ensure you have the necessary dependencies installed, including Node.js and npm.

2. Clone the project repository to your local machine.

3. Install the project dependencies by running the following command:

   ```
   npm install
   ```

4. Start the React development server with the following command:

   ```
   npm start
   ```

5. Access the application by opening a web browser and navigating to `http://localhost:3000`.

## Usage

1. Enter your search query in the Search Form.

2. Press the Enter key or click the search button to submit the query.

3. The application will communicate with the local Python API to fetch the search results.

4. Once the results are retrieved, they will be displayed in the Search Results component.

5. Click on a file in the search results to view the corresponding source and target texts in the Active Text component.

6. The found segment will be highlighted in the Active Text component.

7. To scroll to the highlighted segment, click the "Scroll to Segment" button.

8. Additional information from Linguee related to the search query will be displayed in the Linguee component.

## Configuration

The application is configured to communicate with the local Python API hosted at `http://localhost:5000`. Ensure that the API is running and accessible before using the application. If your API is hosted on a different address or port, you can modify the API URL in the following lines of code in the `App.js` file:

```javascript
const response = await fetch(`http://localhost:5000/search?expression=${query}`);
```

```javascript
const response = await fetch(`http://localhost:5000/file?filename=${filename}`);
```

## Troubleshooting

- If you encounter any errors or issues while running the application, make sure you have followed the setup steps correctly and that all dependencies are properly installed.

- If the application fails to communicate with the Python API, ensure that the API is running and accessible. Check the API URL configuration in the `App.js` file.

- For any other problems or inquiries, please refer to the documentation or leave an issue on the git repo.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- This application was built using React, and it makes use of various open-source libraries and components. Special thanks to the open-source community for their contributions.