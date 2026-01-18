import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

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
        response = requests.get(url, timeout=10)
        resultado["Status"] = response.status_code
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            resultado["Title"] = soup.title.string.strip() if soup.title else ""
            meta_title_tag = soup.find("meta", attrs={"name": "title"})
            resultado["MetaTitle"] = meta_title_tag["content"].strip() if meta_title_tag else ""
            meta_desc_tag = soup.find("meta", attrs={"name": "description"})
            resultado["MetaDescription"] = meta_desc_tag["content"].strip() if meta_desc_tag else ""
            robots_tag = soup.find("meta", attrs={"name": "robots"})
            resultado["Indexable"] = "NO" if robots_tag and "noindex" in robots_tag.get("content","").lower() else "SI"
        else:
            resultado["Indexable"] = "NO"
    except Exception as e:
        resultado["Status"] = "Error"
        resultado["Indexable"] = "NO"
    return resultado

def ejecutar_auditoria(ruta_archivo):
    """Lee el archivo de URLs y ejecuta la auditoría"""
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            urls = [u.strip() for u in f if u.strip()]
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
        return

    resultados = []
    log_text.delete(1.0, tk.END)
    for i, url in enumerate(urls, 1):
        log_text.insert(tk.END, f"[{i}/{len(urls)}] Procesando: {url}\n")
        log_text.see(tk.END)
        root.update()
        res = analizar_url(url)
        resultados.append(res)

    # Guardar Excel
    output_file = os.path.join(os.path.dirname(ruta_archivo), "seo_auditoria_semaforo.xlsx")
    df = pd.DataFrame(resultados)
    
    # Agregar columna Semáforo
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
    ruta = entry_archivo.get()
    if not ruta or not os.path.exists(ruta):
        messagebox.showerror("Error", "Selecciona un archivo válido")
        return
    ejecutar_auditoria(ruta)

# ===================== Ventana =====================

root = tk.Tk()
root.title("Auditoría SEO")
root.geometry("700x500")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Archivo de URLs:").pack(side=tk.LEFT)
entry_archivo = tk.Entry(frame_top, width=50)
entry_archivo.pack(side=tk.LEFT, padx=5)
tk.Button(frame_top, text="Seleccionar", command=seleccionar_archivo).pack(side=tk.LEFT)

tk.Button(root, text="Ejecutar Auditoría", command=ejecutar, bg="green", fg="white").pack(pady=10)

log_text = scrolledtext.ScrolledText(root, width=85, height=20)
log_text.pack(padx=10, pady=10)

root.mainloop()

