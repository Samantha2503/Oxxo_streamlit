import streamlit as st
import os
import pandas as pd
import numpy as np
import plotly.express as px
import joblib as joblib


# --- Configuración de la página con diseño elegante ---
st.set_page_config(
    page_title="Análisis de Ubicación OXXO",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.oxxo.com',
        'About': "### Herramienta de Análisis de Potencial de Ubicación OXXO\n*Decisiones basadas en datos para la expansión minorista*"
    }
)

# --- Tema Claro Moderno con Colores Acuáticos de OXXO ---
st.markdown(
    """
    <style>
    :root {
        --primary: #E31937;  /* Rojo OXXO */
        --text-dark: #333333; /* Gris oscuro para texto principal */
        --text-light: #F8F8F8; /* Gris claro para texto inverso */
        --background-light: #FFFFFF; /* Fondo blanco */
        --card-background-light: #F0F2F6; /* Gris claro para tarjetas */
        --border-light: #DDDDDD; /* Borde claro para elementos */
        --accent-blue: #007BFF; /* Un sutil azul de acento para enlaces/información */
        --sidebar-bg-start: #F0F2F6; /* Inicio más claro para el gradiente de la barra lateral */
        --sidebar-bg-end: #E8ECF2; /* Fin ligeramente más oscuro para el gradiente de la barra lateral */
    }
    
    /* Fuente Global - Sans-serif Moderna (imitando a Gemini) */
    body, .stApp, .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>select,
    .stButton>button, .stText, p, li, h1, h2, h3, h4, h5, h6, [data-testid="stSidebarNav"] * {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
    }

    /* Fondo principal de la aplicación */
    .stApp {
        background-color: var(--background-light);
        color: var(--text-dark);
    }
    
    /* Estilo de la barra lateral */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--sidebar-bg-start) 0%, var(--sidebar-bg-end) 100%) !important;
        border-right: 1px solid var(--border-light);
        box-shadow: 2px 0 15px rgba(0, 0, 0, 0.08); /* Sombra sutil más prominente */
        padding-top: 2rem; /* Añadir algo de espacio en la parte superior */
    }
    
    /* Texto de la barra lateral */
    [data-testid="stSidebar"] * {
        color: var(--text-dark) !important;
    }

    /* Ajustar el encabezado de la barra lateral (texto OXXO) */
    .st-emotion-cache-1mlwun0 { /* Apunta al div del encabezado en la barra lateral */
        padding: 0 1rem 1.5rem 1rem; /* Ajustar el relleno para el contenedor del logo/título */
        border-bottom: 1px solid var(--border-light); /* Separador sutil debajo del encabezado */
        margin-bottom: 2rem; /* Espacio debajo del separador */
    }
    
    /* Elementos de navegación de la barra lateral */
    [data-testid="stSidebarNav"] li div a {
        padding: 12px 20px; /* Relleno ligeramente mayor */
        border-radius: 8px; /* Esquinas más redondeadas */
        transition: all 0.3s ease;
        color: var(--text-dark) !important;
        font-weight: 500; /* Ligeramente más negrita para mayor claridad */
        margin-bottom: 0.4rem; /* Espacio entre elementos */
        display: flex;
        align-items: center;
        gap: 10px; /* Espacio entre el icono y el texto */
    }
    
    [data-testid="stSidebarNav"] li div a:hover {
        background-color: rgba(227, 25, 55, 0.15) !important; /* Resaltado de hover ligeramente más intenso */
        color: var(--primary) !important;
        transform: translateX(5px); /* Efecto de deslizamiento sutil al pasar el ratón */
    }
    
    [data-testid="stSidebarNav"] li div a[aria-current="page"] {
        background-color: var(--primary) !important;
        color: var(--text-light) !important;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(227, 25, 55, 0.2); /* Sombra sutil para el elemento activo */
    }
    
    /* Encabezados con rojo OXXO */
    h1, h2, h3, h4, h5, h6 {
        color: var(--primary) !important; /* Rojo OXXO para los encabezados */
        margin-bottom: 1rem;
    }
    
    h1 {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
    }
    
    /* Tarjetas y contenedores */
    .st-emotion-cache-1y4p8pa { /* Esto apunta al fondo predeterminado de st.container/st.expander */
        background-color: var(--card-background-light);
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08); /* Sombra más clara */
        border-left: 4px solid var(--primary); /* Borde rojo OXXO */
        color: var(--text-dark); /* Asegurar que el texto dentro de los contenedores sea oscuro */
    }
    
    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, #C8102E 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 10px rgba(227, 25, 55, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(227, 25, 55, 0.4) !important;
    }
    
    /* Pestañas */
    [data-baseweb="tab-list"] {
        gap: 8px !important;
    }
    
    [data-baseweb="tab"] {
        background-color: var(--card-background-light) !important; /* Fondo claro para pestañas inactivas */
        border-radius: 8px !important;
        padding: 8px 16px !important;
        transition: all 0.3s ease !important;
        color: var(--text-dark) !important; /* Texto oscuro para pestañas inactivas */
    }
    
    [data-baseweb="tab"]:hover {
        background-color: var(--border-light) !important; /* Ligeramente más oscuro al pasar el ratón */
    }
    
    [aria-selected="true"] {
        background-color: var(--primary) !important;
        color: white !important;
    }
    
    /* Divisores */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, var(--primary) 50%, transparent 100%);
        margin: 2rem 0;
    }
    
    /* Campos de entrada */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>select {
        background-color: var(--card-background-light) !important;
        color: var(--text-dark) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 8px !important;
    }
    
    /* Dataframes */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        color: var(--text-dark); /* Asegurar que el texto sea oscuro */
    }
    
    /* Métricas */
    [data-testid="stMetric"] {
        background-color: var(--card-background-light);
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid var(--primary);
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-dark) !important; /* Etiqueta más oscura */
    }
    
    [data-testid="stMetricValue"] {
        color: var(--primary) !important; /* Rojo OXXO para el valor */
        font-size: 1.8rem !important;
    }
    
    /* Barra de desplazamiento personalizada */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--card-background-light);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary);
        border-radius: 4px;
    }
    
    /* Consejos de herramientas */
    .stTooltip {
        background-color: var(--text-dark) !important; /* Fondo oscuro para consejos de herramientas */
        color: var(--text-light) !important; /* Texto claro para consejos de herramientas */
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
    }
    
    /* Enlaces */
    a {
        color: var(--accent-blue) !important; /* Azul para enlaces */
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }

    /* Ajustar colores de texto específicos dentro de los divs de markdown si es necesario */
    .st-emotion-cache-1y4p8pa p, .st-emotion-cache-1y4p8pa li {
        color: var(--text-dark);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Navegación de la barra lateral con iconos ---
with st.sidebar:
    # Contenedor para el logo/título de la barra lateral
    st.markdown("""
    <div class="st-emotion-cache-1mlwun0">
        <h3 style="color: var(--primary); margin-bottom: 0;">OXXO</h3>
        <p style="color: var(--text-dark); margin-top: 0; font-size: 0.9rem;">Análisis de Potencial de Ubicación</p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.selectbox(
        "Navegar",
        ["Inicio", "Análisis", "Mapa Interactivo","Modelo de Predicción"],
        label_visibility="collapsed" # Oculta la etiqueta "Navegar"
    )
    
    st.markdown("---") # Separador visual

    # Añadir algunos widgets útiles en la barra lateral
    st.markdown("### Filtros")
    analysis_period = st.select_slider(
        "Período de Análisis",
        options=["1 Mes", "3 Meses", "6 Meses", "1 Año", "2 Años"],
        value="1 Año"
    )
    
    st.markdown("---")
    
    st.markdown("### Acerca de")
    st.markdown("""
    Esta herramienta ayuda a OXXO a identificar ubicaciones de alto potencial para nuevas tiendas utilizando análisis avanzados.
    """)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; color: var(--text-dark); font-size: 0.8rem; opacity: 0.7;">
        OXXO Retail Analytics © 2023
    </div>
    """, unsafe_allow_html=True)

# --- Página: Inicio ---
if page == "Inicio":
    # Sección Héroe
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        <div style="margin-bottom: 2rem;">
            <h1 style="margin-bottom: 0.5rem;">Análisis de Potencial de Ubicación OXXO</h1>
            <p style="color: var(--text-dark); font-size: 1.1rem;">Decisiones basadas en datos para la estrategia de expansión minorista</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Usando la imagen local, asegúrate de que la ruta sea correcta desde la ubicación de tu script.
        # Si prefieres una URL pública: "https://upload.wikimedia.org/wikipedia/commons/e/e9/OXXO_logo.png"
        st.image("Streamlit/oxxo.png", width=150)
    
    st.markdown("---")
    
    # Métricas Clave
    st.markdown("### Resumen del Proyecto")
    metric1, metric2, metric3, metric4 = st.columns(4)
    
    with metric1:
        st.metric("Tiendas Analizadas", "900+", "15 nuevas este mes")
    
    with metric2:
        st.metric("Precisión del Modelo", "83%", "3% de mejora")
    
    with metric3:
        st.metric("Ubicaciones Potenciales", "142", "8 de alta confianza")
    
    with metric4:
        st.metric("Aumento Prom. de Ventas", "12%", "vs línea base")
    
    st.markdown("---")
    
    # Secciones de Contenido
    with st.expander("📌 Contexto del Proyecto", expanded=True):
        st.markdown(f"""
        <div style="background-color: var(--card-background-light); padding: 1.5rem; border-radius: 12px;">
            <p style="color: var(--primary); font-weight: 600; margin-bottom: 0.5rem;">DESAFÍO EMPRESARIAL</p>
            <p style="color: var(--text-dark);">OXXO, la cadena de tiendas de conveniencia líder en nuestra División de Proximidad, trabaja constantemente para estar cerca de los clientes, ofreciendo productos y servicios que les facilitan la vida. La ubicación de la tienda es clave para asegurar el éxito.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("🎯 Objetivos", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="background-color: var(--card-background-light); padding: 1.5rem; border-radius: 12px; height: 100%;">
                <h4 style="color: var(--primary); margin-top: 0;">Meta Principal</h4>
                <p style="color: var(--text-dark);">Crear un modelo predictivo que, dada una ubicación (latitud/longitud), determine si una tienda OXXO tiene un alto potencial de éxito y puede cumplir sus objetivos de ventas.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background-color: var(--card-background-light); padding: 1.5rem; border-radius: 12px; height: 100%;">
                <h4 style="color: var(--primary); margin-top: 0;">Objetivos Específicos</h4>
                <ul style="color: var(--text-dark);">
                    <li>Crear un dashboard para visualizar el rendimiento actual de la tienda</li>
                    <li>Desarrollar un modelo predictivo con >80% de precisión</li>
                    <li>Adaptar el modelo para otros formatos de negocio</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with st.expander("📊 Resumen del Conjunto de Datos", expanded=True):
        st.markdown(f"""
        <div style="background-color: var(--card-background-light); padding: 1.5rem; border-radius: 12px;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div>
                    <p style="color: var(--primary); font-weight: 600; margin-bottom: 0.5rem;">DATOS CENTRALES</p>
                    <ul style="color: var(--text-dark);">
                        <li>Más de 900 tiendas con datos de ubicación</li>
                        <li>Características internas</li>
                        <li>Datos del entorno circundante</li>
                        <li>Objetivos de ventas</li>
                    </ul>
                </div>
                <div>
                    <p style="color: var(--primary); font-weight: 600; margin-bottom: 0.5rem;">DATOS COMPLEMENTARIOS</p>
                    <ul style="color: var(--text-dark);">
                        <li>2 años de datos de ventas mensuales</li>
                        <li>Datos del censo de población</li>
                        <li>Métricas de actividad económica</li>
                        <li>Información sociodemográfica</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- Página: Análisis ---
elif page == "Análisis":
    st.title("📊 Análisis de Datos")
    st.markdown("Explora los hallazgos clave y las visualizaciones del análisis de ubicación de OXXO.")

    tab1, tab2, tab3, tab4 = st.tabs(["📋 Observaciones","📈 Métricas de Rendimiento", "📊 Análisis de Desempeño", "📈 Evolución Mensual de Ventas"])

    # ---------- TAB 1 ----------
    df_mes=pd.read_csv('Streamlit/df_por_tienda.csv')
    df_tienda=pd.read_csv('Streamlit/datos_parte1.csv')
    df_tienda2=pd.read_csv('Streamlit/datos_parte2.csv')
    df_tienda3=pd.read_csv('Streamlit/datos_parte3.csv')
    df_tienda = pd.concat([df_tienda, df_tienda2, df_tienda3], ignore_index=True)
    df_mes=df_tienda
    df_tienda=df_mes
    with tab1:
        st.markdown("## 📋 Observaciones Generales del Desempeño de Tiendas OXXO")

        # === Cálculos ===
        df_mes['CUMPLIMIENTO'] = df_mes['VENTA_TOTAL'] / df_mes['META']
        df_mes['EXITO_MENSUAL'] = df_mes['CUMPLIMIENTO'] >= 1

        cumplimiento_resumen = df_mes.groupby('TIENDA_ID')['EXITO_MENSUAL'].agg(['sum', 'count'])
        cumplimiento_resumen['PORC_MESES_CUMPLIDOS'] = cumplimiento_resumen['sum'] / cumplimiento_resumen['count']
        cumplimiento_resumen['TIENDA_EXITOSA'] = cumplimiento_resumen['PORC_MESES_CUMPLIDOS'] >= 0.8

        porcentaje_exito_global = round(100 * cumplimiento_resumen['TIENDA_EXITOSA'].mean(), 1)

        df_resumen = df_tienda.merge(cumplimiento_resumen, on='TIENDA_ID')

        exito_por_entorno = df_resumen.groupby('ENTORNO_DES')['TIENDA_EXITOSA'].mean().reset_index()
        exito_por_entorno.columns = ['ENTORNO', 'EXITO_%']
        entornos_con_alto_exito = exito_por_entorno[exito_por_entorno['EXITO_%'] > exito_por_entorno['EXITO_%'].mean()]['ENTORNO'].tolist()

        exito_por_nse = df_resumen.groupby('NIVELSOCIOECONOMICO_DES')['TIENDA_EXITOSA'].mean()
        nse_mejor = exito_por_nse.idxmax()

        tiendas_con_datos = cumplimiento_resumen.reset_index()
        tiendas_nuevas = tiendas_con_datos[tiendas_con_datos['count'] < 6].shape[0]

        variabilidad = df_mes.groupby('TIENDA_ID')['VENTA_TOTAL'].agg(['mean', 'std'])
        variabilidad['cv'] = variabilidad['std'] / variabilidad['mean']
        porc_alta_var = round(100 * (variabilidad['cv'] > 0.3).mean(), 1)

        ultimo_mes = df_mes['MES_ID'].max()
        ventas_ult_mes = df_mes[df_mes['MES_ID'] == ultimo_mes]
        ventas_ult_mes = ventas_ult_mes.merge(cumplimiento_resumen['PORC_MESES_CUMPLIDOS'], on='TIENDA_ID')
        ventas_ult_mes['CUMPLIMIENTO_MES'] = ventas_ult_mes['VENTA_TOTAL'] / ventas_ult_mes['META']
        bajaron_rendimiento = (ventas_ult_mes['CUMPLIMIENTO_MES'] < ventas_ult_mes['PORC_MESES_CUMPLIDOS']).sum()

        # === Visualización ===

        st.markdown(f"""
        A continuación se presentan los hallazgos más relevantes derivados del análisis mensual de cumplimiento de tiendas, útiles para la toma de decisiones estratégicas:

        - *{porcentaje_exito_global}% de las tiendas* cumplen su meta de ventas en al menos el 80% de los meses en operación, lo que indica un rendimiento positivo general y metas bien calibradas.

        - *Entornos con mejor desempeño: Los entornos con mayores tasas de tiendas exitosas son: *{", ".join(entornos_con_alto_exito)}**. Estas zonas son buenos candidatos para expansión.

        - *Nivel Socioeconómico destacado: El nivel socioeconómico *{nse_mejor}** presenta el mayor porcentaje de tiendas exitosas, lo que sugiere una fuerte afinidad entre el modelo OXXO y dicho segmento.

        - *Tiendas nuevas bajo observación: Se identificaron *{tiendas_nuevas} tiendas** con menos de 6 meses de operación, por lo que no pueden clasificarse aún como exitosas o no.

        - *Alta variabilidad mensual: Un *{porc_alta_var}%** de las tiendas muestran alta variación en ventas mes a mes (CV > 0.3), indicando posible estacionalidad o influencia de factores externos.

        - *Descenso reciente en rendimiento: Al menos *{bajaron_rendimiento} tiendas** tuvieron un cumplimiento inferior a su promedio histórico en el último mes, lo que podría señalar problemas de abastecimiento o cambios competitivos.

        ---
        """)


     # ---------- TAB 2 ----------
    with tab2:
        st.markdown("### 🧭 Análisis Descriptivo de Tiendas")
        st.markdown("Este apartado ofrece una visión general de la composición de las tiendas OXXO según variables clave como entorno, nivel socioeconómico y ventas promedio.")
        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Distribución de Tiendas por Entorno")
            conteo_entornos = df_tienda['ENTORNO_DES'].value_counts().reset_index()
            conteo_entornos.columns = ['Entorno', 'Tiendas']
            fig_entorno = px.pie(conteo_entornos, names='Entorno', values='Tiendas',
                                hole=0.4,
                                color_discrete_sequence=['#E31937', '#C8102E', '#A8071C', '#7A0513', '#4D030C'])
            fig_entorno.update_traces(textposition='inside', textfont_size=16)
            fig_entorno.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=16, color='#333333'),
                legend=dict(
                    orientation="h", 
                    y=-0.2, 
                    x=0.5, 
                    xanchor='center',
                    font=dict(size=14, color='#333333')
                )
            )
            st.plotly_chart(fig_entorno, use_container_width=True)

        with col2:
            st.markdown("#### Ventas Promedio por Entorno")
            df_ventas_entorno = df_mes.groupby('ENTORNO_DES')['VENTA_TOTAL'].mean().reset_index()
            fig_ventas = px.bar(
                df_ventas_entorno, 
                x='ENTORNO_DES', 
                y='VENTA_TOTAL',
                color='ENTORNO_DES',
                text='VENTA_TOTAL',
                color_discrete_sequence=['#E31937', '#FF6B6B', '#FF8E8E', '#FFB6B6', '#FFD3D3'],
                height=400
            )
            fig_ventas.update_traces(texttemplate='$%{text:,.0f}', textposition='outside', textfont_size=14)
            fig_ventas.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=16, color='#333333'),
                showlegend=False,
                yaxis_title="Ventas Promedio (MXN)",
                xaxis_title=""
            )
            st.plotly_chart(fig_ventas, use_container_width=True)

        st.markdown("---")
        st.markdown("#### Distribución de Tiendas por Nivel Socioeconómico")
        df_nse_count = df_tienda['NIVELSOCIOECONOMICO_DES'].value_counts().reset_index()
        df_nse_count.columns = ['NSE', 'Tiendas']
        fig_nse = px.bar(df_nse_count, x='NSE', y='Tiendas',
                        color='Tiendas',
                        text='Tiendas',
                        color_continuous_scale=['#FFD700', '#E31937'])
        fig_nse.update_traces(texttemplate='%{text}', textposition='outside', textfont_size=14)
        fig_nse.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=16, color='#333333'),
            xaxis_title="Nivel Socioeconómico",
            yaxis_title="Cantidad de Tiendas"
        )
        st.plotly_chart(fig_nse, use_container_width=True)

    # ---------- TAB 3 ----------
    with tab3:
        st.markdown("### 📊 Análisis de Desempeño") 

        df_tienda['BAJO_RENDIMIENTO'] = df_tienda['PORCENTAJE_CUMPLIMIENTO'] < 0.5
        bajo_rendimiento = df_tienda[df_tienda['BAJO_RENDIMIENTO']]
        bajo_entorno = bajo_rendimiento['ENTORNO_DES'].value_counts().reset_index()
        bajo_entorno.columns = ['Entorno', 'Tiendas']
        fig_bajo = px.bar(bajo_entorno, x='Entorno', y='Tiendas',
                          color='Tiendas', text_auto=True,
                          color_continuous_scale=['#FFD700', '#E31937'])
        fig_bajo.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color=st.get_option('theme.textColor'),
            xaxis_title="Entorno",
            yaxis_title="Cantidad de Tiendas < 50%",
            title="Distribución de Bajo Rendimiento por Entorno"
        )
        st.plotly_chart(fig_bajo, use_container_width=True)

        st.markdown("#### Cumplimiento Promedio por Nivel Socioeconómico")
        df_nse = df_tienda.groupby('NIVELSOCIOECONOMICO_DES')['PORCENTAJE_CUMPLIMIENTO'].mean().reset_index()
        fig_nse = px.bar(df_nse, x='NIVELSOCIOECONOMICO_DES', y='PORCENTAJE_CUMPLIMIENTO',
                         color='PORCENTAJE_CUMPLIMIENTO', text_auto='.2f',
                         color_continuous_scale=['#FFD700', '#E31937'])
        fig_nse.update_layout(
            title="Cumplimiento por NSE",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color=st.get_option('theme.textColor'),
            xaxis_title="Nivel Socioeconómico",
            yaxis_title="% Cumplimiento"
        )
        st.plotly_chart(fig_nse, use_container_width=True)

        st.markdown("#### 🏅 Top 10 Tiendas con Mayor Cumplimiento")
        top_high = df_tienda.sort_values('PORCENTAJE_CUMPLIMIENTO', ascending=False).head(10)
        st.dataframe(
            top_high[['TIENDA_ID', 'ENTORNO_DES', 'NIVELSOCIOECONOMICO_DES', 'PORCENTAJE_CUMPLIMIENTO']]
            .rename(columns={
                'TIENDA_ID': 'ID Tienda',
                'ENTORNO_DES': 'Entorno',
                'NIVELSOCIOECONOMICO_DES': 'NSE',
                'PORCENTAJE_CUMPLIMIENTO': '% Cumplimiento'
            })
            .style.format({'% Cumplimiento': '{:.2%}'})
        , use_container_width=True)

        st.markdown("#### 🚨 Top 10 Tiendas con Menor Cumplimiento")
        top_low = df_tienda.sort_values('PORCENTAJE_CUMPLIMIENTO', ascending=True).head(10)
        st.dataframe(
            top_low[['TIENDA_ID', 'ENTORNO_DES', 'NIVELSOCIOECONOMICO_DES', 'PORCENTAJE_CUMPLIMIENTO']]
            .rename(columns={
                'TIENDA_ID': 'ID Tienda',
                'ENTORNO_DES': 'Entorno',
                'NIVELSOCIOECONOMICO_DES': 'NSE',
                'PORCENTAJE_CUMPLIMIENTO': '% Cumplimiento'
            })
            .style.format({'% Cumplimiento': '{:.2%}'})
        , use_container_width=True)

        st.markdown("---")

    # ---------- TAB 4 ----------
    
    with tab4:
        st.markdown("""
        <style>
        /* Forzar color negro en texto de radio y selectbox */
        div[data-testid="stRadio"] > div > label > div,
        div[data-testid="stSelectbox"] > label,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] div {
            color: black !important;
            font-weight: 600 !important;
        }

        /* Texto de las opciones (dentro del dropdown) */
        div[data-testid="stSelectbox"] span {
            color: black !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.subheader("📈 Evolución Mensual de Ventas")

        modo = st.radio("", ["Tienda individual", "Promedio por entorno", "Comparar varias tiendas"])


        if modo == "Tienda individual":
            tienda_sel = st.selectbox("Selecciona una tienda", sorted(df_mes['TIENDA_ID'].unique()))
            df_tienda_sel = df_mes[df_mes['TIENDA_ID'] == tienda_sel].sort_values('MES_ID')
            meta_fija = df_tienda_sel['META'].iloc[0]
            
            fig = px.line(df_tienda_sel, x='MES_ID', y='VENTA_TOTAL', markers=True,
                        title=f"🏍️ Tienda {tienda_sel} - Ventas Mensuales",
                        template='plotly_white')
            fig.update_traces(line=dict(color='#E31937'), marker=dict(size=8))
            fig.add_scatter(x=df_tienda_sel['MES_ID'], 
                            y=[meta_fija]*len(df_tienda_sel),
                            mode='lines', name='META', 
                            line=dict(color='gray', dash='dash'))
            fig.update_layout(
                font=dict(size=16, color='#333333'),
                xaxis_title="Mes",
                yaxis_title="Venta Total (MXN)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

        elif modo == "Promedio por entorno":
            df_agg = df_mes.groupby(['MES_ID', 'ENTORNO_DES'])[['VENTA_TOTAL', 'META']].mean().reset_index()

            fig_venta = px.line(df_agg, x='MES_ID', y='VENTA_TOTAL', color='ENTORNO_DES', markers=True,
                                title="🔵 Ventas promedio por entorno",
                                color_discrete_sequence=['#7A0513', '#A8071C', '#C8102E', '#E31937'])
            fig_venta.update_layout(
                font=dict(size=16, color='#333333'),
                xaxis_title="Mes",
                yaxis_title="Ventas Promedio (MXN)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_venta, use_container_width=True)

            fig_meta = px.line(df_agg, x='MES_ID', y='META', color='ENTORNO_DES', markers=True,
                            title="🔴 Meta promedio por entorno",
                            color_discrete_sequence=['#FFD700', '#E31937', '#A8071C', '#7A0513'])
            fig_meta.update_layout(
                font=dict(size=16, color='#333333'),
                xaxis_title="Mes",
                yaxis_title="Meta Promedio (MXN)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_meta, use_container_width=True)

        elif modo == "Comparar varias tiendas":
            tiendas_sel = st.multiselect("Selecciona tiendas", sorted(df_mes['TIENDA_ID'].unique()))
            if tiendas_sel:
                df_multi = df_mes[df_mes['TIENDA_ID'].isin(tiendas_sel)].sort_values(['TIENDA_ID', 'MES_ID'])

                # Paleta de colores oscuros para asegurar visibilidad
                colores_oxxo = [
                    "#E31937",  # Rojo OXXO oscuro
                    "#F2A007",  # Mostaza fuerte (amarillo OXXO)
                    "#3C3C3B",  # Gris oscuro neutro
                    "#0B3D91",  # Azul profundo (para contraste)
                    "#8C1D40",  # Vino/burdeo serio
                    "#58508D",  # Morado oscuro sobrio
                    "#BC4E00",  # Naranja quemado (parecido a uniforme)
                    "#2F4F4F",  # Verde grisáceo (profundo y neutro)
                    "#00736B",  # Verde petróleo
                    "#702963",  # Púrpura oscuro
                ]


                fig = px.line(df_multi, x='MES_ID', y='VENTA_TOTAL', color='TIENDA_ID', markers=True,
                            title="Comparación de Ventas por Tienda",
                            color_discrete_sequence=colores_oxxo)   
                fig.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='black')
                )

                metas = df_multi.groupby('TIENDA_ID')['META'].first()
                if metas.nunique() == 1:
                    meta_ref = metas.iloc[0]
                    fig.add_scatter(x=df_multi['MES_ID'].unique(),
                                    y=[meta_ref]*len(df_multi['MES_ID'].unique()),
                                    mode='lines', name='META',
                                    line=dict(color='gray', dash='dash'))

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Selecciona al menos una tienda para comparar.")

# --- Página: Mapa Interactivo ---

elif page == "Mapa Interactivo":
    import streamlit.components.v1 as components

    st.title("🗺️ Mapa de Análisis de Ubicación")
    st.markdown("Explora las ubicaciones de tiendas OXXO y el potencial de mercado geográficamente.")
    st.title("🗺️ Visualización del Mapa")
    try:
        with open("Streamlit/mapa_oxxo_tot.html", "r", encoding="utf-8") as f:
            html_mapa = f.read()
        components.html(html_mapa, height=600)
    except FileNotFoundError:
        st.error("❌ No se encontró el archivo `mapa.html`")

    # MODELO REGRESSOR

    import streamlit as st
    import pandas as pd
    import joblib

    # Cargar modelo
    modelo = joblib.load("Streamlit/xgb_final_cv_model.pkl")

    # Lista de features usadas en el modelo
    features = [
        'MTS2VENTAS_NUM', 'LATITUD_NUM', 'LONGITUD_NUM', 
        'densidad_varias_500m', 'oxxo_500m', 'densidad_pob_500m',
        'NIVELSOCIOECONOMICO_DES_A', 'NIVELSOCIOECONOMICO_DES_AB',
        'NIVELSOCIOECONOMICO_DES_B', 'NIVELSOCIOECONOMICO_DES_BC',
        'NIVELSOCIOECONOMICO_DES_C', 'NIVELSOCIOECONOMICO_DES_CD',
        'NIVELSOCIOECONOMICO_DES_D', 'ENTORNO_DES_Base', 'ENTORNO_DES_Hogar',
        'ENTORNO_DES_Peatonal', 'ENTORNO_DES_Receso',
        'LID_UBICACION_TIENDA_UT_CARRETERA_GAS',
        'LID_UBICACION_TIENDA_UT_DENSIDAD',
        'LID_UBICACION_TIENDA_UT_GAS_URBANA',
        'LID_UBICACION_TIENDA_UT_TRAFICO_PEATONAL',
        'LID_UBICACION_TIENDA_UT_TRAFICO_VEHICULAR',
        'SEGMENTO_MAESTRO_DESC_Barrio Competido'
    ]

    # Variables numéricas
    numeric_inputs = ['MTS2VENTAS_NUM', 'LATITUD_NUM', 'LONGITUD_NUM', 
                    'densidad_varias_500m', 'oxxo_500m', 'densidad_pob_500m']

    # Variables binarias (checkboxes)
    binary_inputs = [col for col in features if col not in numeric_inputs]

    st.title("🧠 Predicción de Viabilidad de Negocio")

    # Inputs numéricos
    input_data = {}
    for col in numeric_inputs:
        input_data[col] = st.number_input(col, value=0.0)

    # Agrupar por categorías según el prefijo
    nivel_socio = [col for col in binary_inputs if col.startswith("NIVELSOCIOECONOMICO_")]
    entorno = [col for col in binary_inputs if col.startswith("ENTORNO_DES_")]
    ubicacion = [col for col in binary_inputs if col.startswith("LID_UBICACION_TIENDA_")]
    otros = [col for col in binary_inputs if col not in nivel_socio + entorno + ubicacion]

    # Checkboxes dentro de expanders
    with st.expander("Nivel Socioeconómico"):
        for col in nivel_socio:
            input_data[col] = 1 if st.checkbox(col) else 0

    with st.expander("Entorno"):
        for col in entorno:
            input_data[col] = 1 if st.checkbox(col) else 0

    with st.expander("Ubicación de la tienda"):
        for col in ubicacion:
            input_data[col] = 1 if st.checkbox(col) else 0

    with st.expander("Otros"):
        for col in otros:
            input_data[col] = 1 if st.checkbox(col) else 0


    # Botón de predicción
    if st.button("Predecir", key="predecir_button"):
        df_input = pd.DataFrame([input_data])
        pred = modelo.predict(df_input)[0]
        proba = modelo.predict_proba(df_input)[0][1]

        st.markdown("### 🔍 Resultado:")
        st.success(f"¿Es viable? {'Sí ✅' if pred == 1 else 'No ❌'}")
        st.info(f"Probabilidad de éxito: {proba:.2%}")



        st.markdown("---")


#=========================================================================================================================================================

## MODELO XBOST
# Título de la aplicación
elif page == "Modelo de Predicción":
    st.title("Modelo de Predicción de Ventas")
    st.title("📊 Sistema de Predicción de Ventas")

    # Cargar el modelo
    @st.cache_resource
    def load_model():
        try:
            model = joblib.load('Streamlit/xgb_final_cv_model.pkl')
            return model
        except Exception as e:
            st.error(f"Error al cargar el modelo: {str(e)}")
            return None

    model = load_model()

    if model is None:
        st.stop()

    # Obtener nombres de características
    feature_names = model.get_booster().feature_names

    # Definir metas por entorno
    META_VENTA = {
        'Base': 480000,
        'Hogar': 490000,
        'Peatonal': 420000,
        'Receso': 516000
    }

    # Función para hacer predicción
    def make_prediction(input_df):
        try:
            # Asegurar el orden correcto de columnas
            input_df = input_df[feature_names]
            prediction = model.predict(input_df)[0]
            return prediction
        except Exception as e:
            st.error(f"Error en predicción: {str(e)}")
            return None

    # Clasificar características
    binary_inputs = [
        col for col in feature_names 
        if any(col.startswith(prefix) for prefix in ['NIVELSOCIOECONOMICO_', 'ENTORNO_DES_', 'LID_UBICACION_TIENDA_','SEGMENTO_MAESTRO_DESC_'])
    ]

    numeric_inputs = [col for col in feature_names if col not in binary_inputs]

    # Inicializar datos de entrada
    input_data = {feature: 0 for feature in binary_inputs}
    input_data.update({feature: 0.0 for feature in numeric_inputs})

    # Interfaz de usuario
    st.sidebar.header("Configuración")
    st.sidebar.info("Complete los valores requeridos y haga clic en 'Predecir'")

    # Sección para variables numéricas
    st.header("1. Características Numéricas")
    cols = st.columns(3)
    for i, feature in enumerate(numeric_inputs):
        with cols[i % 3]:
            if feature == 'TIENDA_ID':
                input_data[feature] = st.number_input(feature, min_value=1, value=100, key=f"num_{feature}")
            else:
                input_data[feature] = st.number_input(feature, value=0)

    # Sección para variables binarias (one-hot)
    st.header("2. Características Categóricas")

    # Agrupar por categorías según el prefijo
    nivel_socio = [col for col in binary_inputs if col.startswith("NIVELSOCIOECONOMICO_")]
    entorno = [col for col in binary_inputs if col.startswith("ENTORNO_DES_")]
    ubicacion = [col for col in binary_inputs if col.startswith("LID_UBICACION_TIENDA_")]
    otros = [col for col in binary_inputs if col not in nivel_socio + entorno + ubicacion]

    # Checkboxes dentro de expanders
    with st.expander("🔹 Nivel Socioeconómico"):
        cols = st.columns(2)
        for i, col in enumerate(nivel_socio):
            with cols[i % 2]:
                input_data[col] = 1 if st.checkbox(col.replace("NIVELSOCIOECONOMICO_", ""), key=col) else 0

    with st.expander("🏙️ Entorno de la Tienda"):
        # Solo permitir una selección (radio buttons)
        entorno_seleccionado = st.radio("Seleccione el entorno:", 
                                    [e.replace("ENTORNO_DES_", "") for e in entorno])
        for col in entorno:
            input_data[col] = 1 if col == f"ENTORNO_DES_{entorno_seleccionado}" else 0

    with st.expander("📍 Ubicación de la Tienda"):
        cols = st.columns(2)
        for i, col in enumerate(ubicacion):
            with cols[i % 2]:
                input_data[col] = 1 if st.checkbox(col.replace("LID_UBICACION_TIENDA_", ""), key=col) else 0

    if otros:
        with st.expander("⚙️ Otras Características"):
            cols = st.columns(2)
            for i, col in enumerate(otros):
                with cols[i % 2]:
                    input_data[col] = 1 if st.checkbox(col, key=col) else 0

    # Botón de predicción
    if st.button("🔮 Predecir Ventas", type="primary"):
        # Crear DataFrame con los datos de entrada
        input_df = pd.DataFrame([input_data])
        
        # Hacer predicción
        prediction = make_prediction(input_df)
        
        if prediction is not None:
            st.success("✅ Predicción realizada con éxito!")
            st.markdown("---")
            
            # Mostrar resultados
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Resultado de Predicción")
                st.metric("Ventas Totales Predichas", f"${prediction:,.2f}")
                
                # Determinar entorno seleccionado para comparar con meta
                entorno_actual = None
                for col in entorno:
                    if input_data[col] == 1:
                        entorno_actual = col.replace("ENTORNO_DES_", "")
                        break
                
                if entorno_actual in META_VENTA:
                    meta = META_VENTA[entorno_actual]
                    porcentaje = (prediction / meta) * 100
                    st.metric(f"Meta para entorno {entorno_actual}", 
                            f"${meta:,.2f}", 
                            f"{porcentaje:.1f}%",
                            delta_color="off" if porcentaje < 100 else "normal")
            
            with col2:
                st.subheader("Visualización")
                
                if entorno_actual in META_VENTA:
                    fig, ax = plt.subplots(figsize=(8, 3))
                    ax.bar(['Predicción'], [prediction], color='#4CAF50')
                    ax.axhline(y=meta, color='red', linestyle='--', label='Meta')
                    ax.set_ylabel('Ventas ($)')
                    ax.set_title('Comparación con Meta de Ventas')
                    ax.legend()
                    st.pyplot(fig)
                else:
                    st.info("Seleccione un entorno para comparar con la meta")
            
            # Mostrar detalles técnicos
            with st.expander("🔍 Detalles Técnicos"):
                st.write("**Características utilizadas:**")
                st.json({k: v for k, v in input_data.items() if v != 0})
                
                st.write("**Importancia de características:**")
                # Aquí podrías agregar la importancia de características si está disponible

