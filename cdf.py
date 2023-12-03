"""
Process the raw data file into distinct CDF files.
"""

import sys
from collections import defaultdict

if __name__ == "__main__":
    raw_data = open(sys.argv[1], "r")
    print("Reading CDF data from %s" % raw_data.name)

    lines = raw_data.readlines()
    workload_cdfs = defaultdict(lambda: [])

    prev_line = (None, 0, 0.0)
    for i, line in enumerate(lines):
        if i == 0:
            continue

        cells = line.split()

        if cells[0] != "Homa":
            break
        if cells[1] != "0.5":
            continue

        workload = cells[2]
        msg_sz = int(cells[3])
        msg_freq = float(cells[4])

        if (workload, msg_sz, msg_freq) == prev_line:
            continue
        
        prev_freq = 0 if len(workload_cdfs[workload]) == 0 else workload_cdfs[workload][-1][1]
        workload_cdfs[workload].append((msg_sz, round(prev_freq + msg_freq, 5)))

        prev_line = (workload, msg_sz, msg_freq)
    
    for workload, cdfs in workload_cdfs.items():
        with open(f"{workload}_MsgSizeDist.txt", "w+") as fp:
            cdfs[-1] = (cdfs[-1][0], 100.0)
            print(workload)
            for sz, freq in cdfs:
                freq = round(freq / 100, 6)
                fp.write(f"{sz}      {freq}")
                print(f"{sz}\t{freq}")
    