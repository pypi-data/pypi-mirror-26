/*
Copyright (c) 2016 Robert Wolterman

Original BBIO Author Justin Cooper
Modified for CHIP_IO Author Robert Wolterman

This file incorporates work covered by the following copyright and
permission notice, all modified code adopts the original license:

Copyright (c) 2013 Adafruit

Original RPi.GPIO Author Ben Croston
Modified for BBIO Author Justin Cooper

This file incorporates work covered by the following copyright and
permission notice, all modified code adopts the original license:

Copyright (c) 2013 Ben Croston

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

#include <stdio.h>
#include "stdlib.h"
#include "Python.h"
#include "constants.h"
#include "common.h"
#include "event_gpio.h"

static int gpio_warnings = 1;
static int r8_mem_setup = 0;

int max_gpio = -1;
dyn_int_array_t *gpio_direction = NULL;

struct py_callback
{
   char channel[32];
   int gpio;
   PyObject *py_cb;
   unsigned long long lastcall;
   unsigned int bouncetime;
   struct py_callback *next;
};
static struct py_callback *py_callbacks = NULL;

// python function toggle_debug()
static PyObject *py_toggle_debug(PyObject *self, PyObject *args)
{
    // toggle debug printing
    toggle_debug();

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

static int init_r8_gpio_mem(void)
{
    clear_error_msg();

    if (DEBUG)
        printf(" ** init_r8_gpio_mem: mapping memory **\n");
    
    if (map_pio_memory() < 0) {
        char err[2000];
        snprintf(err, sizeof(err), "init_r8_gpio_mem error (%s)", get_error_msg());
        PyErr_SetString(PyExc_RuntimeError, err);
        return 0;
    }

    // If we make it here, we're good to go
    if (DEBUG)
        printf(" ** init_r8_gpio_mem: setup complete **\n");
    r8_mem_setup = 1;
    
    return 0;
}

// python function value = is_chip_pro
static PyObject *py_is_chip_pro(PyObject *self, PyObject *args)
{
    PyObject *py_value;
    
    py_value = Py_BuildValue("i", is_this_chippro());

    return py_value;
}

static void remember_gpio_direction(int gpio, int direction)
{
    dyn_int_array_set(&gpio_direction, gpio, direction, -1);
}

// Dummy function to mimic RPi.GPIO for easier porting.
// python function setmode(mode)
static PyObject *py_setmode(PyObject *self, PyObject *args)
{
    Py_RETURN_NONE;
}

// python function cleanup(channel=None)
static PyObject *py_cleanup(PyObject *self, PyObject *args, PyObject *kwargs)
{
    int gpio;
    char *channel;
    int inchan;
    static char *kwlist[] = {"channel", NULL};

    clear_error_msg();

    // Channel is optional
    // Try to parse the string
    int rtn;
    rtn = PyArg_ParseTupleAndKeywords(args, kwargs, "|s", kwlist, &channel);
    if (!rtn) {
        // Fall into here are try to parse an int
        rtn = PyArg_ParseTupleAndKeywords(args, kwargs, "|i", kwlist, &inchan);
        if (!rtn) {
            return NULL;
        }
        // We make it here, we can convert inchan to a string for us to ensure it's valid
        asprintf(&channel, "%i", inchan);
    }

    // The !channel fixes issues #50
    if (channel == NULL || strcmp(channel, "\0") == 0) {
        event_cleanup();
    } else {
        if (get_gpio_number(channel, &gpio) < 0) {
            event_cleanup();
        }
        gpio_unexport(gpio);
    }

    Py_RETURN_NONE;
}

// python function setup(channel, direction, pull_up_down=PUD_OFF, initial=None)
static PyObject *py_setup_channel(PyObject *self, PyObject *args, PyObject *kwargs)
{
    int gpio;
    int allowed = -1;
    char *channel;
    int inchan;
    int direction;
    int pud = PUD_OFF;
    int initial = 0;
    static char *kwlist[] = {"channel", "direction", "pull_up_down", "initial", NULL};
 
    clear_error_msg();
 
    // Try to parse the string
    int rtn;
    rtn = PyArg_ParseTupleAndKeywords(args, kwargs, "si|ii", kwlist, &channel, &direction, &pud, &initial);
    if (!rtn) {
        // Fall into here are try to parse an int
        rtn = PyArg_ParseTupleAndKeywords(args, kwargs, "ii|ii", kwlist, &inchan, &direction, &pud, &initial);
        if (!rtn) {
            return NULL;
        }
        // We make it here, we can convert inchan to a string for us to ensure it's valid
        asprintf(&channel, "%i", inchan);
    }
 
    if (!module_setup) {
        init_module();
    }

    if (get_gpio_number(channel, &gpio) < 0) {
        char err[2000];
        snprintf(err, sizeof(err), "Invalid channel %s. (%s)", channel, get_error_msg());
        PyErr_SetString(PyExc_ValueError, err);
        return NULL;
    }

    if (direction != INPUT && direction != OUTPUT)
    {
        PyErr_SetString(PyExc_ValueError, "An invalid direction was passed to setup()");
        return NULL;
    }
    
    // Force pud to be off if we're configured for output
    if (direction == OUTPUT) {
        pud = PUD_OFF;
    }
 
    if (pud != PUD_OFF && pud != PUD_DOWN && pud != PUD_UP)
    {
        PyErr_SetString(PyExc_ValueError, "Invalid value for pull_up_down - should be either PUD_OFF, PUD_UP or PUD_DOWN");
        return NULL;
    }
 
    if (get_gpio_number(channel, &gpio) < 0) {
        char err[2000];
        snprintf(err, sizeof(err), "Invalid channel %s. (%s)", channel, get_error_msg());
        PyErr_SetString(PyExc_ValueError, err);
        return NULL;
    }
    
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

    // Only map /dev/mem if we're not an XIO
    if (!r8_mem_setup && !(gpio >= lookup_gpio_by_name("XIO-P0") && gpio <= lookup_gpio_by_name("XIO-P7"))) {
        init_r8_gpio_mem();
    }
 
    int exprtn = gpio_export(gpio);
    if (exprtn == -1) {
        char err[2000];
        snprintf(err, sizeof(err), "Error setting up channel %s, maybe already exported? (%s)", channel, get_error_msg());
        PyErr_SetString(PyExc_RuntimeError, err);
        return NULL;
    } else if (exprtn == -2 && gpio_warnings) {
        char warn[2000];
        snprintf(warn, sizeof(warn), "Channel %s may already be exported, proceeding with rest of setup", channel);
        PyErr_WarnEx(PyExc_Warning, warn, 1);
    }
    if (gpio_set_direction(gpio, direction) < 0) {
        char err[2000];
        snprintf(err, sizeof(err), "Error setting direction %d on channel %s. (%s)", direction, channel, get_error_msg());
        PyErr_SetString(PyExc_RuntimeError, err);
        return NULL;
    }
    
    // Pull Up/Down
    // Only if the pin we want is able to use it (R8 Owned, no XIO)
    int port, pin;
    if (compute_port_pin(channel, gpio, &port, &pin) == 0) {
        // Set the PUD
        gpio_set_pud(port, pin, pud);
        // Check it was set properly
        int pudr = gpio_get_pud(port, pin);
        if (pudr != pud) {
            char err[2000];
            snprintf(err, sizeof(err), "Error setting pull up down %d on channel %s", pud, channel);
            PyErr_SetString(PyExc_RuntimeError, err);
            return NULL;
        }
    }
    
    if (direction == OUTPUT) {
        if (gpio_set_value(gpio, initial) < 0) {
            char err[2000];
            snprintf(err, sizeof(err), "Error setting initial value %d on channel %s. (%s)", initial, channel, get_error_msg());
            PyErr_SetString(PyExc_RuntimeError, err);
            return NULL;
        }
    }
 
    remember_gpio_direction(gpio, direction);

    Py_RETURN_NONE;
}  /* py_setup_channel */

