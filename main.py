import genshape
import sys
import os
import time
import csv
from datetime import datetime
import random

def main():
    # result(s)
    generated_shapes = []
    dirr = datetime.now().strftime('%m-%d-%Y_%H-%M-%S')
    cd = os.getcwd()
    try:
        # sample. . .
        if len(sys.argv) == 2 and str(sys.argv[1]).lower() == 'sample':
            genshape.generate(shape='sample')
            print('sample can now be found in the directory')
            endprogram()
        else:
            print('shapegen by hyun')
        # read input
        os.mkdir(os.path.join(cd, dirr))
        while True:
            r = lambda: random.randint(0,255)
            randomcolor = '#%02X%02X%02X' % (r(),r(),r())
            print("Enter a number or a name of any shape from the following or type q to exit:")
            for n in range(len(genshape.LIST)):
                print('{}) {}'.format(n+1, genshape.LIST[n]), end=' ')
            print()
            # stdin input method
            line = sys.stdin.readline().strip('\n').strip()
            # if valid num
            if line in [str(i+1) for i in range(len(genshape.LIST))]:
                shape = genshape.LIST[int(line) - 1]
                # input() input method
                #need to MAKE CSVVVVVVV
                filename, params = genshape.generate(shape=shape, color=randomcolor, sample=False, dirr=dirr)
                finalize_csv(filename, params, os.path.join(cd, dirr))
                time.sleep(1)
            # if valid shape
            elif line.lower() in genshape.LIST:
                shape = line.lower()
                filename, params = genshape.generate(shape=shape, color=randomcolor, sample=False, dirr=dirr)
                finalize_csv(filename, params, os.path.join(cd, dirr))
                time.sleep(1)
            # if escape/quit
            elif line.lower() == 'q' or line.lower() == 'quit' or line.lower() == 'esc':
                endprogram()
            # invalid input
            else:
                print('invalid input. . . returning')
                time.sleep(1)
    # graceful termination
    except KeyboardInterrupt:
        endprogram()

# handle SIGINT // ctrl + c // quit
def endprogram():
    print('terminating. . .')
    sys.exit(0)

def finalize_csv(fn, p, d):
    stats = [fn]
    for k, v in p.items():
        if k != 'sample' and k != 'dirr':
            stats.append(k+': '+str(v))
    with open(os.path.join(d, 'info.csv'), 'a+', newline='') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(stats)

if __name__ == '__main__':
    main()