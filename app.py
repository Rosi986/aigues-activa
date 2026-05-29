import streamlit as st
import folium
from streamlit_folium import st_folium
import base64
from PIL import Image

# Intentar cargar la imagen del pino transparente como Favicon oficial del navegador
try:
    favicon = Image.open("tree.png")
except Exception:
    favicon = "🌲"

# 1. Configuración de la página (Favicon de pestaña del navegador personalizado)
st.set_page_config(
    page_title="Aigües Activa", 
    page_icon=favicon,
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Función para codificar imagen local a Base64
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded}"
    except Exception:
        return ""

logo_base64 = get_image_base64("logo.png")
tree_base64 = get_image_base64("tree.png")

# 2. Inyección de CSS premium para estética Glassmorphic en Smartphones
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    /* Global */
    .stApp {
        font-family: 'Outfit', sans-serif !important;
        background: linear-gradient(185deg, #09130d 0%, #102517 50%, #061922 100%) !important;
        color: #f8fafc !important;
    }
    
    /* Esconder elementos innecesarios */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    
    /* Contenedor App Móvil */
    .block-container {
        max-width: 460px !important;
        padding: 2rem 1.25rem !important;
        margin: 1.5rem auto !important;
        background: rgba(16, 32, 23, 0.65) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border-radius: 36px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6) !important;
    }
    
    /* Ficha Técnica Card */
    .tech-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
    }
    
    .tech-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
        margin-top: 0.75rem;
    }
    
    .tech-item {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 0.6rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.03);
    }
    
    .tech-label {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        margin-bottom: 0.15rem;
    }
    
    .tech-value {
        font-size: 1rem;
        font-weight: 700;
        color: #f1f5f9;
    }
    
    /* Selector de Rutas */
    .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        color: white !important;
    }
    
    /* Tabs Navegación */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.25rem !important;
        background-color: rgba(255, 255, 255, 0.03) !important;
        border-radius: 20px !important;
        padding: 0.35rem !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        width: 100% !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        flex: 1 !important;
        text-align: center !important;
        border-radius: 14px !important;
        padding: 0.5rem 0.25rem !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #94a3b8 !important;
        background-color: transparent !important;
        transition: all 0.25s ease !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #22c55e !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.25) !important;
    }
    
    /* Alerta Municipal */
    .municipal-alert {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.25);
        border-left: 5px solid #ef4444;
        color: #fca5a5;
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 1.25rem;
        font-size: 0.9rem;
    }
    
    /* Botón S.O.S. */
    .sos-button button {
        width: 100% !important;
        background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%) !important;
        color: white !important;
        border: none !important;
        padding: 1.2rem !important;
        border-radius: 20px !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important;
        box-shadow: 0 10px 30px rgba(239, 68, 68, 0.4) !important;
        transition: all 0.3s ease !important;
        letter-spacing: 1px;
    }
    
    .sos-button button:hover {
        background: linear-gradient(135deg, #f87171 0%, #dc2626 100%) !important;
        box-shadow: 0 15px 35px rgba(239, 68, 68, 0.6) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Tickets de Descuento */
    .ticket-container {
        position: relative;
        background: radial-gradient(circle at 0px 50% , transparent 10px, rgba(255,255,255,0.04) 11px), 
                    radial-gradient(circle at 100% 50% , transparent 10px, rgba(255,255,255,0.04) 11px);
        background-color: rgba(255, 255, 255, 0.04) !important;
        border: 1px dashed rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        overflow: hidden;
    }
    
    .ticket-locked {
        opacity: 0.4;
        filter: blur(1px);
        background-color: rgba(255, 255, 255, 0.01) !important;
    }
    
    .ticket-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px dashed rgba(255,255,255,0.1);
        padding-bottom: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .barcode {
        font-family: monospace;
        font-size: 1.5rem;
        color: #94a3b8;
        letter-spacing: 6px;
        text-align: center;
        margin-top: 0.5rem;
        opacity: 0.6;
    }
    
    /* Botón General */
    .stButton>button {
        width: 100% !important;
        background: rgba(255, 255, 255, 0.08) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 0.75rem !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        transition: all 0.25s ease !important;
    }
    
    .stButton>button:hover {
        background: #22c55e !important;
        border-color: #22c55e !important;
        box-shadow: 0 5px 15px rgba(34, 197, 94, 0.3) !important;
    }
    
    /* Custom info boxes */
    div[data-testid="stNotification"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-left: 4px solid #22c55e !important;
        border-radius: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Estado de la Sesión (Base de datos local en caché)
if 'checked_in' not in st.session_state:
    st.session_state.checked_in = {}
if 'redeemed' not in st.session_state:
    st.session_state.redeemed = {}
if 'alert' not in st.session_state:
    # Simula una alerta meteorológica activa recibida desde el panel de administración
    st.session_state.alert = "⚠️ Alerta Meteorológica: Alerta naranja por calor extremo hoy. Se desaconseja transitar por la Umbría entre las 12:00h y 17:00h."

# 4. Datos de Rutas y Waypoints
ROUTES = {
    "SL-CV 121: Vuelta a Aigües": {
        "id": "route_aigues_sl121",
        "dificultad": "Baja / Familiar 🟢",
        "distancia": "7.0 km",
        "desnivel": "+200 m",
        "tiempo": "1h 45m - 2h",
        "color": "green",
        "center": [38.4983, -0.4008],
        "zoom": 14,
        "path": [[38.4983, -0.4008], [38.4975, -0.4035], [38.5015, -0.4095], [38.5065, -0.4135], [38.5085, -0.4090], [38.5030, -0.4020], [38.4989, -0.4006], [38.4983, -0.4008]],
        "waypoints": [
            {"name": "Polideportivo Municipal (Inicio)", "coords": [38.4983, -0.4008], "desc": "Punto de salida oficial con zona de parking y Pino Manolo."},
            {"name": "Casco Antiguo y Torre de Aigües", "coords": [38.4989, -0.4006], "desc": "Atalaya defensiva del s. XIV catalogada como BIC con vistas a la bahía."},
            {"name": "Entorno del Preventorio", "coords": [38.5065, -0.4135], "desc": "Cercano al antiguo Balneario de Aguas de Busot. Patrimonio histórico."}
        ]
    },
    "PR-CV 243: El Camí de la Bacorera": {
        "id": "route_aigues_pr243",
        "dificultad": "Moderada 🟡",
        "distancia": "9.3 km",
        "desnivel": "+390 m",
        "tiempo": "2h 45m - 3h 15m",
        "color": "orange",
        "center": [38.5030, -0.3880],
        "zoom": 13,
        "path": [[38.4983, -0.4008], [38.4950, -0.3930], [38.5030, -0.3880], [38.5090, -0.3840], [38.5180, -0.3950], [38.5140, -0.4010], [38.5110, -0.4050], [38.5040, -0.4030], [38.4983, -0.4008]],
        "waypoints": [
            {"name": "Umbría de la Bacorera", "coords": [38.5030, -0.3880], "desc": "Zona forestal densa con microclima característico y abundante flora mediterránea."},
            {"name": "Vistas del Cabeçó d'Or", "coords": [38.5180, -0.3950], "desc": "Mirador natural idóneo para fotografiar la mole caliza del Cabeçó (1.208m)."},
            {"name": "Barranc de Salmitre", "coords": [38.5110, -0.4050], "desc": "Descenso entre características formaciones erosivas prelitorales."}
        ]
    },
    "Preventorio a la Cova de les Dones": {
        "id": "route_aigues_cova_dones",
        "dificultad": "Técnica / Moderada 🔴",
        "distancia": "8.0 km",
        "desnivel": "+280 m",
        "tiempo": "2h 30m",
        "color": "red",
        "center": [38.5065, -0.4135],
        "zoom": 14,
        "path": [[38.5065, -0.4135], [38.5090, -0.4110], [38.5115, -0.4140], [38.5125, -0.4160], [38.5140, -0.4180], [38.5130, -0.4210], [38.5080, -0.4180], [38.5065, -0.4135]],
        "waypoints": [
            {"name": "Preventorio / Hotel Miramar", "coords": [38.5065, -0.4135], "desc": "Antiguo e imponente balneario termal decimonónico con altísima demanda visual."},
            {"name": "Collado del Salmitre", "coords": [38.5125, -0.4160], "desc": "Paso de montaña elevado con vistas abiertas de Aitana y Benidorm."},
            {"name": "Cova de les Dones", "coords": [38.5140, -0.4180], "desc": "Cueva histórica catalogada como lugar de culto ibérico. Acceso empinado."}
        ]
    }
}

# 5. Cabecera Visual HTML Flexbox (Escudo Aigües - Título - Pino 3D)
header_html = f"""
<div style="display: flex; align-items: center; justify-content: space-between; width: 100%; margin-bottom: 1.25rem;">
    <img src="{logo_base64}" style="width: 58px; height: auto;" />
    <h1 style="font-family: 'Outfit', sans-serif; font-size: 1.95rem; font-weight: 800; margin: 0; padding: 0; background: linear-gradient(135deg, #a3e635 0%, #22c55e 50%, #06b6d4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Aigües Activa</h1>
    <img src="{tree_base64}" style="width: 58px; height: auto;" />
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# Mostrar Alerta activa si existe
if st.session_state.alert:
    st.markdown(f"<div class='municipal-alert'>{st.session_state.alert}</div>", unsafe_allow_html=True)

# 6. Menú de Navegación de la Aplicación en Pestañas
tab_explora, tab_pasaporte, tab_comercio, tab_sos, tab_eventos = st.tabs([
    "🗺️ Senderos", "🏆 Pasaporte", "🛍️ Comercios", "🚨 S.O.S.", "📅 Eventos"
])

# ================= TAB EXPLORA =================
with tab_explora:
    st.write("### 🧭 Selecciona tu Aventura:")
    selected_name = st.selectbox(
        "Ver detalles de la ruta:",
        list(ROUTES.keys()),
        label_visibility="collapsed"
    )
    
    route = ROUTES[selected_name]
    
    # Ficha Técnica
    st.markdown(f"""
    <div class='tech-card'>
        <div style='font-weight: 700; font-size: 1.15rem; color: #a3e635; margin-bottom: 0.25rem;'>
            {selected_name}
        </div>
        <div style='font-size: 0.9rem; color: #cbd5e1;'>
            Marcas oficiales de la ruta homologada. Pistas y sendas transitables.
        </div>
        <div class='tech-grid'>
            <div class='tech-item'>
                <div class='tech-label'>Dificultad</div>
                <div class='tech-value'>{route["dificultad"]}</div>
            </div>
            <div class='tech-item'>
                <div class='tech-label'>Distancia</div>
                <div class='tech-value'>{route["distancia"]}</div>
            </div>
            <div class='tech-item'>
                <div class='tech-label'>Desnivel</div>
                <div class='tech-value'>{route["desnivel"]}</div>
            </div>
            <div class='tech-item'>
                <div class='tech-label'>Tiempo Est.</div>
                <div class='tech-value'>{route["tiempo"]}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Mapa interactivo
    st.write("#### 🗺️ Mapa del Recorrido:")
    mapa = folium.Map(location=route["center"], zoom_start=route["zoom"], tiles="OpenStreetMap")
    
    # Dibujar traza de ruta
    folium.PolyLine(
        route["path"], 
        color=route["color"], 
        weight=4, 
        opacity=0.8, 
        tooltip=selected_name
    ).add_to(mapa)
    
    # Añadir waypoints al mapa
    for i, wp in enumerate(route["waypoints"]):
        icon_color = "darkgreen" if i == 0 else "blue"
        if i == len(route["waypoints"]) - 1 and "cova" in route["id"]:
            icon_color = "red"  # Cueva peligrosa
            
        folium.Marker(
            wp["coords"],
            popup=f"<b>{wp['name']}</b><br>{wp['desc']}",
            tooltip=wp["name"],
            icon=folium.Icon(color=icon_color, icon="info-sign")
        ).add_to(mapa)

    # INYECCIÓN JAVASCRIPT DE GEOLOCALIZACIÓN Y SEGUIMIENTO REAL EN LEAFLET
    gps_tracking_script = """
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        setTimeout(function() {
            // Encontrar la instancia de Leaflet Map de Folium
            var maps = [];
            for (var key in window) {
                if (key.indexOf("map_") === 0 && window[key] instanceof L.Map) {
                    maps.push(window[key]);
                }
            }
            if (maps.length === 0) return;
            var map = maps[0];

            // Crear capa para dibujar el recorrido del usuario (Polyline verde)
            var walkPoints = [];
            var walkPolyline = L.polyline(walkPoints, {
                color: '#22c55e', // Verde brillante de Aigües Activa
                weight: 6,
                opacity: 0.9,
                dashArray: '5, 8'
            }).addTo(map);

            var userDot = null;
            var userAccuracyCircle = null;
            var watchId = null;
            var isTracking = false;

            // Inyectar botón de Geolocalización Real en la barra de Leaflet
            var GpsControl = L.Control.extend({
                options: { position: 'topleft' },
                onAdd: function (map) {
                    var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-gps-control');
                    container.style.backgroundColor = '#15803d';
                    container.style.color = '#ffffff';
                    container.style.width = '34px';
                    container.style.height = '34px';
                    container.style.display = 'flex';
                    container.style.alignItems = 'center';
                    container.style.justifyContent = 'center';
                    container.style.borderRadius = '6px';
                    container.style.cursor = 'pointer';
                    container.style.boxShadow = '0 1px 5px rgba(0,0,0,0.5)';
                    container.innerHTML = '🛰️';
                    container.title = 'Activar GPS Real y Seguir Ruta';

                    container.onclick = function(e) {
                        e.stopPropagation();
                        if (!isTracking) {
                            startGpsTracking();
                        } else {
                            stopGpsTracking();
                        }
                    };
                    return container;
                }
            });
            map.addControl(new GpsControl());

            function startGpsTracking() {
                if (!navigator.geolocation) {
                    alert("⚠️ CONTEXTO INSEGURO (HTTP): Los navegadores móviles bloquean el GPS por seguridad en enlaces HTTP ordinarios.\n\nPara probar el GPS real en tu móvil de inmediato, tienes dos opciones:\n1. Sube la app a Streamlit Cloud (¡es gratis y automático con HTTPS!)\n2. O bien, accede desde tu ordenador con localhost.\n\nMientras tanto, puedes usar la pestaña 'Pasaporte' para simular el GPS.");
                    return;
                }
                
                isTracking = true;
                var btn = document.querySelector('.leaflet-gps-control');
                if (btn) {
                    btn.style.backgroundColor = '#ef4444'; // Cambiar a rojo (Activo)
                    btn.title = 'Detener GPS Real';
                    btn.innerHTML = '🛑';
                }

                watchId = navigator.geolocation.watchPosition(function(position) {
                    var lat = position.coords.latitude;
                    var lng = position.coords.longitude;
                    var acc = position.coords.accuracy;
                    var currentPos = [lat, lng];

                    // Añadir coordenada a la traza y actualizar línea verde
                    walkPoints.push(currentPos);
                    walkPolyline.setLatLngs(walkPoints);

                    // Posicionar marcador circular del usuario
                    if (!userDot) {
                        userDot = L.circleMarker(currentPos, {
                            color: '#15803d',
                            fillColor: '#22c55e',
                            fillOpacity: 0.9,
                            radius: 8,
                            weight: 3
                        }).addTo(map);
                        
                        userAccuracyCircle = L.circle(currentPos, {
                            radius: acc,
                            color: '#22c55e',
                            fillColor: '#22c55e',
                            fillOpacity: 0.15,
                            weight: 1
                        }).addTo(map);
                    } else {
                        userDot.setLatLng(currentPos);
                        userAccuracyCircle.setLatLng(currentPos);
                        userAccuracyCircle.setRadius(acc);
                    }

                    // Seguir y centrar el mapa suavemente en la posición del caminante
                    map.setView(currentPos, 16);
                }, function(error) {
                    console.error("Error capturando señal GPS:", error);
                    if (error.code === 1) { // PERMISSION_DENIED
                        alert("⚠️ Permiso de Ubicación Denegado: Por favor, activa el permiso de GPS en los ajustes de tu navegador para esta página.");
                    } else {
                        alert("⚠️ Error del GPS móvil (Código " + error.code + "): Asegúrate de estar al aire libre con buena visibilidad de satélites.");
                    }
                }, {
                    enableHighAccuracy: true,
                    maximumAge: 0,
                    timeout: 10000
                });
            }

            function stopGpsTracking() {
                isTracking = false;
                var btn = document.querySelector('.leaflet-gps-control');
                if (btn) {
                    btn.style.backgroundColor = '#15803d';
                    btn.title = 'Activar GPS Real y Seguir Ruta';
                    btn.innerHTML = '🛰️';
                }
                
                if (watchId !== null) {
                    navigator.geolocation.clearWatch(watchId);
                    watchId = null;
                }
                if (userDot) {
                    map.removeLayer(userDot);
                    userDot = null;
                }
                if (userAccuracyCircle) {
                    map.removeLayer(userAccuracyCircle);
                    userAccuracyCircle = null;
                }
            }

            // AUTO-INICIAR GEOLOCALIZACIÓN AL CARGAR
            setTimeout(function() {
                startGpsTracking();
            }, 100);
            
        }, 1500); // Pequeño retraso para asegurar carga del DOM de Leaflet
    });
    </script>
    """
    mapa.get_root().html.add_child(folium.Element(gps_tracking_script))
    
    # RENDERIZAR MAPA COMO HTML REAL PARA SOPORTAR INYECCIÓN JAVASCRIPT DE GEOLOCALIZACIÓN
    st.components.v1.html(mapa._repr_html_(), height=320)
    
    # Alertas específicas de la ruta
    if "cova" in route["id"]:
        st.warning("⚠️ **Alerta de Seguridad**: El acceso directo a la boca de la Cova de les Dones es abrupto y estrecho. Extrema las precauciones y lleva calzado con excelente adherencia.")
        
    # Toggle de guiado de voz
    st.write("---")
    guiado = st.toggle("📢 Activar Guiado por Voz (Asistente Turístico)", key="voice_guide")
    if guiado:
        st.info("🎙️ *El asistente de voz está activo. Recibirás indicaciones sonoras en los puntos de interés oficiales y avisos de desvío.*")

# ================= TAB PASAPORTE =================
with tab_pasaporte:
    st.write("### 🏆 Tu Pasaporte Digital de Aigües")
    st.write("Visita los puntos emblemáticos y boscosos oficiales para conseguir trofeos digitales y desbloquear descuentos.")
    
    route_name = selected_name
    route = ROUTES[route_name]
    waypoints = route["waypoints"]
    
    # Calcular progreso
    completed_wps = [wp["name"] for wp in waypoints if st.session_state.checked_in.get(wp["name"], False)]
    progress_val = len(completed_wps) / len(waypoints)
    
    st.write(f"Ruta activa: **{route_name}**")
    st.progress(progress_val)
    st.write(f"Progreso: **{len(completed_wps)} de {len(waypoints)} puntos visitados**")
    
    st.write("---")
    
    # Listar Waypoints de control
    for wp in waypoints:
        col_text, col_check = st.columns([3, 1])
        
        is_checked = st.session_state.checked_in.get(wp["name"], False)
        
        with col_text:
            st.markdown(f"**📍 {wp['name']}**")
            st.caption(wp["desc"])
            
        with col_check:
            if is_checked:
                st.markdown("<div style='color:#a3e635; font-weight:700; text-align:center; padding-top:10px;'>✅ VISITA</div>", unsafe_allow_html=True)
            else:
                if st.button("Simular GPS", key=f"chk_{wp['name']}"):
                    st.session_state.checked_in[wp["name"]] = True
                    st.rerun()
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        
    # Comprobar si completó toda la ruta activa
    all_done = all(st.session_state.checked_in.get(wp["name"], False) for wp in waypoints)
    
    if all_done:
        st.balloons()
        st.success(f"🎉 ¡Felicidades! Has completado el 100% de la ruta **{route_name}**. Has desbloqueado una nueva insignia oficial y tus cupones de descuento están listos en la sección de Comercio Local.")

# ================= TAB COMERCIO =================
with tab_comercio:
    st.write("### 🛍️ Comercio Local y Reactivación")
    st.write("Presenta tu pantalla al pagar en los establecimientos de Aigües para canjear tus ventajas. ¡Apoya a la economía local!")
    
    # Negocios locales y sus cupones
    COMMERCES = [
        {
            "name": "Restaurante El Preventorio",
            "desc": "Cocina de montaña y carnes a la brasa al lado del Balneario.",
            "coupon": "10% de descuento en Menú de Fin de Semana",
            "condition": "Completa la ruta del Preventorio o SL-CV 121",
            "unlocked": all(st.session_state.checked_in.get(wp["name"], False) for wp in ROUTES["SL-CV 121: Vuelta a Aigües"]["waypoints"]) or 
                        all(st.session_state.checked_in.get(wp["name"], False) for wp in ROUTES["Preventorio a la Cova de les Dones"]["waypoints"]),
            "code": "PREV-AIGUES-10"
        },
        {
            "name": "Cafetería La Plaza de Aigües",
            "desc": "Desayunos, cafés de especialidad y almuerzos tradicionales en el centro del pueblo.",
            "coupon": "Café o Bebida Gratis con tu almuerzo de montaña",
            "condition": "Visita al menos 1 punto de control de cualquier ruta",
            "unlocked": len([w for w in st.session_state.checked_in.values() if w]) >= 1,
            "code": "CAF-PLAZA-AIGUES"
        },
        {
            "name": "Horno Tradicional y Pastelería Aigües",
            "desc": "Pan tradicional a leña y las mejores cocas de la comarca.",
            "coupon": "Un Dulce Tradicional Gratis por compra superior a 5€",
            "condition": "Completa el PR-CV 243 (La Bacorera)",
            "unlocked": all(st.session_state.checked_in.get(wp["name"], False) for wp in ROUTES["PR-CV 243: El Camí de la Bacorera"]["waypoints"]),
            "code": "PAN-BACORERA-FREE"
        }
    ]
    
    for idx, shop in enumerate(COMMERCES):
        if shop["unlocked"]:
            is_redeemed = st.session_state.redeemed.get(shop["name"], False)
            
            if is_redeemed:
                st.markdown(f"""
                <div class='ticket-container' style='opacity:0.5;'>
                    <div class='ticket-header'>
                        <span style='font-weight:700; color:#94a3b8;'>{shop["name"]}</span>
                        <span style='color:#ef4444; font-weight:700;'>❌ CANJEADO</span>
                    </div>
                    <p style='margin:0.5rem 0; font-size:0.95rem; text-decoration:line-through;'>{shop["coupon"]}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='ticket-container'>
                    <div class='ticket-header'>
                        <span style='font-weight:700; color:#a3e635;'>{shop["name"]}</span>
                        <span style='background:#22c55e; color:white; font-size:0.75rem; padding:2px 8px; border-radius:10px; font-weight:700;'>🎟️ ACTIVO</span>
                    </div>
                    <p style='margin:0.5rem 0; font-size:0.95rem; font-weight:600; color:#f1f5f9;'>{shop["coupon"]}</p>
                    <p style='font-size:0.8rem; color:#94a3b8;'>{shop["desc"]}</p>
                    <div class='barcode'>{shop["code"]}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Validar y Canjear en {shop['name']}", key=f"red_{idx}"):
                    st.session_state.redeemed[shop["name"]] = True
                    st.success(f"¡Cupón de {shop['name']} canjeado con éxito! Que aproveche. 🥳")
                    st.rerun()
        else:
            st.markdown(f"""
            <div class='ticket-container ticket-locked'>
                <div class='ticket-header'>
                    <span style='font-weight:700; color:#94a3b8;'>{shop["name"]}</span>
                    <span style='color:#94a3b8;'>🔒 BLOQUEADO</span>
                </div>
                <p style='margin:0.5rem 0; font-size:0.95rem;'>{shop["coupon"]}</p>
                <p style='font-size:0.8rem; color:#64748b; font-weight:500;'>Requisito: {shop["condition"]}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ================= TAB S.O.S. =================
with tab_sos:
    st.write("### 🚨 Centro de Emergencias y S.O.S.")
    st.write("Si necesitas asistencia durante la ruta por la montaña, activa el botón de socorro para enviar tu posición geográfica.")
    
    # Coordenadas simuladas
    st.markdown("""
    <div style='background:rgba(255,255,255,0.03); border-radius:16px; padding:1rem; border:1px solid rgba(255,255,255,0.05); margin-bottom:1.5rem;'>
        <div style='display:flex; justify-content:space-between; margin-bottom:0.4rem;'>
            <span style='color:#94a3b8; font-size:0.85rem;'>Ubicación GPS</span>
            <span style='color:#22c55e; font-size:0.85rem; font-weight:600;'>🟢 Conectado</span>
        </div>
        <div style='font-size:1.15rem; font-weight:700; font-family:monospace; color:#f1f5f9;'>
            Lat: 38.4983° N <br> Lon: -0.4008° W
        </div>
        <div style='color:#94a3b8; font-size:0.8rem; margin-top:0.3rem;'>
            Precisión GPS: ±4 metros | Altitud: 342m
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='sos-button'>", unsafe_allow_html=True)
    if st.button("🚨 ACTIVAR BOTÓN S.O.S.", key="sos_btn"):
        st.error("⚠️ **ALERTA DE EMERGENCIA ACTIVADA**")
        st.markdown("""
        <div style='background:rgba(239, 68, 68, 0.1); border:1px solid rgba(239, 68, 68, 0.3); border-radius:16px; padding:1.25rem; margin-top:1rem;'>
            <h4 style='color:#f87171; margin-top:0;'>⚠️ Transmisión de Emergencia Iniciada</h4>
            <p style='font-size:0.9rem; color:#fca5a5; margin-bottom:0.5rem;'>
                Tus coordenadas exactas (<b>38.4983, -0.4008</b>) han sido simuladas y transmitidas a los Servicios de Emergencia del Ayuntamiento de Aigües y Protección Civil.
            </p>
            <p style='font-size:0.85rem; font-weight:600; color:#ffffff;'>
                👉 Qué hacer ahora:
            </p>
            <ul style='font-size:0.85rem; color:#cbd5e1; padding-left:20px; margin-bottom:0;'>
                <li>No te muevas del sendero señalizado.</li>
                <li>Mantén tu dispositivo con batería.</li>
                <li>Espera instrucciones por llamada o SMS.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("---")
    
    offline_mode = st.toggle("💾 Descarga de Mapas y Alertas en Caché (Modo Offline)", value=False)
    if offline_mode:
        st.success("📂 **Modo Offline Activado**: Se han descargado los datos de las 3 rutas y la topografía local en la caché SQLite local de la aplicación. Mantendrás el mapa activo incluso si pierdes cobertura en los desfiladeros de la Bacorera o la Cova de les Dones.")

# ================= TAB EVENTOS =================
with tab_eventos:
    st.write("### 📅 Agenda Cultural y Eventos")
    st.write("Mantente al día con los conciertos, exposiciones y actividades culturales organizadas por el Ayuntamiento de Aigües.")
    
    # NUEVO EVENTO: EXPOSICIÓN DE PINTURA (PRIMER EVENTO WEB OFICIAL)
    st.markdown("""
    <div class='ticket-container' style='border: 1px solid rgba(255, 255, 255, 0.1);'>
        <div class='ticket-header'>
            <span style='font-weight:700; color:#eab308;'>🎨 José Manuel Cámara</span>
            <span style='background:#ec4899; color:white; font-size:0.75rem; padding:2px 8px; border-radius:10px; font-weight:700;'>EXPOSICIÓN</span>
        </div>
        <p style='margin:0.5rem 0; font-size:0.95rem; font-weight:600; color:#f1f5f9;'>Exposición de Pintura «por Dibujo Alicante»</p>
        <p style='font-size:0.85rem; color:#cbd5e1; margin-bottom:0.8rem;'>
            Una magnífica colección artística de ilustraciones y dibujos al aire libre que capturan rincones y paisajes urbanos emblemáticos de la provincia de Alicante.
        </p>
        <p style='font-size:0.8rem; color:#94a3b8; margin: 3px 0;'><b>📍 Ubicación:</b> Excmo. Ayuntamiento de Aigües (Calle Mayor 5, Entrada Libre)</p>
        <p style='font-size:0.8rem; color:#94a3b8; margin: 3px 0;'><b>⏰ Fechas:</b> Del 22 de Mayo al 10 de Junio de 2026</p>
        <p style='font-size:0.8rem; color:#94a3b8; margin: 3px 0;'><b>⏰ Horario de visitas:</b> Lunes a Viernes de 09:00h a 14:00h</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Renderizar el cartel de la exposición
    st.image(
        "https://www.aigues.es/wp-content/uploads/2026/05/Exposicion-por-Dibujo-Alicante.jpg", 
        use_column_width=True, 
        caption="Cartel Oficial de la Exposición - Ayuntamiento de Aigües"
    )
    
    if st.button("🔔 Recordar Exposición", key="exposicion_btn"):
        st.success("¡Recordatorio añadido con éxito! 🗓️ Recibirás un aviso en tu móvil para asistir a la exposición en el Ayuntamiento.")
        
    st.write("---")
    
    # EVENTO EXISTENTE ACTUALIZADO CON SU FECHA REAL DE LA WEB
    st.markdown("""
    <div class='ticket-container' style='border: 1px solid rgba(255, 255, 255, 0.1);'>
        <div class='ticket-header'>
            <span style='font-weight:700; color:#a3e635;'>🎷 Le Jazz Hot</span>
            <span style='background:#3b82f6; color:white; font-size:0.75rem; padding:2px 8px; border-radius:10px; font-weight:700;'>CONCIERTO</span>
        </div>
        <p style='margin:0.5rem 0; font-size:0.95rem; font-weight:600; color:#f1f5f9;'>Ciclo de Conciertos de Verano en Aigües</p>
        <p style='font-size:0.85rem; color:#cbd5e1; margin-bottom:0.8rem;'>
            Disfruta de una noche estival única bajo las estrellas de Aigües con el mejor jazz clásico y tradicional en directo.
        </p>
        <p style='font-size:0.8rem; color:#94a3b8; margin: 3px 0;'><b>📍 Ubicación:</b> Jardín de la Casa de Cultura (Entrada Gratuita)</p>
        <p style='font-size:0.8rem; color:#94a3b8; margin: 3px 0;'><b>⏰ Horario:</b> Sábado, 30 de Mayo de 2026 a las 20:00h</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Renderizar el cartel del concierto
    st.image(
        "https://www.aigues.es/wp-content/uploads/2026/05/Le-Jazz-Hot.jpg", 
        use_column_width=True, 
        caption="Cartel Oficial del Evento - Ayuntamiento de Aigües"
    )
    
    if st.button("📅 Recordar y Añadir a mi Calendario", key="calendar_btn"):
        st.success("¡Evento añadido con éxito! 🗓️ Recibirás un recordatorio automático en tu móvil 2 horas antes de que empiece el concierto.")

# Pie de página institucional oficial con Escudo y Árbol 3D
st.write("---")
footer_html = f"""
<div style='display:flex; align-items:center; justify-content:center; gap:0.55rem; opacity:0.85; margin-top:1rem;'>
    <img src='{logo_base64}' style='width:24px; height:auto;' />
    <span style='color:#64748b; font-size:0.82rem; font-weight:600; letter-spacing:0.5px;'>
        Excmo. Ayuntamiento de Aigües
    </span>
    <img src='{tree_base64}' style='width:24px; height:auto;' />
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#475569; font-size:0.75rem; margin-top:0.15rem; font-style:italic;'>Aigües Activa: Deporte y Patrimonio Natural del Municipio</p>", unsafe_allow_html=True)