// python function output(channel, value)
static PyObject *py_output_gpio(PyObject *self, PyObject *args)
{
    int gpio;
    int value;
    char *channel;
    int inchan;
    int allowed = -1;

    clear_error_msg();

    // Try to parse the string
    int rtn;
    rtn = PyArg_ParseTuple(args, "si", &channel, &value);
    if (!rtn) {
        // Fall into here are try to parse an int
        rtn = PyArg_ParseTuple(args, "ii", &inchan, &value);
        if (!rtn) {
            return NULL;
        }
        // We make it here, we can convert inchan to a string for us to ensure it's valid
        asprintf(&channel, "%i", inchan);
    }

    if (get_gpio_number(channel, &gpio)) {
        PyErr_SetString(PyExc_ValueError, "Invalid channel");
        return NULL;
    }

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

    if (!module_setup || dyn_int_array_get(&gpio_direction, gpio, -1) != OUTPUT)
    {
        char err[2000];
        snprintf(err, sizeof(err), "Channel %s not set up or is not an output", channel);
        PyErr_SetString(PyExc_RuntimeError, err);
        return NULL;
    }

    int result = gpio_set_value(gpio, value);
    if (result < 0) {
        char err[2000];
        snprintf(err, sizeof(err), "Could no write %d on channel %s. (%s)", value, channel, get_error_msg());
        PyErr_SetString(PyExc_RuntimeError, err);
        return NULL;
    }

    Py_RETURN_NONE;
}  /* py_output_gpio */


// python function value = input(channel)
static PyObject *py_input_gpio(PyObject *self, PyObject *args)
{
    int gpio;
    char *channel;
    int inchan;
    unsigned int value;
    PyObject *py_value;
    int allowed = -1;

    clear_error_msg();

    // Try to parse the string
    int rtn;
    rtn = PyArg_ParseTuple(args, "s", &channel);
    if (!rtn) {
        // Fall into here are try to parse an int
        rtn = PyArg_ParseTuple(args, "i", &inchan);
        if (!rtn) {
            return NULL;
        }
        // We make it here, we can convert inchan to a string for us to ensure it's valid
        asprintf(&channel, "%i", inchan);
    }

    if (get_gpio_number(channel, &gpio)) {
        PyErr_SetString(PyExc_ValueError, "Invalid channel");
        return NULL;
    }

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

   // check channel is set up as an input or output
    if (!module_setup || (dyn_int_array_get(&gpio_direction, gpio, -1) == -1))
    {
        PyErr_SetString(PyExc_RuntimeError, "You must setup() the GPIO channel first");
        return NULL;
    }

    if (gpio_get_value(gpio, &value) < 0) {
      char err[1024];
      snprintf(err, sizeof(err), "Could not get value ('%s')", get_error_msg());
      PyErr_SetString(PyExc_RuntimeError, err);
      return NULL;
    }

    py_value = Py_BuildValue("i", value);

    return py_value;
}

