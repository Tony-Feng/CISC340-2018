import board, digitalio, time, adafruit_sdcard, busio, storage, adafruit_thermistor, adafruit_lis3dh, neopixel, analogio

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

uart = busio.UART(board.TX, board.RX, baudrate=115200)

def temperature(pause=1):
    c = thermistor.temperature
    time.sleep(pause)
    return c

def motion(pause=1):
    x, y, z = lis3dh.acceleration
    time.sleep(pause)
    return dict(zip(["x", "y", "z"], [x, y, z]))

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
            s = "timestamp = " + str(time.time())
            s += ", SIG = %d, IBI = %d, BMP = %d, " % (readData, IBI, BPM)
            s += "t = %d, " % temperature(0)
            stmp = motion(0)
            s += "x = %f, y = %f, z = %f" % (stmp['x'], stmp['y'], stmp['z'])
            with open("/sd/records.txt", "a") as f:
                f.write(s+"\r\n")
            result = [i.split(" = ")[1] for i in s.split(", ")]
            result = ", ".join([result[0]]+result[3:])+")"
            uart.write(result)
            print(s)
            # timestamp, heartrate, temp, motion_x, motion_y, motion_z
        timeCount += 1
        time.sleep(0.02)
