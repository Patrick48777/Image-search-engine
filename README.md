# One-Shot Image Search Engine

A semantic image search engine built with CLIP and FAISS that allows searching by text descriptions or similar images.

## Features

- **Text-to-Image Search**: Find images by describing them in natural language
- **Image-to-Image Search**: Upload an image to find visually similar ones
- **Fast Vector Search**: Uses FAISS for efficient similarity search
- **Pre-trained AI Model**: Leverages OpenAI's CLIP for understanding image content
- **Web Interface**: Clean, responsive UI built with Flask and Bootstrap

## Technologies Used

- **CLIP**: OpenAI's Contrastive Language-Image Pre-training model
- **FAISS**: Facebook AI Similarity Search for vector similarity search
- **PyTorch**: Deep learning framework
- **Flask**: Web application framework
- **Bootstrap**: Frontend styling

## Installation

1. Clone this repository:
git clone https://github.com/shubhrat12/Image-search-engine.git
cd image-search-engine
2. Create a virtual environment and install dependencies:
python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
3. Run the application:
python app.py
4. Open your browser and go to http://127.0.0.1:5000

## How It Works

1. The application uses CLIP to convert images into vector embeddings
2. These embeddings capture the semantic meaning of each image
3. When searching with text, the query is also converted to the same vector space
4. FAISS finds the most similar image vectors to your query vector
5. Results are returned based on cosine similarity scores
