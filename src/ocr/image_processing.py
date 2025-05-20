import cv2
import numpy as np

def compute_image_stats(gray):
    """Compute basic statistics for the image."""
    mean = np.mean(gray)
    std = np.std(gray)
    variance = std ** 2
    contrast = std / (mean + 1e-5)  # avoid division by zero
    return {'mean': mean, 'std': std, 'variance': variance, 'contrast': contrast}

def apply_gaussian_blur(gray, variance, contrast):
    # Use a dynamic relationship between variance and contrast for better control
    if contrast < 0.5:
        print("Low contrast detected, applying less blur.")
        ksize = 3  # Low contrast, sharper text, less blur
    elif variance < 500:
        print("Moderate variance detected, applying moderate blur.")
        ksize = 7  # Moderate variance, balanced smoothing
    else:
        print("High variance detected, applying more blur.")
        ksize = 11  # High variance, more blur to reduce background noise

    # Ensure ksize is odd to prevent errors
    ksize = ksize if ksize % 2 != 0 else ksize + 1
    return cv2.GaussianBlur(gray, (ksize, ksize), 0)

def apply_bilateral_filter(blurred, std, contrast):
    # Adjust sigma_color based on std
    sigma_color = min(max(25, std * 2), 150)  # More variance → higher blur strength

    # Adjust sigma_space based on contrast (higher contrast requires more spatial blur)
    sigma_space = min(max(5, contrast * 15), 75)  # Higher contrast → stronger spatial smoothing

    return cv2.bilateralFilter(blurred, d=9, sigmaColor=sigma_color, sigmaSpace=sigma_space)


def apply_adaptive_threshold(filtered, contrast):
    """Apply adaptive thresholding based on image contrast."""
    block_size = int(min(max(11, contrast * 30), 31))
    block_size += 1 if block_size % 2 == 0 else 0
    C = int(min(10, 15 - contrast * 10))
    return cv2.adaptiveThreshold(filtered,
                                 255,
                                 cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY,
                                 block_size,
                                 C)

def enhance_contrast(thresh):
    """Enhance local contrast using CLAHE."""
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(thresh)

def preprocess_image(img):
    """
    Preprocess an input image for OCR.
    Returns an RGB image after adaptive thresholding and optional contrast enhancement.
    """
    # Convert the image to grayscale.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Compute image statistics.
    stats = compute_image_stats(gray)
    # Apply preprocessing steps.
      
    print("Applying filtering....") 
    gray = apply_bilateral_filter(gray, stats['std'], stats['contrast'])
    gray = apply_gaussian_blur(gray, stats['variance'], stats['contrast'])

    #gray = enhance_contrast(gray)
    gray = apply_adaptive_threshold(gray, stats['contrast'])

    return cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
