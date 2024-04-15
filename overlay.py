import requests
from PIL import Image
from io import BytesIO

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
    (314, 1720, 766, 2269),
    (889, 1720, 1346, 2271),
    (1472, 1716, 1925, 2270)
]


# Example usage with new coordinates
mockup_output = add_book_cover_to_mockup(
  mockup_url='https://peer-digital.github.io/image_hosting/base_image.png',
      cover_urls=[
        'https://bilder.akademibokhandeln.se/images_akb/9789189820692_383/omgiven-av-lognare',  # URL to the first book cover
        'https://dyson-h.assetsadobe2.com/is/image/content/dam/dyson/images/products/hero/447002-01.png?$responsive$&cropPathE=desktop&fit=stretch,1&wid=960',  # URL to the second book cover
        'https://img01.ztat.net/article/spp-media-p1/bb09f307007d4a9ba130fadcae69e2ea/351b85e5913d4c46956b0eba790030c1.jpg?imwidth=1800&filter=packshot'   # URL to the third book cover
    ],
    output_path='final_mockup_with_covers.png',  # Path where the final image will be saved
    areas=areas  # The list of areas where each book cover should be placed
)

print(f"Updated mockup saved to {mockup_output}")







