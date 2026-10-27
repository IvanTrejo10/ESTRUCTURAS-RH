"""Componentes visuales del portal DATA RH con diseño editorial y SaaS."""
from __future__ import annotations

from html import escape
from pathlib import Path
import streamlit as st

PATHS = {
    "layers": '<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 12 9 5 9-5M3 16l9 5 9-5"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1.75"/><rect x="14" y="3" width="7" height="7" rx="1.75"/><rect x="3" y="14" width="7" height="7" rx="1.75"/><rect x="14" y="14" width="7" height="7" rx="1.75"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c5 5 5 13 0 18-5-5-5-13 0-18Z"/>',
    "wallet": '<path d="M20 8V5a2 2 0 0 0-2-2H6a3 3 0 0 0 0 6h14v11H6a3 3 0 0 1-3-3V6"/><path d="M20 12h-5v5h5M17 14.5h.01"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2.5"/><path d="M16 3v4M8 3v4M3 11h18"/>',
    "check": '<path d="m5 12.5 4.2 4.2L19 7"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "download": '<path d="M12 3v12m-5-5 5 5 5-5M4 16v4a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-4"/>',
    "sparkles": '<path d="m12 3 1.9 4.6L18.5 9.5l-4.6 1.9L12 16l-1.9-4.6L5.5 9.5l4.6-1.9L12 3Z"/><path d="m19 15 .9 2.1 2.1.9-2.1.9-.9 2.1-.9-2.1-2.1-.9 2.1-.9.9-2.1Z"/>',
    "shield": '<path d="M12 3 4 6.5v5.3c0 5 3.4 8.9 8 10.2 4.6-1.3 8-5.2 8-10.2V6.5L12 3Z"/><path d="m9 12 2 2 4-4"/>',
    "sheet": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h8M10 9H8"/>',
    "compare": '<path d="M16 3h5v5M4 20 21 3M21 16v5h-5M15 15l6 6M4 4l5 5"/>',
}

CR_COUNTRIES = ("México", "Guatemala", "Perú", "El Salvador", "Colombia", "Honduras", "Nicaragua")
VALES_BRANDS = ("RapiVale", "Vale Perú", "Vale Amigo", "Viva Vale")
SEGMENT_COLORS = ("#0D9488", "#2563EB", "#7C3AED", "#F59E0B", "#EC4899", "#06B6D4", "#10B981")


def _format_bytes(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size / (1024 * 1024):.2f} MB"


def icon(name: str, size: int = 22) -> str:
    path = PATHS.get(name, PATHS["layers"])
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{path}</svg>'
    )


