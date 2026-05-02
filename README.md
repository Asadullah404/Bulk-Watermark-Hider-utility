# Sipra-Productions | Pro Image Studio

An enterprise-grade, desktop graphical application designed for batch processing images. This tool allows users to seamlessly apply custom logo watermarks (or dynamic text watermarks) and automatically convert images to the lightweight, high-quality `.webp` format.

Built with a sleek, dark-mode CustomTkinter interface, it's designed for production environments where speed and aesthetics matter.

## ✨ Features

- **Enterprise UI**: A gorgeous, dark-mode graphical user interface built with CustomTkinter.
- **Batch Processing**: Select multiple folders at once. The engine will scan and process all `.jpg`, `.jpeg`, and `.png` files found.
- **Logo Watermarking**: Upload your own premium `.png` (with transparency) or `.jpg` logo. The engine auto-scales and blends it seamlessly into the bottom right corner of your images.
- **Dynamic Text Fallback**: Don't have a logo? No problem. The tool can dynamically render a circular text watermark using a fallback text (e.g., "AS").
- **WebP Conversion**: All processed images are automatically converted to `.webp` format at 90% quality for massive storage savings without losing visual fidelity.
- **Smart Outputs**: Processed files are never mixed with originals. The app automatically creates a `[FolderName]_processed` directory right next to your original folders.

## 🛠️ Requirements

- Python 3.8+
- [OpenCV](https://pypi.org/project/opencv-python/) (`cv2`)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [Pillow](https://pypi.org/project/Pillow/)
- [NumPy](https://pypi.org/project/numpy/)

*(Note: The script has an auto-installer built-in that will attempt to install `customtkinter` and `Pillow` automatically upon its first run if they are missing.)*

## 🚀 Usage

### Running the Python Script
Simply run the script via Python:
```bash
python removewatermark.py
```

### Compiling into a Standalone `.exe`
If you want to distribute this tool without requiring Python to be installed on the target machine, you can build it using `PyInstaller`.

1. Install PyInstaller:
```bash
python -m pip install pyinstaller
```
2. Build the executable:
```bash
python -m PyInstaller --noconfirm --onefile --windowed --collect-all customtkinter --name "SipraWatermarkStudio" removewatermark.py
```
3. Your standalone executable will be located in the newly created `dist/` folder!

## 🏢 About

Developed for **Sipra-Productions Private Limited** as an in-house Divine Watermarking & Conversion Engine.
