from PIL import Image
import time
 
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy 

def CudaBrightness(inPath , outPath):

    totalT0 = time.clock()
 
    im = Image.open(inPath)
    px = numpy.array(im)
    px = px.astype(numpy.float32)
 
    getAndConvertT1 = time.clock()
 
    allocT0 = time.clock()
    d_px = cuda.mem_alloc(px.nbytes)
    cuda.memcpy_htod(d_px, px)
 
    allocT1 = time.clock()
 
    #Kernel declaration
    kernelT0 = time.clock()
 
    #Kernel grid and block size
    BLOCK_SIZE = 1024
    block = (1024,1,1)
    checkSize = numpy.int32(im.size[0]*im.size[1])
    grid = (int(im.size[0]*im.size[1]/BLOCK_SIZE)+1,1,1)
 
    #Kernel text
    kernel = """
 
    __global__ void br( float *inIm, int check, int brightness ){
 
        int idx = (threadIdx.x ) + blockDim.x * blockIdx.x ;
        if(idx *3 < check*3)
        { 
			if(inIm[idx*3]+brightness > 255)
				inIm[idx*3] = 255;
			else 
        		inIm[idx*3]= inIm[idx*3]+brightness;
        	
        	if(inIm[idx*3+1]+brightness > 255)
				inIm[idx*3+1] = 255;
			else 
        		inIm[idx*3+1]= inIm[idx*3+1]+brightness;
        	
        	if(inIm[idx*3+2]+brightness > 255)
				inIm[idx*3+2] = 255;
			else 
        		inIm[idx*3+2]= inIm[idx*3+2]+brightness;
        }
    }
    """
    
    brightness = int(raw_input("Enter the level of brightness (-255 to 255): "))
    print
    if brightness > 255:
        brightness = 255
    if brightness < -255:
        brightness = -255 
    brightness = numpy.int32(brightness)
    #Compile and get kernel function
    mod = SourceModule(kernel)
    func = mod.get_function("br")
    func(d_px,checkSize,brightness,block=block,grid = grid)
 
    kernelT1 = time.clock()
 
    #Get back data from gpu
    backDataT0 = time.clock()
 
    brPx = numpy.empty_like(px)
    cuda.memcpy_dtoh(brPx, d_px)
    brPx = (numpy.uint8(brPx))
 
    backDataT1 = time.clock()
 
    #Save image
    storeImageT0 = time.clock()
    pil_im = Image.fromarray(brPx,mode ="RGB")
 
    pil_im.save(outPath)
     
    totalT1 = time.clock()
 
    getAndConvertTime = getAndConvertT1 - totalT0
    allocTime = allocT1 - allocT0
    kernelTime = kernelT1 - kernelT0
    backDataTime = backDataT1 - backDataT0
    storeImageTime =totalT1 - storeImageT0
    totalTime = totalT1-totalT0
 
    print "Brightness filter"
    print "Image size : ",im.size
    print "Time taken to get and convert image data: " ,getAndConvertTime
    print "Time taken to allocate memory on the GPU: " , allocTime
    print "Kernel execution time: " , kernelTime
    print "Time taken to get image data from GPU and convert it: " , backDataTime
    print "Time taken to save the image: " , storeImageTime
    print "Total execution time: " ,totalTime
    print

