# Book Recommender System

A Flask-based book recommendation system using collaborative filtering and content-based recommendations.

## Setup Instructions

1. Clone the repository:
```bash
git clone <your-repo-url>
cd book_recommendor
```

2. Create a virtual environment:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Unix/MacOS:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Ensure data files are in place:
- Place `books.csv` and `ratings.csv` in the `data/` directory

5. Run the application:
### Development mode:
```bash
python app.py
```

### Production mode:
```bash
gunicorn app:app
```

## Project Structure
```
book_recommendor/
├── data/
│   ├── books.csv
│   └── ratings.csv
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   └── js/
├── app.py
├── requirements.txt
└── README.md
```

## Features
- Book recommendations based on title and author similarity
- Search functionality for books
- Popular books listing
- Real-time recommendations

## Deployment
For permanent deployment, you can:
1. Deploy on a cloud platform (Heroku, AWS, etc.)
2. Run as a system service using systemd
3. Use Docker for containerization

## Maintenance
- Regularly update the book database
- Monitor system performance
- Backup data periodically 