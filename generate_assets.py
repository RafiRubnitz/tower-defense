"""
Generate background image and sound effects for Tower Defense game.
Run this script once to create assets.
"""

from PIL import Image, ImageDraw
import os


def create_menu_background(filename='assets/images/menu_background.png'):
    """Create a tower defense themed menu background."""
    width, height = 980, 600

    # Create image with gradient background
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

    # Create gradient background (dark blue to darker)
    for y in range(height):
        ratio = y / height
        r = int(20 + (50 - 20) * ratio)
        g = int(30 + (60 - 30) * ratio)
        b = int(50 + (80 - 50) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b), width=1)

    # Draw subtle grid pattern in background
    grid_size = 40
    grid_color = (50, 70, 100)
    for x in range(0, width, grid_size):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, grid_size):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

    # Draw some tower defense elements (subtle decorative towers)
    tower_color = (100, 150, 200)
    tower_positions = [
        (100, 100, 30), (250, 150, 25), (900, 100, 28),
        (150, 500, 32), (800, 480, 26)
    ]

    for x, y, size in tower_positions:
        # Draw tower circle
        draw.ellipse([x - size, y - size, x + size, y + size], outline=tower_color, width=2)
        # Draw inner circle (range indicator)
        draw.ellipse([x - size // 2, y - size // 2, x + size // 2, y + size // 2],
                     outline=(70, 100, 150), width=1)

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    image.save(filename)
    print(f"Created {filename}")


def create_menu_music(filename='assets/sounds/menu_music.wav'):
    """Create a simple menu background music tone."""
    import wave
    import struct
    import math

    sample_rate = 22050
    duration = 10  # 10 seconds of ambient music
    frequency = 60  # Low ambient tone

    num_samples = sample_rate * duration

    # Create ambient background tone (very quiet)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        # Slow, ambient sine wave
        value = math.sin(2 * math.pi * frequency * t) * 0.1
        samples.append(struct.pack('<h', int(value * 32767)))

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'wb') as wav:
        wav.setnchannels(1)  # Mono
        wav.setsampwidth(2)  # 16-bit
        wav.setframerate(sample_rate)
        for sample in samples:
            wav.writeframes(sample)

    print(f"Created {filename}")


def create_button_click_sound(filename='assets/sounds/button_click.wav'):
    """Create a simple button click sound effect."""
    import wave
    import struct
    import math

    sample_rate = 22050
    duration = 0.1  # 100ms click

    num_samples = int(sample_rate * duration)
    samples = []

    # Simple click: descending pitch
    for i in range(num_samples):
        t = i / sample_rate
        # Envelope: fade out
        envelope = max(0, 1 - t / duration)
        # Pitch bends down from 800 to 300 Hz
        freq = 800 - (500 * t / duration)
        value = math.sin(2 * math.pi * freq * t) * envelope * 0.3
        samples.append(struct.pack('<h', int(value * 32767)))

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        for sample in samples:
            wav.writeframes(sample)

    print(f"Created {filename}")


if __name__ == '__main__':
    print("Generating Tower Defense game assets...")
    create_menu_background()
    create_menu_music()
    create_button_click_sound()
    print("\nAll assets created successfully!")
