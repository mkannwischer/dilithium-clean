import os
import shutil
import subprocess
from pathlib import Path
TARGET_FOLDER = "../PQClean/crypto_sign/"

params = [
    {'name': 'dilithium2', 'aes': False, 'def' : ['DILITHIUM_MODE=2', "GAMMA2=95232", "Q=8380417", "GAMMA1=131072",  "ETA=2", "K=4","L=4"], 'undef' : ['DILITHIUM_USE_AES', 'DBENCH']},
    {'name': 'dilithium2-AES', 'aes': True, 'def' : ['DILITHIUM_MODE=2', "GAMMA2=95232", "Q=8380417", "GAMMA1=131072",  "ETA=2", "K=4", "L=4", 'DILITHIUM_USE_AES'], 'undef' : [ 'DBENCH']},

    {'name': 'dilithium3', 'aes': False, 'def' : ['DILITHIUM_MODE=3', "GAMMA2=261888", "Q=8380417", "GAMMA1=524288",  "ETA=4", "K=6", "L=5"], 'undef' : ['DILITHIUM_USE_AES', 'DBENCH']},
    {'name': 'dilithium3-AES', 'aes': True, 'def' : ['DILITHIUM_MODE=3', "GAMMA2=261888", "Q=8380417", "GAMMA1=524288",  "ETA=4", "K=6", "L=5", 'DILITHIUM_USE_AES'], 'undef' : ['DBENCH']},

    {'name': 'dilithium5', 'aes': False, 'def' : ['DILITHIUM_MODE=5', "GAMMA2=261888", "Q=8380417", "GAMMA1=524288",  "ETA=2", "K=8", "L=7"], 'undef' : ['DILITHIUM_USE_AES', 'DBENCH']},
    {'name': 'dilithium5-AES', 'aes': True, 'def' : ['DILITHIUM_MODE=5', "GAMMA2=261888", "Q=8380417", "GAMMA1=524288",  "ETA=2", "K=8", "L=7", 'DILITHIUM_USE_AES'], 'undef' : ['DBENCH']},
]

for param in params:
    for randomized in [True, False]:
        for implementation in ["clean", "avx2"]:

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


            pqcleanDir = f"{TARGET_FOLDER}/{parameterSet}/{implementation}/"

            # delete old files
            if Path(pqcleanDir).exists():
                shutil.rmtree(pqcleanDir)
            os.makedirs(pqcleanDir)

            nmspc = "PQCLEAN_"+parameterSet.upper().replace("-", "")+f"_{implementation.upper()}"

            for dir in [f"dilithium-{implementation}", "dilithium-common"]:
                for f in os.listdir(dir):
                    # copy over common source files
                    shutil.copyfile(f"{dir}/{f}", f"{pqcleanDir}/{f}")

                    # namespace source files
                    cmd = f"sed -i 's/PQCLEAN_NAMESPACE/{nmspc}/g' {pqcleanDir}/{f}"
                    subprocess.call(cmd, shell=True)

                    # remove preprocessor conditionals
                    cmd = f"unifdef -m " + " ".join(["-D"+d for d in param['def']]) + " " + " ".join(["-U"+d for d in param['undef']]) +  f" {pqcleanDir}/{f}"
                    print(cmd)
                    subprocess.call(cmd, shell=True)


            if param['aes']:
                symmetric = f"dilithium-aes-{implementation}"
            else:
                symmetric = f"dilithium-shake-{implementation}"

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
