import pifacedigitalio
pfd = pifacedigitalio.PiFaceDigital()
while True:
    for i in range(0,8):
        print i,' ' , pfd.input_pins[i].value,
    print