def CudaBlackWhite(inPath , outPath):

    totalT0 = time.clock()
 
    im = Image.open(inPath)
    px = numpy.array(im)
    px = px.astype(numpy.float32)
 
    getAndConvertT1 = time.clock()
 
    allocT0 = time.clock()
    d_px = cuda.mem_alloc(px.nbytes)
    cuda.memcpy_htod(d_px, px)
 
    allocT1 = time.clock()
 
    #Kernel declaration
    kernelT0 = time.clock()
 
    #Kernel grid and block size
    BLOCK_SIZE = 1024
    block = (1024,1,1)
    checkSize = numpy.int32(im.size[0]*im.size[1])
    grid = (int(im.size[0]*im.size[1]/BLOCK_SIZE)+1,1,1)
 
    #Kernel text
    kernel = """
 
    __global__ void bw( float *inIm, int check ){
 
        int idx = (threadIdx.x ) + blockDim.x * blockIdx.x ;
        if(idx *3 < check*3)
        {
       		int val = 0.21 *inIm[idx*3] + 0.71*inIm[idx*3+1] + 0.07 * inIm[idx*3+2];
        	inIm[idx*3]= val;
        	inIm[idx*3+1]= val;
        	inIm[idx*3+2]= val;
        }
    }
    """
 
    #Compile and get kernel function
    mod = SourceModule(kernel)
    func = mod.get_function("bw")
    func(d_px,checkSize, block=block,grid = grid)
 
    kernelT1 = time.clock()
 
    #Get back data from gpu
    backDataT0 = time.clock()
 
    bwPx = numpy.empty_like(px)
    cuda.memcpy_dtoh(bwPx, d_px)
    bwPx = (numpy.uint8(bwPx))
 
    backDataT1 = time.clock()
 
    #Save image
    storeImageT0 = time.clock()
    pil_im = Image.fromarray(bwPx,mode ="RGB")
 
    pil_im.save(outPath)
     
    totalT1 = time.clock()
 
    getAndConvertTime = getAndConvertT1 - totalT0
    allocTime = allocT1 - allocT0
    kernelTime = kernelT1 - kernelT0
    backDataTime = backDataT1 - backDataT0
    storeImageTime =totalT1 - storeImageT0
    totalTime = totalT1-totalT0
 
    print "Black and white image"
    print "Image size: ",im.size
    print "Time taken to get and convert image data: " ,getAndConvertTime
    print "Time taken to allocate memory on the GPU: " , allocTime
    print "Kernel execution time: " , kernelTime
    print "Time taken to get image data from GPU and convert it: " , backDataTime
    print "Time taken to save the image: " , storeImageTime
    print "Total execution time : " ,totalTime
    print
    
def CudaColor(inPath , outPath):

    totalT0 = time.clock()
 
    im = Image.open(inPath)
    px = numpy.array(im)
    px = px.astype(numpy.float32)
 
    getAndConvertT1 = time.clock()
 
    allocT0 = time.clock()
    d_px = cuda.mem_alloc(px.nbytes)
    cuda.memcpy_htod(d_px, px)
 
    allocT1 = time.clock()
 
    #Kernel declaration
    kernelT0 = time.clock()
 
    #Kernel grid and block size
    BLOCK_SIZE = 1024
    block = (1024,1,1)
    checkSize = numpy.int32(im.size[0]*im.size[1])
    grid = (int(im.size[0]*im.size[1]/BLOCK_SIZE)+1,1,1)
 
    #Kernel text
    kernel = """
 
    __global__ void co( float *inIm, int check, int color){
 
        int idx = (threadIdx.x ) + blockDim.x * blockIdx.x ;
        if(idx*3 < check*3)
        { 
			if(color == 0)
			{
				inIm[idx*3+1] = inIm[idx*3+1]-255;
				inIm[idx*3+2] = inIm[idx*3+2]-255;
			}
			else if(color == 1)
			{
				inIm[idx*3] = inIm[idx*3]-255;
				inIm[idx*3+2] = inIm[idx*3+2]-255;
			}
			else if(color == 2)
			{
				inIm[idx*3] = inIm[idx*3]-255;
				inIm[idx*3+1] = inIm[idx*3+1]-255;
			}
			
			if(inIm[idx*3] < 0)
				inIm[idx*3] = 0;
			if(inIm[idx*3] > 255)
				inIm[idx*3] = 255;
				
			if(inIm[idx*3+1] < 0)
				inIm[idx*3+1] = 0;
			if(inIm[idx*3+1] > 255)
				inIm[idx*3+1] = 255;
				
			if(inIm[idx*3+2] < 0)
				inIm[idx*3+2] = 0;
			if(inIm[idx*3+2] > 255)
				inIm[idx*3+2] = 255;
        }
    }
    """
    
    color = int(raw_input("Enter the color of the filter (0-Red;1-Green;2-Blue): ")) 
    print
    color = numpy.int32(color)
    #Compile and get kernel function
    mod = SourceModule(kernel)
    func = mod.get_function("co")
    func(d_px,checkSize,color,block=block,grid = grid)
 
    kernelT1 = time.clock()
 
    #Get back data from gpu
    backDataT0 = time.clock()
 
    coPx = numpy.empty_like(px)
    cuda.memcpy_dtoh(coPx, d_px)
    coPx = (numpy.uint8(coPx))
 
    backDataT1 = time.clock()
 
    #Save image
    storeImageT0 = time.clock()
    pil_im = Image.fromarray(coPx,mode ="RGB")
 
    pil_im.save(outPath)
     
    totalT1 = time.clock()
 
    getAndConvertTime = getAndConvertT1 - totalT0
    allocTime = allocT1 - allocT0
    kernelTime = kernelT1 - kernelT0
    backDataTime = backDataT1 - backDataT0
    storeImageTime =totalT1 - storeImageT0
    totalTime = totalT1-totalT0
 
    print "Color Filter"
    print "Image size : ",im.size
    print "Time taken to get and convert image data: " ,getAndConvertTime
    print "Time taken to allocate memory on the GPU: " , allocTime 
    print "Kernel execution time: " , kernelTime
    print "Time taken to get image data from GPU and convert it: " , backDataTime
    print "Time taken to save the image: " , storeImageTime
    print "Total execution time: " ,totalTime 
    print

