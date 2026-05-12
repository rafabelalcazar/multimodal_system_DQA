import pandas as pd

def analyze_quality(csv_path, thresholds=None):
    df = pd.read_csv(csv_path)
    
    if thresholds is None:
        thresholds = {
            'blur': 10,
            'dark': 50,
            'bright': 220,
            'contrast': 15,
            'entropy': 4.0
        }
    
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
    blurry = df[df['blur_score_laplacian_var'] < thresholds['blur']]
    issues['blurry_images'] = len(blurry)
    
    # 2. Brightness
    dark = df[df['brightness_mean'] < thresholds['dark']]
    issues['dark_images'] = len(dark)
    
    bright = df[df['brightness_mean'] > thresholds['bright']]
    issues['bright_images'] = len(bright)
    
    # 3. Contrast (Standard deviation of pixels)
    low_contrast = df[df['contrast_std'] < thresholds['contrast']]
    issues['low_contrast_images'] = len(low_contrast)
    
    # 4. Aspect Ratio
    non_square = df[df['aspect_ratio'] != 1.0]
    issues['non_square_images'] = len(non_square)
    
    # 5. Entropy (Information content)
    low_entropy = df[df['entropy'] < thresholds['entropy']]
    issues['low_entropy_images'] = len(low_entropy)
    
    # 6. Channels
    single_channel = df[df['channels'] != 3]
    issues['single_channel_images'] = len(single_channel)
    
    return issues, df, thresholds

def print_report(issues, df, thresholds):
    print("=== REPORTE DE PROBLEMAS DE CALIDAD DE IMÁGENES ===")
    print(f"Total de imágenes analizadas: {len(df)}")
    print(f"1. Imágenes borrosas (Laplacian Var < {thresholds['blur']}): {issues['blurry_images']}")
    print(f"2. Imágenes muy oscuras (Brillo Medio < {thresholds['dark']}): {issues['dark_images']}")
    print(f"3. Imágenes sobreexpuestas (Brillo Medio > {thresholds['bright']}): {issues['bright_images']}")
    print(f"4. Imágenes de bajo contraste (Std Dev < {thresholds['contrast']}): {issues['low_contrast_images']}")
    print(f"5. Imágenes no cuadradas (Aspect Ratio != 1.0): {issues['non_square_images']}")
    print(f"6. Imágenes con baja entropía (Entropía < {thresholds['entropy']}): {issues['low_entropy_images']}")
    print(f"7. Imágenes sin 3 canales (Escala de grises): {issues['single_channel_images']}")
    
    print("\n--- Estadísticas Descriptivas ---")
    print(df[['blur_score_laplacian_var', 'brightness_mean', 'contrast_std', 'entropy']].describe())

if __name__ == '__main__':
    # Use the test file if it exists, otherwise the default
    import os
    csv_file = 'image_quality_metrics_test.csv' if os.path.exists('image_quality_metrics_test.csv') else 'image_quality_metrics.csv'
    issues, df, thresholds = analyze_quality(csv_file)
    print_report(issues, df, thresholds)

