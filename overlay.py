from PIL import Image
from io import BytesIO
import requests
import subprocess

def download_image(image_url: str) -> Image:
    """Download an image from a URL and return a PIL Image object."""
    response = requests.get(image_url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))

def calculate_resize_dimensions(image: Image, max_width: int, max_height: int) -> tuple:
    """Calculate new dimensions for resizing an image while maintaining aspect ratio."""
    original_width, original_height = image.size
    width_ratio = max_width / original_width
    height_ratio = max_height / original_height
    min_ratio = min(width_ratio, height_ratio)
    return int(original_width * min_ratio), int(original_height * min_ratio)

def add_book_cover_to_mockup(mockup_url: str, cover_urls: list, output_path: str, areas: list, fill_percent: float = 0.8) -> str:
    """Composite book covers onto a mockup image and save the result."""
    mockup = download_image(mockup_url).convert('RGBA')
    for cover_url, (x1, y1, x2, y2) in zip(cover_urls, areas):
        cover = download_image(cover_url).convert('RGBA')
        max_width = (x2 - x1) * fill_percent
        max_height = (y2 - y1) * fill_percent
        new_width, new_height = calculate_resize_dimensions(cover, max_width, max_height)
        cover = cover.resize((new_width, new_height), Image.LANCZOS)
        new_x = x1 + (x2 - x1 - new_width) // 2
        new_y = y1 + (y2 - y1 - new_height) // 2
        mockup.paste(cover, (new_x, new_y), cover)
    
    # Save the final image to a BytesIO object
    bytes_io = BytesIO()
    mockup.save(bytes_io, format='PNG')
    bytes_io.seek(0)  # Rewind the file-like object

    # Compress the image using pngquant through subprocess piping
    process = subprocess.Popen([
        'pngquant', 
        '--force', 
        '--speed', '1',  # Adjust speed for a balance of compression quality and speed
        '--quality', '70-100',  # Set a more aggressive quality range
        '--colors', '256',  # Reduce the number of colors
        '--skip-if-larger',  # Skip compression if it results in a larger file
        '-', 
        '--output', output_path],
        stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    _, errors = process.communicate(bytes_io.getvalue())
    if process.returncode != 0:
        raise RuntimeError(f"pngquant failed: {errors.decode()}")

    return output_path

# Example usage remains the same.


# Correct coordinates for each area
areas = [
    (316, 1404, 728, 1936),  # Updated from coords="316,1404,728,1936"
    (830, 1405, 1243, 1936), # Updated from coords="830,1405,1243,1936"
    (1345, 1405, 1760, 1941) # Updated from coords="1345,1405,1760,1941"
]




# Example usage remains the same.
mockup_output = add_book_cover_to_mockup(
    mockup_url='https://peer-digital.github.io/image_hosting/base_image.png',
    cover_urls=[
        'https://s2.adlibris.com/images/69134732/sista-bilden.jpg',
        'https://s1.adlibris.com/images/68318876/far-inte-till-havet.jpg',
        'https://s2.adlibris.com/images/68370795/rummet-i-jorden.jpg'
    ],
    output_path='.png',
    areas=areas
)

print(f"Updated mockup saved to {mockup_output}")
