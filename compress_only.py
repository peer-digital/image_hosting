from PIL import Image
from io import BytesIO
import subprocess

def compress_image(input_path: str, output_path: str) -> str:
    """
    Compresses an image using pngquant with specific settings and saves the compressed image.

    Args:
        input_path (str): The file path of the image to compress.
        output_path (str): The file path to save the compressed image.

    Returns:
        str: The file path of the compressed image.
    """
    # Open the image from the given file path
    with Image.open(input_path) as img:
        # Save the image to a BytesIO object to pipe to pngquant
        bytes_io = BytesIO()
        img.save(bytes_io, format='PNG')
        bytes_io.seek(0)  # Rewind the file-like object

        # Set up the subprocess with pngquant command
        process = subprocess.Popen([
            'pngquant',
            '--force',  # Force overwrite of existing output files
            '--speed', '1',  # Adjust speed for a balance of compression quality and speed
            '--quality', '70-100',  # Set a more aggressive quality range
            '--colors', '256',  # Reduce the number of colors
            '--skip-if-larger',  # Skip compression if it results in a larger file
            '-',  # Read image from stdin
            '--output', output_path  # Output file path
        ], stdin=subprocess.PIPE, stderr=subprocess.PIPE)

        # Communicate the image bytes to pngquant through stdin
        _, errors = process.communicate(bytes_io.getvalue())
        if process.returncode != 0:
            raise RuntimeError(f"pngquant failed: {errors.decode()}")

    return output_path

# Example usage of the compress_image function
compressed_image_path = compress_image('Group 95.jpg', '.jpg')
print(f"Compressed image saved to {compressed_image_path}")
