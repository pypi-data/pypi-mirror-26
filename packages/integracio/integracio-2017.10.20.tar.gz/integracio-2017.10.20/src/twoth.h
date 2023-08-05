#ifndef CGRACIO_TWOTHETA_H_   /* Include guard */
#define CGRACIO_TWOTHETA_H_


#ifndef M_PI
#define M_PI       3.14159265358979323846
#endif  /* M_PI */
#define DSA_ORDER  3.0  /* by default we correct for 1/cos(2th), fit2d corrects for 1/cos^3(2th) */
#define R2D        180.0 / M_PI
#define D2R        M_PI / 180.0
#define M_PI2      2.0 * M_PI


#define QUOTE(name)       #name
#define STR(macro)        QUOTE(macro)
#define PPCAT_NX(A, B)    A ## B
#define PPCAT(A, B)       PPCAT_NX(A, B)
#define FLOAT_ID          f
#define DOUBLE_ID         d


#if !defined(USE_FLOATS) && !defined(USE_DOUBLES)
#define USE_FLOATS
#endif /* !defined(USE_FLOATS) && !defined(USE_DOUBLES) */


#ifdef USE_FLOATS
typedef float float_ti;
#define FLOAT_TYPE        FLOAT_ID
#endif /* USE_FLOATS */

#ifdef USE_DOUBLES
typedef double float_ti;
#define FLOAT_TYPE        DOUBLE_ID
#endif /* USE_DOUBLES */

#define SO_NAME           _cgracio
#define TP_NAME           STR(SO_NAME) "_" STR(FLOAT_TYPE)
#define TP_NAME_CGRACIO   TP_NAME "._integration"
#define TP_NAME_RESULTS   TP_NAME "._results"
#define TP_NAME_ERROR     TP_NAME ".Error"
#define MODULE_NAME       PPCAT(PPCAT(PPCAT(PyInit_, SO_NAME), _), FLOAT_TYPE)
#define EXPORT_TYPE       STR(FLOAT_TYPE)
#define IMPORT_TYPE       "OO" STR(FLOAT_TYPE) STR(FLOAT_TYPE)


enum units_t {tth, q};


typedef struct {
    float_ti distance;
    float_ti poni1;
    float_ti poni2;
    float_ti pixelsize1;
    float_ti pixelsize2;
    float_ti rot1;
    float_ti rot2;
    float_ti rot3;
    float_ti wavelength;
    enum units_t units;
    float_ti radmin;
    float_ti radmax;
    float_ti pol;
    int sa;
    int bins;
} geometry;


typedef struct {
    int dim1;
    int dim2;
    int s_array;
    int s_buf;
    float_ti *tth;
    float_ti *sa;
    float_ti *chi;
    float_ti *upper;
    float_ti *lower;
    float_ti *pos;
    int bins;
    size_t py_bins;
    int s_pos;
    float_ti min;
    float_ti max;
    float_ti delta;
    float_ti *azl;
    float_ti *azu;
    int use_sa;
    int use_pol;
    float_ti *pol;
} positions;


typedef struct {
    float_ti *tth[4];
    float_ti *chi[4];
    float_ti *deltatth[4];
    float_ti *_deltatth[4];
    float_ti *deltachi[4];
    float_ti *_deltachi[4];
    float_ti *dtth[4];
    float_ti *dchi[4];
    float_ti *_dchi;
    float_ti *_dtth;
    int s_array;
    int s_buf;
} corners;


typedef struct {
    positions *pos;
    corners *crn;
} integration;


integration *calculate_positions(int dim1, int dim2, geometry *geo);
void destroy_integration(integration *intg);

#endif /* CGRACIO_TWOTHETA_H_ */
