import matplotlib.pyplot as plt
import numpy as np

# VOS DONNÉES (issues de votre benchmark)
bitrates = ['150k', '300k']
# PSNR
psnr_h264 = [31.25, 37.18]
psnr_h265 = [37.28, 41.32]
# Temps encodage
time_h264 = [1.38, 1.34]
time_h265 = [1.61, 2.00]

x = np.arange(len(bitrates))
width = 0.35

# --- GRAPHIQUE 1 : QUALITÉ (PSNR) ---
fig, ax = plt.subplots(figsize=(8, 5))
rects1 = ax.bar(x - width/2, psnr_h264, width, label='H.264 (AVC)', color='#e74c3c')
rects2 = ax.bar(x + width/2, psnr_h265, width, label='H.265 (HEVC)', color='#2ecc71')

ax.set_ylabel('Qualité PSNR (dB)')
ax.set_title('Comparaison de la Qualité Visuelle (Plus haut = Meilleur)')
ax.set_xticks(x)
ax.set_xticklabels(bitrates)
ax.legend()
ax.set_ylim(25, 45) # Zoom sur la zone intéressante

# Ajouter les valeurs sur les barres
ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

plt.savefig('graphique_qualite_psnr.png')
print("Graphique Qualité généré : graphique_qualite_psnr.png")

# --- GRAPHIQUE 2 : PERFORMANCE (TEMPS) ---
fig2, ax2 = plt.subplots(figsize=(8, 5))
rects1 = ax2.bar(x - width/2, time_h264, width, label='H.264 (AVC)', color='#e74c3c')
rects2 = ax2.bar(x + width/2, time_h265, width, label='H.265 (HEVC)', color='#f39c12')

ax2.set_ylabel('Temps de calcul (secondes)')
ax2.set_title("Complexité d'Encodage (Plus bas = Plus rapide)")
ax2.set_xticks(x)
ax2.set_xticklabels(bitrates)
ax2.legend()

ax2.bar_label(rects1, padding=3)
ax2.bar_label(rects2, padding=3)

plt.savefig('graphique_performance_temps.png')
print("Graphique Performance généré : graphique_performance_temps.png")