from __future__ import division             # forces floating point division 
import numpy as np                          # Numerical Python 
import matplotlib.pyplot as plt             # Python plotting
from PIL import Image                       # Python Imaging Library
from numpy.fft import fft2, fftshift, ifft2 # Python DFT
import os 
import requests

path_img = "Waldo3.jpg"
colour = "r"
sf= 0.2031

def web_scraber(path_img):
	if (os.path.isfile(path_img) ==True):
		return path_img

	elif ("https" in path_img):
		response = requests.get(path_img)
		cwd = os.getcwd()

		file = open("{}/Waldo_temp.png".format(cwd), "wb")
		file.write(response.content)
		file.close()
		return "Waldo_temp.png"
		# except:
		# 	print("Give a correct file path or a correct Url")
		# 	exit()

class Waldo():
	"""docstring for ClassName"""
	def __init__(self, path_img, colour, sf, boxradius=20):
		#Setup
		self.img_full = Image.open(path_img)
		self.chosen_colour = colour
		self.sf =sf
		self.box_radius = boxradius

		#Functions
		self.mono_colour()
		self.fourier_image()
		self.sin_cos()
		self.create_image()

	def mono_colour(self):
		r,g,b = self.img_full.split()
		r_np = np.array(r)
		g_np = np.array(g)
		b_np = np.array(b)

		if (self.chosen_colour =="r"):
			colour_supressed = r_np-(0.5*g_np+b_np)
		

		elif (self.chosen_colour == "g"):
			colour_supressed = g_np-(0.5*r_np+b_np)

		elif (self.chosen_colour == "b"):
			colour_supressed = b_np-(0.5*r_np+b_np)

		self.img_mono = Image.fromarray(colour_supressed)
		I = self.img_mono.convert('L')
		self.img_array = np.asarray(I, dtype = np.float64)

	def fourier_image(self):
		self.Height, self.Width = np.shape(self.img_array)
		self.img_fourier = fft2(self.img_array)/(self.Width*self.Height)
		self.img_fourier = fftshift(self.img_fourier)

	def sin_cos(self):
		xx,yy = np.meshgrid(np.linspace(-self.Width/2,self.Width/2,self.Width), np.linspace(-self.Height/2,self.Height/2,self.Height))
		sigma = 1/self.sf;  #width of Gaussian (1/e half-width)
		Gaussian = np.exp(-(xx**2+yy**2)/sigma**2);

		Sinus_generated = np.sin(2*np.pi*self.sf*yy)
		Cos_mixed = Sinus_generated*Gaussian;
		self.Fourier_sin = fft2(Cos_mixed)/(self.Width*self.Height)
		self.Fourier_sin = fftshift(self.Fourier_sin)
		Filter_sin = self.img_fourier*self.Fourier_sin
		self.img_filtered_sin = ifft2(Filter_sin)*self.Width*self.Height
		self.img_filtered_sin = fftshift(self.img_filtered_sin)

		Cosin_generated = np.cos(2*np.pi*self.sf*yy)
		Cos_mixed = Cosin_generated*Gaussian;
		self.Fourier_cos = fft2(Cos_mixed)/(self.Width*self.Height)
		self.Fourier_cos = fftshift(self.Fourier_cos)
		Filter_cos = self.img_fourier*self.Fourier_cos
		self.img_filtered_cos = ifft2(Filter_cos)*self.Width*self.Height
		self.img_filtered_cos = fftshift(self.img_filtered_cos)

		self.img_filtered = np.sqrt(self.img_filtered_sin**2+self.img_filtered_cos**2)

	def create_image(self):
		self.img_filtered_scaled = self.img_filtered/np.max(self.img_filtered)
		self.img_filtered_scaled = np.abs((self.img_filtered_scaled+.25)/1.2)

		center_coord = np.where(self.img_filtered_scaled == np.amax(self.img_filtered_scaled))
		for x_coord in range(center_coord[0][0]-self.box_radius, center_coord[0][0]+self.box_radius):
			for y_coord in range(center_coord[0][0]-self.box_radius, center_coord[1][0]+self.box_radius):
				self.img_filtered_scaled[x_coord, y_coord] = 0.9

		self.img_filtered_scaled_transposed = np.asarray([self.img_filtered_scaled]*3).transpose(1, 2, 0)
		# self.img_filtered_scaled = np.abs(filtImg)
		self.img_final = np.asarray(np.asarray(self.img_full, dtype = np.float64)*self.img_filtered_scaled_transposed, dtype="uint8");

	def normal_image_print(self):
		plt.imshow(self.img_full)
		plt.show()

	def mono_colour_print(self):
		plt.imshow(self.img_mono)
		plt.show()

	def fourier_image_print(self):
		plt.imshow(np.log(np.abs(self.img_fourier)))
		plt.show()

	def image_filtered_print(self):
		plt.imshow(np.abs(self.img_filtered))
		plt.show()

	def image_final_print(self):
		plt.imshow(self.img_final)
		plt.show()


if __name__ == "__main__":
	path_img = web_scraber(path_img)

	Waldo = Waldo(path_img, colour, sf)
	Waldo.normal_image_print()
	# Waldo.mono_colour_print()
	# Waldo.fourier_image_print()
	# Waldo.image_filtered_print()

	Waldo.image_final_print()