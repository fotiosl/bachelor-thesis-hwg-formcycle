import os
import subprocess
import sys
import shutil

def find_executable(name):
    # 1. System PATH
    found = shutil.which(name)
    if found:
        return found
    
    # 2. Check current user LOCALAPPDATA / APPDATA
    user_candidates = []
    local_appdata = os.environ.get("LOCALAPPDATA")
    if local_appdata:
        user_candidates.append(os.path.join(local_appdata, "Programs", "MiKTeX", "miktex", "bin", "x64", f"{name}.exe"))
    
    home_dir = os.path.expanduser("~")
    user_candidates.append(os.path.join(home_dir, "AppData", "Local", "Programs", "MiKTeX", "miktex", "bin", "x64", f"{name}.exe"))
    
    # 3. Check system-wide paths
    system_candidates = [
        os.path.join(r"C:\Program Files", "MiKTeX", "miktex", "bin", "x64", f"{name}.exe"),
        os.path.join(r"C:\Program Files (x86)", "MiKTeX", "miktex", "bin", f"{name}.exe"),
        os.path.join(r"C:\texlive", "2026", "bin", "windows", f"{name}.exe"),
        os.path.join(r"C:\texlive", "2025", "bin", "windows", f"{name}.exe"),
        os.path.join(r"C:\texlive", "2024", "bin", "windows", f"{name}.exe"),
    ]
    
    for c in user_candidates + system_candidates:
        if os.path.exists(c):
            return c
    return None

def build():
    pdflatex = find_executable("pdflatex")
    biber = find_executable("biber")
    
    if not pdflatex:
        print("FEHLER: 'pdflatex' wurde weder im PATH noch in Standard-Installationspfaden (MiKTeX/TeX Live) gefunden.")
        print("Bitte installieren Sie MiKTeX oder TeX Live oder fügen Sie das 'bin'-Verzeichnis zu den Umgebungsvariablen hinzu.")
        sys.exit(1)
        
    print(f"Verwende pdflatex: {pdflatex}")
    if biber:
        print(f"Verwende biber:    {biber}")
    else:
        print("HINWEIS: 'biber' nicht gefunden. Literaturverzeichnis wird möglicherweise nicht neu generiert.")
        
    thesis_dir = os.path.abspath("thesis")
    
    extra_flags = ["-enable-installer"] if "miktex" in pdflatex.lower() else []

    print("\n=== [1/4] Erste Kompilierung mit pdflatex ===")
    res1 = subprocess.run([pdflatex, "-interaction=nonstopmode", *extra_flags, "main.tex"], cwd=thesis_dir, capture_output=True, text=True)
    print("pdflatex 1 beendet, Return Code:", res1.returncode)
    
    bcf_file = os.path.join(thesis_dir, "main.bcf")
    if os.path.exists(bcf_file) and biber:
        print("\n=== [2/4] Literaturverzeichnis mit Biber verarbeiten ===")
        res2 = subprocess.run([biber, "main"], cwd=thesis_dir, capture_output=True, text=True)
        print("biber beendet, Return Code:", res2.returncode)
        
    print("\n=== [3/4] Zweite Kompilierung mit pdflatex (Referenzen) ===")
    res3 = subprocess.run([pdflatex, "-interaction=nonstopmode", *extra_flags, "main.tex"], cwd=thesis_dir, capture_output=True, text=True)
    print("pdflatex 2 beendet, Return Code:", res3.returncode)

    print("\n=== [4/4] Finale Kompilierung mit pdflatex (Seitenumbrüche & Verzeichnisse) ===")
    res4 = subprocess.run([pdflatex, "-interaction=nonstopmode", *extra_flags, "main.tex"], cwd=thesis_dir, capture_output=True, text=True)
    print("pdflatex final beendet, Return Code:", res4.returncode)
    
    pdf_path = os.path.join(thesis_dir, "main.pdf")
    if os.path.exists(pdf_path):
        size_kb = os.path.getsize(pdf_path) / 1024
        print(f"\nERFOLG! PDF erfolgreich generiert: {pdf_path} ({size_kb:.1f} KB)")
    else:
        print("\nACHTUNG: PDF wurde nicht erstellt. Prüfe main.log auf Fehler.")

if __name__ == "__main__":
    build()
