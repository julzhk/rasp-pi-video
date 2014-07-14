__author__ = 'julz'
from time import sleep

class PhaseChange(Exception):
    pass

class startphase0(PhaseChange):
    pass

class startphase1(PhaseChange):
    pass

class quitphase(PhaseChange):
    pass

def phase0():
    print 'phase0'
    sleep(4)
    raise startphase1

def phase1():
    print 'phase1'
    sleep(3)
    raise quitphase

def quit():
    exit()

def main(phase=0):
    run_phase = phase0
    while True:
        try:
            run_phase()
        except startphase0:
            run_phase=phase0
        except startphase1:
            run_phase=phase1
        except quitphase:
            run_phase=quit

if __name__ == "__main__":
    main()
