import requests
from PIL import Image
from io import BytesIO

import requests
from PIL import Image, ImageOps
from io import BytesIO

def download_image(image_url):
    """
    Download an image from a URL.
    :param image_url: str, URL of the image to be downloaded.
    :return: Image, the downloaded image.
    """
    response = requests.get(image_url)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    return Image.open(BytesIO(response.content))

def add_book_cover_to_mockup(mockup_url, cover_urls, output_path, areas):
    """
    Download book covers from URLs, resize them to fit specified areas while maintaining aspect ratio,
    and overlay them onto a mockup image.
    :param mockup_url: str, URL of the original mockup image.
    :param cover_urls: list, URLs of the book cover images.
    :param output_path: str, path to save the final image.
    :param areas: list of tuples, each tuple contains coordinates (x1, y1, x2, y2) defining an area.
    :return: str, path to the output image.
    """
    # Download the mockup image
    mockup = download_image(mockup_url)
    if mockup.mode != 'RGBA':
        mockup = mockup.convert('RGBA')  # Convert to RGBA if not already

    # Overlay each book cover onto the mockup
    for cover_url, (x1, y1, x2, y2) in zip(cover_urls, areas):
        # Download the book cover image
        cover = download_image(cover_url)
        if cover.mode != 'RGBA':
            cover = cover.convert('RGBA')  # Convert to RGBA if not already
        
        # Calculate the size to resize the cover to fit the area while maintaining aspect ratio
        area_width, area_height = x2 - x1, y2 - y1
        cover.thumbnail((area_width, area_height), Image.LANCZOS)  # Resize image within the area bounds

        # Calculate new position to center the image in the designated area
        cover_width, cover_height = cover.size
        new_x = x1 + (area_width - cover_width) // 2
        new_y = y1 + (area_height - cover_height) // 2

        # Create a mask for transparency handling
        mask = cover if 'A' in cover.getbands() else None

        # Paste the book cover image onto the mockup at the newly calculated position
        mockup.paste(cover, (new_x, new_y), mask)

    # Save the updated mockup as PNG to preserve transparency
    mockup.save(output_path, 'PNG')

    return output_path

# Example usage
mockup_output = add_book_cover_to_mockup(
    mockup_url='https://peer-digital.github.io/image_hosting/base_image.png',
    cover_urls=[
        'https://bilder.akademibokhandeln.se/images_akb/9789189820692_383/omgiven-av-lognare',  # URL to the first book cover
        'https://bilder.akademibokhandeln.se/images_akb/9789189820692_383/omgiven-av-lognare',  # URL to the second book cover
        'https://bilder.akademibokhandeln.se/images_akb/9789189820692_383/omgiven-av-lognare'   # URL to the third book cover
    ],
    output_path='final_mockup_with_covers.png',
    areas=[(36, 150, 78, 199), (107, 150, 149, 199), (178, 150, 220, 199)]
)

print(f"Updated mockup saved to {mockup_output}")






