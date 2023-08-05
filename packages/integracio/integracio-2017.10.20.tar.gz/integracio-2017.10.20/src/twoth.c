#include <stdlib.h>
#include <math.h>
#include "twoth.h"


typedef struct {
    float_ti s1;
    float_ti s2;
    float_ti s3;
    float_ti c1;
    float_ti c2;
    float_ti c3;
    float_ti c2c3;
    float_ti c3s1s2;
    float_ti c1s3;
    float_ti c1c3s2;
    float_ti s1s3;
    float_ti c2s3;
    float_ti c1c3;
    float_ti s1s2s3;
    float_ti c3s1;
    float_ti c1s2s3;
    float_ti c2s1;
    float_ti c1c2;
    float_ti dt1;
    float_ti dt2;
    float_ti dt3;
    float_ti c3s1s2c1s3;
    float_ti c1c3s1s2s3;
    float_ti pp1;
    float_ti pp2;
    float_ti dist2;
    float_ti tth2q;
    enum units_t units;
} geotri;


static int init_aux(integration *intg)
{
    char *mem;
    float_ti *m;
    size_t i;

    intg->crn->s_array = (intg->pos->dim1 + 1) * (intg->pos->dim2 + 1);
    intg->crn->s_buf = intg->crn->s_array * sizeof(float_ti);

    mem = malloc(intg->crn->s_buf * 2 + intg->pos->s_buf * 10);
    if (!mem)
        return 0;

    intg->pos->tth = (float_ti *)mem;
    intg->pos->chi = intg->pos->tth + intg->pos->s_array;
    intg->crn->_dtth = intg->pos->chi + intg->pos->s_array;
    intg->crn->_dchi = intg->crn->_dtth + intg->crn->s_array;

    m = intg->crn->_dtth + intg->crn->s_array * 2;
    for (i=0; i<4; ++i) {
        intg->crn->tth[i]       = intg->pos->tth;
        intg->crn->chi[i]       = intg->pos->chi;
        intg->crn->dtth[i]      = intg->crn->_dtth;
        intg->crn->dchi[i]      = intg->crn->_dchi;
        intg->crn->deltatth[i]  = m + intg->pos->s_array * i;
        intg->crn->deltachi[i]  = m + intg->pos->s_array * 4 + intg->pos->s_array * i;
        intg->crn->_deltatth[i] = intg->crn->deltatth[i];
        intg->crn->_deltachi[i] = intg->crn->deltachi[i];
    }
    return 1;
}


static int init_positions(integration *intg, geometry *geo)
{
    char *mem;

    intg->pos->s_array = intg->pos->dim1 * intg->pos->dim2;
    intg->pos->s_buf = sizeof(float_ti) * intg->pos->s_array;
    if (geo->bins > 0)
        intg->pos->bins = geo->bins;
    else
        intg->pos->bins = (intg->pos->dim1 >= intg->pos->dim2 ? intg->pos->dim1 : intg->pos->dim2) * 2;
    intg->pos->py_bins = (size_t)intg->pos->bins;
    intg->pos->s_pos = sizeof(float_ti) * intg->pos->bins;
    intg->pos->min = 0;
    intg->pos->max = 0;
    intg->pos->use_sa = geo->sa;
    intg->pos->use_pol = (geo->pol >= -1 && geo->pol <= 1) ? 1 : 0;

    mem = malloc(intg->pos->s_buf * 6 + intg->pos->s_pos);
    if (!mem)
        return 0;

    intg->pos->lower = (float_ti *)mem;
    intg->pos->upper = intg->pos->lower + intg->pos->s_array;
    intg->pos->azl = intg->pos->upper + intg->pos->s_array;
    intg->pos->azu = intg->pos->azl + intg->pos->s_array;
    intg->pos->sa = intg->pos->azu + intg->pos->s_array;
    intg->pos->pol = intg->pos->sa + intg->pos->s_array;
    intg->pos->pos = intg->pos->pol + intg->pos->s_array;
    return 1;
}


static void destroy_aux(integration *intg)
{
    if (intg && intg->pos && intg->pos->tth) {
        free(intg->pos->tth);
        intg->pos->tth = NULL;
        intg->pos->chi = NULL;
        intg->crn->_dtth = NULL;
        intg->crn->_dchi = NULL;
    }
}


void destroy_integration(integration *intg)
{
    destroy_aux(intg);
    if (intg) {
        if (intg->pos && intg->pos->lower) {
            free(intg->pos->lower);
            intg->pos->lower = NULL;
            intg->pos->upper = NULL;
            intg->pos->azl = NULL;
            intg->pos->azu = NULL;
            intg->pos->sa = NULL;
            intg->pos->pos = NULL;
            intg->pos->pol = NULL;
        }
        free(intg);
        intg = NULL;
    }
}


