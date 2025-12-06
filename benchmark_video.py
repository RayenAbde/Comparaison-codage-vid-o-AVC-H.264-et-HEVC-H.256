import subprocess
import time
import re
import os

# --- CONFIGURATION ---
SOURCE_FILE = "source.mp4"       # Votre vidéo originale (doit être de haute qualité)
BITRATES = ["150k", "300k"]      # Les débits très bas à tester (150kbps, 300kbps)
CODECS = {
    "H.264": "libx264",
    "H.265": "libx265"
}

# Fonction pour encoder
def encode_video(codec_name, lib_name, bitrate, output_file):
    print(f"--- Encodage {codec_name} à {bitrate} ---")
    
    # Commande FFmpeg pour encoder
    # -tune zerolatency : CRUCIAL pour la simulation visioconférence (optimise le délai)
    # -preset fast : Un compromis vitesse/qualité pour le test
    cmd = [
        "ffmpeg", "-y",                # -y pour écraser le fichier si existant
        "-i", SOURCE_FILE,             # Fichier entrée
        "-c:v", lib_name,              # Codec (x264 ou x265)
        "-b:v", bitrate,               # Débit cible
        "-maxrate", bitrate,           # Plafond débit (pour simuler contrainte réseau)
        "-bufsize", bitrate,           # Taille tampon
        "-tune", "zerolatency",        # Optimisation latence
        "-an",                         # Pas d'audio (on teste la vidéo)
        output_file
    ]
    
    start_time = time.time()
    # Exécution de la commande sans afficher tout le blabla ffmpeg (sauf erreurs)
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end_time = time.time()
    
    duration = end_time - start_time
    print(f"-> Terminé en {duration:.2f} secondes.")
    return duration

# Fonction pour calculer la qualité (PSNR et SSIM)
def measure_quality(encoded_file):
    # On compare la vidéo encodée par rapport à la source
    # SSIM est plus proche de la vision humaine (1.0 = parfait)
    cmd = [
        "ffmpeg", "-i", encoded_file,
        "-i", SOURCE_FILE,
        "-lavfi", "ssim;[0:v][1:v]psnr", # Filtres de qualité
        "-f", "null", "-"
    ]
    
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    output = result.stderr
    
    # Extraction des scores via Regex (expressions régulières)
    psnr_match = re.search(r"average:([0-9\.]+)", output) # Cherche "average:35.4"
    ssim_match = re.search(r"All:([0-9\.]+)", output)    # Cherche "All:0.95"
    
    psnr = psnr_match.group(1) if psnr_match else "N/A"
    ssim = ssim_match.group(1) if ssim_match else "N/A"
    
    return psnr, ssim

# --- MAIN ---
print(f"Démarrage du test sur {SOURCE_FILE}...\n")
print(f"{'CODEC':<10} | {'DEBIT':<8} | {'TEMPS (s)':<10} | {'PSNR (dB)':<10} | {'SSIM (0-1)':<10}")
print("-" * 60)

results = []

for bitrate in BITRATES:
    for name, lib in CODECS.items():
        output_filename = f"output_{name}_{bitrate}.mp4"
        
        # 1. Encodage
        enc_time = encode_video(name, lib, bitrate, output_filename)
        
        # 2. Mesure Qualité
        psnr_val, ssim_val = measure_quality(output_filename)
        
        # Affichage tableau
        print(f"{name:<10} | {bitrate:<8} | {enc_time:<10.2f} | {psnr_val:<10} | {ssim_val:<10}")

print("\nTerminé. Les fichiers vidéos sont dans le dossier.")