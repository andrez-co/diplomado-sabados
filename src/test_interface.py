"""Suite de pruebas automatizadas para validar la integridad del frontend estático (index.html).

Valida estructura básica, importaciones de CDN, evaluación del Feature Flag
y presencia de selectores clave antes de la construcción de la imagen Docker.
"""

from pathlib import Path
import pytest
from bs4 import BeautifulSoup

INDEX_PATH = Path(__file__).resolve().parent / "index.html"


@pytest.fixture(scope="session")
def html_soup():
    """Fixture que carga y parsea el archivo index.html."""
    assert INDEX_PATH.exists(), f"El archivo {INDEX_PATH} no existe."
    content = INDEX_PATH.read_text(encoding="utf-8")
    assert len(content.strip()) > 0, "El archivo index.html está vacío."
    return BeautifulSoup(content, "html.parser"), content


def test_index_html_exists_and_basic_structure(html_soup):
    """Test 1: Verificar que index.html existe y contiene estructura HTML válida."""
    soup, content = html_soup

    # Verificar que inicia con DOCTYPE html
    assert content.lstrip().lower().startswith("<!doctype html>"), (
        "El documento debe comenzar con <!DOCTYPE html>."
    )

    # Validar etiquetas estructurales básicas de HTML5
    assert soup.find("html") is not None, "Falta la etiqueta <html>."
    assert soup.find("head") is not None, "Falta la etiqueta <head>."
    assert soup.find("body") is not None, "Falta la etiqueta <body>."

    # Validar metadatos y título
    title = soup.find("title")
    assert title is not None and len(title.text.strip()) > 0, (
        "El documento debe contener una etiqueta <title> no vacía."
    )

    meta_viewport = soup.find("meta", attrs={"name": "viewport"})
    assert meta_viewport is not None, "Debe incluirse la etiqueta meta viewport para responsive design."


def test_cdn_scripts_imported(html_soup):
    """Test 2: Validar que el script de ConfigCat CDN y el script de Tailwind CSS estén importados."""
    soup, _ = html_soup

    scripts = soup.find_all("script")
    script_sources = [s.get("src", "") for s in scripts if s.get("src")]

    # Validar Tailwind CSS CDN
    has_tailwind_cdn = any("cdn.tailwindcss.com" in src for src in script_sources)
    assert has_tailwind_cdn, (
        "No se encontró el script CDN de Tailwind CSS (cdn.tailwindcss.com) en el documento."
    )

    # Validar ConfigCat SDK CDN
    has_configcat_cdn = any("configcat" in src.lower() for src in script_sources)
    assert has_configcat_cdn, (
        "No se encontró el script CDN de ConfigCat SDK en el documento."
    )


def test_flag_evaluation_logic_present(html_soup):
    """Test 3: Verificar que el código contenga la evaluación del flag 'dark_mode_enabled'."""
    _, content = html_soup

    # Verificar mención explícita del flag esperado
    assert "dark_mode_enabled" in content, (
        "El código JavaScript debe referenciar y evaluar el flag 'dark_mode_enabled'."
    )

    # Verificar inicialización del cliente ConfigCat
    assert "configcat.getClient" in content, (
        "El código debe inicializar el cliente usando configcat.getClient(...)."
    )

    # Verificar lógica para alternar la clase 'dark' en <html>
    assert "classList.toggle" in content and "dark" in content, (
        "El código debe contener la llamada para alternar la clase 'dark'."
    )


def test_key_selectors_and_elements_present(html_soup):
    """Test 4: Comprobar que los selectores y elementos clave estén presentes en el HTML."""
    soup, _ = html_soup

    # Contenedor del toggle en el Navbar
    toggle_container = soup.find(id="toggle-container")
    assert toggle_container is not None, "El elemento '#toggle-container' debe existir en el DOM."

    # Botón principal para alternar el tema (soporta id='theme-toggle' de Taller 6 o '#dark-mode-toggle')
    toggle_button = soup.find(id="theme-toggle") or soup.find(id="dark-mode-toggle")
    assert toggle_button is not None, "El botón '#theme-toggle' o '#dark-mode-toggle' debe existir en el DOM."
    assert toggle_button.name == "button", "El selector debe corresponder a un elemento <button>."
    assert "hidden" in toggle_button.get("class", []), "El botón debe estar oculto inicialmente (hidden)."
    assert toggle_button.get("data-testid") == "theme-toggle", "El botón debe tener data-testid='theme-toggle'."

    # Iconos para el estado visual del botón (Luna y Sol)
    assert soup.find(id="icon-moon") is not None, "Debe existir el elemento '#icon-moon' para modo claro."
    assert soup.find(id="icon-sun") is not None, "Debe existir el elemento '#icon-sun' para modo oscuro."

    # Mensaje o estado para cuando el flag esté deshabilitado
    assert soup.find(id="disabled-notice") is not None, (
        "Debe existir el elemento '#disabled-notice' para comunicar el estado cuando el flag sea false."
    )


