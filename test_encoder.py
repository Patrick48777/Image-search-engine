from clip_encoder import ClipEncoder
import time

def main():
    # Initialize the encoder
    encoder = ClipEncoder()
    
    # Encode the images in the static/images directory
    encoder.encode_images('static/images')
    
    # Save the index
    encoder.save_index()
    
    # Test a text search
    print("\nTesting text search...")
    query = "a beautiful landscape"
    results = encoder.search(query, k=3)
    
    print(f"Top 3 results for '{query}':")
    for i, result in enumerate(results):
        print(f"{i+1}. {result['filename']} (score: {result['score']:.3f})")
    
    # If there are results, test image search with the first result
    if results:
        print("\nTesting image search...")
        image_path = results[0]['image_path']
        image_results = encoder.search_by_image(image_path, k=3)
        
        print(f"Top 3 similar images to {results[0]['filename']}:")
        for i, result in enumerate(image_results):
            print(f"{i+1}. {result['filename']} (score: {result['score']:.3f})")

if __name__ == "__main__":
    main()