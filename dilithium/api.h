#ifndef PQCLEAN_NAMESPACE_API_H
#define PQCLEAN_NAMESPACE_API_H

#include <stddef.h>
#include <stdint.h>

#ifdef DILITHIUM_RANDOMIZED_SIGNING
#if DILITHIUM_MODE == 2
    #ifdef DILITHIUM_USE_AES
    #define PQCLEAN_NAMESPACE_CRYPTO_ALGNAME "Dilithium2-AES-R"
    #else 
    #define PQCLEAN_NAMESPACE_CRYPTO_ALGNAME "Dilithium2-R"
    #endif
#elif DILITHIUM_MODE == 3
    #ifdef DILITHIUM_USE_AES
    #define PQCLEAN_NAMESPACE_CRYPTO_ALGNAME "Dilithium3-AES-R"
    #else 
    #define PQCLEAN_NAMESPACE_CRYPTO_ALGNAME "Dilithium3-R"
    #endif
#elif DILITHIUM_MODE == 5
    #ifdef DILITHIUM_USE_AES
    #define PQCLEAN_NAMESPACE_CRYPTO_ALGNAME "Dilithium5-AES-R"
    #else 
    #define PQCLEAN_NAMESPACE_CRYPTO_ALGNAME "Dilithium5-R"
    #endif
#endif
#else
#if DILITHIUM_MODE == 2
    #ifdef DILITHIUM_USE_AES
    #define PQCLEAN_NAMESPACE_CRYPTO_ALGNAME "Dilithium2-AES"
    #else 
    #define PQCLEAN_NAMESPACE_CRYPTO_ALGNAME "Dilithium2"
    #endif
#elif DILITHIUM_MODE == 3
    #ifdef DILITHIUM_USE_AES
    #define PQCLEAN_NAMESPACE_CRYPTO_ALGNAME "Dilithium3-AES"
    #else 
    #define PQCLEAN_NAMESPACE_CRYPTO_ALGNAME "Dilithium3"
    #endif
#elif DILITHIUM_MODE == 5
    #ifdef DILITHIUM_USE_AES
    #define PQCLEAN_NAMESPACE_CRYPTO_ALGNAME "Dilithium5-AES"
    #else 
    #define PQCLEAN_NAMESPACE_CRYPTO_ALGNAME "Dilithium5"
    #endif
#endif
#endif

#if DILITHIUM_MODE == 2
#define PQCLEAN_NAMESPACE_CRYPTO_PUBLICKEYBYTES 1312
#define PQCLEAN_NAMESPACE_CRYPTO_SECRETKEYBYTES 2544
#define PQCLEAN_NAMESPACE_CRYPTO_BYTES 2420

#elif DILITHIUM_MODE == 3
#define PQCLEAN_NAMESPACE_CRYPTO_PUBLICKEYBYTES 1952
#define PQCLEAN_NAMESPACE_CRYPTO_SECRETKEYBYTES 4016
#define PQCLEAN_NAMESPACE_CRYPTO_BYTES 3293

#elif DILITHIUM_MODE == 5
#define PQCLEAN_NAMESPACE_CRYPTO_PUBLICKEYBYTES 2592
#define PQCLEAN_NAMESPACE_CRYPTO_SECRETKEYBYTES 4880
#define PQCLEAN_NAMESPACE_CRYPTO_BYTES 4595
#endif

int PQCLEAN_NAMESPACE_crypto_sign_keypair(uint8_t *pk, uint8_t *sk);


int PQCLEAN_NAMESPACE_crypto_sign(uint8_t *sm, size_t *smlen,
                const uint8_t *msg, size_t len,
                const uint8_t *sk);

int PQCLEAN_NAMESPACE_crypto_sign_open(uint8_t *m, size_t *mlen,
                     const uint8_t *sm, size_t smlen,
                     const uint8_t *pk);

int PQCLEAN_NAMESPACE_crypto_sign_signature(uint8_t *sig, size_t *siglen,
                          const uint8_t *m, size_t mlen,
                          const uint8_t *sk);

int PQCLEAN_NAMESPACE_crypto_sign_verify(const uint8_t *sig, size_t siglen,
                       const uint8_t *m, size_t mlen,
                       const uint8_t *pk);

#endif
