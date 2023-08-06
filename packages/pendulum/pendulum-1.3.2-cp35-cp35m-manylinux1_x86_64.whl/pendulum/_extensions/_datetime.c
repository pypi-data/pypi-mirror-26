
#include <Python.h>
#include <structmember.h>

#define MIN_YEAR 0
#define MAX_YEAR 9999

/*
 * class DateTime():
 */
typedef struct {
    PyObject_HEAD
    int year;
    int month;
    int day;
    int hour;
    int minute;
    int second;
    int microsecond;
} DateTime;


/*
 * def __init__(self, years, months, days, hours, minutes, seconds, microseconds):
 *     self.years = years
 *     # ...
*/
static int DateTime_init(DateTime *self, PyObject *args, PyObject *kwargs) {
    int year;
    int month;
    int day;
    int hour;
    int minute;
    int second;
    int microsecond;

    if (!PyArg_ParseTuple(args, "iiiiiii", &year, &month, &day, &hour, &minute, &second, &microsecond))
        return -1;

    if (year < MIN_YEAR || year > MAX_YEAR) {
        PyErr_SetString(
            PyExc_ValueError, "year must be between 0 and 9999"
        );

        return -1;
    }

    self->year = year;
    self->month = month;
    self->day = day;
    self->hour = hour;
    self->minute = minute;
    self->second = second;
    self->microsecond = microsecond;

    return 0;
}

static PyObject *DateTime_repr(DateTime *self) {
    char repr[37] = {0};

    sprintf(
        repr,
        "DateTime(%d, %d, %d, %d, %d, %d, %d)",
        self->year,
        self->month,
        self->day,
        self->hour,
        self->minute,
        self->second,
        self->microsecond
    );

    return PyUnicode_FromString(repr);
}


static PyMemberDef DateTime_members[] = {
    {"year", T_INT, offsetof(DateTime, year), 0, "years in diff"},
    {"month", T_INT, offsetof(DateTime, month), 0, "months in diff"},
    {"day", T_INT, offsetof(DateTime, day), 0, "days in diff"},
    {"hour", T_INT, offsetof(DateTime, hour), 0, "hours in diff"},
    {"minute", T_INT, offsetof(DateTime, minute), 0, "minutes in diff"},
    {"second", T_INT, offsetof(DateTime, second), 0, "seconds in diff"},
    {"microsecond", T_INT, offsetof(DateTime, microsecond), 0, "microseconds in diff"},
    {NULL}
};

static PyTypeObject DateTime_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "DateTime",                  /* tp_name */
    sizeof(DateTime),                           /* tp_basicsize */
    0,                                      /* tp_itemsize */
    0,                                      /* tp_dealloc */
    0,                                      /* tp_print */
    0,                                      /* tp_getattr */
    0,                                      /* tp_setattr */
    0,                                      /* tp_as_async */
    (reprfunc)DateTime_repr,                    /* tp_repr */
    0,                                      /* tp_as_number */
    0,                                      /* tp_as_sequence */
    0,                                      /* tp_as_mapping */
    0,                                      /* tp_hash  */
    0,                                      /* tp_call */
    (reprfunc)DateTime_repr,                    /* tp_str */
    0,                                      /* tp_getattro */
    0,                                      /* tp_setattro */
    0,                                      /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT|Py_TPFLAGS_BASETYPE, /* tp_flags */
    "Precise difference between two datetime objects",             /* tp_doc */
};


static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_datetime",
    NULL,
    -1,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
};


PyMODINIT_FUNC
PyInit__datetime(void)
{
    PyObject *module;

    module = PyModule_Create(&moduledef);

    if (module == NULL)
        return NULL;

    // Diff declaration
    DateTime_type.tp_new = PyType_GenericNew;
    DateTime_type.tp_members = DateTime_members;
    DateTime_type.tp_init = (initproc)DateTime_init;

    if (PyType_Ready(&DateTime_type) < 0)
        return NULL;

    PyModule_AddObject(module, "DateTime", (PyObject *)&DateTime_type);

    return module;
}
