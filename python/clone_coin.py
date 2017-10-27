import subprocess, sys
from params import t,z,n,a,v 

def clone_genesish0():
    popen = subprocess.Popen(["git","clone","https://github.com/jdavidthomson/GenesisH0.git"],stdout=subprocess.PIPE)
    return_code = popen.wait()
    if return_code != 0:
        print return_code
        while True:
                out = popen.stdout.read(1)
                if out == '' and popen.poll() != None:
                    break
                if out != '':
                    sys.stdout.write(out)
                    sys.stdout.flush()
        raise Exception('Error running subprocess command "git clone"')

def clone_bitcoin():
    popen = subprocess.Popen(["git","clone","https://github.com/jdavidthomson/bitcoin.git","-b","v0.15.0.1"],stdout=subprocess.PIPE)
    return_code = popen.wait()
    if return_code != 0:
        print return_code
        while True:
            out = popen.stdout.read(1)
            if out == '' and popen.poll() != None:
                break
            if out != '':
                sys.stdout.write(out)
                sys.stdout.flush()
        raise Exception('Error running subprocess command "git clone"')

def setup_genesish0():
    popen = subprocess.Popen(["pip","install","scrypt","construct==2.5.2"],stdout=subprocess.PIPE)
    return_code = popen.wait()
    if return_code != 0:
        print return_code
        while True:
            open = popen.stdout.read(1)
            if out == '' and popen.poll() != None:
                break
            if out != '':
                sys.stdout.write(out)
                sys.stdout.flush()
        raise Exception ('Error running subprocess command "pip install..."')

def run_genesish0():
    popen = subprocess.Popen(["python","./GenesisH0/genesis.py","-t",str(t),"-z",str(z),"-n",str(n),"-a",str(a),"-v",str(v)],stdout=subprocess.PIPE)
    print "Processing genesis block.  This will take MANY HOURS.  Go for a night out and check back in the morning..."
    return_code = popen.wait()
    if return_code != 0:
        print return_code
        while True:
            out = popen.stdout.read(1)
            if out == '' and popen.poll() != None:
                break
            if out != '':
                sys.stdout.write(out)
                sys.stdout.flush()
        raise Exception('Error running subprocess command "git clone"')
    else:
        with open('./data/genesis_block.txt','w') as genesis_block:
            for line in popen.stdout:
                genesis_block.write(line + "\n")    

def get_genesis_params():
    merkle_hash = None
    pszTimestamp = None
    pubkey = None
    time = None
    bits = None
    nonce = None
    genesis_hash = None

    with open('./data/genesis_block.txt') as genesis_block:
        for line in genesis_block:
            if "merkle hash:" in line:
                merkle_hash = line.split(":")[1].strip()
            elif "pszTimestamp:" in line:
                pszTimestamp = line.split(":")[1].strip()
            elif "pubkey:" in line:
                pubkey = line.split(":")[1].strip()
            elif "time:" in line:
                time = line.split(":")[1].strip()
            elif "bits:" in line:
                bits = line.split(":")[1].strip()
            elif "nonce:" in line:
                nonce = line.split(":")[1].strip()
            elif "genesis hash:" in line:
                genesis_hash = line.split(":")[1].strip()

    return merkle_hash, pszTimestamp, pubkey, time, bits, nonce, genesis_hash

def modify_chainparams_cpp(merkle_hash, pszTimestamp, pubkey, time, bits, nonce, genesis_hash):
    print merkle_hash
    print pszTimestamp
    print pubkey
    print time
    print bits
    print nonce
    print genesis_hash
    raise Exception("not implemented yet")


if __name__ == "__main__":
    #clone_genesish0()
    #clone_bitcoin()
    #setup_genesish0()
    #run_genesish0()
    merkle_hash, pszTimestamp, pubkey, time, bits, nonce, genesis_hash = get_genesis_params()
    modify_chainparams_cpp(merkle_hash, pszTimestamp, pubkey, time, bits, nonce, genesis_hash)
