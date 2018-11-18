import board, digitalio, time, adafruit_sdcard, busio, storage, adafruit_thermistor, adafruit_lis3dh, neopixel, analogio, os

sw = digitalio.DigitalInOut(board.SLIDE_SWITCH)
sw.direction = digitalio.Direction.INPUT
sw.pull = digitalio.Pull.UP

hb = analogio.AnalogIn(board.A5)

thermistor = adafruit_thermistor.Thermistor(board.TEMPERATURE, 10000, 10000, 25, 3950)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.03)

lis3dh_i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(lis3dh_i2c, address=0x19)
lis3dh.range = adafruit_lis3dh.RANGE_8_G

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.SCL)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

def printDirectoryHelper(path, tabs=0):
    for file in os.listdir(path):
        stats = os.stat(path + "/" + file)
        filesize = stats[6]
        isdir = stats[0] & 0x4000
 
        if filesize < 1000:
            sizestr = str(filesize) + " by"
        elif filesize < 1000000:
            sizestr = "%0.1f KB" % (filesize / 1000)
        else:
            sizestr = "%0.1f MB" % (filesize / 1000000)
 
        prettyprintname = ""
        for _ in range(tabs):
            prettyprintname += "   "
        prettyprintname += file
        if isdir:
            prettyprintname += "/"
        print('{0:<40} Size: {1:>10}'.format(prettyprintname, sizestr))

        if isdir:
            printDirectoryHelper(path + "/" + file, tabs + 1)

def printDirectory():
    print("Files on filesystem:")
    print("====================")
    printDirectoryHelper("/sd")

def temperature(pause=1):
    c = thermistor.temperature
    f = c * 9 / 5 + 32
    # print("Temperature is: %f C and %f F" % (c, f))
    time.sleep(pause)
    return dict(zip(["c", "f"], [c, f]))

def motion(pause=1):
    x, y, z = lis3dh.acceleration
    time.sleep(pause)
    return dict(zip(["x", "y", "z"], [x, y, z]))

def heartBeat(pause=1):
    return hb.value

def analysis():
    hbs = []
    for i in range(0,10):
        hbs.append(int(hb.value/65535*4096))
        time.sleep(0.02)
    return sum(sorted(hbs)[1:9])/8

def blink(pause=0.3, c=3, color=(0, 255, 0)):
    # (0, 255, 0) green (0,0xBF,0x11)
    for i in range(0, c):
        pixels.fill(color)
        pixels.show()
        time.sleep(pause)
        pixels.fill((0,0,0))
        pixels.show()
        time.sleep(pause)

# blink(pause=1, c=1) #ini finishes

dfilter, dmax, dmin, dmid = 0, 0, 0, 0
PULSE, PRE_PULSE = False, False
pulseCount = 0
IBI, BPM, SIG = 0, 0, 0
readData, preReadData = 0, 0
#发送给上位机的三个量 IBI: 相邻两个心跳的时间，BPM: 心率值， SIG: 脉象图的数值化表示
timeCount, firstTimeCount, secondTimeCount = 0, 0, 0
data = []

while True:
    if sw.value: #left is True
        preReadData = readData
        readData = analysis()
        if (readData - preReadData) < dfilter:
            data.append(readData)
        if len(data) >= 50:
            dmax = max(data)
            dmin = min(data)
            dmid = (dmax+dmin)/2
            dfilter = (dmax-dmin)/2
            data = []
        PRE_PULSE = PULSE
        PULSE = True if readData > dmid else False
        if PRE_PULSE == False and PULSE == True:
            pulseCount += 1
            pulseCount %= 2
            if pulseCount == 1:
                firstTimeCount = timeCount
            if pulseCount == 0:
                secondTimeCount = timeCount
                timeCount = 0
                if secondTimeCount > firstTimeCount:
                    IBI = (secondTimeCount - firstTimeCount) * 160
                    BPM = 60000 / IBI
                    if BPM > 200:
                        BPM = 200                 
                    if BPM < 30:
                        BPM = 30
            print("SIG = %d IBI = %d, BMP = %d\n\n" % (readData, IBI, BPM))
        timeCount += 1
        time.sleep(0.02)
