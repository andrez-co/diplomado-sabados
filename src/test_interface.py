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

    # Botón principal para alternar el tema
    toggle_button = soup.find(id="dark-mode-toggle")
    assert toggle_button is not None, "El botón '#dark-mode-toggle' debe existir en el DOM."
    assert toggle_button.name == "button", "El selector #dark-mode-toggle debe corresponder a un elemento <button>."

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