//TODO: Come up with a way to merge py_read_byte_gpio and py_read_word_gpio
// python function value = read_byte(channel)
static PyObject *py_read_byte_gpio(PyObject *self, PyObject *args)
{
    int gpio;
    char *channel;
    int inchan;
    unsigned int value = 0;
    PyObject *py_value;
    int allowed = -1;

    clear_error_msg();

    // Try to parse the string
    int rtn;
    rtn = PyArg_ParseTuple(args, "s", &channel);
    if (!rtn) {
        // Fall into here are try to parse an int
        rtn = PyArg_ParseTuple(args, "i", &inchan);
        if (!rtn) {
            return NULL;
        }
        // We make it here, we can convert inchan to a string for us to ensure it's valid
        asprintf(&channel, "%i", inchan);
    }

    if (get_gpio_number(channel, &gpio)) {
        PyErr_SetString(PyExc_ValueError, "Invalid channel");
        return NULL;
    }

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

   // check channel is set up as an input or output
    if (!module_setup || (dyn_int_array_get(&gpio_direction, gpio, -1) == -1))
    {
        PyErr_SetString(PyExc_RuntimeError, "You must setup() the GPIO channel first");
        return NULL;
    }

    // We only want to get a 8 bits here
    if (gpio_get_more(gpio, 8, &value) < 0) {
      char err[1024];
      snprintf(err, sizeof(err), "Could not get 8 bits of data ('%s')", get_error_msg());
      PyErr_SetString(PyExc_RuntimeError, err);
      return NULL;
    }

    py_value = Py_BuildValue("i", value);

    return py_value;
}

// python function value = read_word(channel)
static PyObject *py_read_word_gpio(PyObject *self, PyObject *args)
{
    int gpio;
    char *channel;
    int inchan;
    unsigned int value = 0;
    PyObject *py_value;
    int allowed = -1;

    clear_error_msg();

    // Try to parse the string
    int rtn;
    rtn = PyArg_ParseTuple(args, "s", &channel);
    if (!rtn) {
        // Fall into here are try to parse an int
        rtn = PyArg_ParseTuple(args, "i", &inchan);
        if (!rtn) {
            return NULL;
        }
        // We make it here, we can convert inchan to a string for us to ensure it's valid
        asprintf(&channel, "%i", inchan);
    }

    if (get_gpio_number(channel, &gpio)) {
        PyErr_SetString(PyExc_ValueError, "Invalid channel");
        return NULL;
    }
    
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
    
    // check channel is set up as an input or output
    if (!module_setup || (dyn_int_array_get(&gpio_direction, gpio, -1) == -1))
    {
        PyErr_SetString(PyExc_RuntimeError, "You must setup() the GPIO channel first");
        return NULL;
    }

    // We only want to get a 8 bits here
    if (gpio_get_more(gpio, 16, &value) < 0) {
      char err[1024];
      snprintf(err, sizeof(err), "Could not get 16 bits of data ('%s')", get_error_msg());
      PyErr_SetString(PyExc_RuntimeError, err);
      return NULL;
    }

    py_value = Py_BuildValue("i", value);

    return py_value;
}

static void run_py_callbacks(int gpio, void* data)
{
   PyObject *result;
   PyGILState_STATE gstate;
   struct py_callback *cb = py_callbacks;
   struct timeval tv_timenow;
   unsigned long long timenow;

   clear_error_msg();

   while (cb != NULL)
   {
      if (cb->gpio == gpio)
      {
         gettimeofday(&tv_timenow, NULL);
         timenow = tv_timenow.tv_sec*1E6 + tv_timenow.tv_usec;
         if (cb->bouncetime == 0 || timenow - cb->lastcall > cb->bouncetime*1000 || cb->lastcall == 0 || cb->lastcall > timenow) {

            // save lastcall before calling func to prevent reentrant bounce
            cb->lastcall = timenow;

            // run callback
            gstate = PyGILState_Ensure();
            result = PyObject_CallFunction(cb->py_cb, "s", cb->channel);

            if (result == NULL && PyErr_Occurred())
            {
               PyErr_Print();
               PyErr_Clear();
            }
            Py_XDECREF(result);
            PyGILState_Release(gstate);
         }
         cb->lastcall = timenow;
      }
      cb = cb->next;
   }
}

static int add_py_callback(char *channel, int gpio, int edge, unsigned int bouncetime, PyObject *cb_func)
{
   struct py_callback *new_py_cb;
   struct py_callback *cb = py_callbacks;

   clear_error_msg();

   // add callback to py_callbacks list
   new_py_cb = malloc(sizeof(struct py_callback));
   if (new_py_cb == 0)
   {
      PyErr_NoMemory();
      return -1;
   }
   new_py_cb->py_cb = cb_func;
   Py_XINCREF(cb_func);         // Add a reference to new callback
   memset(new_py_cb->channel, 0, sizeof(new_py_cb->channel));
   strncpy(new_py_cb->channel, channel, sizeof(new_py_cb->channel) - 1);
   new_py_cb->gpio = gpio;
   new_py_cb->lastcall = 0;
   new_py_cb->bouncetime = bouncetime;
   new_py_cb->next = NULL;
   if (py_callbacks == NULL) {
      py_callbacks = new_py_cb;
   } else {
      // add to end of list
      while (cb->next != NULL)
         cb = cb->next;
      cb->next = new_py_cb;
   }
   add_edge_callback(gpio, edge, run_py_callbacks, NULL);
   return 0;
}

