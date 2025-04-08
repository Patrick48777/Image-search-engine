import torch
from PIL import Image
import os
from transformers import CLIPProcessor, CLIPModel
import numpy as np
import faiss
import pickle
import time

class ClipEncoder:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Load CLIP model
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        
        # Initialize FAISS index
        self.dimension = 512  # CLIP embedding dimension
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
        
        # Store mapping of indices to image paths
        self.image_paths = []
    
    def encode_images(self, image_dir):
        """Encode all images in the directory and build the FAISS index"""
        start_time = time.time()
        print(f"Starting to encode images from {image_dir}...")
        
        image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        all_embeddings = []
        
        for img_path in image_paths:
            try:
                image = Image.open(img_path).convert('RGB')
                inputs = self.processor(images=image, return_tensors="pt").to(self.device)
                
                with torch.no_grad():
                    image_features = self.model.get_image_features(**inputs)
                    image_embeddings = image_features.cpu().numpy()
                
                # Normalize embeddings
                image_embeddings = image_embeddings / np.linalg.norm(image_embeddings, axis=1, keepdims=True)
                
                all_embeddings.append(image_embeddings[0])
                self.image_paths.append(img_path)
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
        
        # Add all embeddings to the FAISS index
        if all_embeddings:
            all_embeddings_array = np.array(all_embeddings).astype('float32')
            self.index.add(all_embeddings_array)
            print(f"Added {len(all_embeddings)} images to the index")
        else:
            print("No images were successfully encoded")
        
        elapsed_time = time.time() - start_time
        print(f"Encoding completed in {elapsed_time:.2f} seconds")
    
    def encode_text(self, text):
        """Encode text query using CLIP"""
        inputs = self.processor(text=text, return_tensors="pt", padding=True).to(self.device)
        
        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs)
            text_embeddings = text_features.cpu().numpy()
        
        # Normalize embeddings
        text_embeddings = text_embeddings / np.linalg.norm(text_embeddings, axis=1, keepdims=True)
        
        return text_embeddings
    
    def search(self, query, k=8):
        """Search for similar images using text query"""
        text_embedding = self.encode_text(query)
        scores, indices = self.index.search(text_embedding.astype('float32'), k)
        
        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx != -1:  # Valid index
                results.append({
                    'image_path': self.image_paths[idx],
                    'score': float(score),
                    'filename': os.path.basename(self.image_paths[idx])
                })
        
        return results
    
    def encode_query_image(self, image_path):
        """Encode query image using CLIP"""
        image = Image.open(image_path).convert('RGB')
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)
            image_embeddings = image_features.cpu().numpy()
        
        # Normalize embeddings
        image_embeddings = image_embeddings / np.linalg.norm(image_embeddings, axis=1, keepdims=True)
        
        return image_embeddings
    
    def search_by_image(self, image_path, k=8):
        """Search for similar images using an image query"""
        image_embedding = self.encode_query_image(image_path)
        scores, indices = self.index.search(image_embedding.astype('float32'), k)
        
        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx != -1:  # Valid index
                results.append({
                    'image_path': self.image_paths[idx],
                    'score': float(score),
                    'filename': os.path.basename(self.image_paths[idx])
                })
        
        return results
    
    def save_index(self, filename="clip_search_index.pkl"):
        """Save the index and image paths to a file"""
        with open(filename, 'wb') as f:
            pickle.dump({
                'index': faiss.serialize_index(self.index),
                'image_paths': self.image_paths
            }, f)
        print(f"Index saved to {filename}")
    
    def load_index(self, filename="clip_search_index.pkl"):
        """Load the index and image paths from a file"""
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            self.index = faiss.deserialize_index(data['index'])
            self.image_paths = data['image_paths']
        print(f"Loaded index with {len(self.image_paths)} images")