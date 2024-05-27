import cv2
import numpy as np

#memuat citra dan menyalin
img_source = cv2.imread(r'D:\INSTRUMENTASI CITRA DIGITAL\Kuliah_Citra_27_5_2024\cars.jpg')
img_copy = np.copy(img_source)

#membuat citra kosong untuk penanda dan segmentasi
img_penanda = np.zeros(img_source.shape[:2], dtype=np.int32)
img_segmnetasi = np.zeros(img_source.shape, dtype=np.uint8)

#fungsi untuk membuat warna RGB pada citra segmentasi
def create_rgb(i):
    colormap = cv2.applyColorMap(np.array([[i*25]], dtype=np.uint8), cv2.COLORMAP_JET)
    return tuple(int(c) for c in colormap[0,0])

#membuat daftar warna
colors = [create_rgb(i) for i in range(10)]

#status penanda
n_markers = 10
current_marker = 1
marks_update = False

#fungsi callback untuk fungsi mouse
def mouse_callback(event, x, y, flags, param):
    global marks_update
    if event == cv2.EVENT_LBUTTONDOWN:
        #menambahkan lingkaran pada citra penanda
        cv2.circle(img_penanda, (x,y), 10, (current_marker), -1)
        #menambahkan lingkaran pada citra salinan
        cv2.circle(img_copy, (x,y), 10, colors[current_marker], -1)
        #mengupdate marker
        marks_update = True

#membuat jendela untuk menampilkan citra
cv2.namedWindow('Citra Sumber')
cv2.namedWindow('Citra Segmentasi')
cv2.setMouseCallback('Citra Sumber', mouse_callback)

#loop process
while True:
    #menampilkan citra segmentasi dan citra yang tersalin
    cv2.imshow('Citra Segmentasi', img_segmnetasi)
    cv2.imshow('Citra Sumber', img_copy)

    #mengubah ukuran jendela citra
    cv2.resizeWindow('Citra Segmentasi', 700, 600)
    cv2.resizeWindow('Citra Sumber', 700, 600)

    #menunggu input dari pengguna 
    k = cv2.waitKey(1)
    if k ==27:
        break
    #jika tombol c di tekan, maka semua penanda di citra dibersihkan
    if k == ord('c'):
        img_copy = img_source.copy()
        img_penanda = np.zeros(img_source.shape[:2], dtype=np.int32)
        img_segmnetasi = np.zeros(img_source.shape, dtype=np.uint8)
    
    #jika tombol angka 0-9 di tekan, amka ganti warna penanda
    elif k > 0 and chr(k).isdigit():
        current_marker = int(chr(k))
        n = int(chr(k))
        if 1 <= n <= n_markers :
            current_marker = n

    #jika penanda diperbarui, maka terapkan segmentasi watershed
    if marks_update:
        #membuat salinan citra 
        marker_image_copy = img_penanda.copy()
        #menerapkan algoritma watershed
        cv2.watershed(img_source, marker_image_copy)
        #mengisi segmentasi dengan warna
        img_segmnetasi = np.zeros(img_source.shape, dtype=np.uint8)
        for color_ind in range(n_markers):
            img_segmnetasi[marker_image_copy == color_ind] = colors[color_ind]
        marks_update = False

cv2.destroyAllWindows()
