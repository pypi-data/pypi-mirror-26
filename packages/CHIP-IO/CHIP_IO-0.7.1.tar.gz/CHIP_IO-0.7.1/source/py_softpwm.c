/*
Copyright (c) 2016 Brady Hurlburt

Original BBIO Author Justin Cooper
Modified for CHIP_IO Author Brady Hurlburt

This file incorporates work covered by the following copyright and
permission notice, all modified code adopts the original license:

Copyright (c) 2013 Adafruit
Author: Justin Cooper

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

#include "Python.h"
#include "constants.h"
#include "common.h"
#include "c_softpwm.h"

// python function toggle_debug()
static PyObject *py_toggle_debug(PyObject *self, PyObject *args)
{
    // toggle debug printing
    toggle_debug();

    Py_RETURN_NONE;
}

// python function cleanup(channel)
static PyObject *py_cleanup(PyObject *self, PyObject *args, PyObject *kwargs)
{
    char key[8];
    char *channel;
    static char *kwlist[] = {"channel", NULL};

    clear_error_msg();

    // Channel is optional
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|s", kwlist, &channel)) {
        return NULL;
    }

    // The !channel fixes issues #50
    if (channel == NULL || strcmp(channel, "\0") == 0) {
        softpwm_cleanup();
    } else {
        if (!get_key(channel, key)) {
            softpwm_cleanup();
        }
        softpwm_disable(key);
    }

    Py_RETURN_NONE;
}

static int init_module(void)
{
    clear_error_msg();

    // If we make it here, we're good to go
    if (DEBUG)
        printf(" ** init_module: setup complete **\n");
    module_setup = 1;

    return 0;
}

// python function value = is_chip_pro()
static PyObject *py_is_chip_pro(PyObject *self, PyObject *args)
{
    PyObject *py_value;
    
    py_value = Py_BuildValue("i", is_this_chippro());

    return py_value;
}

// python function start(channel, duty_cycle, freq, polarity)
static PyObject *py_start_channel(PyObject *self, PyObject *args, PyObject *kwargs)
{
    char key[8];
    char *channel = NULL;
    float frequency = 2000.0;
    float duty_cycle = 0.0;
    int polarity = 0;
    int gpio;
    int allowed = -1;
    static char *kwlist[] = {"channel", "duty_cycle", "frequency", "polarity", NULL};

    clear_error_msg();

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|ffi", kwlist, &channel, &duty_cycle, &frequency, &polarity)) {
        return NULL;
    }
    ASSRT(channel != NULL);

    if (!module_setup) {
        init_module();
    }

    if (!get_key(channel, key)) {
        PyErr_SetString(PyExc_ValueError, "Invalid SOFTPWM key or name.");
        return NULL;
    }

    // check to ensure gpio is one of the allowed pins
    // Not protecting the call as if the get_key() fails, we won't make it here
    get_gpio_number(channel, &gpio);

    // Check to see if GPIO is allowed on the hardware
    // A 1 means we're good to go
    allowed = gpio_allowed(gpio);
    if (allowed == -1) {
        char err[2000];
        snprintf(err, sizeof(err), "Error determining hardware. (%s)", get_error_msg());
        PyErr_SetString(PyExc_ValueError, err);
        return NULL;
    } else if (allowed == 0) {
        char err[2000];
        snprintf(err, sizeof(err), "GPIO %d not available on current Hardware", gpio);
        PyErr_SetString(PyExc_ValueError, err);
        return NULL;
    }

    if (duty_cycle < 0.0 || duty_cycle > 100.0) {
        PyErr_SetString(PyExc_ValueError, "duty_cycle must have a value from 0.0 to 100.0");
        return NULL;
    }

    if (frequency <= 0.0) {
        PyErr_SetString(PyExc_ValueError, "frequency must be greater than 0.0");
        return NULL;
    }

    if (polarity < 0 || polarity > 1) {
        PyErr_SetString(PyExc_ValueError, "polarity must be either 0 or 1");
        return NULL;
    }

    if (softpwm_start(key, duty_cycle, frequency, polarity) < 0) {
       printf("softpwm_start failed");
       char err[2000];
       snprintf(err, sizeof(err), "Error starting softpwm on pin %s (%s)", key, get_error_msg());
       PyErr_SetString(PyExc_RuntimeError, err);
       return NULL;
    }

    Py_RETURN_NONE;
}

// python function stop(channel)
static PyObject *py_stop_channel(PyObject *self, PyObject *args, PyObject *kwargs)
{
    char key[8];
    char *channel;
    int gpio;
    int allowed = -1;

    clear_error_msg();

    if (!PyArg_ParseTuple(args, "s", &channel))
        return NULL;

    if (!get_key(channel, key)) {
        PyErr_SetString(PyExc_ValueError, "Invalid PWM key or name.");
        return NULL;
    }

    // check to ensure gpio is one of the allowed pins
    // Not protecting the call as if the get_key() fails, we won't make it here
    get_gpio_number(channel, &gpio);

    // Check to see if GPIO is allowed on the hardware
    // A 1 means we're good to go
    allowed = gpio_allowed(gpio);
    if (allowed == -1) {
        char err[2000];
        snprintf(err, sizeof(err), "Error determining hardware. (%s)", get_error_msg());
        PyErr_SetString(PyExc_ValueError, err);
        return NULL;
    } else if (allowed == 0) {
        char err[2000];
        snprintf(err, sizeof(err), "GPIO %d not available on current Hardware", gpio);
        PyErr_SetString(PyExc_ValueError, err);
        return NULL;
    }

    softpwm_disable(key);

    Py_RETURN_NONE;
}

// python method PWM.set_duty_cycle(channel, duty_cycle)
static PyObject *py_set_duty_cycle(PyObject *self, PyObject *args, PyObject *kwargs)
{
    char key[8];
    char *channel;
    int gpio;
    int allowed = -1;
    float duty_cycle = 0.0;
    static char *kwlist[] = {"channel", "duty_cycle", NULL};

    clear_error_msg();

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|f", kwlist, &channel, &duty_cycle))
        return NULL;

    if (duty_cycle < 0.0 || duty_cycle > 100.0) {
        PyErr_SetString(PyExc_ValueError, "duty_cycle must have a value from 0.0 to 100.0");
        return NULL;
    }

    if (!get_key(channel, key)) {
        PyErr_SetString(PyExc_ValueError, "Invalid PWM key or name.");
        return NULL;
    }

    // check to ensure gpio is one of the allowed pins
    // Not protecting the call as if the get_key() fails, we won't make it here
    get_gpio_number(channel, &gpio);

    // Check to see if GPIO is allowed on the hardware
    // A 1 means we're good to go
    allowed = gpio_allowed(gpio);
    if (allowed == -1) {
        char err[2000];
        snprintf(err, sizeof(err), "Error determining hardware. (%s)", get_error_msg());
        PyErr_SetString(PyExc_ValueError, err);
        return NULL;
    } else if (allowed == 0) {
        char err[2000];
        snprintf(err, sizeof(err), "GPIO %d not available on current Hardware", gpio);
        PyErr_SetString(PyExc_ValueError, err);
        return NULL;
    }

    if (softpwm_set_duty_cycle(key, duty_cycle) == -1) {
        PyErr_SetString(PyExc_RuntimeError, "You must start() the PWM channel first");
        return NULL;
    }

    Py_RETURN_NONE;
}

// python method PWM.set_frequency(channel, frequency)
static PyObject *py_set_frequency(PyObject *self, PyObject *args, PyObject *kwargs)
{
    char key[8];
    char *channel;
    int gpio;
    int allowed = -1;
    float frequency = 1.0;
    static char *kwlist[] = {"channel", "frequency", NULL};

    clear_error_msg();

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|f", kwlist, &channel, &frequency))
        return NULL;

    if ((frequency <= 0.0) || (frequency > 10000.0)) {
        PyErr_SetString(PyExc_ValueError, "frequency must be greater than 0.0 and less than 10000.0");
        return NULL;
    }

    if (!get_key(channel, key)) {
        PyErr_SetString(PyExc_ValueError, "Invalid PWM key or name.");
        return NULL;
    }

    // check to ensure gpio is one of the allowed pins
    // Not protecting the call as if the get_key() fails, we won't make it here
    get_gpio_number(channel, &gpio);

    // Check to see if GPIO is allowed on the hardware
    // A 1 means we're good to go
    allowed = gpio_allowed(gpio);
    if (allowed == -1) {
        char err[2000];
        snprintf(err, sizeof(err), "Error determining hardware. (%s)", get_error_msg());
        PyErr_SetString(PyExc_ValueError, err);
        return NULL;
    } else if (allowed == 0) {
        char err[2000];
        snprintf(err, sizeof(err), "GPIO %d not available on current Hardware", gpio);
        PyErr_SetString(PyExc_ValueError, err);
        return NULL;
    }

    if (softpwm_set_frequency(key, frequency) == -1) {
        PyErr_SetString(PyExc_RuntimeError, "You must start() the PWM channel first");
        return NULL;
    }

    Py_RETURN_NONE;
}

static const char moduledocstring[] = "Software PWM functionality of a CHIP using Python";

PyMethodDef pwm_methods[] = {
    {"start", (PyCFunction)py_start_channel, METH_VARARGS | METH_KEYWORDS, "Set up and start the PWM channel.  channel can be in the form of 'XIO-P0', or 'U14_13'"},
    {"stop", (PyCFunction)py_stop_channel, METH_VARARGS | METH_KEYWORDS, "Stop the PWM channel.  channel can be in the form of 'XIO-P0', or 'U14_13'"},
    {"set_duty_cycle", (PyCFunction)py_set_duty_cycle, METH_VARARGS, "Change the duty cycle\ndutycycle - between 0.0 and 100.0" },
    {"set_frequency", (PyCFunction)py_set_frequency, METH_VARARGS, "Change the frequency\nfrequency - frequency in Hz (freq > 0.0)" },
    {"cleanup", (PyCFunction)py_cleanup, METH_VARARGS | METH_KEYWORDS, "Clean up by resetting all GPIO channels that have been used by this program to INPUT with no pullup/pulldown and no event detection"},
    {"toggle_debug", py_toggle_debug, METH_VARARGS, "Toggles the enabling/disabling of Debug print output"},
    {"is_chip_pro", py_is_chip_pro, METH_VARARGS, "Is hardware a CHIP Pro? Boolean False for normal CHIP/PocketCHIP (R8 SOC)"},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION > 2
static struct PyModuleDef chipspwmmodule = {
    PyModuleDef_HEAD_INIT,
    "SOFTPWM",       // name of module
    moduledocstring,  // module documentation, may be NULL
    -1,               // size of per-interpreter state of the module, or -1 if the module keeps state in global variables.
    pwm_methods
};
#endif

#if PY_MAJOR_VERSION > 2
PyMODINIT_FUNC PyInit_SOFTPWM(void)
#else
PyMODINIT_FUNC initSOFTPWM(void)
#endif
{
    PyObject *module = NULL;

#if PY_MAJOR_VERSION > 2
    if ((module = PyModule_Create(&chipspwmmodule)) == NULL)
       return NULL;
#else
    if ((module = Py_InitModule3("SOFTPWM", pwm_methods, moduledocstring)) == NULL)
       return;
#endif

   define_constants(module);


#if PY_MAJOR_VERSION > 2
    return module;
#else
    return;
#endif
}