// python function add_event_callback(channel, callback, bouncetime=0)
static PyObject *py_add_event_callback(PyObject *self, PyObject *args, PyObject *kwargs)
{
   int gpio;
   char *channel;
   int inchan;
   int allowed = -1;
   unsigned int bouncetime = 0;
   PyObject *cb_func;
   char *kwlist[] = {"gpio", "callback", "bouncetime", NULL};

   clear_error_msg();

    // Try to parse the string
    int rtn;
    rtn = PyArg_ParseTupleAndKeywords(args, kwargs, "sO|i", kwlist, &channel, &cb_func, &bouncetime);
    if (!rtn) {
        // Fall into here are try to parse an int
        rtn = PyArg_ParseTupleAndKeywords(args, kwargs, "iO|i", kwlist, &inchan, &cb_func, &bouncetime);
        if (!rtn) {
            return NULL;
        }
        // We make it here, we can convert inchan to a string for us to ensure it's valid
        asprintf(&channel, "%i", inchan);
    }

   if (!PyCallable_Check(cb_func))
   {
      PyErr_SetString(PyExc_TypeError, "Parameter must be callable");
      return NULL;
   }

    if (get_gpio_number(channel, &gpio)) {
        PyErr_SetString(PyExc_ValueError, "Invalid channel");
        return NULL;
    }

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

   // check to ensure gpio is one of the allowed pins
   if (gpio != lookup_gpio_by_name("AP-EINT3")
       && gpio != lookup_gpio_by_name("AP-EINT1")
       && gpio != lookup_gpio_by_name("I2S-MCLK") // CHIP PRO
       && gpio != lookup_gpio_by_name("I2S-DI") // CHIP PRO
       && gpio != lookup_gpio_by_name("PWM1") // CHIP PRO
       && !(gpio >= lookup_gpio_by_name("XIO-P0") && gpio <= lookup_gpio_by_name("XIO-P7"))) {
     PyErr_SetString(PyExc_ValueError, "Callbacks currently available on AP-EINT1, AP-EINT3, and XIO-P0 to XIO-P7 only");
     return NULL;
   }

   // check channel is set up as an input
   if (!module_setup || dyn_int_array_get(&gpio_direction, gpio, -1) != INPUT)
   {
      PyErr_SetString(PyExc_RuntimeError, "You must setup() the GPIO channel as an input first");
      return NULL;
   }

   if (!gpio_is_evented(gpio))
   {
      PyErr_SetString(PyExc_RuntimeError, "Add event detection using add_event_detect first before adding a callback");
      return NULL;
   }
   // Defaulting to Falling edge
   if (add_py_callback(channel, gpio, 2, bouncetime, cb_func) != 0)
      return NULL;

   Py_RETURN_NONE;
}

// python function add_event_detect(channel, edge, callback=None, bouncetime=0)
static PyObject *py_add_event_detect(PyObject *self, PyObject *args, PyObject *kwargs)
{
   int gpio;
   char *channel;
   int inchan;
   int edge, result;
   unsigned int bouncetime = 0;
   int allowed = -1;
   PyObject *cb_func = NULL;
   char *kwlist[] = {"gpio", "edge", "callback", "bouncetime", NULL};

   clear_error_msg();

    // Try to parse the string
    int rtn;
    rtn = PyArg_ParseTupleAndKeywords(args, kwargs, "si|Oi", kwlist, &channel, &edge, &cb_func, &bouncetime);
    if (!rtn) {
        // Fall into here are try to parse an int
        rtn = PyArg_ParseTupleAndKeywords(args, kwargs, "ii|Oi", kwlist, &inchan, &edge, &cb_func, &bouncetime);
        if (!rtn) {
            return NULL;
        }
        // We make it here, we can convert inchan to a string for us to ensure it's valid
        asprintf(&channel, "%i", inchan);
    }

   if (cb_func != NULL && !PyCallable_Check(cb_func))
   {
      PyErr_SetString(PyExc_TypeError, "Parameter must be callable");
      return NULL;
   }

   if (get_gpio_number(channel, &gpio)) {
       PyErr_SetString(PyExc_ValueError, "Invalid channel");
       return NULL;
   }

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

   // check to ensure gpio is one of the allowed pins
   if (gpio != lookup_gpio_by_name("AP-EINT3")
       && gpio != lookup_gpio_by_name("AP-EINT1")
       && gpio != lookup_gpio_by_name("I2S-MCLK") // CHIP PRO
       && gpio != lookup_gpio_by_name("I2S-DI") // CHIP PRO
       && gpio != lookup_gpio_by_name("PWM1") // CHIP PRO
       && !(gpio >= lookup_gpio_by_name("XIO-P0") && gpio <= lookup_gpio_by_name("XIO-P7"))) {
     PyErr_SetString(PyExc_ValueError, "Edge Detection currently available on AP-EINT1, AP-EINT3, and XIO-P0 to XIO-P7 only");
     return NULL;
   }

   // is edge valid value
   if (edge != RISING_EDGE && edge != FALLING_EDGE && edge != BOTH_EDGE)
   {
      PyErr_SetString(PyExc_ValueError, "The edge must be set to RISING, FALLING or BOTH");
      return NULL;
   }

   // check channel is set up as an input
   if (!module_setup || dyn_int_array_get(&gpio_direction, gpio, -1) != INPUT)
   {
      PyErr_SetString(PyExc_RuntimeError, "You must setup() the GPIO channel as an input first");
      return NULL;
   }

   if ((result = add_edge_detect(gpio, edge)) != 0)   // starts a thread
   {
      if (result == 1)
      {
         PyErr_SetString(PyExc_RuntimeError, "Edge detection already enabled for this GPIO channel");
         return NULL;
      } else {
         PyErr_SetString(PyExc_RuntimeError, "Failed to add edge detection");
         return NULL;
      }
   }

   if (cb_func != NULL)
      if (add_py_callback(channel, gpio, edge, bouncetime, cb_func) != 0)
         return NULL;

   Py_RETURN_NONE;
}

