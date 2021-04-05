import struct
import os
import zlib
print("Pubg Mobile Pakfile Extractor \nMade By Nihinivi \n ")
FILEPATH =str(input("Enter the pak path: "))
ExtractPath=str(input("Enter extraction folder: "))


file = open(FILEPATH,"rb")
def xor(a):
    return bytearray([b^0x79 for b in bytearray(a)])  
file2 = open(FILEPATH,"rb")


def clog(NAME, OFFSET, ZSIZE, SIZE, FNUM ,XSIZE,XOR):
    file2.seek(OFFSET)   
    data=file2.read(ZSIZE) 
    if XOR:
    	data=xor(data) 
    
    data=zlib.decompress(data)
    open(os.path.join(ExtractPath,NAME),"wb").write(data)
    

def cleanexit():
    os._exit(1)
    
    
def read_uint8(fh):
    return ord(fh.read(1))

def read_uint32(fh):
    return struct.unpack('<L', fh.read(4))[0]

def read_int32(fh):
    return struct.unpack('<l', fh.read(4))[0]

def read_uint64(fh):
    return struct.unpack('<Q', fh.read(8))[0]

 

def read_bytes(fh,count):
    return fh.read(count)

def log(NAME ,OFFSET, SIZE ,FNUM,XSIZE,XOR):
    file2.seek(OFFSET) 
    data=file2.read(SIZE)  
    if XOR:
    	data=xor(data) 
    open(os.path.join(ExtractPath,NAME),"wb").write(data  )
   

asize=len(file.read())
CURR_POS=0


CHUNK_OFFSET_ABSOLUTE = -1 



 
OFFSET = asize

 


FILES = 0x7fffffff
MAX_OFF = OFFSET
file.seek(0)
NAME = ""
BASE_NAME = "" 
 
  
 

CHUNK_SIZE = 0x10000   



for i in range(FILES):
    XOR=False
    NAME = "%08d"%i
    NAME = NAME + ".dat" 
    TMP_OFF = CURR_POS 
    HASH=file.read(20) 
    CURR_POS= CURR_POS+20
    OFFSET= read_uint64(file)
   
    CURR_POS= CURR_POS+8
    SIZE =  read_uint64(file)
    CURR_POS= CURR_POS+8
    ZIP =  read_uint32(file)
    CURR_POS= CURR_POS+4
    ZSIZE =  read_uint64(file)
    CURR_POS= CURR_POS+8
    DUMMY2 = file.read(21)  
    CURR_POS= CURR_POS+21 
    if OFFSET != 0: 
        print ("Extraction complete!")
        cleanexit()
     
    
    CHUNKS = 0
    ENCRYPTED = 0
    if 1:
        if ZIP != 0:
            CHUNKS = read_uint32(file)
            CURR_POS= CURR_POS+4
            Zero={}
            One={}
            for x in range(CHUNKS):
                CHUNK_OFFSET = read_uint64(file) 
                CURR_POS= CURR_POS+8
                CHUNK_END_OFFSET = read_uint64(file) 
                CURR_POS= CURR_POS+8
                Zero[str(x)]=CHUNK_OFFSET
                One[str(x)]=CHUNK_END_OFFSET
               
        CHUNK_SIZE = read_uint32(file) 
        CURR_POS= CURR_POS+4
        
        ENCRYPTED = read_uint8(file)
        CURR_POS= CURR_POS+1
       
 
        
   
    
    TMP_OFF = CURR_POS 
    OFFSET=OFFSET + TMP_OFF
     
    if ZIP & 1:
        comtype="zlib"
    elif ZIP&0x06:
	    comtype="zstd"
    else:
         ZIP = 0
    
     
    if CHUNKS > 0: 
        TMP_SIZE = SIZE
        if (CHUNK_OFFSET_ABSOLUTE < 0) and (OFFSET != 0):
            CHUNK_OFFSET = Zero["0"] 
            if (CHUNK_OFFSET < OFFSET)  >= 5:
                CHUNK_OFFSET_ABSOLUTE = 0
            else:
                CHUNK_OFFSET_ABSOLUTE = 1
     
        for x in range(CHUNKS):
            CHUNK_OFFSET = Zero[str(x)]
             
            CHUNK_END_OFFSET = One[str(x)]
            CHUNK_ZSIZE = CHUNK_END_OFFSET
            CHUNK_ZSIZE = CHUNK_ZSIZE - CHUNK_OFFSET
            CHUNK_XSIZE = CHUNK_ZSIZE
             
            if TMP_SIZE < CHUNK_SIZE:
                CHUNK_SIZE = TMP_SIZE
           
            if CHUNK_OFFSET_ABSOLUTE == 0:
                CHUNK_OFFSET = OFFSET
            
            if ENCRYPTED !=0:
                XOR=True
            else:
                 XOR=False
             
            if ZIP == 0:
                log(NAME, CHUNK_OFFSET ,CHUNK_SIZE, 0 ,CHUNK_XSIZE,XOR)
            else:
                clog(NAME, CHUNK_OFFSET, CHUNK_ZSIZE, CHUNK_SIZE, 0 ,CHUNK_XSIZE,XOR)
                  
         
            
            TMP_SIZE = TMP_SIZE - CHUNK_SIZE
        
     
     
    else:
       
        BASE_OFF = CURR_POS  
        BASE_OFF= BASE_OFF - TMP_OFF
        OFFSET= OFFSET + BASE_OFF
        XSIZE = ZSIZE
        
        if ZIP == 0:
            log (NAME, OFFSET, SIZE ,0, XSIZE,XOR)
          
        else:
            clog (NAME, OFFSET ,ZSIZE, SIZE ,0 ,XSIZE,XOR)
      
 
    
    OFFSET= OFFSET + ZSIZE 
    file.seek(OFFSET)
    CURR_POS=OFFSET
    if OFFSET == MAX_OFF:
        break
       
         
 