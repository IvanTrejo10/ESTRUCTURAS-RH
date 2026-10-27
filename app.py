from __future__ import annotations

from datetime import datetime, timedelta
from hashlib import sha256
import importlib
import logging
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

from structures import Result, StructureError, bundle, changes_csv, generate
import ui as _ui

importlib.reload(_ui)
from ui import (
    action_summary,
    apply_styles,
    brand,
    distribution_card,
    empty_results,
    file_status,
    footer,
    hero_banner,
    icon,
    report_meta_card,
    results_banner,
    schema_blueprint,
    section,
    topbar,
    upload_heading,
    workflow_stepper,
)

st.set_page_config(
    page_title="DATA RH · Estructuras",
    page_icon=":material/account_tree:",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_styles()


def fingerprint(year, week, files):
    digest = sha256(f"{year}:{week}".encode())
    for file in files:
        digest.update(b"present" if file is not None else b"absent")
        if file is not None:
            data = file.getvalue()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def render_result(result: Result):
    label = "Rutas" if result.kind == "cr" else "Coordinaciones"
    columns = st.columns(4)
    columns[0].metric(label, f"{result.total:,}")
    if result.compared:
        for col, field in zip(columns[1:], ("Altas", "Bajas", "Modificados")):
            col.metric(field, sum(row[field] for row in result.summary))
    else:
        columns[1].metric("Países" if result.kind == "cr" else "Marcas", len(result.sheets))
        columns[2].metric("Semana", f"{result.week:02d}")
        columns[3].metric("Año", str(result.year))

    download_col, detail_col = st.columns([1, 2.2], vertical_alignment="center")
    with download_col:
        st.download_button(
            "Descargar Excel",
            result.content,
            result.filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"download_{result.kind}",
            type="primary",
            icon=":material/download:",
            width="stretch",
            on_click="ignore",
        )
    with detail_col:
        report_meta_card(result)

    distribution_card(result)

    st.markdown('<p class="table-heading">Resumen ejecutivo de la estructura</p>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(result.summary), hide_index=True, width="stretch")

    with st.expander("Explorar las estructuras", expanded=True, icon=":material/table_view:"):
        select_col, count_col = st.columns([2, 1], vertical_alignment="bottom")
        sheet = select_col.selectbox(
            "País" if result.kind == "cr" else "Marca",
            list(result.sheets),
            key=f"sheet_{result.kind}",
        )
        count_col.caption(f"{len(result.sheets[sheet]):,} registros en esta hoja")
        st.dataframe(
            pd.DataFrame(result.sheets[sheet], columns=result.headers[sheet]),
            hide_index=True,
            width="stretch",
            height=320,
        )

    if result.compared:
        with st.expander("Detalle de los cambios", expanded=bool(result.changes), icon=":material/compare_arrows:"):
            if result.changes:
                st.dataframe(pd.DataFrame(result.changes), hide_index=True, width="stretch")
            else:
                st.success("Las columnas de RH no tuvieron cambios respecto al archivo anterior.")
            st.download_button(
                "Descargar detalle de cambios",
                changes_csv(result),
                file_name=f"Cambios {'CR' if result.kind == 'cr' else 'Vales'} - SEM {result.week}.csv",
                mime="text/csv",
                key=f"changes_{result.kind}",
                icon=":material/download:",
                on_click="ignore",
            )
            st.caption(
                "Las claves se comparan por Ruta o Coordinación dentro de cada hoja. "
                "Un cambio de clave aparece como una alta y una baja."
            )


today = datetime.now(ZoneInfo("America/Mexico_City")).date()
iso = today.isocalendar()
date_range_label = ""

with st.sidebar:
    brand()
    st.markdown('<div class="side-eyebrow">ESPACIO DE TRABAJO</div>', unsafe_allow_html=True)
    st.markdown(
        f'<a class="side-nav active" href="#cargar-bases" target="_self">{icon("grid", 18)} Generar estructuras</a>'
        f'<a class="side-nav" href="#resultados" target="_self">{icon("download", 18)} Reportes y descargas</a>'
        '<div class="side-divider"></div><div class="side-eyebrow">PERIODO DEL REPORTE</div>',
        unsafe_allow_html=True,
    )
    year_col, week_col = st.columns(2)
    year = year_col.number_input("Año", min_value=2000, max_value=2100, value=iso.year, step=1, key="year")
    week = week_col.number_input("Semana", min_value=1, max_value=53, value=iso.week, step=1, key="week")
    try:
        monday = datetime.fromisocalendar(int(year), int(week), 1).date()
        sunday = monday + timedelta(days=6)
        date_range_label = f"{monday:%d/%m/%Y} al {sunday:%d/%m/%Y}"
        st.markdown(
            f'<div class="side-period">{icon("calendar", 19)}<div><b>Semana {week:02d} de {year}</b>'
            f'<span>{date_range_label}</span></div></div>',
            unsafe_allow_html=True,
        )
        valid_period = True
    except ValueError:
        st.error("Esa semana no existe en el año elegido.")
        valid_period = False
    with st.expander("Guía rápida", icon=":material/help_outline:"):
        st.markdown(
            "1. **Elige el periodo** en el calendario ISO.\n"
            "2. **Sube tus bases** CR, Vales o ambas.\n"
            "3. **Crea las estructuras** para validar datos.\n"
            "4. **Explora y descarga** tus libros Excel."
        )
        st.caption("Agrega los reportes anteriores si quieres comparar los cambios y conservar su formato.")
    st.markdown(
        '<div class="side-note"><h4>Un flujo, dos reportes.</h4>'
        '<p>CR por país y Vales por marca.<br>El formato corporativo de RH, listo cada semana.</p></div>',
        unsafe_allow_html=True,
    )

topbar(int(week), int(year))
header_slot = st.container()

section(
    "01",
    "Carga las bases de esta semana",
    "Puedes trabajar con una sola base o procesar los dos reportes corporativos simultáneamente.",
    "cargar-bases",
)
cr_col, vales_col = st.columns(2, gap="medium")
with cr_col:
    with st.container(key="upload_cr"):
        upload_heading("cr")
        cr = st.file_uploader("Base CR de esta semana", type=["xlsx"], key="source_cr")
        file_status(cr)
with vales_col:
    with st.container(key="upload_vales"):
        upload_heading("vales")
        vales = st.file_uploader("Base Vales de esta semana", type=["xlsx"], key="source_vales")
        file_status(vales)

with st.expander("Comparar con la semana anterior · opcional", icon=":material/history:"):
    st.write(
        "Carga los reportes finales anteriores para identificar altas, bajas y cambios, "
        "y conservar sus fuentes, colores y anchos de columna."
    )
    old_cr_col, old_vales_col = st.columns(2)
    with old_cr_col:
        old_cr = st.file_uploader("Reporte anterior por país", type=["xlsx"], key="previous_cr")
        file_status(old_cr)
    with old_vales_col:
        old_vales = st.file_uploader("Reporte anterior de Vales", type=["xlsx"], key="previous_vales")
        file_status(old_vales)
    st.caption("Si no cargas un reporte anterior, se utiliza el formato habitual de RH.")

current = fingerprint(year, week, (cr, vales, old_cr, old_vales))
loaded = int(cr is not None) + int(vales is not None)
with st.container(key="create_action"):
    hint_col, button_col = st.columns([2.2, 1], vertical_alignment="center")
    with hint_col:
        action_summary(
            loaded,
            int(week),
            int(year),
            has_cr=cr is not None,
            has_vales=vales is not None,
            has_old_cr=old_cr is not None,
            has_old_vales=old_vales is not None,
        )
    with button_col:
        create = st.button(
            "Crear estructuras",
            type="primary",
            key="create_structures",
            width="stretch",
            icon=":material/arrow_forward:",
            icon_position="right",
            disabled=not loaded or not valid_period,
        )

if create:
    results, errors = [], []
    with st.spinner("Validando las bases y preparando tus reportes…"):
        for kind, source, previous in (("cr", cr, old_cr), ("vales", vales, old_vales)):
            if source is None:
                continue
            try:
                results.append(
                    generate(
                        kind,
                        source.getvalue(),
                        int(week),
                        int(year),
                        previous.getvalue() if previous is not None else None,
                    )
                )
            except StructureError as exc:
                errors.append(("CR" if kind == "cr" else "Vales", str(exc)))
            except Exception:
                logging.exception("Error al generar la estructura %s", kind)
                errors.append(
                    (
                        "CR" if kind == "cr" else "Vales",
                        "No se pudo completar el archivo. Revisa las bases y vuelve a intentarlo.",
                    )
                )
    st.session_state["generated"] = {"fingerprint": current, "results": results, "errors": errors}

generated = st.session_state.get("generated")
fresh_results = generated["results"] if (generated and generated["fingerprint"] == current) else []

with header_slot:
    hero_banner(int(week), int(year), date_range_label, loaded=loaded, ready_reports=len(fresh_results))
    workflow_stepper(loaded=loaded, has_results=bool(fresh_results))

section("02", "Tus reportes", "Revisa las estructuras, explora la distribución y descarga los archivos finales.", "resultados")
if generated and generated["fingerprint"] != current:
    st.info(
        "Cambiaste los archivos o el periodo. Vuelve a crear las estructuras para actualizar las descargas.",
        icon=":material/info:",
    )
    empty_results()
elif generated:
    for label, message in generated["errors"]:
        st.error(f"{label}: {message}")
    results = generated["results"]
    if results:
        results_banner(results, int(week), int(year))
        if len(results) == 2:
            st.download_button(
                "Descargar los dos Excel en ZIP",
                bundle(results),
                file_name=f"Estructuras RH {year} - SEM {week}.zip",
                mime="application/zip",
                key="download_bundle",
                icon=":material/folder_zip:",
                on_click="ignore",
            )
        tabs = st.tabs(["Por país · CR" if result.kind == "cr" else "Por marca · Vales" for result in results])
        for tab, result in zip(tabs, results):
            with tab:
                render_result(result)
    else:
        empty_results()
else:
    empty_results()

with st.expander("Conoce el formato de los reportes", icon=":material/info:"):
    schema_blueprint()
    st.caption(
        "Los Excel descargados contienen únicamente valores limpios sin fórmulas externas. "
        "Las bases se procesan en memoria durante tu sesión y no se almacenan en el servidor."
    )
footer()
