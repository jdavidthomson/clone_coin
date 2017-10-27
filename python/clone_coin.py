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
    with open('./bitcoin/src/chainparams.cpp') as chainparams_src, open('./bitcoin/src/chainparams_new.cpp','w') as chainparams_dest:
        for line in chainparams_src:
            check_line = line.strip()
            if check_line == 'const char* pszTimestamp = "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks";':
                check_line = 'const char* pszTimestamp = "' + pszTimestamp + '"'
            elif check_line == 'const CScript genesisOutputScript = CScript() << ParseHex("04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f") << OP_CHECKSIG;' :
                check_line = 'const CScript genesisOutputScript = CScript() << ParseHex("' + pubkey + '") << OP_CHECKSIG;'
            elif check_line == 'consensus.BIP34Height = 227931;':
                check_line = 'consensus.BIP34Height = 0;'
            elif check_line == 'consensus.BIP34Hash = uint256S("0x000000000000024b89b42a942fe0d9fea3bb44ab7bd1b19115dd6a759c0808b8");':
                check_line = 'consensus.BIP34Hash = uint256S("0x' + genesis_hash + '");'
            elif check_line == 'consensus.BIP65Height = 388381;':
                check_line = 'consensus.BIP65Height = 1;'
            elif check_line == 'consensus.BIP66Height = 363725;':
                check_line = 'consensus.BIP66Height = 1;'
            elif check_line == 'consensus.powLimit = uint256S("00000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffff");':
                check_line = 'consensus.powLimit = uint256S("7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff");'
            elif check_line == 'consensus.vDeployments[Consensus::DEPLOYMENT_TESTDUMMY].nStartTime = 1199145601; // January 1, 2008':
                check_line = 'consensus.vDeployments[Consensus::DEPLOYMENT_TESTDUMMY].nStartTime = 0;'
            elif check_line == 'consensus.vDeployments[Consensus::DEPLOYMENT_TESTDUMMY].nTimeout = 1230767999; // December 31, 2008':
                check_line = 'consensus.vDeployments[Consensus::DEPLOYMENT_TESTDUMMY].nTimeout = 999999999999ULL;'
            elif check_line == 'consensus.vDeployments[Consensus::DEPLOYMENT_CSV].bit = 0;':
                check_line = 'consensus.vDeployments[Consensus::DEPLOYMENT_CSV].bit = 0;'
            elif check_line == 'consensus.vDeployments[Consensus::DEPLOYMENT_CSV].nStartTime = 1462060800; // May 1st, 2016':
                check_line = 'consensus.vDeployments[Consensus::DEPLOYMENT_CSV].nStartTime = 0;'
            elif check_line == 'consensus.vDeployments[Consensus::DEPLOYMENT_CSV].nTimeout = 1493596800; // May 1st, 2017':
                check_line = 'consensus.vDeployments[Consensus::DEPLOYMENT_CSV].nTimeout = 999999999999ULL;'
            elif check_line == 'consensus.vDeployments[Consensus::DEPLOYMENT_SEGWIT].bit = 1;':
                check_line = 'consensus.vDeployments[Consensus::DEPLOYMENT_SEGWIT].bit = 1;'
            elif check_line == 'consensus.vDeployments[Consensus::DEPLOYMENT_SEGWIT].nStartTime = 1479168000; // November 15th, 2016.':
                check_line = 'consensus.vDeployments[Consensus::DEPLOYMENT_SEGWIT].nStartTime = 0;'
            elif check_line == 'consensus.vDeployments[Consensus::DEPLOYMENT_SEGWIT].nTimeout = 1510704000; // November 15th, 2017.':
                check_line = 'consensus.vDeployments[Consensus::DEPLOYMENT_SEGWIT].nTimeout = 999999999999ULL;'
            elif check_line == 'consensus.nMinimumChainWork = uint256S("0x000000000000000000000000000000000000000000723d3581fe1bd55373540a");':
                check_line = 'consensus.nMinimumChainWork = uint256S("0x00");'
            elif check_line == 'consensus.defaultAssumeValid = uint256S("0x0000000000000000003b9ce759c2a087d52abc4266f8f4ebd6d768b89defa50a"); //477890':
                check_line = 'consensus.defaultAssumeValid = uint256S("0x00");'
            elif check_line == 'genesis = CreateGenesisBlock(1506654905,3468599434,0x1d00ffff, 1, 20000 * COIN);':
                check_line = 'genesis = CreateGenesisBlock(' + str(time) + ', ' + str(nonce) + ',' + str(bits) + ', 1, 20000 * COIN);'
            elif check_line == 'assert(consensus.hashGenesisBlock == uint256S("0x000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"));':
                check_line = 'assert(consensus.hashGenesisBlock == uint256S("0x' + str(genesis_hash) + '"));'
            elif check_line == 'assert(genesis.hashMerkleRoot == uint256S("0x4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"));':
                check_line = 'assert(genesis.hashMerkleRoot == uint256S("0x' + str(merkle_hash) + '"));'
            elif check_line == 'vSeeds.emplace_back("seed.bitcoin.sipa.be", true); // Pieter Wuille, only supports x1, x5, x9, and xd':
                check_line = ''
            elif check_line == 'vSeeds.emplace_back("dnsseed.bluematt.me", true); // Matt Corallo, only supports x9':
                check_line = ''
            elif check_line == 'vSeeds.emplace_back("dnsseed.bitcoin.dashjr.org", false); // Luke Dashjr':
                check_line = ''
            elif check_line == 'vSeeds.emplace_back("seed.bitcoinstats.com", true); // Christian Decker, supports x1 - xf':
                checkline = ''
            elif check_line == 'vSeeds.emplace_back("seed.bitcoin.jonasschnelli.ch", true); // Jonas Schnelli, only supports x1, x5, x9, and xd':              
                check_line = ''
            elif check_line == 'vSeeds.emplace_back("seed.btc.petertodd.org", true); // Peter Todd, only supports x1, x5, x9, and xd':
                check_line = ''
            elif check_line == '{ 11111, uint256S("0x0000000069e244f73d78e8fd29ba2fd2ed618bd6fa2ee92559f542fdb26e7c1d")},':
                check_line = '{0, uint256S("' + str(genesis_hash) + '")},'
            elif check_line == '{ 33333, uint256S("0x000000002dd5588a74784eaa7ab0507a18ad16a236e7b1ce69f00d7ddfb5d0a6")},':
                check_line = ''
            elif check_line == '{ 74000, uint256S("0x0000000000573993a3c9e41ce34471c079dcf5f52a0e824a81e7f953b8661a20")},':
                check_line = ''
            elif check_line == '{105000, uint256S("0x00000000000291ce28027faea320c8d2b054b2e0fe44a773f3eefb151d6bdc97")},':
                check_line = ''
            elif check_line == '{134444, uint256S("0x00000000000005b12ffd4cd315cd34ffd4a594f430ac814c91184a0d42d2b0fe")},':
                check_line = ''
            elif check_line == '{168000, uint256S("0x000000000000099e61ea72015e79632f216fe6cb33d7899acb35b75c8303b763")},':
                check_line = ''
            elif check_line == '{193000, uint256S("0x000000000000059f452a5f7340de6682a977387c17010ff6e6c3bd83ca8b1317")},':
                check_line = ''
            elif check_line == '{210000, uint256S("0x000000000000048b95347e83192f69cf0366076336c639f9b7228e9ba171342e")},':
                check_line = ''
            elif check_line == '{216116, uint256S("0x00000000000001b4f4b433e81ee46494af945cf96014816a4e2370f11b23df4e")},':
                check_line = ''
            elif check_line == '{225430, uint256S("0x00000000000001c108384350f74090433e7fcf79a606b8e797f065b130575932")},':
                check_line = ''
            elif check_line == '{250000, uint256S("0x000000000000003887df1f29024b06fc2200b55f8af8f35453d7be294df2d214")},':
                check_line = ''
            elif check_line == '{279000, uint256S("0x0000000000000001ae8c72a0b0c301f67e3afca10e819efa9041e458e9bd7e40")},':
                check_line = ''
            elif check_line == '{295000, uint256S("0x00000000000000004d9b4ef50f0f9d686fd69db2e03af35a100370c64632a983")},':
                check_line = ''
            elif check_line == '1501801925, // * UNIX timestamp of last known number of transactions':
                check_line = '0'
            elif check_line == '243756039,  // * total number of transactions between genesis and that timestamp':
                check_line = '0'
            elif check_line == '//   (the tx=... number in the SetBestChain debug.log lines)':
                check_line = ''
            elif check_line == '3.1         // * estimated number of transactions per second after that timestamp':
                check_line = '0'

            chainparams_dest.write(check_line + "\n")

if __name__ == "__main__":
    #clone_genesish0()
    #clone_bitcoin()
    #setup_genesish0()
    #run_genesish0()
    merkle_hash, pszTimestamp, pubkey, time, bits, nonce, genesis_hash = get_genesis_params()
    modify_chainparams_cpp(merkle_hash, pszTimestamp, pubkey, time, bits, nonce, genesis_hash)
