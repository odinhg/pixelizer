import streamlit as st
from PIL import Image, ImageEnhance
from io import BytesIO
from pathlib import Path

def load_palette_file(path: Path):
    """Load a .hex palette file into a list of RGB tuples."""
    colors = []
    with open(path, "r") as f:
        for line in f:
            hexcode = line.strip().lstrip("#")
            if len(hexcode) == 6:  # valid hex
                r = int(hexcode[0:2], 16)
                g = int(hexcode[2:4], 16)
                b = int(hexcode[4:6], 16)
                colors.append((r, g, b))
            else:
                st.warning(f"Invalid hex code in palette file: {line}")
    return colors

def apply_custom_palette(image: Image.Image, colors, dithering: bool):
    """Quantize an image to a custom palette with optional dithering."""
    # Build palette (zero pad to 256 colors if needed)
    palette_img = Image.new("P", (1, 1))
    palette_data = []
    for r, g, b in colors[:256]:
        palette_data.extend([r, g, b])
    palette_data.extend([0] * (768 - len(palette_data)))
    palette_img.putpalette(palette_data)

    # Quantize with the custom palette
    dither_mode = Image.FLOYDSTEINBERG if dithering else Image.NONE
    image = image.quantize(palette=palette_img, dither=dither_mode, method=Image.MEDIANCUT)
    return image.convert("RGB")

st.set_page_config(page_title="Pixelizer", layout="wide")
st.sidebar.title("Pixelizer")
st.sidebar.header("Image Controls")
uploaded_file = st.sidebar.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
show_original = st.sidebar.toggle("Show original", value=False)
dithering = st.sidebar.toggle("Enable dithering", value=True)
pixel_size = st.sidebar.number_input("Pixel size", min_value=1, max_value=100, value=4, step=1)
palette_dir = Path("palettes")
palette_files = sorted(palette_dir.glob("*.hex"))
palette_names = [f.stem for f in palette_files]
palette = st.sidebar.selectbox("Palette", palette_names) 

contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0, 0.1)
brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0, 0.1)

if uploaded_file:
    original_image = Image.open(uploaded_file).convert("RGB")

    # Contrast and brightness adjustment 
    image = original_image.copy()
    enhancer_contrast = ImageEnhance.Contrast(image)
    image = enhancer_contrast.enhance(contrast)
    enhancer_brightness = ImageEnhance.Brightness(image)
    image = enhancer_brightness.enhance(brightness)

    # Downscale for pixelization
    processed_image = image.copy()
    w, h = processed_image.size
    processed_image = processed_image.resize(
        (max(1, w // pixel_size), max(1, h // pixel_size)),
        resample=Image.NEAREST
    )

    # Apply palette
    palette_file = palette_dir / f"{palette}.hex"
    processed_image = apply_custom_palette(processed_image, load_palette_file(palette_file), dithering) 
    upscaled_processed_image = processed_image.resize((w, h), Image.NEAREST)

    # Display
    if show_original:
        st.image(original_image, caption="Original", width="content")
    else:
        st.image(upscaled_processed_image, caption="Processed", width="content")

    # Save 
    buf = BytesIO()
    processed_image.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.sidebar.download_button(
        "Save image",
        data=byte_im,
        file_name="pixelized.png",
        mime="image/png"
    )

