# Tidak Bisa Dipakai

import os
os.system("ffmpeg -f image2 -r 1/0.33 -i ./bahanvid/frame_%01d.jpg -vcodec mpeg4 -y ./videos/frame.mp4")