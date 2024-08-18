# MOVIE-FY

MOVIE-FY is a web application that recommends movies based on user preferences. The application uses a responsive design and provides users with the ability to search for movies and receive personalized recommendations.




https://github.com/user-attachments/assets/214f1070-5b47-45f4-8375-cd8b4ecb9eb6


## AI Methodology

MOVIE-FY leverages a Content-Based Filtering technique to recommend movies. This method uses the following approach:

- **Data Preprocessing**: The movie data is cleaned and preprocessed, focusing on important features like genres, cast, directors, and keywords.
- **Vectorization**: The textual data (like genres and keywords) is converted into numerical vectors using techniques like TF-IDF (Term Frequency-Inverse Document Frequency).
- **Cosine Similarity**: The similarity between movies is calculated using the cosine similarity metric, which helps in finding movies that are most similar to a given movie.
- **Recommendation**: Based on the similarity scores, a list of top N movies similar to the selected movie is generated and presented to the user.


## Project Structure

```plaintext
MOVIE-FY/
│
├── data/                      # Directory for storing datasets or any other data files

├── models/                    # Directory for storing models or any backend logic
│   ├── movies.pkl             # Pickle file containing movie data
│   └── similarity.pkl         # Pickle file containing similarity data
│
├── static/                    # Directory for all static files (CSS, JS, Images, etc.)
│   ├── css/                   # Contains all CSS files
│   ├── js/                    # Contains all JavaScript files

│
├── templates/                 # Contains all HTML templates
│
├── .gitattributes             # Git attributes configuration
├── .gitignore                 # Git ignore file for excluding files from version control
├── app.py                     # Main application file
└── README.md                  # Project documentation file'
```
# MOVIE-FY

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/MOVIE-FY.git
   cd MOVIE-FY
   ```

2. Install dependencies:
   Ensure you have Python installed. Then install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Access the application:
   Open your web browser and go to http://127.0.0.1:5000/.

## Usage
- **AI-Powered Recommendations**: Utilizes Content-Based Filtering and Cosine Similarity for providing personalized movie recommendations.
- **Homepage**: The homepage provides a starting point for the user to explore the application.
- **Recommendation Page**: Users can select a movie and get recommendations based on their preferences.
- **Movie Page**: Detailed information about the selected movie, including related recommendations.

## File Structure

- `app.py`: This is the main Flask application that handles routing and rendering of templates.
- `static/css/*.css`: These files contain all the custom CSS used for styling the different pages of the application.
- `static/js/*.js`: These files contain JavaScript used for interactivity and functionality specific to different pages.
- `templates/`: This directory contains all the HTML files that define the structure and content of the website pages.

## Features
- Utilizes Content-Based Filtering and Cosine Similarity for providing personalized movie recommendations
- Responsive design using Tailwind CSS.
- Movie recommendations based on user input.
- A loader animation to enhance user experience during navigation.
- Back to Homepage button for easy navigation.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -a 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
