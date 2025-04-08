import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from clip_encoder import ClipEncoder
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize the CLIP encoder
encoder = ClipEncoder()

# Check if the index file exists, otherwise create it
if os.path.exists('clip_search_index.pkl'):
    encoder.load_index()
else:
    # Build the index from images in the static/images directory
    encoder.encode_images('static/images')
    encoder.save_index()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if 'text_query' in request.form:
        # Text-based search
        query = request.form['text_query']
        if not query:
            return redirect(url_for('index'))
        
        start_time = time.time()
        results = encoder.search(query, k=12)
        search_time = time.time() - start_time
        
        # Convert image paths to web paths
        for result in results:
            result['image_url'] = '/' + result['image_path'].replace('\\', '/')
        
        return render_template('results.html', 
                               query=query, 
                               results=results, 
                               search_type="text", 
                               search_time=search_time)
    
    elif 'image_query' in request.files:
        # Image-based search
        file = request.files['image_query']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            start_time = time.time()
            results = encoder.search_by_image(file_path, k=12)
            search_time = time.time() - start_time
            
            # Convert image paths to web paths
            query_image_url = url_for('static', filename=f'uploads/{filename}')
            for result in results:
                result['image_url'] = '/' + result['image_path'].replace('\\', '/')
            
            return render_template('results.html', 
                                   query_image=query_image_url, 
                                   results=results, 
                                   search_type="image", 
                                   search_time=search_time)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)