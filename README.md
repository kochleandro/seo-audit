
# SEO Audit & Health Analyzer 🚀

## Descripción 
Esta herramienta es un **Analizador de Salud SEO Automatizado** diseñado para auditar grandes volúmenes de URLs de manera eficiente. Su objetivo principal es proporcionar un diagnóstico rápido sobre la indexabilidad, estructura de metadatos y estado de respuesta del servidor, facilitando la toma de decisiones basada en datos para equipos de Marketing y SEO.

## Funcionalidades Clave
- **Auditoría Multi-factor:** Evaluación automática de Status Codes (200, 301, 404), etiquetas Title, Meta Descriptions, encabezados H1 y validación de URLs canónicas.
- **Lógica de Indexabilidad:** Detección inteligente de directivas `noindex` tanto en meta-tags como en headers HTTP (X-Robots-Tag).
- **Sistema de Semáforo (Visual Reporting):** Clasificación automática del estado SEO mediante un sistema de alertas (Rojo/Amarillo/Verde) exportable directamente a Excel.
- **Detección de Redirecciones:** Monitoreo de saltos entre la URL solicitada y la URL final para identificar cadenas de redirección innecesarias.

## Potencialidades y Escalabilidad
- **Automatización de CI/CD:** Gracias a la integración con GitHub Actions, la herramienta puede compilarse automáticamente como un ejecutable (.exe), permitiendo su uso por personal no técnico sin instalar Python.
- **Monitoreo de Competencia:** Capacidad para procesar sitemaps completos y realizar benchmarks de contenido a escala.
- **Extensibilidad:** Arquitectura preparada para integrar APIs de terceros (como Google Search Console o PageSpeed Insights) para enriquecer el reporte con datos de tráfico y performance.

## Guía de Uso Rápido
1. Instalar dependencias: `pip install -r requirements.txt`
2. Ejecutar auditoría: `python seo_audit.py urls.txt`
3. El resultado se generará automáticamente en un archivo Excel con formato condicional.
