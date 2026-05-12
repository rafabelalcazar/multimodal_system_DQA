import os
import cv2
import numpy as np
import pandas as pd
from pathlib import Path
from skimage.measure import shannon_entropy

def calculate_image_metrics(image_path):
    metrics = {}
    
    # Read image
    img = cv2.imread(image_path)
    
    if img is None:
        return None
        
    # File properties
    metrics['file_name'] = os.path.basename(image_path)
    metrics['class'] = os.path.basename(os.path.dirname(image_path))
    metrics['file_size_kb'] = os.path.getsize(image_path) / 1024
    
    # Dimensions
    h, w = img.shape[:2]
    metrics['height'] = h
    metrics['width'] = w
    metrics['channels'] = img.shape[2] if len(img.shape) == 3 else 1
    metrics['aspect_ratio'] = w / h if h > 0 else 0
    
    # Convert to grayscale for some metrics
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if metrics['channels'] == 3 else img
    
    # Blur / Sharpness (Variance of Laplacian)
    metrics['blur_score_laplacian_var'] = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # Brightness and Contrast
    metrics['brightness_mean'] = np.mean(gray)
    metrics['contrast_std'] = np.std(gray)
    
    # Color metrics (if RGB)
    if metrics['channels'] == 3:
        b, g, r = cv2.split(img)
        metrics['r_mean'] = np.mean(r)
        metrics['g_mean'] = np.mean(g)
        metrics['b_mean'] = np.mean(b)
    else:
        metrics['r_mean'] = np.nan
        metrics['g_mean'] = np.nan
        metrics['b_mean'] = np.nan
        
    # Entropy
    metrics['entropy'] = shannon_entropy(gray)
    
    return metrics

def main():
    archive_dir = 'datasets/archive'
    data = []
    
    for root, _, files in os.walk(archive_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                file_path = os.path.join(root, file)
                metrics = calculate_image_metrics(file_path)
                if metrics:
                    metrics['file_path'] = file_path
                    data.append(metrics)
                    
    df = pd.DataFrame(data)
    
    # Reorder columns to put file path at the end or beginning
    cols = ['file_name', 'class', 'file_size_kb', 'width', 'height', 'channels', 
            'aspect_ratio', 'blur_score_laplacian_var', 'brightness_mean', 'contrast_std', 
            'entropy', 'r_mean', 'g_mean', 'b_mean', 'file_path']
    
    # only keep columns that exist (in case something changed)
    cols = [c for c in cols if c in df.columns]
    df = df[cols]
    
    output_csv = 'image_quality_metrics.csv'
    df.to_csv(output_csv, index=False)
    print(f"Successfully processed {len(df)} images.")
    print(f"Metrics saved to {output_csv}")
    
    print("\nSummary statistics:")
    print(df.describe().to_string())

if __name__ == '__main__':
    main()
