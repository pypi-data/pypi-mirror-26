// This file contains helper functions that are automatically created from
// templates.

#include "nuitka/prelude.h"

extern PyObject *callPythonFunction( PyObject *func, PyObject **args, int count );


PyObject *CALL_FUNCTION_WITH_ARGS1( PyObject *called, PyObject **args )
{
    CHECK_OBJECT( called );

    // Check if arguments are valid objects in debug mode.
#ifndef __NUITKA_NO_ASSERT__
    for( size_t i = 0; i < 1; i++ )
    {
        CHECK_OBJECT( args[ i ] );
    }
#endif

    if ( Nuitka_Function_Check( called ) )
    {
        if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
        {
            return NULL;
        }

        struct Nuitka_FunctionObject *function = (struct Nuitka_FunctionObject *)called;
        PyObject *result;

        if ( function->m_args_simple && 1 == function->m_args_positional_count )
        {
            for( Py_ssize_t i = 0; i < 1; i++ )
            {
                Py_INCREF( args[ i ] );
            }

            result = function->m_c_code( function, args );
        }
        else if ( function->m_args_simple && 1 + function->m_defaults_given == function->m_args_positional_count )
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
            PyObject *python_pars[ function->m_args_positional_count ];
#endif
            memcpy( python_pars, args, 1 * sizeof(PyObject *) );
            memcpy( python_pars + 1, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

            for( Py_ssize_t i = 0; i < function->m_args_positional_count; i++ )
            {
                Py_INCREF( python_pars[ i ] );
            }

            result = function->m_c_code( function, python_pars );
        }
        else
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
            PyObject *python_pars[ function->m_args_overall_count ];
#endif
            memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

            if ( parseArgumentsPos( function, python_pars, args, 1 ))
            {
                result = function->m_c_code( function, python_pars );
            }
            else
            {
                result = NULL;
            }
        }

        Py_LeaveRecursiveCall();

        return result;
    }
    else if ( Nuitka_Method_Check( called ) )
    {
        struct Nuitka_MethodObject *method = (struct Nuitka_MethodObject *)called;

        // Unbound method without arguments, let the error path be slow.
        if ( method->m_object != NULL )
        {
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }

            struct Nuitka_FunctionObject *function = method->m_function;

            PyObject *result;

            if ( function->m_args_simple && 1 + 1 == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                for( Py_ssize_t i = 0; i < 1; i++ )
                {
                    python_pars[ i + 1 ] = args[ i ];
                    Py_INCREF( args[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else if ( function->m_args_simple && 1 + 1 + function->m_defaults_given == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                memcpy( python_pars+1, args, 1 * sizeof(PyObject *) );
                memcpy( python_pars+1 + 1, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

                for( Py_ssize_t i = 1; i < function->m_args_overall_count; i++ )
                {
                    Py_INCREF( python_pars[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
                PyObject *python_pars[ function->m_args_overall_count ];
#endif
                memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

                if ( parseArgumentsMethodPos( function, python_pars, method->m_object, args, 1 ) )
                {
                    result = function->m_c_code( function, python_pars );
                }
                else
                {
                    result = NULL;
                }
            }

            Py_LeaveRecursiveCall();

            return result;
        }
    }
    else if ( PyCFunction_Check( called ) )
    {
        // Try to be fast about wrapping the arguments.
        int flags = PyCFunction_GET_FLAGS( called ) & ~(METH_CLASS | METH_STATIC | METH_COEXIST);

        if ( flags & METH_NOARGS )
        {
#if 1 == 0
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, NULL );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(
                PyExc_TypeError,
                "%s() takes no arguments (1 given)",
                ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_O )
        {
#if 1 == 1
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, args[0] );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(PyExc_TypeError,
                "%s() takes exactly one argument (1 given)",
                 ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_VARARGS )
        {
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            PyObject *pos_args = MAKE_TUPLE( args, 1 );

            PyObject *result;

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

#if PYTHON_VERSION < 360
            if ( flags & METH_KEYWORDS )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else
            {
                result = (*method)( self, pos_args );
            }
#else
            if ( flags == ( METH_VARARGS | METH_KEYWORDS ) )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else if ( flags == METH_FASTCALL )
            {
                result = (*(_PyCFunctionFast)method)( self, &PyTuple_GET_ITEM( pos_args, 0 ), 1, NULL );;
            }
            else
            {
                result = (*method)( self, pos_args );
            }
#endif

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
                // Some buggy C functions do set an error, but do not indicate it
                // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                Py_DECREF( pos_args );
                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                Py_DECREF( pos_args );
                return NULL;
            }
        }
    }
    else if ( PyFunction_Check( called ) )
    {
        return callPythonFunction(
            called,
            args,
            1
        );
    }

    PyObject *pos_args = MAKE_TUPLE( args, 1 );

    PyObject *result = CALL_FUNCTION(
        called,
        pos_args,
        NULL
    );

    Py_DECREF( pos_args );

    return result;
}

PyObject *CALL_FUNCTION_WITH_ARGS2( PyObject *called, PyObject **args )
{
    CHECK_OBJECT( called );

    // Check if arguments are valid objects in debug mode.
#ifndef __NUITKA_NO_ASSERT__
    for( size_t i = 0; i < 2; i++ )
    {
        CHECK_OBJECT( args[ i ] );
    }
#endif

    if ( Nuitka_Function_Check( called ) )
    {
        if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
        {
            return NULL;
        }

        struct Nuitka_FunctionObject *function = (struct Nuitka_FunctionObject *)called;
        PyObject *result;

        if ( function->m_args_simple && 2 == function->m_args_positional_count )
        {
            for( Py_ssize_t i = 0; i < 2; i++ )
            {
                Py_INCREF( args[ i ] );
            }

            result = function->m_c_code( function, args );
        }
        else if ( function->m_args_simple && 2 + function->m_defaults_given == function->m_args_positional_count )
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
            PyObject *python_pars[ function->m_args_positional_count ];
#endif
            memcpy( python_pars, args, 2 * sizeof(PyObject *) );
            memcpy( python_pars + 2, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

            for( Py_ssize_t i = 0; i < function->m_args_positional_count; i++ )
            {
                Py_INCREF( python_pars[ i ] );
            }

            result = function->m_c_code( function, python_pars );
        }
        else
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
            PyObject *python_pars[ function->m_args_overall_count ];
#endif
            memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

            if ( parseArgumentsPos( function, python_pars, args, 2 ))
            {
                result = function->m_c_code( function, python_pars );
            }
            else
            {
                result = NULL;
            }
        }

        Py_LeaveRecursiveCall();

        return result;
    }
    else if ( Nuitka_Method_Check( called ) )
    {
        struct Nuitka_MethodObject *method = (struct Nuitka_MethodObject *)called;

        // Unbound method without arguments, let the error path be slow.
        if ( method->m_object != NULL )
        {
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }

            struct Nuitka_FunctionObject *function = method->m_function;

            PyObject *result;

            if ( function->m_args_simple && 2 + 1 == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                for( Py_ssize_t i = 0; i < 2; i++ )
                {
                    python_pars[ i + 1 ] = args[ i ];
                    Py_INCREF( args[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else if ( function->m_args_simple && 2 + 1 + function->m_defaults_given == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                memcpy( python_pars+1, args, 2 * sizeof(PyObject *) );
                memcpy( python_pars+1 + 2, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

                for( Py_ssize_t i = 1; i < function->m_args_overall_count; i++ )
                {
                    Py_INCREF( python_pars[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
                PyObject *python_pars[ function->m_args_overall_count ];
#endif
                memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

                if ( parseArgumentsMethodPos( function, python_pars, method->m_object, args, 2 ) )
                {
                    result = function->m_c_code( function, python_pars );
                }
                else
                {
                    result = NULL;
                }
            }

            Py_LeaveRecursiveCall();

            return result;
        }
    }
    else if ( PyCFunction_Check( called ) )
    {
        // Try to be fast about wrapping the arguments.
        int flags = PyCFunction_GET_FLAGS( called ) & ~(METH_CLASS | METH_STATIC | METH_COEXIST);

        if ( flags & METH_NOARGS )
        {
#if 2 == 0
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, NULL );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(
                PyExc_TypeError,
                "%s() takes no arguments (2 given)",
                ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_O )
        {
#if 2 == 1
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, args[0] );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(PyExc_TypeError,
                "%s() takes exactly one argument (2 given)",
                 ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_VARARGS )
        {
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            PyObject *pos_args = MAKE_TUPLE( args, 2 );

            PyObject *result;

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

#if PYTHON_VERSION < 360
            if ( flags & METH_KEYWORDS )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else
            {
                result = (*method)( self, pos_args );
            }
#else
            if ( flags == ( METH_VARARGS | METH_KEYWORDS ) )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else if ( flags == METH_FASTCALL )
            {
                result = (*(_PyCFunctionFast)method)( self, &PyTuple_GET_ITEM( pos_args, 0 ), 2, NULL );;
            }
            else
            {
                result = (*method)( self, pos_args );
            }
#endif

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
                // Some buggy C functions do set an error, but do not indicate it
                // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                Py_DECREF( pos_args );
                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                Py_DECREF( pos_args );
                return NULL;
            }
        }
    }
    else if ( PyFunction_Check( called ) )
    {
        return callPythonFunction(
            called,
            args,
            2
        );
    }

    PyObject *pos_args = MAKE_TUPLE( args, 2 );

    PyObject *result = CALL_FUNCTION(
        called,
        pos_args,
        NULL
    );

    Py_DECREF( pos_args );

    return result;
}

PyObject *CALL_FUNCTION_WITH_ARGS3( PyObject *called, PyObject **args )
{
    CHECK_OBJECT( called );

    // Check if arguments are valid objects in debug mode.
#ifndef __NUITKA_NO_ASSERT__
    for( size_t i = 0; i < 3; i++ )
    {
        CHECK_OBJECT( args[ i ] );
    }
#endif

    if ( Nuitka_Function_Check( called ) )
    {
        if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
        {
            return NULL;
        }

        struct Nuitka_FunctionObject *function = (struct Nuitka_FunctionObject *)called;
        PyObject *result;

        if ( function->m_args_simple && 3 == function->m_args_positional_count )
        {
            for( Py_ssize_t i = 0; i < 3; i++ )
            {
                Py_INCREF( args[ i ] );
            }

            result = function->m_c_code( function, args );
        }
        else if ( function->m_args_simple && 3 + function->m_defaults_given == function->m_args_positional_count )
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
            PyObject *python_pars[ function->m_args_positional_count ];
#endif
            memcpy( python_pars, args, 3 * sizeof(PyObject *) );
            memcpy( python_pars + 3, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

            for( Py_ssize_t i = 0; i < function->m_args_positional_count; i++ )
            {
                Py_INCREF( python_pars[ i ] );
            }

            result = function->m_c_code( function, python_pars );
        }
        else
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
            PyObject *python_pars[ function->m_args_overall_count ];
#endif
            memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

            if ( parseArgumentsPos( function, python_pars, args, 3 ))
            {
                result = function->m_c_code( function, python_pars );
            }
            else
            {
                result = NULL;
            }
        }

        Py_LeaveRecursiveCall();

        return result;
    }
    else if ( Nuitka_Method_Check( called ) )
    {
        struct Nuitka_MethodObject *method = (struct Nuitka_MethodObject *)called;

        // Unbound method without arguments, let the error path be slow.
        if ( method->m_object != NULL )
        {
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }

            struct Nuitka_FunctionObject *function = method->m_function;

            PyObject *result;

            if ( function->m_args_simple && 3 + 1 == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                for( Py_ssize_t i = 0; i < 3; i++ )
                {
                    python_pars[ i + 1 ] = args[ i ];
                    Py_INCREF( args[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else if ( function->m_args_simple && 3 + 1 + function->m_defaults_given == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                memcpy( python_pars+1, args, 3 * sizeof(PyObject *) );
                memcpy( python_pars+1 + 3, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

                for( Py_ssize_t i = 1; i < function->m_args_overall_count; i++ )
                {
                    Py_INCREF( python_pars[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
                PyObject *python_pars[ function->m_args_overall_count ];
#endif
                memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

                if ( parseArgumentsMethodPos( function, python_pars, method->m_object, args, 3 ) )
                {
                    result = function->m_c_code( function, python_pars );
                }
                else
                {
                    result = NULL;
                }
            }

            Py_LeaveRecursiveCall();

            return result;
        }
    }
    else if ( PyCFunction_Check( called ) )
    {
        // Try to be fast about wrapping the arguments.
        int flags = PyCFunction_GET_FLAGS( called ) & ~(METH_CLASS | METH_STATIC | METH_COEXIST);

        if ( flags & METH_NOARGS )
        {
#if 3 == 0
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, NULL );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(
                PyExc_TypeError,
                "%s() takes no arguments (3 given)",
                ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_O )
        {
#if 3 == 1
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, args[0] );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(PyExc_TypeError,
                "%s() takes exactly one argument (3 given)",
                 ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_VARARGS )
        {
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            PyObject *pos_args = MAKE_TUPLE( args, 3 );

            PyObject *result;

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

#if PYTHON_VERSION < 360
            if ( flags & METH_KEYWORDS )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else
            {
                result = (*method)( self, pos_args );
            }
#else
            if ( flags == ( METH_VARARGS | METH_KEYWORDS ) )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else if ( flags == METH_FASTCALL )
            {
                result = (*(_PyCFunctionFast)method)( self, &PyTuple_GET_ITEM( pos_args, 0 ), 3, NULL );;
            }
            else
            {
                result = (*method)( self, pos_args );
            }
#endif

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
                // Some buggy C functions do set an error, but do not indicate it
                // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                Py_DECREF( pos_args );
                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                Py_DECREF( pos_args );
                return NULL;
            }
        }
    }
    else if ( PyFunction_Check( called ) )
    {
        return callPythonFunction(
            called,
            args,
            3
        );
    }

    PyObject *pos_args = MAKE_TUPLE( args, 3 );

    PyObject *result = CALL_FUNCTION(
        called,
        pos_args,
        NULL
    );

    Py_DECREF( pos_args );

    return result;
}

PyObject *CALL_FUNCTION_WITH_ARGS4( PyObject *called, PyObject **args )
{
    CHECK_OBJECT( called );

    // Check if arguments are valid objects in debug mode.
#ifndef __NUITKA_NO_ASSERT__
    for( size_t i = 0; i < 4; i++ )
    {
        CHECK_OBJECT( args[ i ] );
    }
#endif

    if ( Nuitka_Function_Check( called ) )
    {
        if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
        {
            return NULL;
        }

        struct Nuitka_FunctionObject *function = (struct Nuitka_FunctionObject *)called;
        PyObject *result;

        if ( function->m_args_simple && 4 == function->m_args_positional_count )
        {
            for( Py_ssize_t i = 0; i < 4; i++ )
            {
                Py_INCREF( args[ i ] );
            }

            result = function->m_c_code( function, args );
        }
        else if ( function->m_args_simple && 4 + function->m_defaults_given == function->m_args_positional_count )
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
            PyObject *python_pars[ function->m_args_positional_count ];
#endif
            memcpy( python_pars, args, 4 * sizeof(PyObject *) );
            memcpy( python_pars + 4, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

            for( Py_ssize_t i = 0; i < function->m_args_positional_count; i++ )
            {
                Py_INCREF( python_pars[ i ] );
            }

            result = function->m_c_code( function, python_pars );
        }
        else
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
            PyObject *python_pars[ function->m_args_overall_count ];
#endif
            memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

            if ( parseArgumentsPos( function, python_pars, args, 4 ))
            {
                result = function->m_c_code( function, python_pars );
            }
            else
            {
                result = NULL;
            }
        }

        Py_LeaveRecursiveCall();

        return result;
    }
    else if ( Nuitka_Method_Check( called ) )
    {
        struct Nuitka_MethodObject *method = (struct Nuitka_MethodObject *)called;

        // Unbound method without arguments, let the error path be slow.
        if ( method->m_object != NULL )
        {
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }

            struct Nuitka_FunctionObject *function = method->m_function;

            PyObject *result;

            if ( function->m_args_simple && 4 + 1 == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                for( Py_ssize_t i = 0; i < 4; i++ )
                {
                    python_pars[ i + 1 ] = args[ i ];
                    Py_INCREF( args[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else if ( function->m_args_simple && 4 + 1 + function->m_defaults_given == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                memcpy( python_pars+1, args, 4 * sizeof(PyObject *) );
                memcpy( python_pars+1 + 4, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

                for( Py_ssize_t i = 1; i < function->m_args_overall_count; i++ )
                {
                    Py_INCREF( python_pars[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
                PyObject *python_pars[ function->m_args_overall_count ];
#endif
                memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

                if ( parseArgumentsMethodPos( function, python_pars, method->m_object, args, 4 ) )
                {
                    result = function->m_c_code( function, python_pars );
                }
                else
                {
                    result = NULL;
                }
            }

            Py_LeaveRecursiveCall();

            return result;
        }
    }
    else if ( PyCFunction_Check( called ) )
    {
        // Try to be fast about wrapping the arguments.
        int flags = PyCFunction_GET_FLAGS( called ) & ~(METH_CLASS | METH_STATIC | METH_COEXIST);

        if ( flags & METH_NOARGS )
        {
#if 4 == 0
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, NULL );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(
                PyExc_TypeError,
                "%s() takes no arguments (4 given)",
                ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_O )
        {
#if 4 == 1
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, args[0] );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(PyExc_TypeError,
                "%s() takes exactly one argument (4 given)",
                 ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_VARARGS )
        {
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            PyObject *pos_args = MAKE_TUPLE( args, 4 );

            PyObject *result;

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

#if PYTHON_VERSION < 360
            if ( flags & METH_KEYWORDS )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else
            {
                result = (*method)( self, pos_args );
            }
#else
            if ( flags == ( METH_VARARGS | METH_KEYWORDS ) )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else if ( flags == METH_FASTCALL )
            {
                result = (*(_PyCFunctionFast)method)( self, &PyTuple_GET_ITEM( pos_args, 0 ), 4, NULL );;
            }
            else
            {
                result = (*method)( self, pos_args );
            }
#endif

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
                // Some buggy C functions do set an error, but do not indicate it
                // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                Py_DECREF( pos_args );
                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                Py_DECREF( pos_args );
                return NULL;
            }
        }
    }
    else if ( PyFunction_Check( called ) )
    {
        return callPythonFunction(
            called,
            args,
            4
        );
    }

    PyObject *pos_args = MAKE_TUPLE( args, 4 );

    PyObject *result = CALL_FUNCTION(
        called,
        pos_args,
        NULL
    );

    Py_DECREF( pos_args );

    return result;
}

PyObject *CALL_FUNCTION_WITH_ARGS5( PyObject *called, PyObject **args )
{
    CHECK_OBJECT( called );

    // Check if arguments are valid objects in debug mode.
#ifndef __NUITKA_NO_ASSERT__
    for( size_t i = 0; i < 5; i++ )
    {
        CHECK_OBJECT( args[ i ] );
    }
#endif

    if ( Nuitka_Function_Check( called ) )
    {
        if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
        {
            return NULL;
        }

        struct Nuitka_FunctionObject *function = (struct Nuitka_FunctionObject *)called;
        PyObject *result;

        if ( function->m_args_simple && 5 == function->m_args_positional_count )
        {
            for( Py_ssize_t i = 0; i < 5; i++ )
            {
                Py_INCREF( args[ i ] );
            }

            result = function->m_c_code( function, args );
        }
        else if ( function->m_args_simple && 5 + function->m_defaults_given == function->m_args_positional_count )
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
            PyObject *python_pars[ function->m_args_positional_count ];
#endif
            memcpy( python_pars, args, 5 * sizeof(PyObject *) );
            memcpy( python_pars + 5, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

            for( Py_ssize_t i = 0; i < function->m_args_positional_count; i++ )
            {
                Py_INCREF( python_pars[ i ] );
            }

            result = function->m_c_code( function, python_pars );
        }
        else
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
            PyObject *python_pars[ function->m_args_overall_count ];
#endif
            memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

            if ( parseArgumentsPos( function, python_pars, args, 5 ))
            {
                result = function->m_c_code( function, python_pars );
            }
            else
            {
                result = NULL;
            }
        }

        Py_LeaveRecursiveCall();

        return result;
    }
    else if ( Nuitka_Method_Check( called ) )
    {
        struct Nuitka_MethodObject *method = (struct Nuitka_MethodObject *)called;

        // Unbound method without arguments, let the error path be slow.
        if ( method->m_object != NULL )
        {
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }

            struct Nuitka_FunctionObject *function = method->m_function;

            PyObject *result;

            if ( function->m_args_simple && 5 + 1 == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                for( Py_ssize_t i = 0; i < 5; i++ )
                {
                    python_pars[ i + 1 ] = args[ i ];
                    Py_INCREF( args[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else if ( function->m_args_simple && 5 + 1 + function->m_defaults_given == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                memcpy( python_pars+1, args, 5 * sizeof(PyObject *) );
                memcpy( python_pars+1 + 5, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

                for( Py_ssize_t i = 1; i < function->m_args_overall_count; i++ )
                {
                    Py_INCREF( python_pars[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
                PyObject *python_pars[ function->m_args_overall_count ];
#endif
                memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

                if ( parseArgumentsMethodPos( function, python_pars, method->m_object, args, 5 ) )
                {
                    result = function->m_c_code( function, python_pars );
                }
                else
                {
                    result = NULL;
                }
            }

            Py_LeaveRecursiveCall();

            return result;
        }
    }
    else if ( PyCFunction_Check( called ) )
    {
        // Try to be fast about wrapping the arguments.
        int flags = PyCFunction_GET_FLAGS( called ) & ~(METH_CLASS | METH_STATIC | METH_COEXIST);

        if ( flags & METH_NOARGS )
        {
#if 5 == 0
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, NULL );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(
                PyExc_TypeError,
                "%s() takes no arguments (5 given)",
                ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_O )
        {
#if 5 == 1
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, args[0] );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(PyExc_TypeError,
                "%s() takes exactly one argument (5 given)",
                 ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_VARARGS )
        {
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            PyObject *pos_args = MAKE_TUPLE( args, 5 );

            PyObject *result;

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

#if PYTHON_VERSION < 360
            if ( flags & METH_KEYWORDS )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else
            {
                result = (*method)( self, pos_args );
            }
#else
            if ( flags == ( METH_VARARGS | METH_KEYWORDS ) )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else if ( flags == METH_FASTCALL )
            {
                result = (*(_PyCFunctionFast)method)( self, &PyTuple_GET_ITEM( pos_args, 0 ), 5, NULL );;
            }
            else
            {
                result = (*method)( self, pos_args );
            }
#endif

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
                // Some buggy C functions do set an error, but do not indicate it
                // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                Py_DECREF( pos_args );
                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                Py_DECREF( pos_args );
                return NULL;
            }
        }
    }
    else if ( PyFunction_Check( called ) )
    {
        return callPythonFunction(
            called,
            args,
            5
        );
    }

    PyObject *pos_args = MAKE_TUPLE( args, 5 );

    PyObject *result = CALL_FUNCTION(
        called,
        pos_args,
        NULL
    );

    Py_DECREF( pos_args );

    return result;
}

PyObject *CALL_FUNCTION_WITH_ARGS6( PyObject *called, PyObject **args )
{
    CHECK_OBJECT( called );

    // Check if arguments are valid objects in debug mode.
#ifndef __NUITKA_NO_ASSERT__
    for( size_t i = 0; i < 6; i++ )
    {
        CHECK_OBJECT( args[ i ] );
    }
#endif

    if ( Nuitka_Function_Check( called ) )
    {
        if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
        {
            return NULL;
        }

        struct Nuitka_FunctionObject *function = (struct Nuitka_FunctionObject *)called;
        PyObject *result;

        if ( function->m_args_simple && 6 == function->m_args_positional_count )
        {
            for( Py_ssize_t i = 0; i < 6; i++ )
            {
                Py_INCREF( args[ i ] );
            }

            result = function->m_c_code( function, args );
        }
        else if ( function->m_args_simple && 6 + function->m_defaults_given == function->m_args_positional_count )
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
            PyObject *python_pars[ function->m_args_positional_count ];
#endif
            memcpy( python_pars, args, 6 * sizeof(PyObject *) );
            memcpy( python_pars + 6, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

            for( Py_ssize_t i = 0; i < function->m_args_positional_count; i++ )
            {
                Py_INCREF( python_pars[ i ] );
            }

            result = function->m_c_code( function, python_pars );
        }
        else
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
            PyObject *python_pars[ function->m_args_overall_count ];
#endif
            memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

            if ( parseArgumentsPos( function, python_pars, args, 6 ))
            {
                result = function->m_c_code( function, python_pars );
            }
            else
            {
                result = NULL;
            }
        }

        Py_LeaveRecursiveCall();

        return result;
    }
    else if ( Nuitka_Method_Check( called ) )
    {
        struct Nuitka_MethodObject *method = (struct Nuitka_MethodObject *)called;

        // Unbound method without arguments, let the error path be slow.
        if ( method->m_object != NULL )
        {
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }

            struct Nuitka_FunctionObject *function = method->m_function;

            PyObject *result;

            if ( function->m_args_simple && 6 + 1 == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                for( Py_ssize_t i = 0; i < 6; i++ )
                {
                    python_pars[ i + 1 ] = args[ i ];
                    Py_INCREF( args[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else if ( function->m_args_simple && 6 + 1 + function->m_defaults_given == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                memcpy( python_pars+1, args, 6 * sizeof(PyObject *) );
                memcpy( python_pars+1 + 6, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

                for( Py_ssize_t i = 1; i < function->m_args_overall_count; i++ )
                {
                    Py_INCREF( python_pars[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
                PyObject *python_pars[ function->m_args_overall_count ];
#endif
                memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

                if ( parseArgumentsMethodPos( function, python_pars, method->m_object, args, 6 ) )
                {
                    result = function->m_c_code( function, python_pars );
                }
                else
                {
                    result = NULL;
                }
            }

            Py_LeaveRecursiveCall();

            return result;
        }
    }
    else if ( PyCFunction_Check( called ) )
    {
        // Try to be fast about wrapping the arguments.
        int flags = PyCFunction_GET_FLAGS( called ) & ~(METH_CLASS | METH_STATIC | METH_COEXIST);

        if ( flags & METH_NOARGS )
        {
#if 6 == 0
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, NULL );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(
                PyExc_TypeError,
                "%s() takes no arguments (6 given)",
                ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_O )
        {
#if 6 == 1
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, args[0] );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(PyExc_TypeError,
                "%s() takes exactly one argument (6 given)",
                 ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_VARARGS )
        {
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            PyObject *pos_args = MAKE_TUPLE( args, 6 );

            PyObject *result;

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

#if PYTHON_VERSION < 360
            if ( flags & METH_KEYWORDS )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else
            {
                result = (*method)( self, pos_args );
            }
#else
            if ( flags == ( METH_VARARGS | METH_KEYWORDS ) )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else if ( flags == METH_FASTCALL )
            {
                result = (*(_PyCFunctionFast)method)( self, &PyTuple_GET_ITEM( pos_args, 0 ), 6, NULL );;
            }
            else
            {
                result = (*method)( self, pos_args );
            }
#endif

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
                // Some buggy C functions do set an error, but do not indicate it
                // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                Py_DECREF( pos_args );
                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                Py_DECREF( pos_args );
                return NULL;
            }
        }
    }
    else if ( PyFunction_Check( called ) )
    {
        return callPythonFunction(
            called,
            args,
            6
        );
    }

    PyObject *pos_args = MAKE_TUPLE( args, 6 );

    PyObject *result = CALL_FUNCTION(
        called,
        pos_args,
        NULL
    );

    Py_DECREF( pos_args );

    return result;
}

PyObject *CALL_FUNCTION_WITH_ARGS7( PyObject *called, PyObject **args )
{
    CHECK_OBJECT( called );

    // Check if arguments are valid objects in debug mode.
#ifndef __NUITKA_NO_ASSERT__
    for( size_t i = 0; i < 7; i++ )
    {
        CHECK_OBJECT( args[ i ] );
    }
#endif

    if ( Nuitka_Function_Check( called ) )
    {
        if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
        {
            return NULL;
        }

        struct Nuitka_FunctionObject *function = (struct Nuitka_FunctionObject *)called;
        PyObject *result;

        if ( function->m_args_simple && 7 == function->m_args_positional_count )
        {
            for( Py_ssize_t i = 0; i < 7; i++ )
            {
                Py_INCREF( args[ i ] );
            }

            result = function->m_c_code( function, args );
        }
        else if ( function->m_args_simple && 7 + function->m_defaults_given == function->m_args_positional_count )
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
            PyObject *python_pars[ function->m_args_positional_count ];
#endif
            memcpy( python_pars, args, 7 * sizeof(PyObject *) );
            memcpy( python_pars + 7, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

            for( Py_ssize_t i = 0; i < function->m_args_positional_count; i++ )
            {
                Py_INCREF( python_pars[ i ] );
            }

            result = function->m_c_code( function, python_pars );
        }
        else
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
            PyObject *python_pars[ function->m_args_overall_count ];
#endif
            memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

            if ( parseArgumentsPos( function, python_pars, args, 7 ))
            {
                result = function->m_c_code( function, python_pars );
            }
            else
            {
                result = NULL;
            }
        }

        Py_LeaveRecursiveCall();

        return result;
    }
    else if ( Nuitka_Method_Check( called ) )
    {
        struct Nuitka_MethodObject *method = (struct Nuitka_MethodObject *)called;

        // Unbound method without arguments, let the error path be slow.
        if ( method->m_object != NULL )
        {
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }

            struct Nuitka_FunctionObject *function = method->m_function;

            PyObject *result;

            if ( function->m_args_simple && 7 + 1 == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                for( Py_ssize_t i = 0; i < 7; i++ )
                {
                    python_pars[ i + 1 ] = args[ i ];
                    Py_INCREF( args[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else if ( function->m_args_simple && 7 + 1 + function->m_defaults_given == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                memcpy( python_pars+1, args, 7 * sizeof(PyObject *) );
                memcpy( python_pars+1 + 7, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

                for( Py_ssize_t i = 1; i < function->m_args_overall_count; i++ )
                {
                    Py_INCREF( python_pars[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
                PyObject *python_pars[ function->m_args_overall_count ];
#endif
                memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

                if ( parseArgumentsMethodPos( function, python_pars, method->m_object, args, 7 ) )
                {
                    result = function->m_c_code( function, python_pars );
                }
                else
                {
                    result = NULL;
                }
            }

            Py_LeaveRecursiveCall();

            return result;
        }
    }
    else if ( PyCFunction_Check( called ) )
    {
        // Try to be fast about wrapping the arguments.
        int flags = PyCFunction_GET_FLAGS( called ) & ~(METH_CLASS | METH_STATIC | METH_COEXIST);

        if ( flags & METH_NOARGS )
        {
#if 7 == 0
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, NULL );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(
                PyExc_TypeError,
                "%s() takes no arguments (7 given)",
                ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_O )
        {
#if 7 == 1
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, args[0] );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(PyExc_TypeError,
                "%s() takes exactly one argument (7 given)",
                 ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_VARARGS )
        {
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            PyObject *pos_args = MAKE_TUPLE( args, 7 );

            PyObject *result;

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

#if PYTHON_VERSION < 360
            if ( flags & METH_KEYWORDS )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else
            {
                result = (*method)( self, pos_args );
            }
#else
            if ( flags == ( METH_VARARGS | METH_KEYWORDS ) )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else if ( flags == METH_FASTCALL )
            {
                result = (*(_PyCFunctionFast)method)( self, &PyTuple_GET_ITEM( pos_args, 0 ), 7, NULL );;
            }
            else
            {
                result = (*method)( self, pos_args );
            }
#endif

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
                // Some buggy C functions do set an error, but do not indicate it
                // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                Py_DECREF( pos_args );
                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                Py_DECREF( pos_args );
                return NULL;
            }
        }
    }
    else if ( PyFunction_Check( called ) )
    {
        return callPythonFunction(
            called,
            args,
            7
        );
    }

    PyObject *pos_args = MAKE_TUPLE( args, 7 );

    PyObject *result = CALL_FUNCTION(
        called,
        pos_args,
        NULL
    );

    Py_DECREF( pos_args );

    return result;
}

PyObject *CALL_FUNCTION_WITH_ARGS8( PyObject *called, PyObject **args )
{
    CHECK_OBJECT( called );

    // Check if arguments are valid objects in debug mode.
#ifndef __NUITKA_NO_ASSERT__
    for( size_t i = 0; i < 8; i++ )
    {
        CHECK_OBJECT( args[ i ] );
    }
#endif

    if ( Nuitka_Function_Check( called ) )
    {
        if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
        {
            return NULL;
        }

        struct Nuitka_FunctionObject *function = (struct Nuitka_FunctionObject *)called;
        PyObject *result;

        if ( function->m_args_simple && 8 == function->m_args_positional_count )
        {
            for( Py_ssize_t i = 0; i < 8; i++ )
            {
                Py_INCREF( args[ i ] );
            }

            result = function->m_c_code( function, args );
        }
        else if ( function->m_args_simple && 8 + function->m_defaults_given == function->m_args_positional_count )
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
            PyObject *python_pars[ function->m_args_positional_count ];
#endif
            memcpy( python_pars, args, 8 * sizeof(PyObject *) );
            memcpy( python_pars + 8, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

            for( Py_ssize_t i = 0; i < function->m_args_positional_count; i++ )
            {
                Py_INCREF( python_pars[ i ] );
            }

            result = function->m_c_code( function, python_pars );
        }
        else
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
            PyObject *python_pars[ function->m_args_overall_count ];
#endif
            memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

            if ( parseArgumentsPos( function, python_pars, args, 8 ))
            {
                result = function->m_c_code( function, python_pars );
            }
            else
            {
                result = NULL;
            }
        }

        Py_LeaveRecursiveCall();

        return result;
    }
    else if ( Nuitka_Method_Check( called ) )
    {
        struct Nuitka_MethodObject *method = (struct Nuitka_MethodObject *)called;

        // Unbound method without arguments, let the error path be slow.
        if ( method->m_object != NULL )
        {
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }

            struct Nuitka_FunctionObject *function = method->m_function;

            PyObject *result;

            if ( function->m_args_simple && 8 + 1 == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                for( Py_ssize_t i = 0; i < 8; i++ )
                {
                    python_pars[ i + 1 ] = args[ i ];
                    Py_INCREF( args[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else if ( function->m_args_simple && 8 + 1 + function->m_defaults_given == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                memcpy( python_pars+1, args, 8 * sizeof(PyObject *) );
                memcpy( python_pars+1 + 8, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

                for( Py_ssize_t i = 1; i < function->m_args_overall_count; i++ )
                {
                    Py_INCREF( python_pars[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
                PyObject *python_pars[ function->m_args_overall_count ];
#endif
                memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

                if ( parseArgumentsMethodPos( function, python_pars, method->m_object, args, 8 ) )
                {
                    result = function->m_c_code( function, python_pars );
                }
                else
                {
                    result = NULL;
                }
            }

            Py_LeaveRecursiveCall();

            return result;
        }
    }
    else if ( PyCFunction_Check( called ) )
    {
        // Try to be fast about wrapping the arguments.
        int flags = PyCFunction_GET_FLAGS( called ) & ~(METH_CLASS | METH_STATIC | METH_COEXIST);

        if ( flags & METH_NOARGS )
        {
#if 8 == 0
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, NULL );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(
                PyExc_TypeError,
                "%s() takes no arguments (8 given)",
                ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_O )
        {
#if 8 == 1
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, args[0] );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(PyExc_TypeError,
                "%s() takes exactly one argument (8 given)",
                 ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_VARARGS )
        {
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            PyObject *pos_args = MAKE_TUPLE( args, 8 );

            PyObject *result;

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

#if PYTHON_VERSION < 360
            if ( flags & METH_KEYWORDS )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else
            {
                result = (*method)( self, pos_args );
            }
#else
            if ( flags == ( METH_VARARGS | METH_KEYWORDS ) )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else if ( flags == METH_FASTCALL )
            {
                result = (*(_PyCFunctionFast)method)( self, &PyTuple_GET_ITEM( pos_args, 0 ), 8, NULL );;
            }
            else
            {
                result = (*method)( self, pos_args );
            }
#endif

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
                // Some buggy C functions do set an error, but do not indicate it
                // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                Py_DECREF( pos_args );
                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                Py_DECREF( pos_args );
                return NULL;
            }
        }
    }
    else if ( PyFunction_Check( called ) )
    {
        return callPythonFunction(
            called,
            args,
            8
        );
    }

    PyObject *pos_args = MAKE_TUPLE( args, 8 );

    PyObject *result = CALL_FUNCTION(
        called,
        pos_args,
        NULL
    );

    Py_DECREF( pos_args );

    return result;
}

PyObject *CALL_FUNCTION_WITH_ARGS10( PyObject *called, PyObject **args )
{
    CHECK_OBJECT( called );

    // Check if arguments are valid objects in debug mode.
#ifndef __NUITKA_NO_ASSERT__
    for( size_t i = 0; i < 10; i++ )
    {
        CHECK_OBJECT( args[ i ] );
    }
#endif

    if ( Nuitka_Function_Check( called ) )
    {
        if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
        {
            return NULL;
        }

        struct Nuitka_FunctionObject *function = (struct Nuitka_FunctionObject *)called;
        PyObject *result;

        if ( function->m_args_simple && 10 == function->m_args_positional_count )
        {
            for( Py_ssize_t i = 0; i < 10; i++ )
            {
                Py_INCREF( args[ i ] );
            }

            result = function->m_c_code( function, args );
        }
        else if ( function->m_args_simple && 10 + function->m_defaults_given == function->m_args_positional_count )
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
            PyObject *python_pars[ function->m_args_positional_count ];
#endif
            memcpy( python_pars, args, 10 * sizeof(PyObject *) );
            memcpy( python_pars + 10, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

            for( Py_ssize_t i = 0; i < function->m_args_positional_count; i++ )
            {
                Py_INCREF( python_pars[ i ] );
            }

            result = function->m_c_code( function, python_pars );
        }
        else
        {
#ifdef _MSC_VER
            PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
            PyObject *python_pars[ function->m_args_overall_count ];
#endif
            memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

            if ( parseArgumentsPos( function, python_pars, args, 10 ))
            {
                result = function->m_c_code( function, python_pars );
            }
            else
            {
                result = NULL;
            }
        }

        Py_LeaveRecursiveCall();

        return result;
    }
    else if ( Nuitka_Method_Check( called ) )
    {
        struct Nuitka_MethodObject *method = (struct Nuitka_MethodObject *)called;

        // Unbound method without arguments, let the error path be slow.
        if ( method->m_object != NULL )
        {
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }

            struct Nuitka_FunctionObject *function = method->m_function;

            PyObject *result;

            if ( function->m_args_simple && 10 + 1 == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                for( Py_ssize_t i = 0; i < 10; i++ )
                {
                    python_pars[ i + 1 ] = args[ i ];
                    Py_INCREF( args[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else if ( function->m_args_simple && 10 + 1 + function->m_defaults_given == function->m_args_positional_count )
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_positional_count );
#else
                PyObject *python_pars[ function->m_args_positional_count ];
#endif
                python_pars[ 0 ] = method->m_object;
                Py_INCREF( method->m_object );

                memcpy( python_pars+1, args, 10 * sizeof(PyObject *) );
                memcpy( python_pars+1 + 10, &PyTuple_GET_ITEM( function->m_defaults, 0 ), function->m_defaults_given * sizeof(PyObject *) );

                for( Py_ssize_t i = 1; i < function->m_args_overall_count; i++ )
                {
                    Py_INCREF( python_pars[ i ] );
                }

                result = function->m_c_code( function, python_pars );
            }
            else
            {
#ifdef _MSC_VER
                PyObject **python_pars = (PyObject **)_alloca( sizeof( PyObject * ) * function->m_args_overall_count );
#else
                PyObject *python_pars[ function->m_args_overall_count ];
#endif
                memset( python_pars, 0, function->m_args_overall_count * sizeof(PyObject *) );

                if ( parseArgumentsMethodPos( function, python_pars, method->m_object, args, 10 ) )
                {
                    result = function->m_c_code( function, python_pars );
                }
                else
                {
                    result = NULL;
                }
            }

            Py_LeaveRecursiveCall();

            return result;
        }
    }
    else if ( PyCFunction_Check( called ) )
    {
        // Try to be fast about wrapping the arguments.
        int flags = PyCFunction_GET_FLAGS( called ) & ~(METH_CLASS | METH_STATIC | METH_COEXIST);

        if ( flags & METH_NOARGS )
        {
#if 10 == 0
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, NULL );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(
                PyExc_TypeError,
                "%s() takes no arguments (10 given)",
                ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_O )
        {
#if 10 == 1
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

            PyObject *result = (*method)( self, args[0] );

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
            // Some buggy C functions do set an error, but do not indicate it
            // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                return NULL;
            }
#else
            PyErr_Format(PyExc_TypeError,
                "%s() takes exactly one argument (10 given)",
                 ((PyCFunctionObject *)called)->m_ml->ml_name
            );
            return NULL;
#endif
        }
        else if ( flags & METH_VARARGS )
        {
            PyCFunction method = PyCFunction_GET_FUNCTION( called );
            PyObject *self = PyCFunction_GET_SELF( called );

            PyObject *pos_args = MAKE_TUPLE( args, 10 );

            PyObject *result;

            // Recursion guard is not strictly necessary, as we already have
            // one on our way to here.
#ifdef _NUITKA_FULL_COMPAT
            if (unlikely( Py_EnterRecursiveCall( (char *)" while calling a Python object" ) ))
            {
                return NULL;
            }
#endif

#if PYTHON_VERSION < 360
            if ( flags & METH_KEYWORDS )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else
            {
                result = (*method)( self, pos_args );
            }
#else
            if ( flags == ( METH_VARARGS | METH_KEYWORDS ) )
            {
                result = (*(PyCFunctionWithKeywords)method)( self, pos_args, NULL );
            }
            else if ( flags == METH_FASTCALL )
            {
                result = (*(_PyCFunctionFast)method)( self, &PyTuple_GET_ITEM( pos_args, 0 ), 10, NULL );;
            }
            else
            {
                result = (*method)( self, pos_args );
            }
#endif

#ifdef _NUITKA_FULL_COMPAT
            Py_LeaveRecursiveCall();
#endif

            if ( result != NULL )
            {
                // Some buggy C functions do set an error, but do not indicate it
                // and Nuitka inner workings can get upset/confused from it.
                DROP_ERROR_OCCURRED();

                Py_DECREF( pos_args );
                return result;
            }
            else
            {
                // Other buggy C functions do this, return NULL, but with
                // no error set, not allowed.
                if (unlikely( !ERROR_OCCURRED() ))
                {
                    PyErr_Format(
                        PyExc_SystemError,
                        "NULL result without error in PyObject_Call"
                    );
                }

                Py_DECREF( pos_args );
                return NULL;
            }
        }
    }
    else if ( PyFunction_Check( called ) )
    {
        return callPythonFunction(
            called,
            args,
            10
        );
    }

    PyObject *pos_args = MAKE_TUPLE( args, 10 );

    PyObject *result = CALL_FUNCTION(
        called,
        pos_args,
        NULL
    );

    Py_DECREF( pos_args );

    return result;
}

PyObject *CALL_METHOD_WITH_ARGS1( PyObject *source, PyObject *attr_name, PyObject **args )
{
    CHECK_OBJECT( source );
    CHECK_OBJECT( attr_name );

    // Check if arguments are valid objects in debug mode.
#ifndef __NUITKA_NO_ASSERT__
    for( size_t i = 0; i < 1; i++ )
    {
        CHECK_OBJECT( args[ i ] );
    }
#endif

    PyTypeObject *type = Py_TYPE( source );

    if ( type->tp_getattro == PyObject_GenericGetAttr )
    {
        // Unfortunately this is required, although of cause rarely necessary.
        if (unlikely( type->tp_dict == NULL ))
        {
            if (unlikely( PyType_Ready( type ) < 0 ))
            {
                return NULL;
            }
        }

        PyObject *descr = _PyType_Lookup( type, attr_name );
        descrgetfunc func = NULL;

        if ( descr != NULL )
        {
            Py_INCREF( descr );

#if PYTHON_VERSION < 300
            if ( PyType_HasFeature( Py_TYPE( descr ), Py_TPFLAGS_HAVE_CLASS ) )
            {
#endif
                func = Py_TYPE( descr )->tp_descr_get;

                if ( func != NULL && PyDescr_IsData( descr ) )
                {
                    PyObject *called_object = func( descr, source, (PyObject *)type );
                    Py_DECREF( descr );

                    PyObject *result = CALL_FUNCTION_WITH_ARGS1(
                        called_object,
                        args
                    );
                    Py_DECREF( called_object );
                    return result;
                }
#if PYTHON_VERSION < 300
            }
#endif
        }

        Py_ssize_t dictoffset = type->tp_dictoffset;
        PyObject *dict = NULL;

        if ( dictoffset != 0 )
        {
            // Negative dictionary offsets have special meaning.
            if ( dictoffset < 0 )
            {
                Py_ssize_t tsize;
                size_t size;

                tsize = ((PyVarObject *)source)->ob_size;
                if (tsize < 0)
                    tsize = -tsize;
                size = _PyObject_VAR_SIZE( type, tsize );

                dictoffset += (long)size;
            }

            PyObject **dictptr = (PyObject **) ((char *)source + dictoffset);
            dict = *dictptr;
        }

        if ( dict != NULL )
        {
            CHECK_OBJECT( dict );

            Py_INCREF( dict );

            PyObject *called_object = PyDict_GetItem( dict, attr_name );

            if ( called_object != NULL )
            {
                Py_INCREF( called_object );
                Py_XDECREF( descr );
                Py_DECREF( dict );

                PyObject *result = CALL_FUNCTION_WITH_ARGS1(
                    called_object,
                    args
                );
                Py_DECREF( called_object );
                return result;
            }

            Py_DECREF( dict );
        }

        if ( func != NULL )
        {
            if ( func == Nuitka_Function_Type.tp_descr_get )
            {
                PyObject *result = Nuitka_CallMethodFunctionPosArgs(
                    (struct Nuitka_FunctionObject const *)descr,
                    source,
                    args,
                    1
                );

                Py_DECREF( descr );

                return result;
            }
            else
            {
                PyObject *called_object = func( descr, source, (PyObject *)type );
                CHECK_OBJECT( called_object );

                Py_DECREF( descr );

                PyObject *result = CALL_FUNCTION_WITH_ARGS1(
                    called_object,
                    args
                );
                Py_DECREF( called_object );

                return result;
            }
        }

        if ( descr != NULL )
        {
            CHECK_OBJECT( descr );
            return CALL_FUNCTION_WITH_ARGS1(
                descr,
                args
            );
        }

#if PYTHON_VERSION < 300
        PyErr_Format(
            PyExc_AttributeError,
            "'%s' object has no attribute '%s'",
            type->tp_name,
            PyString_AS_STRING( attr_name )
        );
#else
        PyErr_Format(
            PyExc_AttributeError,
            "'%s' object has no attribute '%U'",
            type->tp_name,
            attr_name
        );
#endif
        return NULL;
    }
#if PYTHON_VERSION < 300
    else if ( type == &PyInstance_Type )
    {
        PyInstanceObject *source_instance = (PyInstanceObject *)source;

        // The special cases have their own variant on the code generation level
        // as we are called with constants only.
        assert( attr_name != const_str_plain___dict__ );
        assert( attr_name != const_str_plain___class__ );

        // Try the instance dict first.
        PyObject *called_object = GET_STRING_DICT_VALUE(
            (PyDictObject *)source_instance->in_dict,
            (PyStringObject *)attr_name
        );

        // Note: The "called_object" was found without taking a reference,
        // so we need not release it in this branch.
        if ( called_object != NULL )
        {
            return CALL_FUNCTION_WITH_ARGS1( called_object, args );
        }

        // Then check the class dictionaries.
        called_object = FIND_ATTRIBUTE_IN_CLASS(
            source_instance->in_class,
            attr_name
        );

        // Note: The "called_object" was found without taking a reference,
        // so we need not release it in this branch.
        if ( called_object != NULL )
        {
            descrgetfunc descr_get = Py_TYPE( called_object )->tp_descr_get;

            if ( descr_get == Nuitka_Function_Type.tp_descr_get )
            {
                return Nuitka_CallMethodFunctionPosArgs(
                    (struct Nuitka_FunctionObject const *)called_object,
                    source,
                    args,
                    1
                );
            }
            else if ( descr_get != NULL )
            {
                PyObject *method = descr_get(
                    called_object,
                    source,
                    (PyObject *)source_instance->in_class
                );

                if (unlikely( method == NULL ))
                {
                    return NULL;
                }

                PyObject *result = CALL_FUNCTION_WITH_ARGS1( method, args );
                Py_DECREF( method );
                return result;
            }
            else
            {
                return CALL_FUNCTION_WITH_ARGS1( called_object, args );
            }

        }
        else if (unlikely( source_instance->in_class->cl_getattr == NULL ))
        {
            PyErr_Format(
                PyExc_AttributeError,
                "%s instance has no attribute '%s'",
                PyString_AS_STRING( source_instance->in_class->cl_name ),
                PyString_AS_STRING( attr_name )
            );

            return NULL;
        }
        else
        {
            // Finally allow the "__getattr__" override to provide it or else
            // it's an error.

            PyObject *args2[] = {
                source,
                attr_name
            };

            called_object = CALL_FUNCTION_WITH_ARGS2(
                source_instance->in_class->cl_getattr,
                args2
            );

            if (unlikely( called_object == NULL ))
            {
                return NULL;
            }

            PyObject *result = CALL_FUNCTION_WITH_ARGS1(
                called_object,
                args
            );
            Py_DECREF( called_object );
            return result;
        }
    }
#endif
    else if ( type->tp_getattro != NULL )
    {
        PyObject *called_object = (*type->tp_getattro)(
            source,
            attr_name
        );

        if (unlikely( called_object == NULL ))
        {
            return NULL;
        }

        PyObject *result = CALL_FUNCTION_WITH_ARGS1(
            called_object,
            args
        );
        Py_DECREF( called_object );
        return result;
    }
    else if ( type->tp_getattr != NULL )
    {
        PyObject *called_object = (*type->tp_getattr)(
            source,
            Nuitka_String_AsString_Unchecked( attr_name )
        );

        if (unlikely( called_object == NULL ))
        {
            return NULL;
        }

        PyObject *result = CALL_FUNCTION_WITH_ARGS1(
            called_object,
            args
        );
        Py_DECREF( called_object );
        return result;
    }
    else
    {
        PyErr_Format(
            PyExc_AttributeError,
            "'%s' object has no attribute '%s'",
            type->tp_name,
            Nuitka_String_AsString_Unchecked( attr_name )
        );

        return NULL;
    }
}

PyObject *CALL_METHOD_WITH_ARGS2( PyObject *source, PyObject *attr_name, PyObject **args )
{
    CHECK_OBJECT( source );
    CHECK_OBJECT( attr_name );

    // Check if arguments are valid objects in debug mode.
#ifndef __NUITKA_NO_ASSERT__
    for( size_t i = 0; i < 2; i++ )
    {
        CHECK_OBJECT( args[ i ] );
    }
#endif

    PyTypeObject *type = Py_TYPE( source );

    if ( type->tp_getattro == PyObject_GenericGetAttr )
    {
        // Unfortunately this is required, although of cause rarely necessary.
        if (unlikely( type->tp_dict == NULL ))
        {
            if (unlikely( PyType_Ready( type ) < 0 ))
            {
                return NULL;
            }
        }

        PyObject *descr = _PyType_Lookup( type, attr_name );
        descrgetfunc func = NULL;

        if ( descr != NULL )
        {
            Py_INCREF( descr );

#if PYTHON_VERSION < 300
            if ( PyType_HasFeature( Py_TYPE( descr ), Py_TPFLAGS_HAVE_CLASS ) )
            {
#endif
                func = Py_TYPE( descr )->tp_descr_get;

                if ( func != NULL && PyDescr_IsData( descr ) )
                {
                    PyObject *called_object = func( descr, source, (PyObject *)type );
                    Py_DECREF( descr );

                    PyObject *result = CALL_FUNCTION_WITH_ARGS2(
                        called_object,
                        args
                    );
                    Py_DECREF( called_object );
                    return result;
                }
#if PYTHON_VERSION < 300
            }
#endif
        }

        Py_ssize_t dictoffset = type->tp_dictoffset;
        PyObject *dict = NULL;

        if ( dictoffset != 0 )
        {
            // Negative dictionary offsets have special meaning.
            if ( dictoffset < 0 )
            {
                Py_ssize_t tsize;
                size_t size;

                tsize = ((PyVarObject *)source)->ob_size;
                if (tsize < 0)
                    tsize = -tsize;
                size = _PyObject_VAR_SIZE( type, tsize );

                dictoffset += (long)size;
            }

            PyObject **dictptr = (PyObject **) ((char *)source + dictoffset);
            dict = *dictptr;
        }

        if ( dict != NULL )
        {
            CHECK_OBJECT( dict );

            Py_INCREF( dict );

            PyObject *called_object = PyDict_GetItem( dict, attr_name );

            if ( called_object != NULL )
            {
                Py_INCREF( called_object );
                Py_XDECREF( descr );
                Py_DECREF( dict );

                PyObject *result = CALL_FUNCTION_WITH_ARGS2(
                    called_object,
                    args
                );
                Py_DECREF( called_object );
                return result;
            }

            Py_DECREF( dict );
        }

        if ( func != NULL )
        {
            if ( func == Nuitka_Function_Type.tp_descr_get )
            {
                PyObject *result = Nuitka_CallMethodFunctionPosArgs(
                    (struct Nuitka_FunctionObject const *)descr,
                    source,
                    args,
                    2
                );

                Py_DECREF( descr );

                return result;
            }
            else
            {
                PyObject *called_object = func( descr, source, (PyObject *)type );
                CHECK_OBJECT( called_object );

                Py_DECREF( descr );

                PyObject *result = CALL_FUNCTION_WITH_ARGS2(
                    called_object,
                    args
                );
                Py_DECREF( called_object );

                return result;
            }
        }

        if ( descr != NULL )
        {
            CHECK_OBJECT( descr );
            return CALL_FUNCTION_WITH_ARGS2(
                descr,
                args
            );
        }

#if PYTHON_VERSION < 300
        PyErr_Format(
            PyExc_AttributeError,
            "'%s' object has no attribute '%s'",
            type->tp_name,
            PyString_AS_STRING( attr_name )
        );
#else
        PyErr_Format(
            PyExc_AttributeError,
            "'%s' object has no attribute '%U'",
            type->tp_name,
            attr_name
        );
#endif
        return NULL;
    }
#if PYTHON_VERSION < 300
    else if ( type == &PyInstance_Type )
    {
        PyInstanceObject *source_instance = (PyInstanceObject *)source;

        // The special cases have their own variant on the code generation level
        // as we are called with constants only.
        assert( attr_name != const_str_plain___dict__ );
        assert( attr_name != const_str_plain___class__ );

        // Try the instance dict first.
        PyObject *called_object = GET_STRING_DICT_VALUE(
            (PyDictObject *)source_instance->in_dict,
            (PyStringObject *)attr_name
        );

        // Note: The "called_object" was found without taking a reference,
        // so we need not release it in this branch.
        if ( called_object != NULL )
        {
            return CALL_FUNCTION_WITH_ARGS2( called_object, args );
        }

        // Then check the class dictionaries.
        called_object = FIND_ATTRIBUTE_IN_CLASS(
            source_instance->in_class,
            attr_name
        );

        // Note: The "called_object" was found without taking a reference,
        // so we need not release it in this branch.
        if ( called_object != NULL )
        {
            descrgetfunc descr_get = Py_TYPE( called_object )->tp_descr_get;

            if ( descr_get == Nuitka_Function_Type.tp_descr_get )
            {
                return Nuitka_CallMethodFunctionPosArgs(
                    (struct Nuitka_FunctionObject const *)called_object,
                    source,
                    args,
                    2
                );
            }
            else if ( descr_get != NULL )
            {
                PyObject *method = descr_get(
                    called_object,
                    source,
                    (PyObject *)source_instance->in_class
                );

                if (unlikely( method == NULL ))
                {
                    return NULL;
                }

                PyObject *result = CALL_FUNCTION_WITH_ARGS2( method, args );
                Py_DECREF( method );
                return result;
            }
            else
            {
                return CALL_FUNCTION_WITH_ARGS2( called_object, args );
            }

        }
        else if (unlikely( source_instance->in_class->cl_getattr == NULL ))
        {
            PyErr_Format(
                PyExc_AttributeError,
                "%s instance has no attribute '%s'",
                PyString_AS_STRING( source_instance->in_class->cl_name ),
                PyString_AS_STRING( attr_name )
            );

            return NULL;
        }
        else
        {
            // Finally allow the "__getattr__" override to provide it or else
            // it's an error.

            PyObject *args2[] = {
                source,
                attr_name
            };

            called_object = CALL_FUNCTION_WITH_ARGS2(
                source_instance->in_class->cl_getattr,
                args2
            );

            if (unlikely( called_object == NULL ))
            {
                return NULL;
            }

            PyObject *result = CALL_FUNCTION_WITH_ARGS2(
                called_object,
                args
            );
            Py_DECREF( called_object );
            return result;
        }
    }
#endif
    else if ( type->tp_getattro != NULL )
    {
        PyObject *called_object = (*type->tp_getattro)(
            source,
            attr_name
        );

        if (unlikely( called_object == NULL ))
        {
            return NULL;
        }

        PyObject *result = CALL_FUNCTION_WITH_ARGS2(
            called_object,
            args
        );
        Py_DECREF( called_object );
        return result;
    }
    else if ( type->tp_getattr != NULL )
    {
        PyObject *called_object = (*type->tp_getattr)(
            source,
            Nuitka_String_AsString_Unchecked( attr_name )
        );

        if (unlikely( called_object == NULL ))
        {
            return NULL;
        }

        PyObject *result = CALL_FUNCTION_WITH_ARGS2(
            called_object,
            args
        );
        Py_DECREF( called_object );
        return result;
    }
    else
    {
        PyErr_Format(
            PyExc_AttributeError,
            "'%s' object has no attribute '%s'",
            type->tp_name,
            Nuitka_String_AsString_Unchecked( attr_name )
        );

        return NULL;
    }
}

PyObject *CALL_METHOD_WITH_ARGS3( PyObject *source, PyObject *attr_name, PyObject **args )
{
    CHECK_OBJECT( source );
    CHECK_OBJECT( attr_name );

    // Check if arguments are valid objects in debug mode.
#ifndef __NUITKA_NO_ASSERT__
    for( size_t i = 0; i < 3; i++ )
    {
        CHECK_OBJECT( args[ i ] );
    }
#endif

    PyTypeObject *type = Py_TYPE( source );

    if ( type->tp_getattro == PyObject_GenericGetAttr )
    {
        // Unfortunately this is required, although of cause rarely necessary.
        if (unlikely( type->tp_dict == NULL ))
        {
            if (unlikely( PyType_Ready( type ) < 0 ))
            {
                return NULL;
            }
        }

        PyObject *descr = _PyType_Lookup( type, attr_name );
        descrgetfunc func = NULL;

        if ( descr != NULL )
        {
            Py_INCREF( descr );

#if PYTHON_VERSION < 300
            if ( PyType_HasFeature( Py_TYPE( descr ), Py_TPFLAGS_HAVE_CLASS ) )
            {
#endif
                func = Py_TYPE( descr )->tp_descr_get;

                if ( func != NULL && PyDescr_IsData( descr ) )
                {
                    PyObject *called_object = func( descr, source, (PyObject *)type );
                    Py_DECREF( descr );

                    PyObject *result = CALL_FUNCTION_WITH_ARGS3(
                        called_object,
                        args
                    );
                    Py_DECREF( called_object );
                    return result;
                }
#if PYTHON_VERSION < 300
            }
#endif
        }

        Py_ssize_t dictoffset = type->tp_dictoffset;
        PyObject *dict = NULL;

        if ( dictoffset != 0 )
        {
            // Negative dictionary offsets have special meaning.
            if ( dictoffset < 0 )
            {
                Py_ssize_t tsize;
                size_t size;

                tsize = ((PyVarObject *)source)->ob_size;
                if (tsize < 0)
                    tsize = -tsize;
                size = _PyObject_VAR_SIZE( type, tsize );

                dictoffset += (long)size;
            }

            PyObject **dictptr = (PyObject **) ((char *)source + dictoffset);
            dict = *dictptr;
        }

        if ( dict != NULL )
        {
            CHECK_OBJECT( dict );

            Py_INCREF( dict );

            PyObject *called_object = PyDict_GetItem( dict, attr_name );

            if ( called_object != NULL )
            {
                Py_INCREF( called_object );
                Py_XDECREF( descr );
                Py_DECREF( dict );

                PyObject *result = CALL_FUNCTION_WITH_ARGS3(
                    called_object,
                    args
                );
                Py_DECREF( called_object );
                return result;
            }

            Py_DECREF( dict );
        }

        if ( func != NULL )
        {
            if ( func == Nuitka_Function_Type.tp_descr_get )
            {
                PyObject *result = Nuitka_CallMethodFunctionPosArgs(
                    (struct Nuitka_FunctionObject const *)descr,
                    source,
                    args,
                    3
                );

                Py_DECREF( descr );

                return result;
            }
            else
            {
                PyObject *called_object = func( descr, source, (PyObject *)type );
                CHECK_OBJECT( called_object );

                Py_DECREF( descr );

                PyObject *result = CALL_FUNCTION_WITH_ARGS3(
                    called_object,
                    args
                );
                Py_DECREF( called_object );

                return result;
            }
        }

        if ( descr != NULL )
        {
            CHECK_OBJECT( descr );
            return CALL_FUNCTION_WITH_ARGS3(
                descr,
                args
            );
        }

#if PYTHON_VERSION < 300
        PyErr_Format(
            PyExc_AttributeError,
            "'%s' object has no attribute '%s'",
            type->tp_name,
            PyString_AS_STRING( attr_name )
        );
#else
        PyErr_Format(
            PyExc_AttributeError,
            "'%s' object has no attribute '%U'",
            type->tp_name,
            attr_name
        );
#endif
        return NULL;
    }
#if PYTHON_VERSION < 300
    else if ( type == &PyInstance_Type )
    {
        PyInstanceObject *source_instance = (PyInstanceObject *)source;

        // The special cases have their own variant on the code generation level
        // as we are called with constants only.
        assert( attr_name != const_str_plain___dict__ );
        assert( attr_name != const_str_plain___class__ );

        // Try the instance dict first.
        PyObject *called_object = GET_STRING_DICT_VALUE(
            (PyDictObject *)source_instance->in_dict,
            (PyStringObject *)attr_name
        );

        // Note: The "called_object" was found without taking a reference,
        // so we need not release it in this branch.
        if ( called_object != NULL )
        {
            return CALL_FUNCTION_WITH_ARGS3( called_object, args );
        }

        // Then check the class dictionaries.
        called_object = FIND_ATTRIBUTE_IN_CLASS(
            source_instance->in_class,
            attr_name
        );

        // Note: The "called_object" was found without taking a reference,
        // so we need not release it in this branch.
        if ( called_object != NULL )
        {
            descrgetfunc descr_get = Py_TYPE( called_object )->tp_descr_get;

            if ( descr_get == Nuitka_Function_Type.tp_descr_get )
            {
                return Nuitka_CallMethodFunctionPosArgs(
                    (struct Nuitka_FunctionObject const *)called_object,
                    source,
                    args,
                    3
                );
            }
            else if ( descr_get != NULL )
            {
                PyObject *method = descr_get(
                    called_object,
                    source,
                    (PyObject *)source_instance->in_class
                );

                if (unlikely( method == NULL ))
                {
                    return NULL;
                }

                PyObject *result = CALL_FUNCTION_WITH_ARGS3( method, args );
                Py_DECREF( method );
                return result;
            }
            else
            {
                return CALL_FUNCTION_WITH_ARGS3( called_object, args );
            }

        }
        else if (unlikely( source_instance->in_class->cl_getattr == NULL ))
        {
            PyErr_Format(
                PyExc_AttributeError,
                "%s instance has no attribute '%s'",
                PyString_AS_STRING( source_instance->in_class->cl_name ),
                PyString_AS_STRING( attr_name )
            );

            return NULL;
        }
        else
        {
            // Finally allow the "__getattr__" override to provide it or else
            // it's an error.

            PyObject *args2[] = {
                source,
                attr_name
            };

            called_object = CALL_FUNCTION_WITH_ARGS2(
                source_instance->in_class->cl_getattr,
                args2
            );

            if (unlikely( called_object == NULL ))
            {
                return NULL;
            }

            PyObject *result = CALL_FUNCTION_WITH_ARGS3(
                called_object,
                args
            );
            Py_DECREF( called_object );
            return result;
        }
    }
#endif
    else if ( type->tp_getattro != NULL )
    {
        PyObject *called_object = (*type->tp_getattro)(
            source,
            attr_name
        );

        if (unlikely( called_object == NULL ))
        {
            return NULL;
        }

        PyObject *result = CALL_FUNCTION_WITH_ARGS3(
            called_object,
            args
        );
        Py_DECREF( called_object );
        return result;
    }
    else if ( type->tp_getattr != NULL )
    {
        PyObject *called_object = (*type->tp_getattr)(
            source,
            Nuitka_String_AsString_Unchecked( attr_name )
        );

        if (unlikely( called_object == NULL ))
        {
            return NULL;
        }

        PyObject *result = CALL_FUNCTION_WITH_ARGS3(
            called_object,
            args
        );
        Py_DECREF( called_object );
        return result;
    }
    else
    {
        PyErr_Format(
            PyExc_AttributeError,
            "'%s' object has no attribute '%s'",
            type->tp_name,
            Nuitka_String_AsString_Unchecked( attr_name )
        );

        return NULL;
    }
}
/* Code to register embedded modules for meta path based loading if any. */

#include "nuitka/unfreezing.h"

/* Table for lookup to find compiled or bytecode modules included in this
 * binary or module, or put along this binary as extension modules. We do
 * our own loading for each of these.
 */
MOD_INIT_DECL( __main__ );
MOD_INIT_DECL( __main__ );
MOD_INIT_DECL( _pytest );
MOD_INIT_DECL( _pytest$_argcomplete );
MOD_INIT_DECL( _pytest$_code );
MOD_INIT_DECL( _pytest$_code$_py2traceback );
MOD_INIT_DECL( _pytest$_code$code );
MOD_INIT_DECL( _pytest$_code$source );
MOD_INIT_DECL( _pytest$_pluggy );
MOD_INIT_DECL( _pytest$_version );
MOD_INIT_DECL( _pytest$assertion );
MOD_INIT_DECL( _pytest$assertion$rewrite );
MOD_INIT_DECL( _pytest$assertion$truncate );
MOD_INIT_DECL( _pytest$assertion$util );
MOD_INIT_DECL( _pytest$compat );
MOD_INIT_DECL( _pytest$config );
MOD_INIT_DECL( _pytest$debugging );
MOD_INIT_DECL( _pytest$deprecated );
MOD_INIT_DECL( _pytest$fixtures );
MOD_INIT_DECL( _pytest$freeze_support );
MOD_INIT_DECL( _pytest$hookspec );
MOD_INIT_DECL( _pytest$main );
MOD_INIT_DECL( _pytest$mark );
MOD_INIT_DECL( _pytest$nose );
MOD_INIT_DECL( _pytest$outcomes );
MOD_INIT_DECL( _pytest$python );
MOD_INIT_DECL( _pytest$python_api );
MOD_INIT_DECL( _pytest$recwarn );
MOD_INIT_DECL( _pytest$runner );
MOD_INIT_DECL( _pytest$skipping );
MOD_INIT_DECL( _pytest$unittest );
MOD_INIT_DECL( _pytest$vendored_packages );
MOD_INIT_DECL( _pytest$vendored_packages$pluggy );
MOD_INIT_DECL( algorithms );
MOD_INIT_DECL( appdirs );
MOD_INIT_DECL( archive );
MOD_INIT_DECL( borg );
MOD_INIT_DECL( borg$_version );
MOD_INIT_DECL( borg$archiver );
MOD_INIT_DECL( borg$crypto );
MOD_INIT_DECL( borg$fuse );
MOD_INIT_DECL( borg$helpers );
MOD_INIT_DECL( borg$helpers$checks );
MOD_INIT_DECL( borg$helpers$datastruct );
MOD_INIT_DECL( borg$helpers$errors );
MOD_INIT_DECL( borg$helpers$fs );
MOD_INIT_DECL( borg$helpers$manifest );
MOD_INIT_DECL( borg$helpers$misc );
MOD_INIT_DECL( borg$helpers$msgpack );
MOD_INIT_DECL( borg$helpers$parseformat );
MOD_INIT_DECL( borg$helpers$process );
MOD_INIT_DECL( borg$helpers$progress );
MOD_INIT_DECL( borg$helpers$time );
MOD_INIT_DECL( borg$helpers$usergroup );
MOD_INIT_DECL( borg$lrucache );
MOD_INIT_DECL( borg$platform );
MOD_INIT_DECL( borg$platform$base );
MOD_INIT_DECL( borg$shellpattern );
MOD_INIT_DECL( cache );
MOD_INIT_DECL( constants );
MOD_INIT_DECL( crypto );
MOD_INIT_DECL( crypto$file_integrity );
MOD_INIT_DECL( crypto$key );
MOD_INIT_DECL( crypto$keymanager );
MOD_INIT_DECL( crypto$nonces );
MOD_INIT_DECL( helpers );
MOD_INIT_DECL( helpers$yes );
MOD_INIT_DECL( locking );
MOD_INIT_DECL( logger );
MOD_INIT_DECL( msgpack );
MOD_INIT_DECL( msgpack$_version );
MOD_INIT_DECL( msgpack$exceptions );
MOD_INIT_DECL( msgpack$fallback );
MOD_INIT_DECL( nanorst );
MOD_INIT_DECL( packaging );
MOD_INIT_DECL( packaging$__about__ );
MOD_INIT_DECL( patterns );
MOD_INIT_DECL( pluggy );
MOD_INIT_DECL( pluggy$callers );
MOD_INIT_DECL( py );
MOD_INIT_DECL( py$_apipkg );
MOD_INIT_DECL( py$_code );
MOD_INIT_DECL( py$_code$_assertionnew );
MOD_INIT_DECL( py$_code$_assertionold );
MOD_INIT_DECL( py$_code$_py2traceback );
MOD_INIT_DECL( py$_code$assertion );
MOD_INIT_DECL( py$_code$code );
MOD_INIT_DECL( py$_code$source );
MOD_INIT_DECL( pytest );
MOD_INIT_DECL( remote );
MOD_INIT_DECL( repository );
MOD_INIT_DECL( selftest );
MOD_INIT_DECL( six );
MOD_INIT_DECL( testsuite );
MOD_INIT_DECL( testsuite$chunker );
MOD_INIT_DECL( testsuite$crypto );
MOD_INIT_DECL( testsuite$hashindex );
MOD_INIT_DECL( upgrader );
MOD_INIT_DECL( version );
static struct Nuitka_MetaPathBasedLoaderEntry meta_path_loader_entries[] =
{
    { (char *)"__main__", MOD_INIT_NAME( __main__ ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"__main__", MOD_INIT_NAME( __main__ ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_bz2", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_codecs_cn", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_codecs_hk", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_codecs_iso2022", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_codecs_jp", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_codecs_kr", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_codecs_tw", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_crypt", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_csv", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_ctypes", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_curses", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_curses_panel", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_dbm", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_decimal", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_gdbm", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_hashlib", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_json", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_lsprof", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_lzma", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_multibytecodec", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_multiprocessing", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_opcode", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_pytest", MOD_INIT_NAME( _pytest ), 0, 0, NUITKA_PACKAGE_FLAG },
    { (char *)"_pytest._argcomplete", MOD_INIT_NAME( _pytest$_argcomplete ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest._code", MOD_INIT_NAME( _pytest$_code ), 0, 0, NUITKA_PACKAGE_FLAG },
    { (char *)"_pytest._code._py2traceback", MOD_INIT_NAME( _pytest$_code$_py2traceback ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest._code.code", MOD_INIT_NAME( _pytest$_code$code ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest._code.source", MOD_INIT_NAME( _pytest$_code$source ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest._pluggy", MOD_INIT_NAME( _pytest$_pluggy ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest._version", MOD_INIT_NAME( _pytest$_version ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.assertion", MOD_INIT_NAME( _pytest$assertion ), 0, 0, NUITKA_PACKAGE_FLAG },
    { (char *)"_pytest.assertion.rewrite", MOD_INIT_NAME( _pytest$assertion$rewrite ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.assertion.truncate", MOD_INIT_NAME( _pytest$assertion$truncate ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.assertion.util", MOD_INIT_NAME( _pytest$assertion$util ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.compat", MOD_INIT_NAME( _pytest$compat ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.config", MOD_INIT_NAME( _pytest$config ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.debugging", MOD_INIT_NAME( _pytest$debugging ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.deprecated", MOD_INIT_NAME( _pytest$deprecated ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.fixtures", MOD_INIT_NAME( _pytest$fixtures ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.freeze_support", MOD_INIT_NAME( _pytest$freeze_support ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.hookspec", MOD_INIT_NAME( _pytest$hookspec ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.main", MOD_INIT_NAME( _pytest$main ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.mark", MOD_INIT_NAME( _pytest$mark ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.nose", MOD_INIT_NAME( _pytest$nose ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.outcomes", MOD_INIT_NAME( _pytest$outcomes ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.python", MOD_INIT_NAME( _pytest$python ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.python_api", MOD_INIT_NAME( _pytest$python_api ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.recwarn", MOD_INIT_NAME( _pytest$recwarn ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.runner", MOD_INIT_NAME( _pytest$runner ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.skipping", MOD_INIT_NAME( _pytest$skipping ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.unittest", MOD_INIT_NAME( _pytest$unittest ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_pytest.vendored_packages", MOD_INIT_NAME( _pytest$vendored_packages ), 0, 0, NUITKA_PACKAGE_FLAG },
    { (char *)"_pytest.vendored_packages.pluggy", MOD_INIT_NAME( _pytest$vendored_packages$pluggy ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"_sqlite3", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"_ssl", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"algorithms", MOD_INIT_NAME( algorithms ), 0, 0, NUITKA_PACKAGE_FLAG },
    { (char *)"algorithms.checksums", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"appdirs", MOD_INIT_NAME( appdirs ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"archive", MOD_INIT_NAME( archive ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"audioop", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"borg", MOD_INIT_NAME( borg ), 0, 0, NUITKA_PACKAGE_FLAG },
    { (char *)"borg._version", MOD_INIT_NAME( borg$_version ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"borg.archiver", MOD_INIT_NAME( borg$archiver ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"borg.chunker", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"borg.crypto", MOD_INIT_NAME( borg$crypto ), 0, 0, NUITKA_PACKAGE_FLAG },
    { (char *)"borg.crypto.low_level", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"borg.fuse", MOD_INIT_NAME( borg$fuse ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"borg.hashindex", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"borg.helpers", MOD_INIT_NAME( borg$helpers ), 0, 0, NUITKA_PACKAGE_FLAG },
    { (char *)"borg.helpers.checks", MOD_INIT_NAME( borg$helpers$checks ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"borg.helpers.datastruct", MOD_INIT_NAME( borg$helpers$datastruct ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"borg.helpers.errors", MOD_INIT_NAME( borg$helpers$errors ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"borg.helpers.fs", MOD_INIT_NAME( borg$helpers$fs ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"borg.helpers.manifest", MOD_INIT_NAME( borg$helpers$manifest ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"borg.helpers.misc", MOD_INIT_NAME( borg$helpers$misc ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"borg.helpers.msgpack", MOD_INIT_NAME( borg$helpers$msgpack ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"borg.helpers.parseformat", MOD_INIT_NAME( borg$helpers$parseformat ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"borg.helpers.process", MOD_INIT_NAME( borg$helpers$process ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"borg.helpers.progress", MOD_INIT_NAME( borg$helpers$progress ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"borg.helpers.time", MOD_INIT_NAME( borg$helpers$time ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"borg.helpers.usergroup", MOD_INIT_NAME( borg$helpers$usergroup ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"borg.lrucache", MOD_INIT_NAME( borg$lrucache ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"borg.platform", MOD_INIT_NAME( borg$platform ), 0, 0, NUITKA_PACKAGE_FLAG },
    { (char *)"borg.platform.base", MOD_INIT_NAME( borg$platform$base ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"borg.platform.linux", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"borg.platform.posix", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"borg.shellpattern", MOD_INIT_NAME( borg$shellpattern ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"cache", MOD_INIT_NAME( cache ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"compress", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"constants", MOD_INIT_NAME( constants ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"crypto", MOD_INIT_NAME( crypto ), 0, 0, NUITKA_PACKAGE_FLAG },
    { (char *)"crypto.file_integrity", MOD_INIT_NAME( crypto$file_integrity ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"crypto.key", MOD_INIT_NAME( crypto$key ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"crypto.keymanager", MOD_INIT_NAME( crypto$keymanager ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"crypto.nonces", MOD_INIT_NAME( crypto$nonces ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"helpers", MOD_INIT_NAME( helpers ), 0, 0, NUITKA_PACKAGE_FLAG },
    { (char *)"helpers.yes", MOD_INIT_NAME( helpers$yes ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"item", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"llfuse", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"locking", MOD_INIT_NAME( locking ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"logger", MOD_INIT_NAME( logger ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"mmap", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"msgpack", MOD_INIT_NAME( msgpack ), 0, 0, NUITKA_PACKAGE_FLAG },
    { (char *)"msgpack._packer", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"msgpack._unpacker", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"msgpack._version", MOD_INIT_NAME( msgpack$_version ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"msgpack.exceptions", MOD_INIT_NAME( msgpack$exceptions ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"msgpack.fallback", MOD_INIT_NAME( msgpack$fallback ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"nanorst", MOD_INIT_NAME( nanorst ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"packaging", MOD_INIT_NAME( packaging ), 0, 0, NUITKA_PACKAGE_FLAG },
    { (char *)"packaging.__about__", MOD_INIT_NAME( packaging$__about__ ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"parser", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"patterns", MOD_INIT_NAME( patterns ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"pkg_resources", NULL, 375418, 105051, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"pkg_resources.extern", NULL, 480469, 2519, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"pkg_resources.py31compat", NULL, 482988, 706, NUITKA_BYTECODE_FLAG },
    { (char *)"platform", NULL, 483694, 32272, NUITKA_BYTECODE_FLAG },
    { (char *)"pluggy", MOD_INIT_NAME( pluggy ), 0, 0, NUITKA_PACKAGE_FLAG },
    { (char *)"pluggy.callers", MOD_INIT_NAME( pluggy$callers ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"py", MOD_INIT_NAME( py ), 0, 0, NUITKA_PACKAGE_FLAG },
    { (char *)"py._apipkg", MOD_INIT_NAME( py$_apipkg ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"py._code", MOD_INIT_NAME( py$_code ), 0, 0, NUITKA_PACKAGE_FLAG },
    { (char *)"py._code._assertionnew", MOD_INIT_NAME( py$_code$_assertionnew ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"py._code._assertionold", MOD_INIT_NAME( py$_code$_assertionold ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"py._code._py2traceback", MOD_INIT_NAME( py$_code$_py2traceback ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"py._code.assertion", MOD_INIT_NAME( py$_code$assertion ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"py._code.code", MOD_INIT_NAME( py$_code$code ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"py._code.source", MOD_INIT_NAME( py$_code$source ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"pytest", MOD_INIT_NAME( pytest ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"readline", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"remote", MOD_INIT_NAME( remote ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"repository", MOD_INIT_NAME( repository ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"selftest", MOD_INIT_NAME( selftest ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"six", MOD_INIT_NAME( six ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"termios", NULL, 0, 0, NUITKA_SHLIB_FLAG },
    { (char *)"testsuite", MOD_INIT_NAME( testsuite ), 0, 0, NUITKA_PACKAGE_FLAG },
    { (char *)"testsuite.chunker", MOD_INIT_NAME( testsuite$chunker ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"testsuite.crypto", MOD_INIT_NAME( testsuite$crypto ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"testsuite.hashindex", MOD_INIT_NAME( testsuite$hashindex ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"upgrader", MOD_INIT_NAME( upgrader ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"version", MOD_INIT_NAME( version ), 0, 0, NUITKA_COMPILED_MODULE },
    { (char *)"__future__", NULL, 515966, 4307, NUITKA_BYTECODE_FLAG },
    { (char *)"_compat_pickle", NULL, 520273, 7602, NUITKA_BYTECODE_FLAG },
    { (char *)"_dummy_thread", NULL, 527875, 5049, NUITKA_BYTECODE_FLAG },
    { (char *)"_markupbase", NULL, 532924, 8868, NUITKA_BYTECODE_FLAG },
    { (char *)"_osx_support", NULL, 541792, 10458, NUITKA_BYTECODE_FLAG },
    { (char *)"_pyio", NULL, 552250, 75982, NUITKA_BYTECODE_FLAG },
    { (char *)"_sitebuiltins", NULL, 628232, 3642, NUITKA_BYTECODE_FLAG },
    { (char *)"_strptime", NULL, 631874, 15766, NUITKA_BYTECODE_FLAG },
    { (char *)"_sysconfigdata", NULL, 647640, 239, NUITKA_BYTECODE_FLAG },
    { (char *)"_sysconfigdata_m", NULL, 647879, 21032, NUITKA_BYTECODE_FLAG },
    { (char *)"_threading_local", NULL, 668911, 6908, NUITKA_BYTECODE_FLAG },
    { (char *)"_virtualenv_distutils", NULL, 675819, 379, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"aifc", NULL, 676198, 27674, NUITKA_BYTECODE_FLAG },
    { (char *)"argparse", NULL, 703872, 65770, NUITKA_BYTECODE_FLAG },
    { (char *)"asynchat", NULL, 769642, 8453, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio", NULL, 778095, 840, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"asyncio.base_events", NULL, 778935, 38358, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.base_subprocess", NULL, 817293, 9760, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.compat", NULL, 827053, 767, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.constants", NULL, 827820, 215, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.coroutines", NULL, 828035, 8655, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.events", NULL, 836690, 24411, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.futures", NULL, 861101, 15728, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.locks", NULL, 876829, 15636, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.log", NULL, 892465, 217, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.proactor_events", NULL, 892682, 17646, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.protocols", NULL, 910328, 6064, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.queues", NULL, 916392, 8840, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.selector_events", NULL, 925232, 30570, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.sslproto", NULL, 955802, 21186, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.streams", NULL, 976988, 20794, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.subprocess", NULL, 997782, 7083, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.tasks", NULL, 1004865, 21078, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.test_utils", NULL, 1025943, 16283, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.transports", NULL, 1042226, 12110, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncio.unix_events", NULL, 1054336, 31327, NUITKA_BYTECODE_FLAG },
    { (char *)"asyncore", NULL, 1085663, 17145, NUITKA_BYTECODE_FLAG },
    { (char *)"bdb", NULL, 1102808, 18532, NUITKA_BYTECODE_FLAG },
    { (char *)"binhex", NULL, 1121340, 13400, NUITKA_BYTECODE_FLAG },
    { (char *)"bisect", NULL, 1134740, 2822, NUITKA_BYTECODE_FLAG },
    { (char *)"cProfile", NULL, 1137562, 4579, NUITKA_BYTECODE_FLAG },
    { (char *)"calendar", NULL, 1142141, 27500, NUITKA_BYTECODE_FLAG },
    { (char *)"cgi", NULL, 1169641, 29838, NUITKA_BYTECODE_FLAG },
    { (char *)"cgitb", NULL, 1199479, 10983, NUITKA_BYTECODE_FLAG },
    { (char *)"chunk", NULL, 1210462, 5192, NUITKA_BYTECODE_FLAG },
    { (char *)"cmd", NULL, 1215654, 13381, NUITKA_BYTECODE_FLAG },
    { (char *)"code", NULL, 1229035, 9799, NUITKA_BYTECODE_FLAG },
    { (char *)"codeop", NULL, 1238834, 6427, NUITKA_BYTECODE_FLAG },
    { (char *)"colorsys", NULL, 1245261, 3614, NUITKA_BYTECODE_FLAG },
    { (char *)"compileall", NULL, 1248875, 8710, NUITKA_BYTECODE_FLAG },
    { (char *)"concurrent", NULL, 1257585, 112, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"concurrent.futures", NULL, 1257697, 660, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"concurrent.futures._base", NULL, 1258357, 20888, NUITKA_BYTECODE_FLAG },
    { (char *)"concurrent.futures.process", NULL, 1279245, 16321, NUITKA_BYTECODE_FLAG },
    { (char *)"concurrent.futures.thread", NULL, 1295566, 3886, NUITKA_BYTECODE_FLAG },
    { (char *)"configparser", NULL, 1299452, 48145, NUITKA_BYTECODE_FLAG },
    { (char *)"contextlib", NULL, 1347597, 10888, NUITKA_BYTECODE_FLAG },
    { (char *)"copy", NULL, 1358485, 8103, NUITKA_BYTECODE_FLAG },
    { (char *)"crypt", NULL, 1366588, 2401, NUITKA_BYTECODE_FLAG },
    { (char *)"csv", NULL, 1368989, 12901, NUITKA_BYTECODE_FLAG },
    { (char *)"ctypes", NULL, 1381890, 17492, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"ctypes._endian", NULL, 1399382, 2040, NUITKA_BYTECODE_FLAG },
    { (char *)"ctypes.util", NULL, 1401422, 7157, NUITKA_BYTECODE_FLAG },
    { (char *)"curses", NULL, 1408579, 1898, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"curses.ascii", NULL, 1410477, 4196, NUITKA_BYTECODE_FLAG },
    { (char *)"curses.has_key", NULL, 1414673, 4747, NUITKA_BYTECODE_FLAG },
    { (char *)"curses.panel", NULL, 1419420, 207, NUITKA_BYTECODE_FLAG },
    { (char *)"curses.textpad", NULL, 1419627, 6254, NUITKA_BYTECODE_FLAG },
    { (char *)"datetime", NULL, 1425881, 55476, NUITKA_BYTECODE_FLAG },
    { (char *)"dbm", NULL, 1481357, 4409, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"dbm.dumb", NULL, 1485766, 8058, NUITKA_BYTECODE_FLAG },
    { (char *)"dbm.gnu", NULL, 1493824, 325, NUITKA_BYTECODE_FLAG },
    { (char *)"dbm.ndbm", NULL, 1494149, 186, NUITKA_BYTECODE_FLAG },
    { (char *)"decimal", NULL, 1494335, 171256, NUITKA_BYTECODE_FLAG },
    { (char *)"difflib", NULL, 1665591, 62242, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils", NULL, 1727833, 3120, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"distutils.archive_util", NULL, 1730953, 6784, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.bcppcompiler", NULL, 1737737, 7218, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.ccompiler", NULL, 1744955, 34780, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.cmd", NULL, 1779735, 15608, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command", NULL, 1795343, 544, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"distutils.command.bdist", NULL, 1795887, 4021, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.bdist_dumb", NULL, 1799908, 3941, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.bdist_rpm", NULL, 1803849, 14187, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.bdist_wininst", NULL, 1818036, 9138, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.build", NULL, 1827174, 4259, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.build_clib", NULL, 1831433, 5379, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.build_ext", NULL, 1836812, 18080, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.build_py", NULL, 1854892, 11433, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.build_scripts", NULL, 1866325, 4688, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.check", NULL, 1871013, 5214, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.clean", NULL, 1876227, 2340, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.config", NULL, 1878567, 10986, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.install", NULL, 1889553, 16155, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.install_data", NULL, 1905708, 2517, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.install_egg_info", NULL, 1908225, 3685, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.install_headers", NULL, 1911910, 1824, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.install_lib", NULL, 1913734, 5762, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.install_scripts", NULL, 1919496, 2349, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.register", NULL, 1921845, 9173, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.sdist", NULL, 1931018, 14097, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.command.upload", NULL, 1945115, 5656, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.config", NULL, 1950771, 3777, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.core", NULL, 1954548, 7083, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.cygwinccompiler", NULL, 1961631, 9186, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.debug", NULL, 1970817, 184, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.dep_util", NULL, 1971001, 2826, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.dir_util", NULL, 1973827, 6593, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.dist", NULL, 1980420, 36672, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.errors", NULL, 2017092, 5690, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.extension", NULL, 2022782, 7377, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.fancy_getopt", NULL, 2030159, 11464, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.file_util", NULL, 2041623, 6269, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.filelist", NULL, 2047892, 10081, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.log", NULL, 2057973, 2451, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.msvccompiler", NULL, 2060424, 15914, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.spawn", NULL, 2076338, 5340, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.sysconfig", NULL, 2081678, 13570, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.text_file", NULL, 2095248, 8865, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.unixccompiler", NULL, 2104113, 7678, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.util", NULL, 2111791, 16500, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.version", NULL, 2128291, 7746, NUITKA_BYTECODE_FLAG },
    { (char *)"distutils.versionpredicate", NULL, 2136037, 5342, NUITKA_BYTECODE_FLAG },
    { (char *)"doctest", NULL, 2141379, 79710, NUITKA_BYTECODE_FLAG },
    { (char *)"dummy_threading", NULL, 2221089, 1172, NUITKA_BYTECODE_FLAG },
    { (char *)"email", NULL, 2222261, 1734, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"email._encoded_words", NULL, 2223995, 6019, NUITKA_BYTECODE_FLAG },
    { (char *)"email._header_value_parser", NULL, 2230014, 87237, NUITKA_BYTECODE_FLAG },
    { (char *)"email._parseaddr", NULL, 2317251, 13711, NUITKA_BYTECODE_FLAG },
    { (char *)"email._policybase", NULL, 2330962, 15122, NUITKA_BYTECODE_FLAG },
    { (char *)"email.base64mime", NULL, 2346084, 3342, NUITKA_BYTECODE_FLAG },
    { (char *)"email.charset", NULL, 2349426, 12029, NUITKA_BYTECODE_FLAG },
    { (char *)"email.contentmanager", NULL, 2361455, 8080, NUITKA_BYTECODE_FLAG },
    { (char *)"email.encoders", NULL, 2369535, 1717, NUITKA_BYTECODE_FLAG },
    { (char *)"email.errors", NULL, 2371252, 6248, NUITKA_BYTECODE_FLAG },
    { (char *)"email.feedparser", NULL, 2377500, 11723, NUITKA_BYTECODE_FLAG },
    { (char *)"email.generator", NULL, 2389223, 13570, NUITKA_BYTECODE_FLAG },
    { (char *)"email.header", NULL, 2402793, 17656, NUITKA_BYTECODE_FLAG },
    { (char *)"email.headerregistry", NULL, 2420449, 22590, NUITKA_BYTECODE_FLAG },
    { (char *)"email.iterators", NULL, 2443039, 2001, NUITKA_BYTECODE_FLAG },
    { (char *)"email.message", NULL, 2445040, 39241, NUITKA_BYTECODE_FLAG },
    { (char *)"email.mime", NULL, 2484281, 112, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"email.mime.application", NULL, 2484393, 1434, NUITKA_BYTECODE_FLAG },
    { (char *)"email.mime.audio", NULL, 2485827, 2651, NUITKA_BYTECODE_FLAG },
    { (char *)"email.mime.base", NULL, 2488478, 991, NUITKA_BYTECODE_FLAG },
    { (char *)"email.mime.image", NULL, 2489469, 1893, NUITKA_BYTECODE_FLAG },
    { (char *)"email.mime.message", NULL, 2491362, 1311, NUITKA_BYTECODE_FLAG },
    { (char *)"email.mime.multipart", NULL, 2492673, 1526, NUITKA_BYTECODE_FLAG },
    { (char *)"email.mime.nonmultipart", NULL, 2494199, 768, NUITKA_BYTECODE_FLAG },
    { (char *)"email.mime.text", NULL, 2494967, 1336, NUITKA_BYTECODE_FLAG },
    { (char *)"email.parser", NULL, 2496303, 5883, NUITKA_BYTECODE_FLAG },
    { (char *)"email.policy", NULL, 2502186, 9740, NUITKA_BYTECODE_FLAG },
    { (char *)"email.quoprimime", NULL, 2511926, 8082, NUITKA_BYTECODE_FLAG },
    { (char *)"email.utils", NULL, 2520008, 10431, NUITKA_BYTECODE_FLAG },
    { (char *)"filecmp", NULL, 2530439, 9059, NUITKA_BYTECODE_FLAG },
    { (char *)"fileinput", NULL, 2539498, 13808, NUITKA_BYTECODE_FLAG },
    { (char *)"fnmatch", NULL, 2553306, 3119, NUITKA_BYTECODE_FLAG },
    { (char *)"formatter", NULL, 2556425, 18784, NUITKA_BYTECODE_FLAG },
    { (char *)"fractions", NULL, 2575209, 19984, NUITKA_BYTECODE_FLAG },
    { (char *)"ftplib", NULL, 2595193, 30064, NUITKA_BYTECODE_FLAG },
    { (char *)"getopt", NULL, 2625257, 6673, NUITKA_BYTECODE_FLAG },
    { (char *)"getpass", NULL, 2631930, 4532, NUITKA_BYTECODE_FLAG },
    { (char *)"gettext", NULL, 2636462, 13147, NUITKA_BYTECODE_FLAG },
    { (char *)"glob", NULL, 2649609, 4175, NUITKA_BYTECODE_FLAG },
    { (char *)"gzip", NULL, 2653784, 17553, NUITKA_BYTECODE_FLAG },
    { (char *)"hashlib", NULL, 2671337, 6346, NUITKA_BYTECODE_FLAG },
    { (char *)"hmac", NULL, 2677683, 5119, NUITKA_BYTECODE_FLAG },
    { (char *)"html", NULL, 2682802, 3605, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"html.entities", NULL, 2686407, 55413, NUITKA_BYTECODE_FLAG },
    { (char *)"html.parser", NULL, 2741820, 12208, NUITKA_BYTECODE_FLAG },
    { (char *)"http", NULL, 2754028, 6707, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"http.client", NULL, 2760735, 33627, NUITKA_BYTECODE_FLAG },
    { (char *)"http.cookiejar", NULL, 2794362, 58313, NUITKA_BYTECODE_FLAG },
    { (char *)"http.cookies", NULL, 2852675, 17201, NUITKA_BYTECODE_FLAG },
    { (char *)"http.server", NULL, 2869876, 34540, NUITKA_BYTECODE_FLAG },
    { (char *)"imaplib", NULL, 2904416, 44690, NUITKA_BYTECODE_FLAG },
    { (char *)"imghdr", NULL, 2949106, 4471, NUITKA_BYTECODE_FLAG },
    { (char *)"imp", NULL, 2953577, 10443, NUITKA_BYTECODE_FLAG },
    { (char *)"importlib.abc", NULL, 2964020, 11742, NUITKA_BYTECODE_FLAG },
    { (char *)"importlib.util", NULL, 2975762, 9628, NUITKA_BYTECODE_FLAG },
    { (char *)"ipaddress", NULL, 2985390, 66508, NUITKA_BYTECODE_FLAG },
    { (char *)"json", NULL, 3051898, 12227, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"json.decoder", NULL, 3064125, 10647, NUITKA_BYTECODE_FLAG },
    { (char *)"json.encoder", NULL, 3074772, 11970, NUITKA_BYTECODE_FLAG },
    { (char *)"json.scanner", NULL, 3086742, 2185, NUITKA_BYTECODE_FLAG },
    { (char *)"json.tool", NULL, 3088927, 1655, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3", NULL, 3090582, 109, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"lib2to3.btm_matcher", NULL, 3090691, 5289, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.btm_utils", NULL, 3095980, 6759, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixer_base", NULL, 3102739, 6499, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixer_util", NULL, 3109238, 13325, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes", NULL, 3122563, 115, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"lib2to3.fixes.fix_apply", NULL, 3122678, 1658, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_asserts", NULL, 3124336, 1335, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_basestring", NULL, 3125671, 660, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_buffer", NULL, 3126331, 812, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_callable", NULL, 3127143, 1317, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_dict", NULL, 3128460, 3641, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_except", NULL, 3132101, 3012, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_exec", NULL, 3135113, 1237, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_execfile", NULL, 3136350, 1817, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_exitfunc", NULL, 3138167, 2432, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_filter", NULL, 3140599, 2067, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_funcattrs", NULL, 3142666, 979, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_future", NULL, 3143645, 787, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_getcwdu", NULL, 3144432, 790, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_has_key", NULL, 3145222, 3139, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_idioms", NULL, 3148361, 4119, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_import", NULL, 3152480, 2985, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_imports", NULL, 3155465, 4695, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_imports2", NULL, 3160160, 540, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_input", NULL, 3160700, 976, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_intern", NULL, 3161676, 1022, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_isinstance", NULL, 3162698, 1647, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_itertools", NULL, 3164345, 1593, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_itertools_imports", NULL, 3165938, 1734, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_long", NULL, 3167672, 708, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_map", NULL, 3168380, 2813, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_metaclass", NULL, 3171193, 5920, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_methodattrs", NULL, 3177113, 951, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_ne", NULL, 3178064, 819, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_next", NULL, 3178883, 3274, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_nonzero", NULL, 3182157, 944, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_numliterals", NULL, 3183101, 1075, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_operator", NULL, 3184176, 4458, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_paren", NULL, 3188634, 1406, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_print", NULL, 3190040, 2554, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_raise", NULL, 3192594, 2409, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_raw_input", NULL, 3195003, 797, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_reduce", NULL, 3195800, 1130, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_reload", NULL, 3196930, 1022, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_renames", NULL, 3197952, 2084, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_repr", NULL, 3200036, 865, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_set_literal", NULL, 3200901, 1773, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_standarderror", NULL, 3202674, 717, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_sys_exc", NULL, 3203391, 1463, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_throw", NULL, 3204854, 1913, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_tuple_params", NULL, 3206767, 5024, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_types", NULL, 3211791, 1961, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_unicode", NULL, 3213752, 1621, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_urllib", NULL, 3215373, 6483, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_ws_comma", NULL, 3221856, 1183, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_xrange", NULL, 3223039, 2686, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_xreadlines", NULL, 3225725, 1139, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.fixes.fix_zip", NULL, 3226864, 1193, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.main", NULL, 3228057, 9121, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.patcomp", NULL, 3237178, 6305, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.pgen2", NULL, 3243483, 147, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"lib2to3.pgen2.driver", NULL, 3243630, 4436, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.pgen2.grammar", NULL, 3248066, 5674, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.pgen2.literals", NULL, 3253740, 1718, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.pgen2.parse", NULL, 3255458, 6683, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.pgen2.pgen", NULL, 3262141, 10984, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.pgen2.token", NULL, 3273125, 1998, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.pgen2.tokenize", NULL, 3275123, 15933, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.pygram", NULL, 3291056, 1232, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.pytree", NULL, 3292288, 26842, NUITKA_BYTECODE_FLAG },
    { (char *)"lib2to3.refactor", NULL, 3319130, 22776, NUITKA_BYTECODE_FLAG },
    { (char *)"logging", NULL, 3341906, 61374, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"logging.config", NULL, 3403280, 25386, NUITKA_BYTECODE_FLAG },
    { (char *)"logging.handlers", NULL, 3428666, 45060, NUITKA_BYTECODE_FLAG },
    { (char *)"lzma", NULL, 3473726, 12449, NUITKA_BYTECODE_FLAG },
    { (char *)"macpath", NULL, 3486175, 6116, NUITKA_BYTECODE_FLAG },
    { (char *)"macurl2path", NULL, 3492291, 2057, NUITKA_BYTECODE_FLAG },
    { (char *)"mailbox", NULL, 3494348, 69770, NUITKA_BYTECODE_FLAG },
    { (char *)"mailcap", NULL, 3564118, 6478, NUITKA_BYTECODE_FLAG },
    { (char *)"mimetypes", NULL, 3570596, 16620, NUITKA_BYTECODE_FLAG },
    { (char *)"modulefinder", NULL, 3587216, 17233, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing", NULL, 3604449, 536, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"multiprocessing.connection", NULL, 3604985, 27186, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.context", NULL, 3632171, 13485, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.dummy", NULL, 3645656, 4020, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"multiprocessing.dummy.connection", NULL, 3649676, 2640, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.forkserver", NULL, 3652316, 6963, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.heap", NULL, 3659279, 6740, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.managers", NULL, 3666019, 35484, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.pool", NULL, 3701503, 22824, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.popen_fork", NULL, 3724327, 2354, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.popen_forkserver", NULL, 3726681, 2517, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.popen_spawn_posix", NULL, 3729198, 2288, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.process", NULL, 3731486, 8765, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.queues", NULL, 3740251, 9851, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.reduction", NULL, 3750102, 7738, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.resource_sharer", NULL, 3757840, 5607, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.semaphore_tracker", NULL, 3763447, 3695, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.sharedctypes", NULL, 3767142, 7461, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.spawn", NULL, 3774603, 7011, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.synchronize", NULL, 3781614, 12278, NUITKA_BYTECODE_FLAG },
    { (char *)"multiprocessing.util", NULL, 3793892, 10319, NUITKA_BYTECODE_FLAG },
    { (char *)"netrc", NULL, 3804211, 4227, NUITKA_BYTECODE_FLAG },
    { (char *)"nntplib", NULL, 3808438, 36050, NUITKA_BYTECODE_FLAG },
    { (char *)"ntpath", NULL, 3844488, 14802, NUITKA_BYTECODE_FLAG },
    { (char *)"nturl2path", NULL, 3859290, 1668, NUITKA_BYTECODE_FLAG },
    { (char *)"numbers", NULL, 3860958, 12640, NUITKA_BYTECODE_FLAG },
    { (char *)"optparse", NULL, 3873598, 51299, NUITKA_BYTECODE_FLAG },
    { (char *)"pathlib", NULL, 3924897, 44166, NUITKA_BYTECODE_FLAG },
    { (char *)"pdb", NULL, 3969063, 49312, NUITKA_BYTECODE_FLAG },
    { (char *)"pickle", NULL, 4018375, 46695, NUITKA_BYTECODE_FLAG },
    { (char *)"pickletools", NULL, 4065070, 70073, NUITKA_BYTECODE_FLAG },
    { (char *)"pipes", NULL, 4135143, 8329, NUITKA_BYTECODE_FLAG },
    { (char *)"pkgutil", NULL, 4143472, 17455, NUITKA_BYTECODE_FLAG },
    { (char *)"plat-x86_64-linux-gnu.CDROM", NULL, 4160927, 6129, NUITKA_BYTECODE_FLAG },
    { (char *)"plat-x86_64-linux-gnu.DLFCN", NULL, 4167056, 2249, NUITKA_BYTECODE_FLAG },
    { (char *)"plat-x86_64-linux-gnu.IN", NULL, 4169305, 25681, NUITKA_BYTECODE_FLAG },
    { (char *)"plat-x86_64-linux-gnu.TYPES", NULL, 4194986, 4855, NUITKA_BYTECODE_FLAG },
    { (char *)"plat-x86_64-linux-gnu._sysconfigdata_m", NULL, 647879, 21032, NUITKA_BYTECODE_FLAG },
    { (char *)"platform", NULL, 483694, 32272, NUITKA_BYTECODE_FLAG },
    { (char *)"plistlib", NULL, 4199841, 29793, NUITKA_BYTECODE_FLAG },
    { (char *)"poplib", NULL, 4229634, 13901, NUITKA_BYTECODE_FLAG },
    { (char *)"pprint", NULL, 4243535, 17452, NUITKA_BYTECODE_FLAG },
    { (char *)"profile", NULL, 4260987, 15058, NUITKA_BYTECODE_FLAG },
    { (char *)"pstats", NULL, 4276045, 23540, NUITKA_BYTECODE_FLAG },
    { (char *)"pty", NULL, 4299585, 4177, NUITKA_BYTECODE_FLAG },
    { (char *)"py_compile", NULL, 4303762, 6851, NUITKA_BYTECODE_FLAG },
    { (char *)"pyclbr", NULL, 4310613, 9072, NUITKA_BYTECODE_FLAG },
    { (char *)"pydoc", NULL, 4319685, 90781, NUITKA_BYTECODE_FLAG },
    { (char *)"pydoc_data", NULL, 4410466, 112, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"pydoc_data.topics", NULL, 4410578, 387339, NUITKA_BYTECODE_FLAG },
    { (char *)"queue", NULL, 4797917, 9167, NUITKA_BYTECODE_FLAG },
    { (char *)"random", NULL, 4807084, 18973, NUITKA_BYTECODE_FLAG },
    { (char *)"rlcompleter", NULL, 4826057, 5770, NUITKA_BYTECODE_FLAG },
    { (char *)"runpy", NULL, 4831827, 8238, NUITKA_BYTECODE_FLAG },
    { (char *)"sched", NULL, 4840065, 6339, NUITKA_BYTECODE_FLAG },
    { (char *)"selectors", NULL, 4846404, 18801, NUITKA_BYTECODE_FLAG },
    { (char *)"shelve", NULL, 4865205, 9913, NUITKA_BYTECODE_FLAG },
    { (char *)"shlex", NULL, 4875118, 7311, NUITKA_BYTECODE_FLAG },
    { (char *)"shutil", NULL, 4882429, 32724, NUITKA_BYTECODE_FLAG },
    { (char *)"signal", NULL, 4915153, 2750, NUITKA_BYTECODE_FLAG },
    { (char *)"site", NULL, 4917903, 19201, NUITKA_BYTECODE_FLAG },
    { (char *)"sitecustomize", NULL, 4937104, 205, NUITKA_BYTECODE_FLAG },
    { (char *)"smtpd", NULL, 4937309, 29281, NUITKA_BYTECODE_FLAG },
    { (char *)"smtplib", NULL, 4966590, 37004, NUITKA_BYTECODE_FLAG },
    { (char *)"sndhdr", NULL, 5003594, 6878, NUITKA_BYTECODE_FLAG },
    { (char *)"socket", NULL, 5010472, 23009, NUITKA_BYTECODE_FLAG },
    { (char *)"socketserver", NULL, 5033481, 23169, NUITKA_BYTECODE_FLAG },
    { (char *)"sqlite3", NULL, 5056650, 142, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"sqlite3.dbapi2", NULL, 5056792, 2677, NUITKA_BYTECODE_FLAG },
    { (char *)"sqlite3.dump", NULL, 5059469, 2018, NUITKA_BYTECODE_FLAG },
    { (char *)"ssl", NULL, 5061487, 35739, NUITKA_BYTECODE_FLAG },
    { (char *)"statistics", NULL, 5097226, 17071, NUITKA_BYTECODE_FLAG },
    { (char *)"string", NULL, 5114297, 8583, NUITKA_BYTECODE_FLAG },
    { (char *)"subprocess", NULL, 5122880, 46748, NUITKA_BYTECODE_FLAG },
    { (char *)"sunau", NULL, 5169628, 18174, NUITKA_BYTECODE_FLAG },
    { (char *)"symbol", NULL, 5187802, 2703, NUITKA_BYTECODE_FLAG },
    { (char *)"symtable", NULL, 5190505, 10990, NUITKA_BYTECODE_FLAG },
    { (char *)"sysconfig", NULL, 5201495, 17033, NUITKA_BYTECODE_FLAG },
    { (char *)"tabnanny", NULL, 5218528, 7674, NUITKA_BYTECODE_FLAG },
    { (char *)"tarfile", NULL, 5226202, 68953, NUITKA_BYTECODE_FLAG },
    { (char *)"telnetlib", NULL, 5295155, 19204, NUITKA_BYTECODE_FLAG },
    { (char *)"tempfile", NULL, 5314359, 27008, NUITKA_BYTECODE_FLAG },
    { (char *)"textwrap", NULL, 5341367, 14178, NUITKA_BYTECODE_FLAG },
    { (char *)"this", NULL, 5355545, 1289, NUITKA_BYTECODE_FLAG },
    { (char *)"timeit", NULL, 5356834, 10983, NUITKA_BYTECODE_FLAG },
    { (char *)"trace", NULL, 5367817, 23912, NUITKA_BYTECODE_FLAG },
    { (char *)"tracemalloc", NULL, 5391729, 17051, NUITKA_BYTECODE_FLAG },
    { (char *)"tty", NULL, 5408780, 1119, NUITKA_BYTECODE_FLAG },
    { (char *)"typing", NULL, 5409899, 61326, NUITKA_BYTECODE_FLAG },
    { (char *)"unittest", NULL, 5471225, 3086, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"unittest.case", NULL, 5474311, 50602, NUITKA_BYTECODE_FLAG },
    { (char *)"unittest.loader", NULL, 5524913, 15099, NUITKA_BYTECODE_FLAG },
    { (char *)"unittest.main", NULL, 5540012, 7651, NUITKA_BYTECODE_FLAG },
    { (char *)"unittest.mock", NULL, 5547663, 65704, NUITKA_BYTECODE_FLAG },
    { (char *)"unittest.result", NULL, 5613367, 7747, NUITKA_BYTECODE_FLAG },
    { (char *)"unittest.runner", NULL, 5621114, 7491, NUITKA_BYTECODE_FLAG },
    { (char *)"unittest.signals", NULL, 5628605, 2350, NUITKA_BYTECODE_FLAG },
    { (char *)"unittest.suite", NULL, 5630955, 9886, NUITKA_BYTECODE_FLAG },
    { (char *)"unittest.util", NULL, 5640841, 5200, NUITKA_BYTECODE_FLAG },
    { (char *)"urllib", NULL, 5646041, 108, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"urllib.error", NULL, 5646149, 2896, NUITKA_BYTECODE_FLAG },
    { (char *)"urllib.parse", NULL, 5649045, 30071, NUITKA_BYTECODE_FLAG },
    { (char *)"urllib.request", NULL, 5679116, 76363, NUITKA_BYTECODE_FLAG },
    { (char *)"urllib.response", NULL, 5755479, 3368, NUITKA_BYTECODE_FLAG },
    { (char *)"urllib.robotparser", NULL, 5758847, 6686, NUITKA_BYTECODE_FLAG },
    { (char *)"uu", NULL, 5765533, 3928, NUITKA_BYTECODE_FLAG },
    { (char *)"uuid", NULL, 5769461, 21647, NUITKA_BYTECODE_FLAG },
    { (char *)"venv", NULL, 5791108, 16756, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"wave", NULL, 5807864, 18979, NUITKA_BYTECODE_FLAG },
    { (char *)"webbrowser", NULL, 5826843, 17006, NUITKA_BYTECODE_FLAG },
    { (char *)"wsgiref", NULL, 5843849, 706, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"wsgiref.handlers", NULL, 5844555, 17152, NUITKA_BYTECODE_FLAG },
    { (char *)"wsgiref.headers", NULL, 5861707, 8126, NUITKA_BYTECODE_FLAG },
    { (char *)"wsgiref.simple_server", NULL, 5869833, 5699, NUITKA_BYTECODE_FLAG },
    { (char *)"wsgiref.util", NULL, 5875532, 5563, NUITKA_BYTECODE_FLAG },
    { (char *)"wsgiref.validate", NULL, 5881095, 15626, NUITKA_BYTECODE_FLAG },
    { (char *)"xdrlib", NULL, 5896721, 8939, NUITKA_BYTECODE_FLAG },
    { (char *)"xml", NULL, 5905660, 680, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"xml.dom", NULL, 5906340, 5748, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"xml.dom.NodeFilter", NULL, 5912088, 988, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.dom.domreg", NULL, 5913076, 2913, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.dom.expatbuilder", NULL, 5915989, 29803, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.dom.minicompat", NULL, 5945792, 2941, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.dom.minidom", NULL, 5948733, 61355, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.dom.pulldom", NULL, 6010088, 11554, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.dom.xmlbuilder", NULL, 6021642, 14773, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.etree", NULL, 6036415, 111, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"xml.etree.ElementInclude", NULL, 6036526, 1725, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.etree.ElementPath", NULL, 6038251, 6688, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.etree.ElementTree", NULL, 6044939, 47821, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.etree.cElementTree", NULL, 6092760, 155, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.parsers", NULL, 6092915, 287, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"xml.parsers.expat", NULL, 6093202, 328, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.sax", NULL, 6093530, 3323, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"xml.sax._exceptions", NULL, 6096853, 5657, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.sax.expatreader", NULL, 6102510, 13313, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.sax.handler", NULL, 6115823, 12479, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.sax.saxutils", NULL, 6128302, 13723, NUITKA_BYTECODE_FLAG },
    { (char *)"xml.sax.xmlreader", NULL, 6142025, 17503, NUITKA_BYTECODE_FLAG },
    { (char *)"xmlrpc", NULL, 6159528, 108, NUITKA_BYTECODE_FLAG | NUITKA_PACKAGE_FLAG },
    { (char *)"xmlrpc.client", NULL, 6159636, 36780, NUITKA_BYTECODE_FLAG },
    { (char *)"xmlrpc.server", NULL, 6196416, 31192, NUITKA_BYTECODE_FLAG },
    { (char *)"zipapp", NULL, 6227608, 6000, NUITKA_BYTECODE_FLAG },
    { (char *)"zipfile", NULL, 6233608, 49903, NUITKA_BYTECODE_FLAG },
    { NULL, NULL, 0, 0, 0 }
};

void setupMetaPathBasedLoader( void )
{
    static bool init_done = false;

    if ( init_done == false )
    {
        registerMetaPathBasedUnfreezer( meta_path_loader_entries );
        init_done = true;
    }
}
