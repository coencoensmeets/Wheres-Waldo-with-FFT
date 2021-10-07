from __future__ import division             # forces floating point division 
import numpy as np                          # Numerical Python 
import matplotlib.pyplot as plt             # Python plotting
from PIL import Image                       # Python Imaging Library
from numpy.fft import fft2, fftshift, ifft2 # Python DFT
import math

img = Image.open("Waldo3.jpg")
data = img.getdata()

r,g,b = img.split()
print(r, g, b)

r_np = np.array(r)
g_np = np.array(g)
b_np = np.array(b)

g_b_surpessed = r_np-(0.5*g_np+b_np)


img_one = Image.fromarray(g_b_surpessed )
plt.imshow(img_one)
plt.show()

I = img_one.convert('L')                     # 'L' for gray scale mode
A3 = np.asarray(I, dtype = np.float64)  # Image class instance, I1, to float32 Numpy array, a

H,W = np.shape(A3)
hW = int(np.fix(0.5*W))
hH = int(np.fix(0.5*H))

F3 = fft2(A3)/(W*H)
F3 = fftshift(F3)

xx,yy = np.meshgrid(np.linspace(-W/2,W/2,W), np.linspace(-H/2,H/2,H))
sf=0.2031
sigma = 1/sf;  #width of Gaussian (1/e half-width)
Gaussian = np.exp(-(xx**2+yy**2)/sigma**2);

gratingSin = np.sin(2*np.pi*sf*yy)
GaborSin = gratingSin*Gaussian;
F3_sin = fft2(GaborSin)/(W*H)
F3_sin = fftshift(F3_sin)
Filter_sin = F3*F3_sin
filtImgSin = ifft2(Filter_sin)*W*H
filtImgSin = fftshift(filtImgSin)

gratingCos = np.cos(2*np.pi*sf*yy)
GaborCos = gratingCos*Gaussian;
F3_cos = fft2(GaborCos)/(W*H)
F3_cos = fftshift(F3_cos)
Filter_cos = F3*F3_cos
filtImgCos = ifft2(Filter_cos)*W*H
filtImgCos = fftshift(filtImgCos)

filtImg = np.sqrt(filtImgSin**2+filtImgCos**2)
# filtImg = filtImgSin

attenuateImg = filtImg/np.max(filtImg)
attenuateImg = np.abs((attenuateImg+.25)/1.2)

center_coord = np.where(attenuateImg == np.amax(attenuateImg))
box_radius = 25
for x_coord in range(center_coord[0][0]-box_radius, center_coord[0][0]+box_radius):
	for y_coord in range(center_coord[0][0]-box_radius, center_coord[1][0]+box_radius):
		attenuateImg[x_coord, y_coord] = 0.9

attenuateImg_transposed = np.asarray([attenuateImg]*3).transpose(1, 2, 0)
# attenuateImg = np.abs(filtImg)
new_img = np.asarray(np.asarray(img, dtype = np.float64)*attenuateImg_transposed, dtype="uint8");


plt.imshow(np.abs(new_img))
plt.show()