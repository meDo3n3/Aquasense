"""
Cloudinary Helper Utility for AquaSense Project

This script helps upload images from the local static directory to Cloudinary
and provides helper functions for managing images on Cloudinary CDN.
"""

import os
import cloudinary
import cloudinary.uploader
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

# Base directory for images
BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / 'reservations' / 'static' / 'reservations' / 'images'


def upload_image(image_path, public_id=None):
    """
    Upload a single image to Cloudinary
    
    Args:
        image_path: Path to the image file
        public_id: Optional custom public ID for the image
    
    Returns:
        dict: Upload result containing URL and other metadata
    """
    try:
        if public_id is None:
            # Use filename without extension as public_id
            public_id = Path(image_path).stem
        
        result = cloudinary.uploader.upload(
            image_path,
            public_id=f"aquasense/{public_id}",
            folder="aquasense",
            overwrite=True,
            resource_type="image"
        )
        
        print(f"✓ Uploaded: {image_path} -> {result['secure_url']}")
        return result
    except Exception as e:
        print(f"✗ Failed to upload {image_path}: {str(e)}")
        return None


def upload_all_images():
    """
    Upload all images from the static images directory to Cloudinary
    
    Returns:
        dict: Mapping of filename to Cloudinary URL
    """
    if not IMAGES_DIR.exists():
        print(f"Error: Images directory not found at {IMAGES_DIR}")
        return {}
    
    image_mapping = {}
    image_files = list(IMAGES_DIR.glob('*.jpg')) + list(IMAGES_DIR.glob('*.png'))
    
    print(f"\nUploading {len(image_files)} images to Cloudinary...\n")
    
    for image_path in image_files:
        result = upload_image(str(image_path))
        if result:
            image_mapping[image_path.name] = result['secure_url']
    
    print(f"\n✓ Successfully uploaded {len(image_mapping)} images")
    print("\nImage URL Mapping:")
    print("-" * 80)
    for filename, url in image_mapping.items():
        print(f"{filename:30} -> {url}")
    
    return image_mapping


def get_cloudinary_url(public_id, transformations=None):
    """
    Generate a Cloudinary URL for an image with optional transformations
    
    Args:
        public_id: Public ID of the image on Cloudinary
        transformations: Optional dict of transformations (width, height, crop, quality, etc.)
    
    Returns:
        str: Cloudinary URL
    """
    from cloudinary import CloudinaryImage
    
    if transformations:
        return CloudinaryImage(f"aquasense/{public_id}").build_url(**transformations)
    else:
        return CloudinaryImage(f"aquasense/{public_id}").build_url()


if __name__ == "__main__":
    print("=" * 80)
    print("AquaSense - Cloudinary Image Upload Utility")
    print("=" * 80)
    
    # Check if credentials are configured
    if not all([
        os.getenv('CLOUDINARY_CLOUD_NAME'),
        os.getenv('CLOUDINARY_API_KEY'),
        os.getenv('CLOUDINARY_API_SECRET')
    ]):
        print("\n⚠ Error: Cloudinary credentials not found in .env file")
        print("Please add the following to your .env file:")
        print("  CLOUDINARY_CLOUD_NAME=your_cloud_name")
        print("  CLOUDINARY_API_KEY=your_api_key")
        print("  CLOUDINARY_API_SECRET=your_api_secret")
        exit(1)
    
    # Upload all images
    upload_all_images()
    
    print("\n" + "=" * 80)
    print("Upload complete! You can now update your templates with Cloudinary URLs.")
    print("=" * 80)
