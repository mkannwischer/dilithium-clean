#ifndef ROUNDING_H
#define ROUNDING_H

#include "params.h"
#include <stdint.h>

#define power2round_avx DILITHIUM_NAMESPACE(_power2round_avx)
void power2round_avx(__m256i a1[N/8], __m256i a0[N/8], const __m256i a[N/8]);
#define decompose_avx DILITHIUM_NAMESPACE(_decompose_avx)
void decompose_avx(__m256i a1[N/8], __m256i a0[N/8], const __m256i a[N/8]);
#define make_hint_avx DILITHIUM_NAMESPACE(_make_hint_avx)
unsigned int make_hint_avx(__m256i h[N/8], const __m256i a0[N/8], const __m256i a1[N/8]);
#define use_hint_avx DILITHIUM_NAMESPACE(_use_hint_avx)
void use_hint_avx(__m256i b[N/8], const __m256i a[N/8], const __m256i hint[N/8]);

#endif