static integration *init_integration(int dim1, int dim2, geometry *geo)
{
    char *mem;
    integration *intg;

    mem = malloc(
        sizeof(integration) +
        sizeof(positions)   +
        sizeof(corners)
    );
    if (!mem)
        return NULL;

    intg = (integration *)mem;
    intg->pos = (positions *)(intg + 1);
    intg->crn = (corners *)(intg->pos + 1);

    intg->pos->dim1 = dim1;
    intg->pos->dim2 = dim2;

    if (!init_positions(intg, geo) || !init_aux(intg)) {
        destroy_integration(intg);
        return NULL;
    }
    return intg;
}


static void calc_sincos(geometry *geo, geotri *geo3)
{
    geo3->c1 = cos(geo->rot1);
    geo3->c2 = cos(geo->rot2);
    geo3->c3 = cos(geo->rot3);
    geo3->s1 = sin(geo->rot1);
    geo3->s2 = sin(geo->rot2);
    geo3->s3 = sin(geo->rot3);
    geo3->c2c3 = geo3->c2 * geo3->c3;
    geo3->c3s1s2 = geo3->c3 * geo3->s1 * geo3->s2;
    geo3->c1s3 = geo3->c1 * geo3->s3;
    geo3->c1c3s2 = geo3->c1 * geo3->c3 * geo3->s2;
    geo3->s1s3 = geo3->s1 * geo3->s3;
    geo3->c2s3 = geo3->c2 * geo3->s3;
    geo3->c1c3 = geo3->c1 * geo3->c3;
    geo3->s1s2s3 = geo3->s1 * geo3->s2 * geo3->s3;
    geo3->c3s1 = geo3->c3 * geo3->s1;
    geo3->c1s2s3 = geo3->c1 * geo3->s2 * geo3->s3;
    geo3->c2s1 = geo3->c2 * geo3->s1;
    geo3->c1c2 = geo3->c1 * geo3->c2;
    geo3->dt1 = geo->distance * (geo3->c1c3s2 + geo3->s1s3);
    geo3->dt2 = geo->distance * (geo3->c3s1 - geo3->c1s2s3);
    geo3->dt3 = geo->distance * geo3->c1c2;
    geo3->c3s1s2c1s3 = geo3->c3s1s2 - geo3->c1s3;
    geo3->c1c3s1s2s3 = geo3->c1c3 + geo3->s1s2s3;
    geo3->pp1 = geo->pixelsize1 * 0.5 - geo->poni1;
    geo3->pp2 = geo->pixelsize2 * 0.5 - geo->poni2;
    geo3->dist2 = geo->distance * geo->distance;
    geo3->tth2q = 4e-9 * M_PI / geo->wavelength;
    geo3->units = geo->units;
}


static void calc_part(size_t i, corners *crn)
{
    *crn->deltatth[i] = fabs(*crn->dtth[i] - *crn->tth[i]);
    *crn->deltachi[i] = fmod(fabsf(*crn->dchi[i] - *crn->chi[i]), M_PI2);
    crn->deltatth[i]++; crn->dtth[i]++; crn->tth[i]++;
    crn->deltachi[i]++; crn->dchi[i]++; crn->chi[i]++;
}


static void calc_corners(integration *intg, size_t i, size_t j)
{
    if (i == 0 || j == 0) {
        intg->crn->dtth[2]++;
        intg->crn->dchi[2]++;
    } else {
        calc_part(2, intg->crn);
    }
    if (i == 0 || j == intg->pos->dim2) {
        intg->crn->dtth[1]++;
        intg->crn->dchi[1]++;
    } else {
        calc_part(1, intg->crn);
    }
    if (i == intg->pos->dim1 || j == 0) {
        intg->crn->dtth[3]++;
        intg->crn->dchi[3]++;
    } else {
        calc_part(3, intg->crn);
    }
    if (i == intg->pos->dim1 || j == intg->pos->dim2) {
        intg->crn->dtth[0]++;
        intg->crn->dchi[0]++;
    } else {
        calc_part(0, intg->crn);
    }
}