def CudaNegative(inPath , outPath):

    totalT0 = time.clock()
 
    im = Image.open(inPath)
    px = numpy.array(im)
    px = px.astype(numpy.float32)
 
    getAndConvertT1 = time.clock()
 
    allocT0 = time.clock()
    d_px = cuda.mem_alloc(px.nbytes)
    cuda.memcpy_htod(d_px, px)
 
    allocT1 = time.clock()
 
    #Kernel declaration
    kernelT0 = time.clock()
 
    #Kernel grid and block size
    BLOCK_SIZE = 1024
    block = (1024,1,1)
    checkSize = numpy.int32(im.size[0]*im.size[1])
    grid = (int(im.size[0]*im.size[1]/BLOCK_SIZE)+1,1,1)
 
    #Kernel text
    kernel = """
 
    __global__ void ng( float *inIm, int check ){
 
        int idx = (threadIdx.x ) + blockDim.x * blockIdx.x ;
 
        if(idx *3 < check*3)
        { 
        	inIm[idx*3]= 255-inIm[idx*3];
        	inIm[idx*3+1]= 255-inIm[idx*3+1];
        	inIm[idx*3+2]= 255-inIm[idx*3+2];
        }
    }
    """
 
    #Compile and get kernel function
    mod = SourceModule(kernel)
    func = mod.get_function("ng")
    func(d_px,checkSize, block=block,grid = grid)
 
    kernelT1 = time.clock()
 
    #Get back data from gpu
    backDataT0 = time.clock()
 
    ngPx = numpy.empty_like(px)
    cuda.memcpy_dtoh(ngPx, d_px)
    ngPx = (numpy.uint8(ngPx))
 
    backDataT1 = time.clock()
 
    #Save image
    storeImageT0 = time.clock()
    pil_im = Image.fromarray(ngPx,mode ="RGB")
 
    pil_im.save(outPath)
     
    totalT1 = time.clock()
 
    getAndConvertTime = getAndConvertT1 - totalT0
    allocTime = allocT1 - allocT0
    kernelTime = kernelT1 - kernelT0
    backDataTime = backDataT1 - backDataT0
    storeImageTime =totalT1 - storeImageT0
    totalTime = totalT1-totalT0
 
    print "Negative image"
    print "Image size: ",im.size
    print "Time taken to get and convert image data: " ,getAndConvertTime
    print "Time taken to allocate memory on the GPU: " , allocTime
    print "Kernel execution time: " , kernelTime
    print "Time taken to get image data from GPU and convert it: " , backDataTime
    print "Time taken to save the image: " , storeImageTime
    print "Total execution time: " ,totalTime
    print

#CudaBlackWhite('C:\\Users\\AMITH KUMAR V\\Desktop\\a.jpg','C:\\Users\\AMITH KUMAR V\\Desktop\\b.jpg')
CudaBlackWhite('a.jpg','b.jpg')

#CudaBrightness('C:\\Users\\AMITH KUMAR V\\Desktop\\a.jpg','C:\\Users\\AMITH KUMAR V\\Desktop\\c.jpg')
CudaBrightness('a.jpg','c.jpg')

#CudaColor('C:\\Users\\AMITH KUMAR V\\Desktop\\a.jpg','C:\\Users\\AMITH KUMAR V\\Desktop\\d.jpg')
CudaColor('a.jpg','d.jpg')

#CudaNegative('C:\\Users\\AMITH KUMAR V\\Desktop\\a.jpg','C:\\Users\\AMITH KUMAR V\\Desktop\\e.jpg')
CudaNegative('a.jpg','e.jpg')