// python function remove_event_detect(channel)
static PyObject *py_remove_event_detect(PyObject *self, PyObject *args)
{
   int gpio;
   char *channel;
   int inchan;
   struct py_callback *cb = py_callbacks;
   struct py_callback *temp;
   struct py_callback *prev = NULL;
   int allowed = -1;

   clear_error_msg();

    // Try to parse the string
    int rtn;
    rtn = PyArg_ParseTuple(args, "s", &channel);
    if (!rtn) {
        // Fall into here are try to parse an int
        rtn = PyArg_ParseTuple(args, "i", &inchan);
        if (!rtn) {
            return NULL;
        }
        // We make it here, we can convert inchan to a string for us to ensure it's valid
        asprintf(&channel, "%i", inchan);
    }

   if (get_gpio_number(channel, &gpio)) {
       PyErr_SetString(PyExc_ValueError, "Invalid channel");
       return NULL;
   }

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

   // check to ensure gpio is one of the allowed pins
   if (gpio != lookup_gpio_by_name("AP-EINT3")
       && gpio != lookup_gpio_by_name("AP-EINT1")
       && gpio != lookup_gpio_by_name("I2S-MCLK") // CHIP PRO
       && gpio != lookup_gpio_by_name("I2S-DI") // CHIP PRO
       && gpio != lookup_gpio_by_name("PWM1") // CHIP PRO
       && !(gpio >= lookup_gpio_by_name("XIO-P0") && gpio <= lookup_gpio_by_name("XIO-P7"))) {
     PyErr_SetString(PyExc_ValueError, "Edge Detection currently available on AP-EINT1, AP-EINT3, and XIO-P0 to XIO-P7 only");
     return NULL;
   }

   // remove all python callbacks for gpio
   while (cb != NULL)
   {
      if (cb->gpio == gpio)
      {
         Py_XDECREF(cb->py_cb);
         if (prev == NULL)
            py_callbacks = cb->next;
         else
            prev->next = cb->next;
         temp = cb;
         cb = cb->next;
         free(temp);
      } else {
         prev = cb;
         cb = cb->next;
      }
   }

   remove_edge_detect(gpio);

   Py_RETURN_NONE;
}

// python function value = event_detected(channel)
static PyObject *py_event_detected(PyObject *self, PyObject *args)
{
   int gpio;
   char *channel;
   int inchan;
   int allowed = -1;

   clear_error_msg();

    // Try to parse the string
    int rtn;
    rtn = PyArg_ParseTuple(args, "s", &channel);
    if (!rtn) {
        // Fall into here are try to parse an int
        rtn = PyArg_ParseTuple(args, "i", &inchan);
        if (!rtn) {
            return NULL;
        }
        // We make it here, we can convert inchan to a string for us to ensure it's valid
        asprintf(&channel, "%i", inchan);
    }

   if (get_gpio_number(channel, &gpio)) {
       PyErr_SetString(PyExc_ValueError, "Invalid channel");
       return NULL;
   }

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

   if (event_detected(gpio))
      Py_RETURN_TRUE;
   else
      Py_RETURN_FALSE;
}

// python function py_wait_for_edge(gpio, edge, timeout = -1)
static PyObject *py_wait_for_edge(PyObject *self, PyObject *args)
{
   int gpio;
   int edge, result, timeout;
   char *channel;
   int inchan;
   char error[81];
   int allowed = -1;

   clear_error_msg();

   timeout = -1;

    // Try to parse the string
    int rtn;
    rtn = PyArg_ParseTuple(args, "si|i", &channel, &edge, &timeout);
    if (!rtn) {
        // Fall into here are try to parse an int
        rtn = PyArg_ParseTuple(args, "ii|i", &inchan, &edge, &timeout);
        if (!rtn) {
            return NULL;
        }
        // We make it here, we can convert inchan to a string for us to ensure it's valid
        asprintf(&channel, "%i", inchan);
    }

   if (get_gpio_number(channel, &gpio)) {
       PyErr_SetString(PyExc_ValueError, "Invalid channel");
       return NULL;
   }

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

   // check to ensure gpio is one of the allowed pins
   if (gpio != lookup_gpio_by_name("AP-EINT3")
       && gpio != lookup_gpio_by_name("AP-EINT1")
       && gpio != lookup_gpio_by_name("I2S-MCLK") // CHIP PRO
       && gpio != lookup_gpio_by_name("I2S-DI") // CHIP PRO
       && gpio != lookup_gpio_by_name("PWM1") // CHIP PRO
       && !(gpio >= lookup_gpio_by_name("XIO-P0") && gpio <= lookup_gpio_by_name("XIO-P7"))) {
     PyErr_SetString(PyExc_ValueError, "Edge Detection currently available on AP-EINT1, AP-EINT3, and XIO-P0 to XIO-P7 only");
     return NULL;
   }

   // is edge a valid value?
   if (edge != RISING_EDGE && edge != FALLING_EDGE && edge != BOTH_EDGE)
   {
      PyErr_SetString(PyExc_ValueError, "The edge must be set to RISING, FALLING or BOTH");
      return NULL;
   }

   // check channel is setup as an input
   if (!module_setup || dyn_int_array_get(&gpio_direction, gpio, -1) != INPUT)
   {
      PyErr_SetString(PyExc_RuntimeError, "You must setup() the GPIO channel as an input first");
      return NULL;
   }

   Py_BEGIN_ALLOW_THREADS // disable GIL
   result = blocking_wait_for_edge(gpio, edge, timeout);
   Py_END_ALLOW_THREADS   // enable GIL

   if (result == 0) {
      Py_INCREF(Py_None);
      return Py_None;
   } else if (result == 2) {
      PyErr_SetString(PyExc_RuntimeError, "Edge detection events already enabled for this GPIO channel");
      return NULL;
   } else {
      snprintf(error, sizeof(error), "Error #%d waiting for edge", result); BUF2SMALL(error);
      PyErr_SetString(PyExc_RuntimeError, error);
      return NULL;
   }

   Py_RETURN_NONE;
}

