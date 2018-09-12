from PIL import Image
import time

def open_image(path):
  newImage = Image.open(path)
  return newImage

def save_image(image, path):
  image.save(path, 'png')

def create_image(i, j):
  image = Image.new("RGB", (i, j), "white")
  return image

def get_pixel(image, i, j):
  width, height = image.size
  if i > width or j > height:
    return None
  pixel = image.getpixel((i, j))
  return pixel

def convert_BW(image):
  width, height = image.size
  new = create_image(width, height)
  pixels = new.load()
  t0=time.time()
  
  for i in range(width):
    for j in range(height):
      pixel = get_pixel(image, i, j)
      red =   pixel[0]
      green = pixel[1]
      blue =  pixel[2]

      gray = (red * 0.299) + (green * 0.587) + (blue * 0.114)

      pixels[i, j] = (int(gray), int(gray), int(gray))

  t1=time.time()
  print "Processing time to convert to B&W is",t1-t0,"s"
  return new

def color_filter(image,color):
  width, height = image.size
  new = create_image(width, height)
  pixels = new.load()
  t0=time.time()
  
  for i in range(width):
    for j in range(height):
      pixel = get_pixel(image, i, j)
      red =   pixel[0]
      green = pixel[1]
      blue =  pixel[2]

      if(color=='Red'):
        x=red
        y=green-255
        z=blue-255

      if(color=='Green'):
        x=red-255
        y=green
        z=blue-255

      if(color=='Blue'):
        x=red-255
        y=green-255
        z=blue
      
      x=max(x,0)
      x=min(255,x)

      y=max(y,0)
      y=min(255,y)

      z=max(z,0)
      z=min(255,z)
      
      pixels[i, j] = (int(x), int(y), int(z))

  t1=time.time()
  print "Processing time to add color filter is",t1-t0,"s"
  return new


def change_brightness(image,brightness):
  width, height = image.size
  new = create_image(width, height)
  pixels = new.load()

  if(brightness>255):
    brightness=255
  if(brightness<-255):
    brightness=-255

  t0=time.time()
  for i in range(width):
    for j in range(height):
      pixel = get_pixel(image, i, j)
      red =   pixel[0]
      green = pixel[1]
      blue =  pixel[2]

      x=red+brightness
      y=green+brightness
      z=blue+brightness

      if(x>255):
          x=255
      if(y>255):
          y=255
      if(z>255):
          z=255

      pixels[i, j] = (int(x), int(y), int(z))

  t1=time.time()
  print "Processing time to change brightness is",t1-t0,"s"
  return new

def negative(image):
  width, height = image.size
  new = create_image(width, height)
  pixels = new.load()

  t0=time.time()
  for i in range(width):
    for j in range(height):
      pixel = get_pixel(image, i, j)
      red =   pixel[0]
      green = pixel[1]
      blue =  pixel[2]

      pixels[i, j] = (int(255-red), int(255-green), int(255-blue))

  t1=time.time()
  print "Processing time to convert to Negative is",t1-t0,"s"
  return new

if __name__ == "__main__":

  original = open_image('C:\\Users\\S V MANJUNATH\\Desktop\\a.jpg')
  print "Image size",original.size
  
  new = convert_BW(original)
  save_image(new, 'C:\\Users\\S V MANJUNATH\\Desktop\\b.jpg')

  b=int(raw_input("Enter the brightness (-255 to 255)\n"))
  new = change_brightness(original,b)
  save_image(new, 'C:\\Users\\S V MANJUNATH\\Desktop\\c.jpg')

  c=raw_input("Enter the color of the filter (Red,Green,Blue)\n")
  new = color_filter(original,c)
  save_image(new, 'C:\\Users\\S V MANJUNATH\\Desktop\\d.jpg')

  new = negative(original)
  save_image(new, 'C:\\Users\\S V MANJUNATH\\Desktop\\e.jpg')
