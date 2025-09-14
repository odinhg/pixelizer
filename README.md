# pixelizer

A simple tool to create "pixel art" (not really pixel art, but pixelated images) from images. 

![User Interface](images/interface.png)

[Click here for live demo.](https://huggingface.co/spaces/odinhg/pixelizer)

## Features

- No AI
- Streamlit user interface
- Custom palettes (supports HEX files from Lospec.com)
- Dithering 

## Examples

| Original | Pixelized |
|----------|-----------|
| ![Original Image](images/input0.png) | ![Pixelized Image](images/output0.png) |
| ![Original Image](images/input1.png) | ![Pixelized Image](images/output1.png) |
| ![Original Image](images/input2.png) | ![Pixelized Image](images/output2.png) |
| ![Original Image](images/input3.png) | ![Pixelized Image](images/output3.png) |
| ![Original Image](images/input4.png) | ![Pixelized Image](images/output4.png) |

## How to use (locally)

Using `uv`, simply run:

```bash
uv run streamlit run main.py
```

