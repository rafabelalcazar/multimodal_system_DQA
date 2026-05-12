import streamlit as st
import pandas as pd
import os
import plotly.express as px
from analyze_quality import analyze_quality

st.set_page_config(page_title="Image Quality Dashboard", layout="wide", page_icon="🖼️")

# Custom CSS for premium look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1e3a8a;
        font-family: 'Outfit', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🖼️ Image Data Quality Assessment")
st.markdown("### Ajuste de Thresholds y Análisis Interactivo")

# Sidebar for configuration
st.sidebar.header("Configuración de Umbrales")

blur_t = st.sidebar.slider("Blur Threshold (Laplacian Var)", 0, 100, 10, help="Menor a este valor se considera borroso.")
dark_t = st.sidebar.slider("Dark Threshold (Brightness)", 0, 127, 50, help="Menor a este valor se considera muy oscuro.")
bright_t = st.sidebar.slider("Bright Threshold (Brightness)", 128, 255, 220, help="Mayor a este valor se considera sobreexpuesto.")
contrast_t = st.sidebar.slider("Contrast Threshold (Std Dev)", 0, 100, 15, help="Menor a este valor se considera bajo contraste.")
entropy_t = st.sidebar.slider("Entropy Threshold", 0.0, 8.0, 4.0, step=0.1, help="Menor a este valor se considera poca información.")

csv_file = 'image_quality_metrics_test.csv' if os.path.exists('image_quality_metrics_test.csv') else 'image_quality_metrics.csv'

if not os.path.exists(csv_file):
    st.error(f"Archivo {csv_file} no encontrado. Por favor corre `extract_metrics.py` primero.")
else:
    thresholds = {
        'blur': blur_t,
        'dark': dark_t,
        'bright': bright_t,
        'contrast': contrast_t,
        'entropy': entropy_t
    }

    issues, df, active_thresholds = analyze_quality(csv_file, thresholds)

    # Metrics Summary
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Imágenes", len(df))
    col2.metric("Imágenes Borrosas", issues['blurry_images'], delta_color="inverse")
    col3.metric("Baja Entropía", issues['low_entropy_images'], delta_color="inverse")
    col4.metric("Sin 3 Canales", issues['single_channel_images'])

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Muy Oscuras", issues['dark_images'], delta_color="inverse")
    col6.metric("Muy Brillantes", issues['bright_images'], delta_color="inverse")
    col7.metric("Bajo Contraste", issues['low_contrast_images'], delta_color="inverse")
    col8.metric("No Cuadradas", issues['non_square_images'])

    st.divider()

    # Visualizations
    tab1, tab2 = st.tabs(["📊 Distribuciones", "🔍 Datos"])

    with tab1:
        vcol1, vcol2 = st.columns(2)
        
        with vcol1:
            fig_blur = px.histogram(df, x='blur_score_laplacian_var', title="Distribución de Blur (Laplacian Var)",
                                   color_discrete_sequence=['#3b82f6'])
            fig_blur.add_vline(x=blur_t, line_dash="dash", line_color="red", annotation_text="Threshold")
            st.plotly_chart(fig_blur, use_container_width=True)

            fig_bright = px.histogram(df, x='brightness_mean', title="Distribución de Brillo",
                                     color_discrete_sequence=['#fbbf24'])
            fig_bright.add_vline(x=dark_t, line_dash="dash", line_color="red")
            fig_bright.add_vline(x=bright_t, line_dash="dash", line_color="red")
            st.plotly_chart(fig_bright, use_container_width=True)

        with vcol2:
            fig_contrast = px.histogram(df, x='contrast_std', title="Distribución de Contraste",
                                       color_discrete_sequence=['#10b981'])
            fig_contrast.add_vline(x=contrast_t, line_dash="dash", line_color="red")
            st.plotly_chart(fig_contrast, use_container_width=True)

            fig_entropy = px.histogram(df, x='entropy', title="Distribución de Entropía",
                                      color_discrete_sequence=['#8b5cf6'])
            fig_entropy.add_vline(x=entropy_t, line_dash="dash", line_color="red")
            st.plotly_chart(fig_entropy, use_container_width=True)

    with tab2:
        st.dataframe(df, use_container_width=True)

    # Download results
    st.sidebar.divider()
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="📥 Descargar Reporte CSV",
        data=csv_data,
        file_name='quality_analysis_results.csv',
        mime='text/csv',
    )
