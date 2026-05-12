import pandas as pd

def analyze_quality(csv_path):
    df = pd.read_csv(csv_path)
    
    issues = {
        'blurry_images': 0,
        'dark_images': 0,
        'bright_images': 0,
        'low_contrast_images': 0,
        'non_square_images': 0,
        'low_entropy_images': 0,
        'single_channel_images': 0
    }
    
    # 1. Blurriness (Laplacian variance)
    # Threshold < 10 is often considered quite blurry for Laplacian var
    blur_threshold = 10
    blurry = df[df['blur_score_laplacian_var'] < blur_threshold]
    issues['blurry_images'] = len(blurry)
    
    # 2. Brightness
    # Brightness is mean pixel value (0-255). < 50 is dark, > 220 is very bright
    dark = df[df['brightness_mean'] < 50]
    issues['dark_images'] = len(dark)
    
    bright = df[df['brightness_mean'] > 220]
    issues['bright_images'] = len(bright)
    
    # 3. Contrast (Standard deviation of pixels)
    # < 15 is generally low contrast
    low_contrast = df[df['contrast_std'] < 15]
    issues['low_contrast_images'] = len(low_contrast)
    
    # 4. Aspect Ratio
    non_square = df[df['aspect_ratio'] != 1.0]
    issues['non_square_images'] = len(non_square)
    
    # 5. Entropy (Information content)
    # Shannon entropy max is ~8 for 8-bit image. < 4 indicates very flat / empty image
    low_entropy = df[df['entropy'] < 4.0]
    issues['low_entropy_images'] = len(low_entropy)
    
    # 6. Channels
    single_channel = df[df['channels'] != 3]
    issues['single_channel_images'] = len(single_channel)
    
    print("=== REPORTE DE PROBLEMAS DE CALIDAD DE IMÁGENES ===")
    print(f"Total de imágenes analizadas: {len(df)}")
    print(f"1. Imágenes borrosas (Laplacian Var < {blur_threshold}): {issues['blurry_images']}")
    print(f"2. Imágenes muy oscuras (Brillo Medio < 50): {issues['dark_images']}")
    print(f"3. Imágenes sobreexpuestas/muy brillantes (Brillo Medio > 220): {issues['bright_images']}")
    print(f"4. Imágenes de bajo contraste (Std Dev < 15): {issues['low_contrast_images']}")
    print(f"5. Imágenes no cuadradas (Aspect Ratio != 1.0): {issues['non_square_images']}")
    print(f"6. Imágenes con baja entropía / poca información (Entropía < 4.0): {issues['low_entropy_images']}")
    print(f"7. Imágenes sin 3 canales (Escala de grises): {issues['single_channel_images']}")
    
    print("\n--- Estadísticas Descriptivas ---")
    print(df[['blur_score_laplacian_var', 'brightness_mean', 'contrast_std', 'entropy']].describe())

if __name__ == '__main__':
    analyze_quality('image_quality_metrics.csv')
