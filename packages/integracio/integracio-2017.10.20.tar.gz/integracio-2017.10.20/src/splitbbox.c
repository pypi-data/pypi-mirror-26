#include <stdlib.h>
#include <math.h>
#include "twoth.h"
#include "splitbbox.h"


void destroy_results(bbox_results *res)
{
    if (res) {
        if (res->merge) {
            free(res->merge);
            res->merge = NULL;
            res->sigma = NULL;
        }
        free(res);
        res = NULL;
    }
}


static bbox_results *init_results(integration *intg)
{
    bbox_results *res;

    res = malloc(sizeof(bbox_results));
    if (!res)
        return NULL;
    res->merge = calloc(intg->pos->bins * 2, sizeof(float_ti));
    if (res->merge == NULL) {
        destroy_results(res);
        return NULL;
    }
    res->sigma = res->merge + intg->pos->bins;
    res->bins = intg->pos->py_bins;
    res->s_buf = res->bins * sizeof(float_ti);
    res->shape[0] = 2;
    res->shape[1] = res->bins;
    res->strides[0] = (size_t)res->s_buf;
    res->strides[1] = (size_t)sizeof(float_ti);
    return res;
}


static float_ti get_bin_number(float_ti x0, float_ti pos0_min, float_ti delta)
{
    return (x0 - pos0_min) / delta;
}


bbox_results *bbox_integrate(integration *intg, float_ti *image, float_ti azmin, float_ti azmax)
{
    int i, j, bin0_max, bin0_min, check_azimuth;
    float_ti deltaA, deltaL, deltaR, fbin0_min, fbin0_max, *count, *sum, merge, sigma;
    bbox_results *res;

    res = init_results(intg);
    if (res == NULL) {
        destroy_results(res);
        return NULL;
    }

    count = res->merge;
    sum = res->sigma;
    check_azimuth = 0;
    if (azmin != azmax) {
        check_azimuth = 1;
        if (azmin > 180)
            azmin -= 360;
        if (azmax > 180)
            azmax -= 360;
        azmin *= D2R;
        azmax *= D2R;
        if (azmax < azmin)
            azmax += M_PI2;
    }

    for (i=0; i<intg->pos->s_array; i++) {

        if (image[i] < 0) /* intensity is unreasonable */
            continue;

        if (check_azimuth && (intg->pos->azl[i] < azmin || intg->pos->azu[i] > azmax))
            continue;

        fbin0_min = get_bin_number(intg->pos->lower[i], intg->pos->min, intg->pos->delta);
        fbin0_max = get_bin_number(intg->pos->upper[i], intg->pos->min, intg->pos->delta);
        if (fbin0_max < 0 || fbin0_min >= intg->pos->bins)
            continue;
        if (fbin0_max >= intg->pos->bins)
            bin0_max = intg->pos->bins - 1;
        else
            bin0_max = (int)fbin0_max;
        if (fbin0_min < 0)
            bin0_min = 0;
        else
            bin0_min = (int)fbin0_min;

        /* probably, apply corrections here */
        if (intg->pos->use_sa)
            image[i] /= intg->pos->sa[i];

        if (intg->pos->use_pol)
            image[i] /= intg->pos->pol[i];
        /* corrections are done? */

        if (bin0_min == bin0_max) {
            /* All pixel is within a single bin */
            count[bin0_min]++;
            sum[bin0_min] += image[i];
        } else {
            /* we have a pixel splitting */
            deltaA = 1 / (fbin0_max - fbin0_min);
            deltaL = (float_ti)bin0_min + 1 - fbin0_min;
            deltaR = fbin0_max - (float_ti)bin0_max;
            count[bin0_min] += deltaA * deltaL;
            sum[bin0_min] += image[i] * deltaA * deltaL;
            count[bin0_max] += deltaA * deltaR;
            sum[bin0_max] += image[i] * deltaA * deltaR;
            if (bin0_min + 1 < bin0_max)
                for (j=bin0_min+1; j<bin0_max; j++) {
                    count[j] += deltaA;
                    sum[j] += image[i] * deltaA;
                }
        }
    }

    for (j=0; j<intg->pos->bins; j++)
        if (count[j] > 0) {
            merge = sum[j] / count[j];
            sigma = sqrt(sum[j]) / count[j];
            res->merge[j] = merge;
            res->sigma[j] = sigma;
        }
    return res;
}
