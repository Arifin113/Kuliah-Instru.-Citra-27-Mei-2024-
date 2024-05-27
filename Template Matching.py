import cv2
import numpy as np

#memuat citra sumber 
img_source = cv2.imread(r'D:\INSTRUMENTASI CITRA DIGITAL\Kuliah_Citra_27_5_2024\Sampel Citra\source.jpg')

#konversi citra ke grayscale
img_gray = cv2.cvtColor(img_source, cv2.COLOR_BGR2GRAY)

#memuat citra template
template = cv2.imread(r'D:\INSTRUMENTASI CITRA DIGITAL\Kuliah_Citra_27_5_2024\Sampel Citra\template.jpg', 0)

#menghitung ukuran citra template
w, h = template.shape[::-1]

#menerapkan templare matching
hasil = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where(hasil >= threshold)

# Menggambar RoI (Radio of Interest)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_source, pt, (pt[0] + w, pt[1] + h), (0, 255,255), 2)

#menampilkan citra
cv2.imshow('Hasil', img_source)
cv2.waitKey(0)
cv2.destroyAllWindows()