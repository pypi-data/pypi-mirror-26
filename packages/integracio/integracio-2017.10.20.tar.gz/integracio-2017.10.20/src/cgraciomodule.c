#include <Python.h>
#include "twoth.h"
#include "splitbbox.h"


typedef struct {
    PyObject_HEAD
    integration *intg;
} cgracio_integration;


static int cgracio_integration_init(cgracio_integration *self, PyObject *args)
{
    int dim1, dim2;
    Py_buffer geo;
    integration *intg;

    if (!PyArg_ParseTuple(args, "iiy*", &dim1, &dim2, &geo))
        return -1;

    if (geo.len != sizeof(geometry)) {
        PyErr_SetString(PyExc_TypeError, "The PONI geometry structure cannot be interpreted");
        return -1;
    }

    if (dim1 <= 0 || dim2 <= 0) {
        PyErr_SetString(PyExc_ValueError, "The dimensions cannot be less than zero");
        return -1;
    }

    destroy_integration(self->intg);
    Py_BEGIN_ALLOW_THREADS
    intg = calculate_positions(dim1, dim2, (geometry *)geo.buf);
    Py_END_ALLOW_THREADS
    if (intg == NULL) {
        PyErr_SetString(PyExc_MemoryError, "It seems that the memory cannot be allocated. Buy more RAM.");
        return -1;
    }
    self->intg = intg;
    return 0;
}


static void cgracio_integration_dealloc(cgracio_integration *self)
{
    destroy_integration(self->intg);
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static int cgracio_integration_getbuffer(PyObject *obj, Py_buffer *view, int flags)
{
    if (view == NULL) {
        PyErr_SetString(PyExc_ValueError, "NULL view in getbuffer");
        return -1;
    }

    cgracio_integration *self = (cgracio_integration *)obj;
    view->obj = (PyObject *)self;
    view->buf = (void *)self->intg->pos->pos;
    view->len = self->intg->pos->s_pos;
    view->readonly = 1;
    view->itemsize = sizeof(float_ti);
    view->format = EXPORT_TYPE;
    view->ndim = 1;
    view->shape = (Py_ssize_t *)&self->intg->pos->py_bins;
    view->strides = &view->itemsize;
    view->suboffsets = NULL;
    view->internal = NULL;

    Py_INCREF(self);  /* need to increase the reference count */
    return 0;
}


static PyBufferProcs cgracio_integration_as_buffer = {
  (getbufferproc)cgracio_integration_getbuffer,
  (releasebufferproc)0,
};


static PyTypeObject cgracio_integration_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    TP_NAME_CGRACIO,                            /* tp_name */
    sizeof(cgracio_integration),                /* tp_basicsize */
    0,                                          /* tp_itemsize */
    (destructor)cgracio_integration_dealloc,    /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_reserved */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash  */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    0,                                          /* tp_getattro */
    0,                                          /* tp_setattro */
    &cgracio_integration_as_buffer,             /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                         /* tp_flags */
    "_integration object",                      /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    0,                                          /* tp_iter */
    0,                                          /* tp_iternext */
    0,                                          /* tp_methods */
    0,                                          /* tp_members */
    0,                                          /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    (initproc)cgracio_integration_init,         /* tp_init */
};


typedef struct {
    PyObject_HEAD
    bbox_results *res;
} cgracio_results;


static int cgracio_results_init(cgracio_results *self, PyObject *args)
{
    float_ti azmin, azmax;
    PyObject *np_image;
    Py_buffer image;
    cgracio_integration *py_integration;
    bbox_results *results;

    if (!PyArg_ParseTuple(args, IMPORT_TYPE, &py_integration, &np_image, &azmin, &azmax))
        return -1;

    destroy_results(self->res);
    PyObject_GetBuffer(np_image, &image, PyBUF_C_CONTIGUOUS);
    if (image.len != py_integration->intg->pos->s_buf) {
        PyBuffer_Release(&image);
        PyErr_SetString(PyExc_ValueError, "The image has wrong dimensions");
        return -1;
    }

    Py_BEGIN_ALLOW_THREADS
    results = bbox_integrate(py_integration->intg, (float_ti *)image.buf, azmin, azmax);
    Py_END_ALLOW_THREADS
    PyBuffer_Release(&image);
    if (results == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Memory for integration cannot be allocated. Buy more RAM.");
        return -1;
    }
    self->res = results;
    return 0;
}


static int cgracio_results_getbuffer(PyObject *obj, Py_buffer *view, int flags)
{
    if (view == NULL) {
        PyErr_SetString(PyExc_ValueError, "NULL view in getbuffer");
        return -1;
    }

    cgracio_results *self = (cgracio_results *)obj;
    view->obj = (PyObject *)self;
    view->buf = (void *)self->res->merge;
    view->len = self->res->bins * 2 * sizeof(float_ti);
    view->readonly = 1;
    view->itemsize = sizeof(float_ti);
    view->format = EXPORT_TYPE;
    view->ndim = 2;
    view->shape = (Py_ssize_t *)self->res->shape;
    view->strides = (Py_ssize_t *)self->res->strides;
    view->suboffsets = NULL;
    view->internal = NULL;

    Py_INCREF(self);
    return 0;
}


static void cgracio_results_dealloc(cgracio_results *self)
{
    destroy_results(self->res);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyBufferProcs cgracio_results_as_buffer = {
  (getbufferproc)cgracio_results_getbuffer,
  (releasebufferproc)0,
};


static PyTypeObject cgracio_results_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    TP_NAME_RESULTS,                            /* tp_name */
    sizeof(cgracio_results),                    /* tp_basicsize */
    0,                                          /* tp_itemsize */
    (destructor)cgracio_results_dealloc,        /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_reserved */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash  */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    0,                                          /* tp_getattro */
    0,                                          /* tp_setattro */
    &cgracio_results_as_buffer,                 /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                         /* tp_flags */
    "_results object",                          /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    0,                                          /* tp_iter */
    0,                                          /* tp_iternext */
    0,                                          /* tp_methods */
    0,                                          /* tp_members */
    0,                                          /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    (initproc)cgracio_results_init,             /* tp_init */
    0,                                          /* tp_alloc */
    0,                                          /* tp_new */
};


static PyMethodDef cgracio_methods[] = {
    {NULL, NULL, 0, NULL}
};


struct module_state {
    PyObject *error;
};


#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))


static int cgracio_traverse(PyObject *m, visitproc visit, void *arg)
{
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}


static int cgracio_clear(PyObject *m)
{
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}


static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    TP_NAME,
    NULL,
    sizeof(struct module_state),
    cgracio_methods,
    NULL,
    cgracio_traverse,
    cgracio_clear,
    NULL
};


PyMODINIT_FUNC MODULE_NAME(void)
{
    PyObject *module;
    struct module_state *st;

    cgracio_integration_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(&cgracio_integration_type) < 0)
        return NULL;

    cgracio_results_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(&cgracio_results_type) < 0)
        return NULL;

    module = PyModule_Create(&moduledef);
    if (module == NULL)
        return NULL;
    st = GETSTATE(module);
    st->error = PyErr_NewException(TP_NAME_ERROR, NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&cgracio_integration_type);
    PyModule_AddObject(module, "_integration", (PyObject *)&cgracio_integration_type);

    Py_INCREF(&cgracio_results_type);
    PyModule_AddObject(module, "_results", (PyObject *)&cgracio_results_type);

    return module;
}
