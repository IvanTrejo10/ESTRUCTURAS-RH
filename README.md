# Estructuras RH

Página Streamlit para generar las estructuras semanales de RH a partir de las bases CR y Vales.

## Uso

1. Elige el año y la semana.
2. Sube la base CR y/o la base de Vales en formato `.xlsx`.
3. Opcionalmente, sube los reportes finales de la semana anterior para comparar sus datos y conservar su formato.
4. Pulsa **Crear estructuras**. Revisa las pestañas y descarga los Excel, individualmente o en ZIP.

La aplicación admite generar sólo uno de los reportes. Si cambias un archivo o el periodo, debes volver a generarlos para actualizar las descargas.

## Ejecutar en tu computadora

Requiere Python 3.12.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Publicar desde GitHub

Sube **el contenido de esta carpeta** a un repositorio de GitHub. Los archivos principales deben quedar así:

```text
app.py
structures.py
ui.py
assets/styles.css
requirements.txt
.streamlit/config.toml
.gitignore
README.md
tests/
```

El diseño del portal se personaliza en `assets/styles.css`; `ui.py` contiene los componentes visuales. Incluye menú lateral con el periodo, tarjetas para las bases y vista de resultados adaptable a pantallas pequeñas. Sube también esos archivos al repositorio.

En [Streamlit Community Cloud](https://share.streamlit.io), selecciona **Create app**, el repositorio, la rama y `app.py` como archivo principal. En Advanced settings, selecciona Python 3.12 y despliega la app.

No necesitas poner tus bases semanales en GitHub ni configurar credenciales de OneDrive: los archivos se suben desde la página. Este proyecto no incluye datos reales. El `.gitignore` excluye Excel, CSV, ZIP y secretos. Si lo integras en un repositorio más grande, coloca `.streamlit/config.toml` en la raíz de ese repositorio, como requiere Streamlit.

Documentación oficial: [organización de archivos](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization), [despliegue](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).

## Reglas de los reportes

| Reporte | Pestañas | Columnas |
| --- | --- | --- |
| CR México | MEXICO | Ruta, Territorio, Subdireccion, Zona, Sucursal, Marca, País |
| CR otros países | GUATEMALA, PERU, EL SALVADOR, COLOMBIA, HONDURAS, NICARAGUA | Ruta, Territorio, Zona, Sucursal, Marca, País |
| Vales | Rapi, Peru, Vale Amigo, Viva Vale | Coordinacion, Subdirección, Zona, Sucursal, Marca |

En CR fuera de México, **Territorio se toma de Subdireccion** de la base, siguiendo el formato de RH. En México se mantienen ambos campos. Los países y las marcas se identifican sin distinguir mayúsculas o acentos. Los valores de las columnas se conservan como texto, incluidos los ceros iniciales.

La hoja preferida de CR es `Estructuras` y la de Vales es `Hoja 1`. Si existe una única hoja con las columnas requeridas, también puede usarse. La aplicación valida encabezados, registros incompletos, claves duplicadas y países o marcas fuera del catálogo antes de generar la descarga. Si una fórmula de la base no tiene un resultado guardado, abre y guarda el archivo en Excel para actualizarlo.

### Comparación

La clave es Ruta o Coordinacion dentro de cada pestaña. Se muestran altas, bajas y registros modificados. Un registro con varias columnas modificadas cuenta una vez en el resumen y puede aparecer varias veces en el detalle. Un cambio de clave se registra como una alta y una baja; no se infiere un renombre. El detalle se puede descargar en CSV.

Cuando se carga un reporte anterior se reutilizan encabezados, anchos de columna, fuentes, colores, bordes y alineación de las hojas esperadas. Los resultados son libros nuevos que contienen sólo las pestañas de RH y valores, sin fórmulas, vínculos externos ni hojas históricas internas. Si no cargas el anterior, se aplica el formato habitual incluido en el código.

### Archivos y sesiones

Las bases y los resultados se procesan en memoria y se mantienen durante la sesión. La aplicación no escribe las bases en disco, no las añade al repositorio y no realiza peticiones a servicios externos. Al desplegarla, el procesamiento se ejecuta en el servidor de Streamlit; no dentro del navegador. Esta primera versión usa carga manual de archivos y no incorpora acceso automático por enlaces ni inicio de sesión propio.

## Pruebas

Las pruebas incluidas utilizan datos ficticios:

```bash
python -m unittest discover -s tests -v
```
