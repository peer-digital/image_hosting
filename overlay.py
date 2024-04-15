import requests
from PIL import Image
from io import BytesIO
import subprocess


def download_image(image_url):
    response = requests.get(image_url)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    return Image.open(BytesIO(response.content))

def calculate_resize_dimensions(image, max_width, max_height):
    original_width, original_height = image.size
    width_ratio = max_width / original_width
    height_ratio = max_height / original_height
    min_ratio = min(width_ratio, height_ratio)
    new_width = int(original_width * min_ratio)
    new_height = int(original_height * min_ratio)
    return new_width, new_height


def add_book_cover_to_mockup(mockup_url, cover_urls, output_path, areas, fill_percent=0.8):
    mockup = download_image(mockup_url)
    if mockup.mode != 'RGBA':
        mockup = mockup.convert('RGBA')

    for cover_url, (x1, y1, x2, y2) in zip(cover_urls, areas):
        cover = download_image(cover_url)
        if cover.mode != 'RGBA':
            cover = cover.convert('RGBA')

        # Calculate the maximum dimensions for the cover
        max_width = (x2 - x1) * fill_percent
        max_height = (y2 - y1) * fill_percent
        new_width, new_height = calculate_resize_dimensions(cover, max_width, max_height)

        # Resize the cover to the new dimensions
        cover = cover.resize((new_width, new_height), Image.LANCZOS)

        # Calculate the new top-left position to center the cover in the area
        new_x = x1 + (x2 - x1 - new_width) // 2
        new_y = y1 + (y2 - y1 - new_height) // 2

        # Paste the resized and centered cover image onto the mockup
        mockup.paste(cover, (new_x, new_y), cover)

    mockup.save(output_path, 'PNG')
    return output_path

# Correct coordinates for each area
areas = [
    (406, 2067, 1014, 2851),
    (1230, 2066, 1838, 2849),
    (2066, 2063, 2662, 2858)
]


# Example usage with new coordinates
mockup_output = add_book_cover_to_mockup(
  mockup_url='https://peer-digital.github.io/image_hosting/base_image.png',
      cover_urls=[
        'https://www.myrorna.se/app/uploads/561884043_64bf4fd0-819b-4c6b-9a84-0a82c7581a07.jpg',  # URL to the first book cover
        'https://img.tradera.net/large-fit/703/561887703_f382ab3d-2bee-42fe-a2c4-9cd079d0795c.jpg',  # URL to the second book cover
        'https://www.myrorna.se/app/uploads/561892632_f966364d-f40e-4f19-846e-0ef2588b1cb9.jpg'   # URL to the third book cover
    ],
    output_path='myrorna.png',  # Path where the final image will be saved
    areas=areas  # The list of areas where each book cover should be placed
)

print(f"Updated mockup saved to {mockup_output}")







