import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import time

# ===================== Configuración HTTP =====================

session = requests.Session()

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# ===================== Funciones SEO =====================

def analizar_url(url):
    """Analiza una URL y devuelve un diccionario con información SEO"""
    resultado = {
        "URL": url,
        "Status": "",
        "Indexable": "",
        "Title": "",
        "MetaTitle": "",
        "MetaDescription": ""
    }

    try:
        response = session.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        resultado["Status"] = response.status_code

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Title
            resultado["Title"] = soup.title.get_text(strip=True) if soup.title else ""

            # MetaTitle
            meta_title_tag = soup.find("meta", attrs={"name": "title"})
            resultado["MetaTitle"] = meta_title_tag["content"].strip() if meta_title_tag else resultado["Title"]

            # MetaDescription
            meta_desc_tag = soup.find("meta", attrs={"name": "description"})
            resultado["MetaDescription"] = meta_desc_tag["content"].strip() if meta_desc_tag else ""

            # Indexable
            robots_tag = soup.find("meta", attrs={"name": "robots"})
            resultado["Indexable"] = "NO" if robots_tag and "noindex" in robots_tag.get("content", "").lower() else "SI"

        else:
            resultado["Indexable"] = "NO"

    except Exception:
        resultado["Status"] = "Error"
        resultado["Indexable"] = "NO"

    time.sleep(1.2)
    return resultado


# ===================== NUEVO: Leer sitemap =====================

def obtener_urls_desde_sitemap(sitemap_url):

    urls = []

    try:
        response = session.get(sitemap_url, headers=HEADERS, timeout=15)

        if response.status_code != 200:
            messagebox.showerror("Error", f"No se pudo acceder al sitemap ({response.status_code})")
            return []

        soup = BeautifulSoup(response.content, "xml")

        # Detectar sitemap index
        sitemaps = soup.find_all("sitemap")

        if sitemaps:
            for sitemap in sitemaps:

                loc = sitemap.find("loc")

                if loc:
                    sub_sitemap_url = loc.text.strip()

                    sub_resp = session.get(sub_sitemap_url, headers=HEADERS, timeout=15)

                    if sub_resp.status_code == 200:

                        sub_soup = BeautifulSoup(sub_resp.content, "xml")

                        for url in sub_soup.find_all("loc"):
                            urls.append(url.text.strip())

        else:
            # sitemap normal
            for url in soup.find_all("loc"):
                urls.append(url.text.strip())

        return urls

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el sitemap: {e}")
        return []


# ===================== Ejecutar auditoría =====================

def ejecutar_auditoria(origen):
    """Lee URLs desde archivo o sitemap"""

    # Detectar si es URL o archivo
    if origen.startswith("http"):
        urls = obtener_urls_desde_sitemap(origen)
    else:
        try:
            with open(origen, "r", encoding="utf-8") as f:
                urls = [u.strip() for u in f if u.strip()]
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
            return

    if not urls:
        messagebox.showerror("Error", "No se encontraron URLs")
        return
    print("URLs encontradas:", len(urls))

    resultados = []

    log_text.delete(1.0, tk.END)

    for i, url in enumerate(urls, 1):

        log_text.insert(tk.END, f"[{i}/{len(urls)}] Procesando: {url}\n")
        log_text.see(tk.END)

        root.update()

        res = analizar_url(url)

        resultados.append(res)

    # Guardar Excel
    output_file = os.path.join(os.getcwd(), "seo_auditoria_semaforo.xlsx")

    df = pd.DataFrame(resultados)

    # Semáforo SEO
    def semaforo(row):

        if row["Status"] != 200 or row["Indexable"] == "NO":
            return "🔴"

        elif row["Status"] == 200 and row["Indexable"] == "SI":
            return "🟢"

        else:
            return "🟡"

    df["Semaforo"] = df.apply(semaforo, axis=1)

    df.to_excel(output_file, index=False)

    messagebox.showinfo("Auditoría completa", f"Archivo generado:\n{output_file}")


# ===================== GUI =====================

def seleccionar_archivo():

    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo de URLs",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )

    if file_path:
        entry_archivo.delete(0, tk.END)
        entry_archivo.insert(0, file_path)


def ejecutar():

    origen = entry_archivo.get().strip()

    if not origen:
        messagebox.showerror("Error", "Ingresa un archivo .txt o sitemap")
        return

    # Si parece una URL pero no tiene protocolo
    if "." in origen and not origen.startswith("http"):
        origen = "https://" + origen

    ejecutar_auditoria(origen)


# ===================== Ventana =====================

root = tk.Tk()
root.title("Auditoría SEO")
root.geometry("700x500")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Archivo .txt o Sitemap URL:").pack(side=tk.LEFT)

entry_archivo = tk.Entry(frame_top, width=50)
entry_archivo.pack(side=tk.LEFT, padx=5)

tk.Button(frame_top, text="Seleccionar", command=seleccionar_archivo).pack(side=tk.LEFT)

tk.Button(root, text="Ejecutar Auditoría", command=ejecutar, bg="green", fg="white").pack(pady=10)

log_text = scrolledtext.ScrolledText(root, width=85, height=20)
log_text.pack(padx=10, pady=10)

root.mainloop()