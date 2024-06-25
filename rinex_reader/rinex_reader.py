from gnss_tec import rnx

def read_rinex_file(filename):
    with open(filename) as obs_file:
        reader = rnx(obs_file)
        for tec in reader:
            yield tec.timestamp, tec.satellite, tec.phase_tec, tec.p_range_tec
