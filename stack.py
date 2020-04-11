import sys
import PIL
from PIL import Image, ImagePalette

def quantizetopalette(silf, palette, dither=False):
    """Convert an RGB or L mode image to use a given P image's palette."""

    silf.load()

    # use palette from reference image made below
    palette.load()
    im = silf.im.convert("P", 0, palette.im)
    # the 0 above means turn OFF dithering making solid colors
    return silf._new(im)

if __name__ == "__main__":
    import sys, os

for imgfn in sys.argv[1:]:
    palettedata = [ 0, 0, 0, 255, 0, 0, 255, 255, 0, 0, 255, 0, 255, 255, 255,85,255,85, 255,85,85, 255,255,85]

#   palettedata = [ 0, 0, 0, 0,170,0, 170,0,0, 170,85,0,] # pallet 0 dark
#   palettedata = [ 0, 0, 0, 85,255,85, 255,85,85, 255,255,85]  # pallet 0 light

#   palettedata = [ 0, 0, 0, 85,255,255, 255,85,255, 255,255,255,]  #pallete 1 light
#   palettedata = [ 0, 0, 0, 0,170,170, 170,0,170, 170,170,170,] #pallete 1 dark
#   palettedata = [ 0,0,170, 0,170,170, 170,0,170, 170,170,170,] #pallete 1 dark sp

#   palettedata = [ 0, 0, 0, 0,170,170, 170,0,0, 170,170,170,] # pallet 3 dark
#   palettedata = [ 0, 0, 0, 85,255,255, 255,85,85, 255,255,255,] # pallet 3 light

#  grey  85,85,85) blue (85,85,255) green (85,255,85) cyan (85,255,255) lightred 255,85,85 magenta (255,85,255)  yellow (255,255,85)
# black 0, 0, 0,  blue (0,0,170) darkred 170,0,0 green (0,170,0)  cyan (0,170,170)magenta (170,0,170) brown(170,85,0) light grey (170,170,170)
#
# below is the meat we make an image and assign it a palette
# after which it's used to quantize the input image, then that is saved
    palimage = Image.new('P', (16, 16))
    palimage.putpalette(palettedata *32)
    oldimage = Image.open(sys.argv[1])
    oldimage = oldimage.convert("RGB")
    newimage = quantizetopalette(oldimage, palimage, dither=False)
    dirname, filename= os.path.split(imgfn)
    name, ext= os.path.splitext(filename)
    newpathname= os.path.join(dirname, "cga-%s.png" % name)
    newimage.save(newpathname)

#   palimage.putpalette(palettedata *64)  64 times 4 colors on the 256 index 4 times, == 256 colors, we made a 256 color pallet.


def get_colors():
	img = Image.open('palheta1.jpg')
	# img = img.quantize(colors=5, method=1)
	pal = img.getpalette()

	palheta = ImagePalette.ImagePalette(mode='RGB', palette=pal)

	im = Image.open('fonte2.jpg')

	im = im.quantize(colors=50, method=1)
	# im.show()
	im = im.convert('P', palette=Image.ADAPTIVE)
	im.show()
	im.putpalette(palheta)
	im.show()

# get_colors()

def get_colors2():
	# img = Image.open('palheta3.jpg')
	img = Image.open('fonte.jpg')
	# img = img.quantize(colors=5, method=1)
	img = img.quantize(colors=5, method=1)
	# img.show()
	pal = img.getpalette()
	# print(pal)
	# add = 753
	# pal = [255,255,255, 0,0,0, 255,0,0, 0,255,0, 0,0,255] + [0 for _ in range(add)]
	# palheta = ImagePalette.ImagePalette(mode='P', palette=pal, size=15+add)
	palheta = ImagePalette.ImagePalette(mode='P', palette=pal, size=len(pal))

	im = Image.open('fonte2.jpg')
	# im = im.quantize(colors=20, method=1)
	# im.show()
	im = im.quantize(colors=18, method=1)
	im = im.convert('P', palette=Image.ADAPTIVE)
	# im = im.convert('P', palette=palheta)
	im.show()
	im.putpalette(palheta)
	im.show()

get_colors2()

def testos():
	# i = Image.new('RGB', (1,1), (255, 255, 255))
	i = Image.open('fonte2.jpg')
	# p = Image.new('P', (1,1))
	p = Image.open('palheta3.jpg')
	p = p.convert('P')
	# i2 = i.quantize(palette=p)
	i2 = i.quantize(palette=p)
	i2 = i2.convert('RGB')

	i2.show()
	# print(i2.convert('RGB').load()[0, 0])  # (252, 252, 252)

# testos()



# im = Image.open('cores.jpg')
# im = im.quantize(colors=5, method=1)
# im.show()


def main():
	# from PIL import Image
	# palettedata = [0, 0, 0, 102, 102, 102, 176, 176, 176, 255, 255, 255]
	# palimage = Image.new('P', (16, 16))
	# palimage.putpalette(palettedata * 64)
	# oldimage = Image.open("fonte2.jpg")
	# newimage = oldimage.quantize(palette=palimage)
	# newimage.show()

	im = Image.open('fonte2.jpg')
	# using Image.ADAPTIVE to avoid dithering
	# out = im.convert('P', palette=Image.ADAPTIVE, colors=5)
	# m = (0, 0, 0, 102, 102, 102, 176, 176, 176, 255, 255, 255)
	m = (1, 1, 1, 1)
	# out = im.convert('RGB', m)
	palheta_img = Image.open('palheta3.jpg')
	palheta_img = palheta_img.convert('L', palette=Image.ADAPTIVE)
	palheta = palheta_img.getpalette()
	# palheta_img.show()
	# out = im.putpalette(palheta)
	print(palheta)
	palheta = [0, 0, 0, 255]
	# out = im.convert('RGB', palette=palheta)
	out = im.quantize(colors=5, method=0, kmeans=1)
	# out = im.convert('RGB', matrix=m, palette=Image.ADAPTIVE, colors=10)
	# out = im.convert('1', dither=Image.NONE)
	# out = im.convert('P', colors=5)
	out.show()


# main()
