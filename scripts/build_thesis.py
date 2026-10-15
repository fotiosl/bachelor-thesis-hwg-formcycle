import os
import subprocess
import sys

def build():
    miktex_bin = r"C:\Users\fotii\AppData\Local\Programs\MiKTeX\miktex\bin\x64"
    pdflatex = os.path.join(miktex_bin, "pdflatex.exe")
    biber = os.path.join(miktex_bin, "biber.exe")
    
    thesis_dir = os.path.abspath("thesis")
    
    print("=== [1/3] Erste Kompilierung mit pdflatex ===")
    res1 = subprocess.run([pdflatex, "-interaction=nonstopmode", "-enable-installer", "main.tex"], cwd=thesis_dir, capture_output=True, text=True)
    print("pdflatex 1 beendet, Return Code:", res1.returncode)
    
    # Check if biber is needed
    bcf_file = os.path.join(thesis_dir, "main.bcf")
    if os.path.exists(bcf_file):
        print("=== [2/3] Literaturverzeichnis mit Biber verarbeiten ===")
        res2 = subprocess.run([biber, "main"], cwd=thesis_dir, capture_output=True, text=True)
        print("biber beendet, Return Code:", res2.returncode)
        
    print("=== [3/3] Finale Kompilierung mit pdflatex ===")
    res3 = subprocess.run([pdflatex, "-interaction=nonstopmode", "-enable-installer", "main.tex"], cwd=thesis_dir, capture_output=True, text=True)
    print("pdflatex final beendet, Return Code:", res3.returncode)
    
    pdf_path = os.path.join(thesis_dir, "main.pdf")
    if os.path.exists(pdf_path):
        size_kb = os.path.getsize(pdf_path) / 1024
        print(f"\nERFOLG! PDF erfolgreich generiert: {pdf_path} ({size_kb:.1f} KB)")
    else:
        print("\nACHTUNG: PDF wurde nicht erstellt. Prüfe main.log auf Fehler.")

if __name__ == "__main__":
    build()