def apply_styles():
    css = (Path(__file__).parent / "assets" / "styles.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def brand():
    st.markdown(
        f'<div class="brand">'
        f'<span class="brand-mark">{icon("layers", 24)}</span>'
        f'<div class="brand-name">'
        f'<div class="brand-title">DATA<span>RH</span></div>'
        f'<small>ESTRUCTURAS Y OPERACIONES</small>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def topbar(week: int, year: int):
    st.markdown(
        f'<div class="topbar">'
        f'<div class="breadcrumb">'
        f'<span class="crumb-root">{icon("layers", 14)} Operaciones RH</span>'
        f'<span class="crumb-sep">/</span>'
        f'<span>Portal de Estructuras</span>'
        f'<span class="crumb-sep">/</span>'
        f'<span class="crumb-current">Semana {int(week):02d} · {int(year)}</span>'
        f'</div>'
        f'<div class="topbar-badges">'
        f'<span class="portal-tag subtle">{icon("shield", 13)} Procesamiento en memoria</span>'
        f'<span class="portal-tag"><i></i> Actualización semanal</span>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def hero_banner(week: int, year: int, date_range: str = "", loaded: int = 0, ready_reports: int = 0):
    status_label = (
        f"{ready_reports} {'reporte generado' if ready_reports == 1 else 'reportes generados'}"
        if ready_reports
        else f"{loaded} {'base cargada' if loaded == 1 else 'bases cargadas'}"
        if loaded
        else "Listo para recibir bases"
    )
    range_html = f'<div class="hero-date-pill">{icon("calendar", 13)} {escape(date_range)}</div>' if date_range else ""
    st.markdown(
        f'<div class="hero">'
        f'<div class="hero-copy">'
        f'<div class="eyebrow"><span class="eyebrow-dot"></span>GESTIÓN DE ESTRUCTURAS CORPORATIVAS</div>'
        f'<h1>Tu semana, <span>en orden.</span></h1>'
        f'<p>Transforma tus bases operativas en los reportes oficiales de RH. '
        f'Validación automática por país y por marca, formato corporativo intacto y cada cambio a la vista.</p>'
        f'<div class="hero-pills">'
        f'<span class="hero-chip">{icon("globe", 14)} 7 Países CR</span>'
        f'<span class="hero-chip">{icon("wallet", 14)} 4 Marcas Vales</span>'
        f'<span class="hero-chip">{icon("sparkles", 14)} Auditoría de altas y bajas</span>'
        f'</div>'
        f'</div>'
        f'<div class="hero-period">'
        f'<div class="hero-period-top">'
        f'<span class="hero-period-label">Periodo activo</span>'
        f'<span class="hero-live-badge"><i></i> {escape(status_label)}</span>'
        f'</div>'
        f'<strong>SEM {int(week):02d}</strong>'
        f'<small>Año {int(year)} · CR y Vales</small>'
        f'{range_html}'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def workflow_stepper(loaded: int = 0, has_results: bool = False):
    step1_state = "done" if loaded > 0 else "active"
    step2_state = "done" if has_results else ("active" if loaded > 0 else "")
    step3_state = "active" if has_results else ""

    step1_badge = icon("check", 14) if loaded > 0 else "01"
    step2_badge = icon("check", 14) if has_results else "02"
    step3_badge = "03"

    step1_sub = f"{loaded} {'archivo cargado' if loaded == 1 else 'archivos cargados'}" if loaded > 0 else "Archivos .xlsx de esta semana"
    step2_sub = "Estructuras validadas" if has_results else ("Listo para generar" if loaded > 0 else "Reglas de RH y comparativa")
    step3_sub = "Archivos listos para descarga" if has_results else "Reportes finales en Excel y CSV"

    st.markdown(
        f'<div class="workflow">'
        f'<div class="workflow-step {step1_state}">'
        f'<span class="step-dot">{step1_badge}</span>'
        f'<div class="step-copy"><strong>Carga tus bases</strong><small>{escape(step1_sub)}</small></div>'
        f'<span class="step-tag">Paso 1</span>'
        f'</div>'
        f'<div class="workflow-step {step2_state}">'
        f'<span class="step-dot">{step2_badge}</span>'
        f'<div class="step-copy"><strong>Revisa y valida</strong><small>{escape(step2_sub)}</small></div>'
        f'<span class="step-tag">Paso 2</span>'
        f'</div>'
        f'<div class="workflow-step {step3_state}">'
        f'<span class="step-dot">{step3_badge}</span>'
        f'<div class="step-copy"><strong>Descarga y comparte</strong><small>{escape(step3_sub)}</small></div>'
        f'<span class="step-tag">Paso 3</span>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def section(number: str, title: str, subtitle: str, anchor: str):
    st.markdown(
        f'<div class="section-heading" id="{escape(anchor)}">'
        f'<span class="section-number">{escape(number)}</span>'
        f'<div class="section-text"><h2>{escape(title)}</h2><p>{escape(subtitle)}</p></div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def upload_heading(kind: str):
    cr = kind == "cr"
    title = "Estructura CR" if cr else "Estructura Vales"
    description = (
        "Rutas operativas de México y Latinoamérica separadas por país."
        if cr
        else "Coordinaciones operativas clasificadas por marca comercial."
    )
    tag = "7 países" if cr else "4 marcas"
    sheet_hint = "Hoja: Estructuras" if cr else "Hoja: Hoja 1"
    scopes = CR_COUNTRIES if cr else VALES_BRANDS
    pills_html = "".join(f'<span class="scope-pill">{escape(item)}</span>' for item in scopes)

    st.markdown(
        f'<div class="upload-heading">'
        f'<span class="file-icon {"teal" if cr else "blue"}">{icon("globe" if cr else "wallet", 24)}</span>'
        f'<div class="upload-badges">'
        f'<span class="file-sheet-hint">{escape(sheet_hint)}</span>'
        f'<span class="file-category {"teal" if cr else "blue"}">{escape(tag)}</span>'
        f'</div>'
        f'</div>'
        f'<h3 class="upload-title">{escape(title)}</h3>'
        f'<p class="upload-description">{escape(description)}</p>'
        f'<div class="scope-pills">{pills_html}</div>',
        unsafe_allow_html=True,
    )


def file_status(file):
    if file is None:
        st.markdown(
            f'<div class="file-state">'
            f'<span class="file-state-icon">{icon("clock", 15)}</span>'
            f'<span>Pendiente de carga</span>'
            f'<span class="file-state-meta">.XLSX · máx. 25 MB</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        name = escape(getattr(file, "name", "Archivo.xlsx"))
        try:
            size_str = _format_bytes(len(file.getvalue()))
        except Exception:
            size_str = "Listo"
        st.markdown(
            f'<div class="file-state ready">'
            f'<span class="file-state-icon">{icon("check", 15)}</span>'
            f'<span>Archivo cargado · listo para validar</span>'
            f'<span class="file-state-meta">{name} · {escape(size_str)}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


def action_summary(
    loaded: int,
    week: int,
    year: int,
    has_cr: bool = False,
    has_vales: bool = False,
    has_old_cr: bool = False,
    has_old_vales: bool = False,
):
    title = (
        "Todo empieza con tus bases"
        if not loaded
        else f"{loaded} {'base lista' if loaded == 1 else 'bases listas'} para procesar"
    )
    hint = (
        "Sube al menos un archivo .xlsx en la sección superior para habilitar el generador."
        if not loaded
        else f"Se crearán los reportes oficiales de la semana {int(week):02d} de {int(year)}."
    )
    chips = []
    if has_cr:
        chips.append('<span class="action-chip teal">CR por País</span>')
    if has_vales:
        chips.append('<span class="action-chip blue">Vales por Marca</span>')
    if has_old_cr or has_old_vales:
        comp_label = "Comparativa CR + Vales" if (has_old_cr and has_old_vales) else ("Comparativa CR" if has_old_cr else "Comparativa Vales")
        chips.append(f'<span class="action-chip amber">{escape(comp_label)}</span>')
    chips_html = f'<div class="action-chips">{"".join(chips)}</div>' if chips else ""
    status_cls = "ready" if loaded else "idle"
    status_txt = "LISTO PARA GENERAR" if loaded else "ESPERANDO ARCHIVOS"

    st.markdown(
        f'<div class="action-box">'
        f'<div class="action-status {status_cls}"><i></i>{status_txt}</div>'
        f'<div class="action-title">{escape(title)}</div>'
        f'<p class="action-hint">{escape(hint)}</p>'
        f'{chips_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


def results_banner(results: list, week: int, year: int):
    total_records = sum(r.total for r in results)
    count = len(results)
    st.markdown(
        f'<div class="results-banner">'
        f'<div class="results-banner-left">'
        f'<span class="results-check">{icon("check", 18)}</span>'
        f'<div>'
        f'<strong>Estructuras generadas correctamente</strong>'
        f'<p>Validación completada sin errores de estructura para los archivos listados.</p>'
        f'</div>'
        f'</div>'
        f'<div class="results-banner-pills">'
        f'<span class="banner-pill">Semana {int(week):02d} · {int(year)}</span>'
        f'<span class="banner-pill">{count} {"reporte listo" if count == 1 else "reportes listos"}</span>'
        f'<span class="banner-pill highlight">{total_records:,} registros totales</span>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def report_meta_card(result):
    mode = "Comparado con semana anterior · Formato preservado" if result.compared else "Formato corporativo estándar de RH"
    badge_cls = "compared" if result.compared else "standard"
    st.markdown(
        f'<div class="report-meta-bar">'
        f'<div class="report-meta-file">'
        f'<span class="report-meta-icon">{icon("sheet", 18)}</span>'
        f'<div>'
        f'<span class="report-filename">{escape(result.filename)}</span>'
        f'<span class="report-submeta">{len(result.sheets)} pestañas · {result.total:,} registros validados</span>'
        f'</div>'
        f'</div>'
        f'<span class="report-mode-badge {badge_cls}">{escape(mode)}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def distribution_card(result):
    total = max(result.total, 1)
    segments = []
    cards = []
    summary_by_sheet = {row["Hoja"]: row for row in result.summary}

    for idx, (sheet_name, rows) in enumerate(result.sheets.items()):
        count = len(rows)
        pct = (count / total) * 100 if result.total > 0 else 0.0
        color = SEGMENT_COLORS[idx % len(SEGMENT_COLORS)]
        if count > 0:
            segments.append(
                f'<div class="dist-segment" style="width:{max(pct, 2.0):.2f}%;background:{color};" '
                f'title="{escape(sheet_name)}: {count:,} ({pct:.1f}%)"></div>'
            )
        deltas_html = ""
        if result.compared and sheet_name in summary_by_sheet:
            s_row = summary_by_sheet[sheet_name]
            altas = s_row.get("Altas", 0)
            bajas = s_row.get("Bajas", 0)
            mods = s_row.get("Modificados", 0)
            deltas = []
            if altas:
                deltas.append(f'<span class="delta-pill up">+{altas}</span>')
            if bajas:
                deltas.append(f'<span class="delta-pill down">-{bajas}</span>')
            if mods:
                deltas.append(f'<span class="delta-pill mod">~{mods}</span>')
            if not deltas:
                deltas.append('<span class="delta-pill neutral">Sin cambios</span>')
            deltas_html = f'<div class="dist-deltas">{"".join(deltas)}</div>'

        cards.append(
            f'<div class="dist-item">'
            f'<div class="dist-item-top">'
            f'<span class="dist-dot" style="background:{color};"></span>'
            f'<span class="dist-name">{escape(sheet_name)}</span>'
            f'<span class="dist-pct">{pct:.1f}%</span>'
            f'</div>'
            f'<div class="dist-count">{count:,} <small>registros</small></div>'
            f'{deltas_html}'
            f'</div>'
        )

    bar_html = "".join(segments) if segments else '<div class="dist-segment" style="width:100%;background:#CBD5E1;"></div>'
    label_group = "Distribución por país" if result.kind == "cr" else "Distribución por marca"
    st.markdown(
        f'<div class="dist-card">'
        f'<div class="dist-header">'
        f'<span class="dist-title">{escape(label_group)}</span>'
        f'<span class="dist-total">{result.total:,} registros en {len(result.sheets)} hojas</span>'
        f'</div>'
        f'<div class="dist-bar">{bar_html}</div>'
        f'<div class="dist-grid">{"".join(cards)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def empty_results():
    st.markdown(
        f'<div class="empty-state">'
        f'<span class="empty-icon">{icon("layers", 28)}</span>'
        f'<div class="empty-copy">'
        f'<h3>Aquí verás tus reportes ejecutivos</h3>'
        f'<p>Carga al menos una base semanal y pulsa <b>Crear estructuras</b> para inspeccionar las hojas, '
        f'auditar altas o bajas y descargar tus libros Excel listos para compartir.</p>'
        f'<div class="empty-features">'
        f'<span>{icon("check", 13)} Validación de claves duplicadas</span>'
        f'<span>{icon("check", 13)} Normalización de países y marcas</span>'
        f'<span>{icon("check", 13)} Exportación limpia sin fórmulas</span>'
        f'</div>'
        f'</div>'
        f'<div class="empty-badges">'
        f'<span class="empty-format">.XLSX</span>'
        f'<span class="empty-format subtle">.CSV</span>'
        f'<span class="empty-format subtle">.ZIP</span>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def schema_blueprint():
    st.markdown(
        '<div class="schema-grid">'
        '<div class="schema-card">'
        '<div class="schema-card-head"><span class="schema-badge teal">CR · MÉXICO</span><small>7 columnas</small></div>'
        '<h4>Estructura completa nacional</h4>'
        '<p>Conserva tanto <b>Territorio</b> como <b>Subdirección</b> en su orden oficial.</p>'
        '<div class="schema-cols">'
        '<span>Ruta</span><span>Territorio</span><span>Subdireccion</span><span>Zona</span><span>Sucursal</span><span>Marca</span><span>País</span>'
        '</div>'
        '</div>'
        '<div class="schema-card">'
        '<div class="schema-card-head"><span class="schema-badge cyan">CR · LATAM (6 PAÍSES)</span><small>6 columnas</small></div>'
        '<h4>Homologación regional</h4>'
        '<p>La columna <b>Territorio</b> se alimenta automáticamente del valor de <b>Subdirección</b> de la base.</p>'
        '<div class="schema-cols">'
        '<span>Ruta</span><span>Territorio ← Subdirección</span><span>Zona</span><span>Sucursal</span><span>Marca</span><span>País</span>'
        '</div>'
        '</div>'
        '<div class="schema-card">'
        '<div class="schema-card-head"><span class="schema-badge blue">VALES · 4 MARCAS</span><small>5 columnas</small></div>'
        '<h4>Agrupación comercial</h4>'
        '<p>Clasifica las coordinaciones en pestañas para <b>Rapi</b>, <b>Peru</b>, <b>Vale Amigo</b> y <b>Viva Vale</b>.</p>'
        '<div class="schema-cols">'
        '<span>Coordinacion</span><span>Subdirección</span><span>Zona</span><span>Sucursal</span><span>Marca</span>'
        '</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def footer():
    st.markdown(
        '<footer class="portal-footer">'
        '<div class="footer-left">'
        '<span class="footer-dot"></span>'
        '<span><b>DATA RH</b> · Portal Corporativo de Estructuras Operativas</span>'
        '</div>'
        '<div class="footer-right">'
        '<span>Privacidad garantizada · Procesamiento en sesión</span>'
        '<span class="footer-divider">·</span>'
        '<span>Organiza. Revisa. Descarga.</span>'
        '</div>'
        '</footer>',
        unsafe_allow_html=True,
    )
