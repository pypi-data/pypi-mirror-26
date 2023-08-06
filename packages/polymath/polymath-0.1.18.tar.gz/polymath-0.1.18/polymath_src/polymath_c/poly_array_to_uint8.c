/*
 * This file implements the function Poly_Array_to_uint64 from libpolymath.h
 */

#include "libpolymath.h"

uint8_t* Poly_Array_to_uint8(Poly_Array* poly)
{
    uint8_t* ret = malloc(sizeof(uint8_t) * (poly->deg + 1));
    if (ret) {
        uint64_t ctr = poly->deg;
        uint64_t mask = 1;
        for (size_t i = poly->len - 1; i < poly->len; i--) {
            for (size_t j = 0; j < UINT64_BITS; j++) {
                *(ret + ctr) = *(poly->poly + i) & mask;
                *(poly->poly + i) >>= 1;
                ctr--;
                if (ctr > poly->deg)
                    break;
            }
        }
    }
    return ret;
}