// python function value = gpio_function(channel)
static PyObject *py_gpio_function(PyObject *self, PyObject *args)
{
    int gpio;
    unsigned int value;
    PyObject *func;
    char *channel;
    int inchan;
    int allowed = -1;

    clear_error_msg();

    // Try to parse the string
    int rtn;
    rtn = PyArg_ParseTuple(args, "s", &channel);
    if (!rtn) {
        // Fall into here are try to parse an int
        rtn = PyArg_ParseTuple(args, "i", &inchan);
        if (!rtn) {
            return NULL;
        }
        // We make it here, we can convert inchan to a string for us to ensure it's valid
        asprintf(&channel, "%i", inchan);
    }

    if (get_gpio_number(channel, &gpio)) {
        PyErr_SetString(PyExc_ValueError, "Invalid channel");
        return NULL;
    }

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

    if (setup_error)
    {
        PyErr_SetString(PyExc_RuntimeError, "Module not imported correctly!");
        return NULL;
    }

    if (gpio_get_direction(gpio, &value) < 0) {
      char err[1024];
      snprintf(err, sizeof(err), "Could not get direction ('%s')", get_error_msg());
      PyErr_SetString(PyExc_RuntimeError, err);
      return NULL;
    }
    func = Py_BuildValue("i", value);
    return func;
}

// python function setwarnings(state)
static PyObject *py_setwarnings(PyObject *self, PyObject *args)
{
   clear_error_msg();

   if (!PyArg_ParseTuple(args, "i", &gpio_warnings))
      return NULL;

   if (setup_error)
   {
      PyErr_SetString(PyExc_RuntimeError, "Module not imported correctly!");
      return NULL;
   }

   Py_RETURN_NONE;
}

// python function base = get_xio_base()
static PyObject *py_gpio_base(PyObject *self, PyObject *args)
{
   unsigned int value;
   PyObject *py_value;

   clear_error_msg();

   value = get_xio_base();
   if (value <= 0) {
      char err[1024];
      snprintf(err, sizeof(err), "Could not get XIO base ('%s')", get_error_msg());
      PyErr_SetString(PyExc_RuntimeError, err);
      return NULL;
   }
   py_value = Py_BuildValue("i", value);

   return py_value;
}

