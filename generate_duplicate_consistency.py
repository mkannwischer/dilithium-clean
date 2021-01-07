import os
import shutil
import subprocess
from pathlib import Path
TARGET_FOLDER = "../PQClean/test/duplicate_consistency/"


ALL_FILES = [
             # COMMON STUFF
             "api.h", "packing.c", "packing.h", "params.h", "sign.h", "symmetric.h",
             "ntt.h", "poly.c","poly.h", "polyvec.c", "polyvec.h", "rounding.c",
             "rounding.h" ,"sign.c",
             # AES STUFF
             "aes256ctr.c", "aes256ctr.h", "symmetric-aes.c",
             # AVX2 STUFF
             "alignment.h", "cdecl.inc", "consts.c", "consts.h", "invntt.S",
             "ntt.S", "pointwise.S", "rejsample.c", "rejsample.h", 
             "shuffle.inc",
             # CLEAN STUFF
             "ntt.c", "reduce.c", "reduce.h",
             # SHAKE STUFF
             "symmetric-shake.c",
             # SHAKE+AVX2 stuff
             "fips202x4.c", "fips202x4.h"
             ]

def hasFile(file, thisImpl, thisSymmetric):
    if file in ["api.h", "packing.c", "packing.h", "params.h", "sign.h",
                "symmetric.h", "ntt.h", "poly.c","poly.h", "polyvec.c",
                "polyvec.h", "rounding.c","rounding.h"]:
        return True
    if thisSymmetric == "aes":
        if file in ["aes256ctr.c", "aes256ctr.h", "symmetric-aes.c"]:
            return True
    else:
        if file in ["symmetric-shake.c"]:
            return True
        if thisImpl == "avx2":
            if file in ["fips202x4.c", "fips202x4.h"]:
                return True

    if thisImpl == "avx2":
        if file in ["alignment.h", "cdecl.inc", "consts.c", "consts.h", "invntt.S",
             "ntt.S", "pointwise.S",  "rejsample.c", "rejsample.h", "shuffle.inc", "sign.c"]:
             return True
    else:
        if file in ["ntt.c", "reduce.c", "reduce.h"]:
            return True
    return False

def isEqual(fileName, implEqual, symmetricEqual, randomizedEqual, paramEqual, impl):
    if fileName == "api.h":
        return symmetricEqual and randomizedEqual and paramEqual
    if fileName in ["packing.c", "packing.h", "sign.h", "ntt.c", "reduce.c", "reduce.h"]:
        return True
    if fileName in ["symmetric.h"]:
        return symmetricEqual
    if fileName in ["aes256ctr.c", "aes256ctr.h", "symmetric-aes.c", 
                    "fips202x4.c", "fips202x4.h", "symmetric-shake.c"]:
        return symmetricEqual and implEqual

    if fileName in ["polyvec.h"]:
        if impl == "avx2":
            return implEqual and symmetricEqual
        else:
            return implEqual

    if fileName in ["poly.h", "polyvec.c"]:
        if impl == "avx2":
            return symmetricEqual and implEqual and paramEqual
        else:
            return implEqual and paramEqual

    if fileName in ["alignment.h", "cdecl.inc", "consts.c", "consts.h", "invntt.S",
             "ntt.h", "ntt.S",
             "rejsample.h",
             "rounding.h" , "shuffle.inc"]:
        return implEqual

    if fileName in ["sign.c"]:
        if impl == "avx2":
            return symmetricEqual and implEqual and randomizedEqual and paramEqual
        else:
            return randomizedEqual

    if fileName in ["poly.c", "rejsample.c"]:
        if impl == "avx2":
            return implEqual and paramEqual and symmetricEqual
        else:
            return paramEqual and implEqual

    if fileName in ["pointwise.S", "rounding.c"]:
        return implEqual and paramEqual

    return False


def genCheck(thisImpl, thisSymmetric, thisRandomized, thisParam,
                                         impl, symmetric, randomized, param):
    if thisImpl == impl and thisSymmetric == symmetric and thisRandomized == randomized and thisParam == param:
        return None

    paramName = f"dilithium{param}"
    if symmetric == "aes":
        paramName += "-AES"
    if randomized:
        paramName += "-R"
    check =   "  - source:\n"
    check += f"      scheme: {paramName}\n"
    check += f"      implementation: {impl}\n"
    check +=  "    files:\n"
    for file in ALL_FILES:
        if hasFile(file, thisImpl, thisSymmetric) and hasFile(file, impl, symmetric):
            if isEqual(file, impl == thisImpl, symmetric == thisSymmetric,
                    randomized == thisRandomized, param == thisParam, impl):
                check +=  f"      - {file}\n"
    return check

def genFile(thisImpl, thisSymmetric, thisRandomized, thisParam):
    paramName = f"dilithium{thisParam}"
    if thisSymmetric == "aes":
        paramName += "-AES"
    if thisRandomized:
        paramName += "-R"
    fileName = f"{paramName}_{thisImpl}.yml"

    with open(TARGET_FOLDER+fileName, "w") as file:
        file.write("consistency_checks:\n")

        for impl in ["clean", "avx2"]:
            for symmetric in ["shake", "aes"]:
                for randomized in [False, True]:
                    for param in [2, 3, 5]:
                        check = genCheck(thisImpl, thisSymmetric, thisRandomized, thisParam,
                                         impl, symmetric, randomized, param)
                        if check:
                            file.write(check)


for impl in ["clean", "avx2"]:
    for symmetric in ["shake", "aes"]:
        for randomized in [False, True]:
            for param in [2, 3, 5]:
                genFile(impl, symmetric, randomized, param)