import os
import shutil
import subprocess
from pathlib import Path
TARGET_FOLDER = "../PQClean/crypto_sign/"

params = [
    {'name': 'dilithium2', 'aes': False, 'def' : ['DILITHIUM_MODE=2', "GAMMA2=95232", "Q=8380417", "GAMMA1=131072",  "ETA=2"], 'undef' : ['DILITHIUM_USE_AES', 'DBENCH']},
    {'name': 'dilithium2-AES', 'aes': True, 'def' : ['DILITHIUM_MODE=2', "GAMMA2=95232", "Q=8380417", "GAMMA1=131072",  "ETA=2", 'DILITHIUM_USE_AES'], 'undef' : [ 'DBENCH']},

    {'name': 'dilithium3', 'aes': False, 'def' : ['DILITHIUM_MODE=3', "GAMMA2=261888", "Q=8380417", "GAMMA1=524288",  "ETA=4"], 'undef' : ['DILITHIUM_USE_AES', 'DBENCH']},
    {'name': 'dilithium3-AES', 'aes': True, 'def' : ['DILITHIUM_MODE=3', "GAMMA2=261888", "Q=8380417", "GAMMA1=524288",  "ETA=4", 'DILITHIUM_USE_AES'], 'undef' : ['DBENCH']},

    {'name': 'dilithium5', 'aes': False, 'def' : ['DILITHIUM_MODE=5', "GAMMA2=261888", "Q=8380417", "GAMMA1=524288",  "ETA=2"], 'undef' : ['DILITHIUM_USE_AES', 'DBENCH']},
    {'name': 'dilithium5-AES', 'aes': True, 'def' : ['DILITHIUM_MODE=5', "GAMMA2=261888", "Q=8380417", "GAMMA1=524288",  "ETA=2", 'DILITHIUM_USE_AES'], 'undef' : ['DBENCH']},
]

for param in params:
    for randomized in [True, False]:
        parameterSet = param['name']

        if randomized:
            parameterSet += "-R"
            param['def'].append("DILITHIUM_RANDOMIZED_SIGNING")
            if "DILITHIUM_RANDOMIZED_SIGNING" in param["undef"]:
                param['undef'].remove("DILITHIUM_RANDOMIZED_SIGNING")
        else:
            param['undef'].append("DILITHIUM_RANDOMIZED_SIGNING")
            if "DILITHIUM_RANDOMIZED_SIGNING" in param["def"]:
                param['def'].remove("DILITHIUM_RANDOMIZED_SIGNING")


        pqcleanDir = f"{TARGET_FOLDER}/{parameterSet}/clean/"

        # delete old files
        if Path(pqcleanDir).exists():
            shutil.rmtree(pqcleanDir)
        os.makedirs(pqcleanDir)

        nmspc = "PQCLEAN_"+parameterSet.upper().replace("-", "")+"_CLEAN"
        for f in os.listdir("dilithium"):
            # copy over common source files
            shutil.copyfile(f"dilithium/{f}", f"{pqcleanDir}/{f}")

            # namespace source files
            cmd = f"sed -i 's/PQCLEAN_NAMESPACE/{nmspc}/g' {pqcleanDir}/{f}"
            subprocess.call(cmd, shell=True)

            # remove preprocessor conditionals
            cmd = f"unifdef -m " + " ".join(["-D"+d for d in param['def']]) + " " + " ".join(["-U"+d for d in param['undef']]) +  f" {pqcleanDir}/{f}"
            print(cmd)
            subprocess.call(cmd, shell=True)


        if param['aes']:
            symmetric = "dilithium-aes"
        else:
            symmetric = "dilithium-shake"

        for f in os.listdir(symmetric):
            # copy over common source files
            shutil.copyfile(f"{symmetric}/{f}", f"{pqcleanDir}/{f}")

            # namespace source files
            cmd = f"sed -i 's/PQCLEAN_NAMESPACE/{nmspc}/g' {pqcleanDir}/{f}"
            subprocess.call(cmd, shell=True)

            # remove preprocessor conditionals
            cmd = f"unifdef -m " + " ".join(["-D"+d for d in param['def']]) + " " + " ".join(["-U"+d for d in param['undef']]) +  f" {pqcleanDir}/{f}"
            print(cmd)
            subprocess.call(cmd, shell=True)


        # copy over Makefiles
        for f in os.listdir(f"{symmetric}-make"):
            shutil.copyfile(f"{symmetric}-make/{f}", f"{pqcleanDir}/{f}")

            # replace lib name
            cmd = f"sed -i 's/SCHEME_NAME/{parameterSet}/g' {pqcleanDir}/{f}"
            subprocess.call(cmd, shell=True)

        # run astyle to fix formatting due to namespace
        cmd = f"astyle --project {pqcleanDir}/*.[ch]"
        subprocess.call(cmd, shell=True)