// Internal unit tests
extern pins_t pins_info[];
static PyObject *py_selftest(PyObject *self, PyObject *args)
{
  int input;

  clear_error_msg();

  if (!PyArg_ParseTuple(args, "i", &input))
    return NULL;

  printf("Testing get_xio_base\n");
  int first_base = get_xio_base();  ASSRT(first_base > 0);
  int second_base = get_xio_base();  ASSRT(second_base == first_base);
  printf("base=%d\n", first_base);

  printf("Testing lookup_gpio_by_key\n");
  ASSRT(-1 == lookup_gpio_by_key("U13_1"));
  ASSRT(48 == lookup_gpio_by_key("U13_9"));
  ASSRT(47 == lookup_gpio_by_key("U13_11"));
  ASSRT(first_base == lookup_gpio_by_key("U14_13"));
  ASSRT((first_base+1) == lookup_gpio_by_key("U14_14"));
  ASSRT((first_base+6) == lookup_gpio_by_key("U14_19"));
  ASSRT((first_base+7) == lookup_gpio_by_key("U14_20"));
  ASSRT(193 == lookup_gpio_by_key("U14_23"));
  ASSRT(139 == lookup_gpio_by_key("U14_38"));
  ASSRT(-1 == lookup_gpio_by_key("U14_40"));
  ASSRT(-1 == lookup_gpio_by_key("NOTFOUND"));
  ASSRT(-1 == lookup_gpio_by_key("U14_"));
  ASSRT(-1 == lookup_gpio_by_key("U14_4000"));

  printf("Testing lookup_gpio_by_name\n");
  ASSRT(-1 == lookup_gpio_by_name("GND"));
  ASSRT(48 == lookup_gpio_by_name("TWI1-SDA"));
  ASSRT(47 == lookup_gpio_by_name("TWI1-SCK"));
  ASSRT(first_base == lookup_gpio_by_name("XIO-P0"));
  ASSRT((first_base+6) == lookup_gpio_by_name("XIO-P6"));
  ASSRT((first_base+7) == lookup_gpio_by_name("XIO-P7"));
  ASSRT(139 == lookup_gpio_by_name("CSID7"));
  ASSRT(-1 == lookup_gpio_by_name("NOTFOUND"));
  ASSRT(-1 == lookup_gpio_by_name("CSID"));
  ASSRT(-1 == lookup_gpio_by_name("CSID777"));

  printf("Testing lookup_ain_by_key\n");
  ASSRT(-1 == lookup_ain_by_key("U14_1"));
  ASSRT(0 == lookup_ain_by_key("U14_11"));
  ASSRT(-1 == lookup_ain_by_key("NOTFOUND"));
  ASSRT(-1 == lookup_ain_by_key("U14_"));
  ASSRT(-1 == lookup_ain_by_key("U14_1111"));

  printf("Testing lookup_ain_by_name\n");
  ASSRT(-1 == lookup_ain_by_name("GND"));
  ASSRT(0 == lookup_ain_by_name("LRADC"));
  ASSRT(-1 == lookup_ain_by_name("NOTFOUND"));
  ASSRT(-1 == lookup_ain_by_name("LR"));
  ASSRT(-1 == lookup_ain_by_name("LRADCCC"));

  char k[9];

  printf("Testing copy_key_by_key\n");
  ASSRT(1 == copy_key_by_key("U13_1", k)); BUF2SMALL(k); ASSRT(0 == strcmp("U13_1", k));
  ASSRT(1 == copy_key_by_key("U14_40", k)); BUF2SMALL(k); ASSRT(0 == strcmp("U14_40", k));
  ASSRT(0 == copy_key_by_key("NOTFOUND", k));
  ASSRT(0 == copy_key_by_key("U14_", k));
  ASSRT(0 == copy_key_by_key("U14_4000", k));

  printf("Testing copy_pwm_key_by_key\n");
  ASSRT(1 == copy_pwm_key_by_key("U13_18", k)); BUF2SMALL(k); ASSRT(0 == strcmp("U13_18", k));
  ASSRT(0 == copy_pwm_key_by_key("U13_1", k));
  ASSRT(0 == copy_pwm_key_by_key("U14_40", k));
  ASSRT(0 == copy_pwm_key_by_key("NOTFOUND", k));
  ASSRT(0 == copy_pwm_key_by_key("U13_", k));
  ASSRT(0 == copy_pwm_key_by_key("U13_1888", k));

  printf("Testing get_key_by_name\n");
  ASSRT(1 == get_key_by_name("GND", k)); BUF2SMALL(k); ASSRT(0 == strcmp("U13_1", k));
  ASSRT(1 == get_key_by_name("CSID7", k)); BUF2SMALL(k); ASSRT(0 == strcmp("U14_38", k));
  ASSRT(0 == get_key_by_name("NOTFOUND", k));
  ASSRT(0 == get_key_by_name("CSID", k));
  ASSRT(0 == get_key_by_name("CSID777", k));

  printf("Testing get_pwm_key_by_name\n");
  ASSRT(1 == get_pwm_key_by_name("PWM0", k)); BUF2SMALL(k); ASSRT(0 == strcmp("U13_18", k));
  ASSRT(0 == get_pwm_key_by_name("NOTFOUND", k));
  ASSRT(0 == get_pwm_key_by_name("PWM", k));
  ASSRT(0 == get_pwm_key_by_name("PWM000", k));

  char fp[80];

  printf("Testing build_path\n");
  ASSRT(1 == build_path("/home", "ch", fp, sizeof(fp)));  ASSRT(0 == strcmp("/home/chip", fp));
  ASSRT(1 == build_path("/home", "chip", fp, sizeof(fp)));  ASSRT(0 == strcmp("/home/chip", fp));
  ASSRT(0 == build_path("/home", "NOTFOUND", fp, sizeof(fp)));
  ASSRT(0 == build_path("/home", "chipp", fp, sizeof(fp)));
  ASSRT(0 == build_path("/home", "ip", fp, sizeof(fp)));
  ASSRT(0 == build_path("/NOTFOUND", "ch", fp, sizeof(fp)));

  printf("Testing error message buffer\n");
  clear_error_msg();
  ASSRT(0 == strlen(get_error_msg()));
  char *s100 = "1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890";
  add_error_msg(s100);  ASSRT(100 == strlen(get_error_msg()));
  // Subsequent messages added include a newline separator.
  add_error_msg(s100);  add_error_msg(s100);  add_error_msg(s100);  ASSRT(403 == strlen(get_error_msg()));
  add_error_msg(s100);  add_error_msg(s100);  add_error_msg(s100);  ASSRT(706 == strlen(get_error_msg()));
  add_error_msg(s100);  add_error_msg(s100);  add_error_msg(s100);  ASSRT(1009 == strlen(get_error_msg()));
  add_error_msg(s100);  add_error_msg(s100);  add_error_msg(s100);  ASSRT(1023 == strlen(get_error_msg()));

  printf("Testing dynamic integer array\n");
  dyn_int_array_t *my_array = NULL;
  ASSRT(-2 == dyn_int_array_get(&my_array, 29, -2));  ASSRT(my_array->num_elements == 45);
  dyn_int_array_set(&my_array, 44, 3, -2);            ASSRT(my_array->num_elements == 45);
  ASSRT(3 == dyn_int_array_get(&my_array, 44, -2));   ASSRT(my_array->num_elements == 45);
  dyn_int_array_set(&my_array, 45, 6, -2);            ASSRT(my_array->num_elements == 69);
  ASSRT(6 == dyn_int_array_get(&my_array, 45, -2));   ASSRT(my_array->num_elements == 69);
  dyn_int_array_delete(&my_array);

  int value = input;

  PyObject *py_value = Py_BuildValue("i", value);
  return py_value;
}

static const char moduledocstring[] = "GPIO functionality of a CHIP using Python";

/*
mine for changing pin directipn
*/
// python function set_direction(channel, direction)
static PyObject *py_set_direction(PyObject *self, PyObject *args, PyObject *kwargs)
{
	int gpio;
	char *channel;
    int inchan;
	int direction;
	int allowed = -1;
	static char *kwlist[] = { "channel", "direction", NULL };

	clear_error_msg();

    // Try to parse the string
    int rtn;
    rtn = PyArg_ParseTupleAndKeywords(args, kwargs, "si", kwlist, &channel, &direction);
    if (!rtn) {
        // Fall into here are try to parse an int
        rtn = PyArg_ParseTupleAndKeywords(args, kwargs, "ii", kwlist, &inchan, &direction);
        if (!rtn) {
            return NULL;
        }
        // We make it here, we can convert inchan to a string for us to ensure it's valid
        asprintf(&channel, "%i", inchan);
    }

	if (!module_setup) {
		init_module();
	}

	if (direction != INPUT && direction != OUTPUT)
	{
		PyErr_SetString(PyExc_ValueError, "An invalid direction was passed to setup()");
		return NULL;
	}

	if (get_gpio_number(channel, &gpio) < 0) {
		char err[2000];
		snprintf(err, sizeof(err), "Invalid channel %s. (%s)", channel, get_error_msg());
		PyErr_SetString(PyExc_ValueError, err);
		return NULL;
	}

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

	if (gpio_set_direction(gpio, direction) < 0) {
		char err[2000];
		snprintf(err, sizeof(err), "Error setting direction %d on channel %s. (%s)", direction, channel, get_error_msg());
		PyErr_SetString(PyExc_RuntimeError, err);
		return NULL;
	}

   remember_gpio_direction(gpio, direction);

   Py_RETURN_NONE;
}