static void calc_bins(integration *intg, geometry *geo)
{
    int i, j, radial = 0;
    float_ti max0, min0, delta, start, stop, maxdtth, maxdchi, m;

    if (geo->radmax != geo->radmin) {
        m = geo->units == tth ? D2R : 1.0;
        intg->pos->max = geo->radmax * m;
        intg->pos->min = geo->radmin * m;
        radial = 1;
    }

    for (i=0; i<intg->pos->s_array; i++) {
        maxdtth = intg->crn->_deltatth[0][i];
        maxdchi = intg->crn->_deltachi[0][i];
        for (j=1; j<4; j++) {
            if (maxdtth < intg->crn->_deltatth[j][i])
                maxdtth = intg->crn->_deltatth[j][i];
            if (maxdchi < intg->crn->_deltachi[j][i])
                maxdchi = intg->crn->_deltachi[j][i];
        }
        min0 = intg->pos->tth[i] - maxdtth;
        max0 = intg->pos->tth[i] + maxdtth;
        intg->pos->upper[i] = max0;
        intg->pos->lower[i] = min0;
        intg->pos->azl[i] = intg->pos->chi[i] + maxdchi;
        intg->pos->azu[i] = intg->pos->chi[i] - maxdchi;
        if (!radial) {
            if (max0 > intg->pos->max)
                intg->pos->max = max0;
            if (min0 < intg->pos->min && min0 >= 0)
                intg->pos->min = min0;

        }
    }

    intg->pos->delta = (intg->pos->max - intg->pos->min) / intg->pos->bins;
    start = intg->pos->min + 0.5 * intg->pos->delta;
    stop  = intg->pos->max - 0.5 * intg->pos->delta;
    delta = (stop - start) / (intg->pos->bins - 1);
    for (i=0; i<intg->pos->bins; i++) {
        intg->pos->pos[i] = start + delta * i;
        if (geo->units == tth)
            intg->pos->pos[i] *= R2D;
    }
}


static float_ti tth2q(float_ti value, geotri *geo3)
{
    return geo3->units == q ? geo3->tth2q * sin(0.5 * value) : value;
}


static void calc_pos(integration *intg, geometry *geo, geotri *geo3)
{
    int i, j;
    float_ti p1, p2, t1, t2, t3, t11, t21, t31, dp1, dp2, *dtth, *dchi, *pol;
    float_ti dt11, dt21, dt31, dt1, dt2, dt3, p1i, p2j, p11, *tth, *sa, *chi, ctth;

    tth = intg->pos->tth;
    sa = intg->pos->sa;
    chi = intg->pos->chi;
    pol = intg->pos->pol;
    dtth = intg->crn->_dtth;
    dchi = intg->crn->_dchi;
    t11 = 0; t21 = 0; t31 = 0;
    for (i=0; i<=intg->pos->dim1; i++) {
        p1i = geo->pixelsize1 * i;
        p1 = p1i + geo3->pp1;
        p11 = geo3->dist2 + p1 * p1;
        dp1 = p1i - geo->poni1;
        t11 = p1 * geo3->c2c3 - geo3->dt1;
        dt11 = dp1 * geo3->c2c3 - geo3->dt1;
        t21 = p1 * geo3->c2s3 + geo3->dt2;
        dt21 = dp1 * geo3->c2s3 + geo3->dt2;
        t31 = p1 * geo3->s2 + geo3->dt3;
        dt31 = dp1 * geo3->s2 + geo3->dt3;
        for (j=0; j<=intg->pos->dim2; j++) {
            p2j = geo->pixelsize2 * j;
            p2 = p2j + geo3->pp2;
            dp2 = p2j - geo->poni2;
            t1 = t11 + p2 * geo3->c3s1s2c1s3;
            dt1 = dt11 + dp2 * geo3->c3s1s2c1s3;
            t2 = t21 + p2 * geo3->c1c3s1s2s3;
            dt2 = dt21 + dp2 * geo3->c1c3s1s2s3;
            t3 = t31 - p2 * geo3->c2s1;
            dt3 = dt31 - dp2 * geo3->c2s1;
            *dtth++ = tth2q(atan2(sqrt(dt1 * dt1 + dt2 * dt2), dt3), geo3);
            *dchi++ = atan2(dt1, dt2);
            if (i != intg->pos->dim1 && j != intg->pos->dim2) {
                *sa++ = pow(geo->distance / sqrt(p11 + p2 * p2), DSA_ORDER);
                *tth = atan2(sqrt(t1 * t1 + t2 * t2), t3);
                *chi = atan2(t1, t2);
                ctth = pow(cos(*tth), 2);
                *pol++ = 0.5 * (1. + ctth - geo->pol * cos(2. * *chi) * (1. - ctth));
                *tth = tth2q(*tth, geo3);
                chi++;
                tth++;
            }
            calc_corners(intg, i, j);
        }
    }
}


integration *calculate_positions(int dim1, int dim2, geometry *geo)
{
    integration *intg;
    geotri geo3;

    intg = init_integration(dim1, dim2, geo);
    if (intg == NULL)
        return NULL;
    calc_sincos(geo, &geo3);
    calc_pos(intg, geo, &geo3);
    calc_bins(intg, geo);
    destroy_aux(intg);
    return intg;
}
