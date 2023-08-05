#ifndef CGRACIO_SPLITBBOX_H_   /* Include guard */
#define CGRACIO_SPLITBBOX_H_

#include "twoth.h"


typedef struct {
    float_ti *merge;
    float_ti *sigma;
    size_t s_buf;
    size_t bins;
    size_t shape[2];
    size_t strides[2];
} bbox_results;


bbox_results* bbox_integrate(integration* intg, float_ti* image, float_ti azmin, float_ti azmax);
void destroy_results(bbox_results *res);

#endif /* CGRACIO_SPLITBBOX_H_ */
