# Kullanimi
# python color_kmeans.py --i images/leaf.jpg --c 3
# python color_kmeans.py --i images/moon.jpg --c 5
# python color_kmeans.py --i images/desert.jpg --c 3

# Gerekli paketler import edildi
from sklearn.cluster import KMeans  
import matplotlib.pyplot as plt
import argparse
import functions
import cv2
from PIL import Image, ImageDraw, ImageFilter 


# Consoldan alinacak fotograf ve baskin renk sayisi
ap = argparse.ArgumentParser()

# -i veya --image ile fotograf yolu alinicak
ap.add_argument("-i", "--image", required = True, help = "Fotograf yolu")

# -c veya --clusters ile baskin renk sayisi alinicak 
ap.add_argument("-c", "--clusters", required = True, type = int,
	help = "baskin renk sayisi")
args = vars(ap.parse_args())

# Fotograf yukenip BGR den RGB renk koduna donusturulucek
# fotograf yuklenirken BGR turunde gelir
image = cv2.imread(args["image"])

cv2.imshow("Orjinal Fotograf",image)
 
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Orjinal Fotografi goruntuleme

# Orjinal fotografi gri renk tonlarina cevirme cevirme 
im_gray = cv2.imread(args["image"], 0)    

# Griye cevrilmis fotografi siyah beyaz yapiyoruz
(thresh, blackAndWhiteImage) = cv2.threshold(im_gray, 127, 255, cv2.THRESH_BINARY_INV)
colorBalance = {
	"white":0,
	"black":0
}

# Fotograftaki siyah ve beyaz renk sayisini color objesine aktariyorum
for i in blackAndWhiteImage:
	for a in i:
		if(a == 255):
			colorBalance["white"]+=1
		else:
			colorBalance["black"]+=1

balance = 127 

# siyah beyaz sayisina gore objenin rengini belirleyip objeyi siyah yapma islemini yapiyorum
if(colorBalance["white"]>colorBalance["black"]):
	(thresh, blackAndWhiteImage) = cv2.threshold(im_gray, balance, 255, cv2.THRESH_BINARY_INV)
else:
	(thresh, blackAndWhiteImage) = cv2.threshold(im_gray, balance, 255, cv2.THRESH_BINARY)

cv2.imshow('blackandwhite',blackAndWhiteImage)

# Fotografi kaydetme islemi yapiyorum
cv2.imwrite('images/bw_img.png',blackAndWhiteImage)

# Baskin renkleri bulmadan once maskeleme islemi yaparak objenin oldugu kismi beyaz birakiyorum
# Bu sayede olusturacagim patterne objenin renkleri karismamis oluyor
im1 = Image.open(args["image"])

# images/pattern2.png : Full beyaz image
im2 = Image.open('images/pattern2.png').resize(im1.size)
mask = Image.open('images/bw_img.png').resize(im1.size)
mask_blur = mask.filter(ImageFilter.GaussianBlur(10))
im = Image.composite(im1, im2, mask)
im.save('images/newImages.png')
# im.show()

image = cv2.imread('images/newImages.png')

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
cv2.imshow('image',image)


image = image.reshape((image.shape[0] * image.shape[1], 3))

# Burada pixel yogunluklarini gruplama islemi yapiliyor
clt = KMeans(n_clusters = args["clusters"])
clt.fit(image)

# histogram grafigini olusturup figure olusturuyor
# her pixelin yogunluguna gore resmi olusturuyor
hist = functions.centroid_histogram(clt)
bar = functions.plot_colors(hist, clt.cluster_centers_) 

# prepare image and figure 
 

plt.figure()
plt.axis("off")
plt.imshow(bar)

# images masking here 
im1 = Image.open(args["image"])
im2 = Image.open('images/pattern.png').resize(im1.size)
mask = Image.open('images/bw_img.png').resize(im1.size)
mask_blur = mask.filter(ImageFilter.GaussianBlur(10))
im = Image.composite(im1, im2, mask)

im.show()

plt.show()
