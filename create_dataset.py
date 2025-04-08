import os
import requests
from PIL import Image
from io import BytesIO
from tqdm import tqdm
import time

# Create directories
os.makedirs("static/images", exist_ok=True)

# Resume-perfect dataset with diverse categories that will impress recruiters
image_urls = [
    # Nature/Landscapes (10 images)
    {"url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb", "filename": "landscape_mountain.jpg", "category": "nature"},
    {"url": "https://images.unsplash.com/photo-1501785888041-af3ef285b470", "filename": "landscape_sunset.jpg", "category": "nature"},
    {"url": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e", "filename": "landscape_forest.jpg", "category": "nature"},
    {"url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05", "filename": "landscape_valley.jpg", "category": "nature"},
    {"url": "https://images.unsplash.com/photo-1587923623987-898d649f2eca", "filename": "beachside_sunset.jpg", "category": "nature"},
    {"url": "https://images.unsplash.com/photo-1528184039930-bd03972bd974", "filename": "mountains_snow.jpg", "category": "nature"},
    {"url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e", "filename": "tropical_beach.jpg", "category": "nature"},
    {"url": "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1", "filename": "autumn_leaves.jpg", "category": "nature"},
    {"url": "https://images.unsplash.com/photo-1490730141103-6cac27aaab94", "filename": "sunset_water.jpg", "category": "nature"},
    {"url": "https://images.unsplash.com/photo-1546514355-7fdc90ccbd03", "filename": "starry_night.jpg", "category": "nature"},
    
    # Animals (10 images)
    {"url": "https://images.unsplash.com/photo-1552053831-71594a27632d", "filename": "dog_golden.jpg", "category": "animals"},
    {"url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1", "filename": "dog_puppy.jpg", "category": "animals"},
    {"url": "https://images.unsplash.com/photo-1561037404-61cd46aa615b", "filename": "cat_tabby.jpg", "category": "animals"},
    {"url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba", "filename": "cat_eyes.jpg", "category": "animals"},
    {"url": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46", "filename": "tiger_closeup.jpg", "category": "animals"},
    {"url": "https://images.unsplash.com/photo-1546182990-dffeafbe841d", "filename": "lion_mane.jpg", "category": "animals"},
    {"url": "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7", "filename": "panda_eating.jpg", "category": "animals"},
    {"url": "https://images.unsplash.com/photo-1437622368342-7a3d73a34c8f", "filename": "turtle_swimming.jpg", "category": "animals"},
    {"url": "https://images.unsplash.com/photo-1516934024742-b461fba47600", "filename": "zebra_stripes.jpg", "category": "animals"},
    {"url": "https://images.unsplash.com/photo-1463852247062-1bbca38f7805", "filename": "flamingo_pink.jpg", "category": "animals"},
    
    # Architecture (10 images)
    {"url": "https://images.unsplash.com/photo-1499092346589-b9b6be3e94b2", "filename": "building_modern.jpg", "category": "architecture"},
    {"url": "https://images.unsplash.com/photo-1486728297118-82a07bc48a28", "filename": "building_tall.jpg", "category": "architecture"},
    {"url": "https://images.unsplash.com/photo-1534067783941-51c9c23ecefd", "filename": "bridge_suspension.jpg", "category": "architecture"},
    {"url": "https://images.unsplash.com/photo-1546640646-89b557854b18", "filename": "bridge_wooden.jpg", "category": "architecture"},
    {"url": "https://images.unsplash.com/photo-1533929736458-ca588d08c8be", "filename": "opera_house.jpg", "category": "architecture"},
    {"url": "https://images.unsplash.com/photo-1496564203457-11bb12075d90", "filename": "empire_state.jpg", "category": "architecture"},
    {"url": "https://images.unsplash.com/photo-1491555103944-7c647fd857e6", "filename": "landmark_tower.jpg", "category": "architecture"},
    {"url": "https://images.unsplash.com/photo-1601893217108-846bdacb73e2", "filename": "building_classic.jpg", "category": "architecture"},
    {"url": "https://images.unsplash.com/photo-1560748952-1d2d768c2337", "filename": "temple_ancient.jpg", "category": "architecture"},
    {"url": "https://images.unsplash.com/photo-1548115184-bc6544d06a58", "filename": "cathedral_gothic.jpg", "category": "architecture"},
    
    # Food (10 images)
    {"url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1", "filename": "food_pasta.jpg", "category": "food"},
    {"url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38", "filename": "food_pizza.jpg", "category": "food"},
    {"url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836", "filename": "food_steak.jpg", "category": "food"},
    {"url": "https://images.unsplash.com/photo-1606787366850-de6330128bfc", "filename": "food_hamburger.jpg", "category": "food"},
    {"url": "https://images.unsplash.com/photo-1541745537411-b8046dc6d66c", "filename": "sushi_plate.jpg", "category": "food"},
    {"url": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445", "filename": "pancakes_berries.jpg", "category": "food"},
    {"url": "https://images.unsplash.com/photo-1514326640560-7d063ef2aed5", "filename": "dessert_cake.jpg", "category": "food"},
    {"url": "https://images.unsplash.com/photo-1563897539064-7f6d6ccb9f1d", "filename": "dessert_cupcake.jpg", "category": "food"},
    {"url": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe", "filename": "fresh_salad.jpg", "category": "food"},
    {"url": "https://images.unsplash.com/photo-1560717845-968823efbee1", "filename": "breakfast_toast.jpg", "category": "food"},
    
    # Technology (10 images)
    {"url": "https://images.unsplash.com/photo-1531297484001-80022131f5a1", "filename": "tech_laptop.jpg", "category": "technology"},
    {"url": "https://images.unsplash.com/photo-1516387938699-a93567ec168e", "filename": "tech_smartphone.jpg", "category": "technology"},
    {"url": "https://images.unsplash.com/photo-1588508065123-287b28e013da", "filename": "tech_tablet.jpg", "category": "technology"},
    {"url": "https://images.unsplash.com/photo-1594731795081-a18959624c9b", "filename": "tech_computer.jpg", "category": "technology"},
    {"url": "https://images.unsplash.com/photo-1585298723682-7115561c51b7", "filename": "tech_drone.jpg", "category": "technology"},
    {"url": "https://images.unsplash.com/photo-1573739022854-abceaeb585dc", "filename": "tech_robot.jpg", "category": "technology"},
    {"url": "https://images.unsplash.com/photo-1535303311164-664fc9ec6532", "filename": "tech_vr.jpg", "category": "technology"},
    {"url": "https://images.unsplash.com/photo-1505236273555-17e947908c0e", "filename": "tech_camera.jpg", "category": "technology"},
    {"url": "https://images.unsplash.com/photo-1551808525-51a94da548ce", "filename": "tech_server.jpg", "category": "technology"},
    {"url": "https://images.unsplash.com/photo-1601388127816-1fec582b3512", "filename": "tech_circuit.jpg", "category": "technology"}
]

# Download images with a progress bar
print(f"Downloading {len(image_urls)} images for your resume project...")
for img in tqdm(image_urls):
    try:
        response = requests.get(img["url"])
        image = Image.open(BytesIO(response.content))
        
        # Save the image
        filepath = f"static/images/{img['filename']}"
        image.save(filepath)
        
        # Brief pause to be nice to the server
        time.sleep(0.2)
    except Exception as e:
        print(f"Error downloading {img['filename']}: {e}")

print(f"\nDownloaded {len(image_urls)} images to static/images/")
print("Your resume-perfect dataset is ready! This diverse collection will showcase your image search capabilities effectively.")