PyMethodDef gpio_methods[] = {
   {"setup", (PyCFunction)py_setup_channel, METH_VARARGS | METH_KEYWORDS, "Set up the GPIO channel, direction and (optional) pull/up down control\nchannel        - Either: CHIP board pin number (not R8 GPIO 00..nn number).  Pins start from 1\n                 or    : CHIP GPIO name\ndirection      - INPUT or OUTPUT\n[pull_up_down] - PUD_OFF (default), PUD_UP or PUD_DOWN\n[initial]      - Initial value for an output channel"},
   {"cleanup", (PyCFunction)py_cleanup, METH_VARARGS | METH_KEYWORDS, "Clean up by resetting all GPIO channels that have been used by this program to INPUT with no pullup/pulldown and no event detection"},
   {"output", py_output_gpio, METH_VARARGS, "Output to a GPIO channel\ngpio  - gpio channel\nvalue - 0/1 or False/True or LOW/HIGH"},
   {"input", py_input_gpio, METH_VARARGS, "Input from a GPIO channel.  Returns HIGH=1=True or LOW=0=False\ngpio - gpio channel"},
   {"read_byte", py_read_byte_gpio, METH_VARARGS, "Read a byte (8 bits) from a set of GPIO channels. Returns 8-bits of integer data\ngpio - gpio channel."},
   {"read_word", py_read_word_gpio, METH_VARARGS, "Read a word (16 bits) from a set of GPIO channels. Returns 16-bits of integer data\ngpio - gpio channel."},
   {"add_event_detect", (PyCFunction)py_add_event_detect, METH_VARARGS | METH_KEYWORDS, "Enable edge detection events for a particular GPIO channel.\nchannel      - either board pin number or BCM number depending on which mode is set.\nedge         - RISING, FALLING or BOTH\n[callback]   - A callback function for the event (optional)\n[bouncetime] - Switch bounce timeout in ms for callback"},
   {"remove_event_detect", py_remove_event_detect, METH_VARARGS, "Remove edge detection for a particular GPIO channel\ngpio - gpio channel"},
   {"event_detected", py_event_detected, METH_VARARGS, "Returns True if an edge has occured on a given GPIO.  You need to enable edge detection using add_event_detect() first.\ngpio - gpio channel"},
   {"add_event_callback", (PyCFunction)py_add_event_callback, METH_VARARGS | METH_KEYWORDS, "Add a callback for an event already defined using add_event_detect()\ngpio         - gpio channel\ncallback     - a callback function\n[bouncetime] - Switch bounce timeout in ms"},
   {"wait_for_edge", py_wait_for_edge, METH_VARARGS, "Wait for an edge.\ngpio - gpio channel\nedge - RISING, FALLING or BOTH\ntimeout (optional) - time to wait in miliseconds. -1 will wait forever (default)"},
   {"gpio_function", py_gpio_function, METH_VARARGS, "Return the current GPIO function (IN, OUT, ALT0)\ngpio - gpio channel"},
   {"setwarnings", py_setwarnings, METH_VARARGS, "Enable or disable warning messages"},
   {"get_gpio_base", py_gpio_base, METH_VARARGS, "Get the XIO base number for sysfs"},
   {"selftest", py_selftest, METH_VARARGS, "Internal unit tests"},
   {"direction", (PyCFunction)py_set_direction, METH_VARARGS | METH_KEYWORDS, "Change direction of gpio channel. Either INPUT or OUTPUT\n" },
   {"setmode", (PyCFunction)py_setmode, METH_VARARGS, "Dummy function that does nothing but maintain compatibility with RPi.GPIO\n" },
   {"toggle_debug", py_toggle_debug, METH_VARARGS, "Toggles the enabling/disabling of Debug print output"},
   {"is_chip_pro", py_is_chip_pro, METH_VARARGS, "Is hardware a CHIP Pro? Boolean False for normal CHIP/PocketCHIP (R8 SOC)"},
   {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION > 2
static struct PyModuleDef chipgpiomodule = {
   PyModuleDef_HEAD_INIT,
   "GPIO",       // name of module
   moduledocstring,  // module documentation, may be NULL
   -1,               // size of per-interpreter state of the module, or -1 if the module keeps state in global variables.
   gpio_methods
};
#endif

#if PY_MAJOR_VERSION > 2
PyMODINIT_FUNC PyInit_GPIO(void)
#else
PyMODINIT_FUNC initGPIO(void)
#endif
{
   PyObject *module = NULL;

   clear_error_msg();

#if PY_MAJOR_VERSION > 2
   if ((module = PyModule_Create(&chipgpiomodule)) == NULL)
      return NULL;
#else
   if ((module = Py_InitModule3("GPIO", gpio_methods, moduledocstring)) == NULL)
      return;
#endif

   define_constants(module);

   if (!PyEval_ThreadsInitialized())
      PyEval_InitThreads();

   if (Py_AtExit(event_cleanup) != 0)
   {
      setup_error = 1;
      event_cleanup();
#if PY_MAJOR_VERSION > 2
      return NULL;
#else
      return;
#endif
   }

#if PY_MAJOR_VERSION > 2
   return module;
#else
   return;
#endif
}