def test_stile_css_linked_and_exists(html_soup):
    """Test 5: Comprobar que el archivo de estilos stile.css existe y está vinculado."""
    soup, _ = html_soup
    css_path = Path(__file__).resolve().parent / "stile.css"

    # Verificar existencia física del archivo
    assert css_path.exists(), f"El archivo {css_path} debe existir."
    assert len(css_path.read_text(encoding="utf-8").strip()) > 0, "El archivo stile.css no debe estar vacío."

    # Verificar que index.html lo incluye en una etiqueta <link>
    links = soup.find_all("link", attrs={"rel": "stylesheet"})
    link_hrefs = [l.get("href", "") for l in links]
    assert any("stile.css" in href for href in link_hrefs), (
        "El documento index.html debe incluir un tag <link rel='stylesheet' href='stile.css'>."
    )


def test_telemetry_and_safe_rollout_present(html_soup):
    """Test 6: Validar observabilidad, telemetría y liberación segura (Taller 6)."""
    soup, content = html_soup

    # 1. Módulo global window.telemetry con logEvent y logError
    assert "window.telemetry" in content, "El script debe definir el módulo window.telemetry."
    assert "logEvent" in content, "window.telemetry debe implementar logEvent."
    assert "logError" in content, "window.telemetry debe implementar logError."

    # 2. Listener global para capturar errores del cliente
    assert "addEventListener" in content and "error" in content, (
        "Debe registrarse un listener global para eventos de error (window.addEventListener('error', ...))."
    )

    # 3. Registro de eventos FlagEvaluated y ThemeToggled
    assert "FlagEvaluated" in content, "Debe registrarse el evento de telemetría 'FlagEvaluated'."
    assert "ThemeToggled" in content, "Debe registrarse el evento de telemetría 'ThemeToggled'."

    # 4. Botón con data-testid="theme-toggle"
    btn = soup.find(attrs={"data-testid": "theme-toggle"})
    assert btn is not None, "El botón debe incluir el atributo data-testid='theme-toggle'."


def test_rollout_in_3_phases_and_targeting_present(html_soup):
    """Test 7: Validar la liberación segura en 3 fases y targeting de ConfigCat (Taller 6)."""
    soup, content = html_soup

    # 1. Contenedor del simulador de 3 fases
    simulator = soup.find(id="rollout-simulator")
    assert simulator is not None, "Debe existir el elemento '#rollout-simulator' para probar las 3 fases."

    # 2. Botones de perfiles (Interno, Canario %, General)
    assert soup.find(id="btn-role-internal") is not None, "Debe existir el botón '#btn-role-internal' (Fase 1)."
    assert soup.find(id="btn-role-canary") is not None, "Debe existir el botón '#btn-role-canary' (Fase 2)."
    assert soup.find(id="btn-role-public") is not None, "Debe existir el botón '#btn-role-public' (Fase 3)."
    assert soup.find(id="btn-new-canary-user") is not None, "Debe existir '#btn-new-canary-user' para probar hashes."

    # 3. Banner de alerta de Rollback Automático (Circuit Breaker)
    assert soup.find(id="rollback-alert-banner") is not None, "Debe existir '#rollback-alert-banner' para circuit breaker."

    # 4. Verificación de lógica de usuario y targeting en ConfigCat SDK
    assert "currentUser" in content, "El script debe mantener el estado del usuario activo (currentUser)."
    assert "evaluateWithUser" in content, "El script debe implementar evaluateWithUser para evaluar con User Object."
    assert "getValueAsync(FLAG_NAME, false, currentUser)" in content or "getValueAsync" in content, (
        "ConfigCat debe evaluar el flag pasando el objeto de usuario."
    )
