/* Generated code for Python source for module 'packaging.__about__'
 * created by Nuitka version 0.5.28.1
 *
 * This code is in part copyright 2017 Kay Hayen.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "nuitka/prelude.h"

#include "__helpers.h"

/* The _module_packaging$__about__ is a Python object pointer of module type. */

/* Note: For full compatibility with CPython, every module variable access
 * needs to go through it except for cases where the module cannot possibly
 * have changed in the mean time.
 */

PyObject *module_packaging$__about__;
PyDictObject *moduledict_packaging$__about__;

/* The module constants used, if any. */
extern PyObject *const_str_plain___copyright__;
static PyObject *const_str_digest_983fc705caa3f427e09b821a1e270e4d;
static PyObject *const_str_digest_05e8c38d628b3aba8abcc5d43ea8d8ea;
extern PyObject *const_str_plain_ModuleSpec;
extern PyObject *const_str_plain___spec__;
extern PyObject *const_str_plain___package__;
extern PyObject *const_str_plain___summary__;
extern PyObject *const_str_plain___all__;
static PyObject *const_str_digest_894ad454fad7a3546de1b3ebcc4ddb55;
extern PyObject *const_str_plain___file__;
extern PyObject *const_str_plain___version__;
extern PyObject *const_list_b5215a344cdfe40170e16c947ed7b43b_list;
extern PyObject *const_str_plain___email__;
static PyObject *const_str_digest_d9806583756695cd1c4f8535a65ff69c;
extern PyObject *const_str_plain_division;
extern PyObject *const_str_plain_packaging;
extern PyObject *const_str_plain___doc__;
extern PyObject *const_str_plain___uri__;
extern PyObject *const_str_plain___author__;
extern PyObject *const_str_plain___license__;
extern PyObject *const_tuple_empty;
extern PyObject *const_str_plain___title__;
static PyObject *const_str_digest_24af0d29525b682afb17c2d2cf4f025f;
static PyObject *const_str_digest_d4542d2880d54a4b54551867fac03d07;
extern PyObject *const_str_plain___loader__;
static PyObject *const_str_digest_43f96eca3406fd8074d16bbbe21aef95;
static PyObject *const_str_digest_e102fcc27d439009a0cbc27e7dee5d68;
static PyObject *const_str_digest_d0abdf6e09828dc9d0cde4f58cf740d1;
extern PyObject *const_str_plain_absolute_import;
extern PyObject *const_str_plain___cached__;
extern PyObject *const_str_plain_print_function;
static PyObject *const_str_digest_7e8039b2a5190b84eaba8e3668438234;
static PyObject *module_filename_obj;

static bool constants_created = false;

static void createModuleConstants( void )
{
    const_str_digest_983fc705caa3f427e09b821a1e270e4d = UNSTREAM_STRING( &constant_bin[ 204904 ], 34, 0 );
    const_str_digest_05e8c38d628b3aba8abcc5d43ea8d8ea = UNSTREAM_STRING( &constant_bin[ 204938 ], 33, 0 );
    const_str_digest_894ad454fad7a3546de1b3ebcc4ddb55 = UNSTREAM_STRING( &constant_bin[ 204971 ], 61, 0 );
    const_str_digest_d9806583756695cd1c4f8535a65ff69c = UNSTREAM_STRING( &constant_bin[ 205032 ], 28, 0 );
    const_str_digest_24af0d29525b682afb17c2d2cf4f025f = UNSTREAM_STRING( &constant_bin[ 205060 ], 4, 0 );
    const_str_digest_d4542d2880d54a4b54551867fac03d07 = UNSTREAM_STRING( &constant_bin[ 205064 ], 34, 0 );
    const_str_digest_43f96eca3406fd8074d16bbbe21aef95 = UNSTREAM_STRING( &constant_bin[ 205098 ], 16, 0 );
    const_str_digest_e102fcc27d439009a0cbc27e7dee5d68 = UNSTREAM_STRING( &constant_bin[ 205040 ], 19, 0 );
    const_str_digest_d0abdf6e09828dc9d0cde4f58cf740d1 = UNSTREAM_STRING( &constant_bin[ 205114 ], 22, 0 );
    const_str_digest_7e8039b2a5190b84eaba8e3668438234 = UNSTREAM_STRING( &constant_bin[ 204991 ], 41, 0 );

    constants_created = true;
}

#ifndef __NUITKA_NO_ASSERT__
void checkModuleConstants_packaging$__about__( void )
{
    // The module may not have been used at all.
    if (constants_created == false) return;


}
#endif

// The module code objects.
static PyCodeObject *codeobj_371bf123e74debd7ee112cab5f4f9987;

static void createModuleCodeObjects(void)
{
    module_filename_obj = MAKE_RELATIVE_PATH( const_str_digest_d0abdf6e09828dc9d0cde4f58cf740d1 );
    codeobj_371bf123e74debd7ee112cab5f4f9987 = MAKE_CODEOBJ( module_filename_obj, const_str_digest_d9806583756695cd1c4f8535a65ff69c, 1, const_tuple_empty, 0, 0, CO_NOFREE );
}

// The module function declarations.


// The module function definitions.



#if PYTHON_VERSION >= 300
static struct PyModuleDef mdef_packaging$__about__ =
{
    PyModuleDef_HEAD_INIT,
    "packaging.__about__",   /* m_name */
    NULL,                /* m_doc */
    -1,                  /* m_size */
    NULL,                /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#endif

#if PYTHON_VERSION >= 300
extern PyObject *metapath_based_loader;
#endif
#if PYTHON_VERSION >= 330
extern PyObject *const_str_plain___loader__;
#endif

extern void _initCompiledCellType();
extern void _initCompiledGeneratorType();
extern void _initCompiledFunctionType();
extern void _initCompiledMethodType();
extern void _initCompiledFrameType();
#if PYTHON_VERSION >= 350
extern void _initCompiledCoroutineTypes();
#endif
#if PYTHON_VERSION >= 360
extern void _initCompiledAsyncgenTypes();
#endif

// The exported interface to CPython. On import of the module, this function
// gets called. It has to have an exact function name, in cases it's a shared
// library export. This is hidden behind the MOD_INIT_DECL.

MOD_INIT_DECL( packaging$__about__ )
{
#if defined(_NUITKA_EXE) || PYTHON_VERSION >= 300
    static bool _init_done = false;

    // Modules might be imported repeatedly, which is to be ignored.
    if ( _init_done )
    {
        return MOD_RETURN_VALUE( module_packaging$__about__ );
    }
    else
    {
        _init_done = true;
    }
#endif

#ifdef _NUITKA_MODULE
    // In case of a stand alone extension module, need to call initialization
    // the init here because that's the first and only time we are going to get
    // called here.

    // Initialize the constant values used.
    _initBuiltinModule();
    createGlobalConstants();

    /* Initialize the compiled types of Nuitka. */
    _initCompiledCellType();
    _initCompiledGeneratorType();
    _initCompiledFunctionType();
    _initCompiledMethodType();
    _initCompiledFrameType();
#if PYTHON_VERSION >= 350
    _initCompiledCoroutineTypes();
#endif
#if PYTHON_VERSION >= 360
    _initCompiledAsyncgenTypes();
#endif

#if PYTHON_VERSION < 300
    _initSlotCompare();
#endif
#if PYTHON_VERSION >= 270
    _initSlotIternext();
#endif

    patchBuiltinModule();
    patchTypeComparison();

    // Enable meta path based loader if not already done.
    setupMetaPathBasedLoader();

#if PYTHON_VERSION >= 300
    patchInspectModule();
#endif

#endif

    /* The constants only used by this module are created now. */
#ifdef _NUITKA_TRACE
    puts("packaging.__about__: Calling createModuleConstants().");
#endif
    createModuleConstants();

    /* The code objects used by this module are created now. */
#ifdef _NUITKA_TRACE
    puts("packaging.__about__: Calling createModuleCodeObjects().");
#endif
    createModuleCodeObjects();

    // puts( "in initpackaging$__about__" );

    // Create the module object first. There are no methods initially, all are
    // added dynamically in actual code only.  Also no "__doc__" is initially
    // set at this time, as it could not contain NUL characters this way, they
    // are instead set in early module code.  No "self" for modules, we have no
    // use for it.
#if PYTHON_VERSION < 300
    module_packaging$__about__ = Py_InitModule4(
        "packaging.__about__",       // Module Name
        NULL,                    // No methods initially, all are added
                                 // dynamically in actual module code only.
        NULL,                    // No __doc__ is initially set, as it could
                                 // not contain NUL this way, added early in
                                 // actual code.
        NULL,                    // No self for modules, we don't use it.
        PYTHON_API_VERSION
    );
#else
    module_packaging$__about__ = PyModule_Create( &mdef_packaging$__about__ );
#endif

    moduledict_packaging$__about__ = MODULE_DICT( module_packaging$__about__ );

    CHECK_OBJECT( module_packaging$__about__ );

// Seems to work for Python2.7 out of the box, but for Python3, the module
// doesn't automatically enter "sys.modules", so do it manually.
#if PYTHON_VERSION >= 300
    {
        int r = PyObject_SetItem( PySys_GetObject( (char *)"modules" ), const_str_digest_e102fcc27d439009a0cbc27e7dee5d68, module_packaging$__about__ );

        assert( r != -1 );
    }
#endif

    // For deep importing of a module we need to have "__builtins__", so we set
    // it ourselves in the same way than CPython does. Note: This must be done
    // before the frame object is allocated, or else it may fail.

    if ( GET_STRING_DICT_VALUE( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain___builtins__ ) == NULL )
    {
        PyObject *value = (PyObject *)builtin_module;

        // Check if main module, not a dict then but the module itself.
#if !defined(_NUITKA_EXE) || !0
        value = PyModule_GetDict( value );
#endif

        UPDATE_STRING_DICT0( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain___builtins__, value );
    }

#if PYTHON_VERSION >= 330
    UPDATE_STRING_DICT0( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain___loader__, metapath_based_loader );
#endif

    // Temp variables if any
    PyObject *tmp_import_from_1__module = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    PyObject *exception_keeper_type_1;
    PyObject *exception_keeper_value_1;
    PyTracebackObject *exception_keeper_tb_1;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_1;
    PyObject *tmp_args_element_name_1;
    PyObject *tmp_args_element_name_2;
    PyObject *tmp_assign_source_1;
    PyObject *tmp_assign_source_2;
    PyObject *tmp_assign_source_3;
    PyObject *tmp_assign_source_4;
    PyObject *tmp_assign_source_5;
    PyObject *tmp_assign_source_6;
    PyObject *tmp_assign_source_7;
    PyObject *tmp_assign_source_8;
    PyObject *tmp_assign_source_9;
    PyObject *tmp_assign_source_10;
    PyObject *tmp_assign_source_11;
    PyObject *tmp_assign_source_12;
    PyObject *tmp_assign_source_13;
    PyObject *tmp_assign_source_14;
    PyObject *tmp_assign_source_15;
    PyObject *tmp_assign_source_16;
    PyObject *tmp_assign_source_17;
    PyObject *tmp_assign_source_18;
    PyObject *tmp_assign_source_19;
    PyObject *tmp_called_name_1;
    PyObject *tmp_import_name_from_1;
    PyObject *tmp_import_name_from_2;
    PyObject *tmp_import_name_from_3;
    struct Nuitka_FrameObject *frame_371bf123e74debd7ee112cab5f4f9987;

    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;

    // Module code.
    tmp_assign_source_1 = Py_None;
    UPDATE_STRING_DICT0( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain___doc__, tmp_assign_source_1 );
    tmp_assign_source_2 = module_filename_obj;
    UPDATE_STRING_DICT0( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain___file__, tmp_assign_source_2 );
    tmp_assign_source_3 = metapath_based_loader;
    UPDATE_STRING_DICT0( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain___loader__, tmp_assign_source_3 );
    // Frame without reuse.
    frame_371bf123e74debd7ee112cab5f4f9987 = MAKE_MODULE_FRAME( codeobj_371bf123e74debd7ee112cab5f4f9987, module_packaging$__about__ );

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStack( frame_371bf123e74debd7ee112cab5f4f9987 );
    assert( Py_REFCNT( frame_371bf123e74debd7ee112cab5f4f9987 ) == 2 );

    // Framed code:
    frame_371bf123e74debd7ee112cab5f4f9987->m_frame.f_lineno = 1;
    {
        PyObject *module = PyImport_ImportModule("importlib._bootstrap");
        if (likely( module != NULL ))
        {
            tmp_called_name_1 = PyObject_GetAttr( module, const_str_plain_ModuleSpec );
        }
        else
        {
            tmp_called_name_1 = NULL;
        }
    }

    if ( tmp_called_name_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 1;

        goto frame_exception_exit_1;
    }
    tmp_args_element_name_1 = const_str_digest_e102fcc27d439009a0cbc27e7dee5d68;
    tmp_args_element_name_2 = metapath_based_loader;
    frame_371bf123e74debd7ee112cab5f4f9987->m_frame.f_lineno = 1;
    {
        PyObject *call_args[] = { tmp_args_element_name_1, tmp_args_element_name_2 };
        tmp_assign_source_4 = CALL_FUNCTION_WITH_ARGS2( tmp_called_name_1, call_args );
    }

    if ( tmp_assign_source_4 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 1;

        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain___spec__, tmp_assign_source_4 );
    tmp_assign_source_5 = Py_None;
    UPDATE_STRING_DICT0( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain___cached__, tmp_assign_source_5 );
    tmp_assign_source_6 = const_str_plain_packaging;
    UPDATE_STRING_DICT0( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain___package__, tmp_assign_source_6 );
    frame_371bf123e74debd7ee112cab5f4f9987->m_frame.f_lineno = 4;
    tmp_assign_source_7 = PyImport_ImportModule("__future__");
    assert( tmp_assign_source_7 != NULL );
    assert( tmp_import_from_1__module == NULL );
    Py_INCREF( tmp_assign_source_7 );
    tmp_import_from_1__module = tmp_assign_source_7;

    // Tried code:
    tmp_import_name_from_1 = tmp_import_from_1__module;

    CHECK_OBJECT( tmp_import_name_from_1 );
    tmp_assign_source_8 = IMPORT_NAME( tmp_import_name_from_1, const_str_plain_absolute_import );
    if ( tmp_assign_source_8 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 4;

        goto try_except_handler_1;
    }
    UPDATE_STRING_DICT1( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain_absolute_import, tmp_assign_source_8 );
    tmp_import_name_from_2 = tmp_import_from_1__module;

    CHECK_OBJECT( tmp_import_name_from_2 );
    tmp_assign_source_9 = IMPORT_NAME( tmp_import_name_from_2, const_str_plain_division );
    if ( tmp_assign_source_9 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 4;

        goto try_except_handler_1;
    }
    UPDATE_STRING_DICT1( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain_division, tmp_assign_source_9 );
    tmp_import_name_from_3 = tmp_import_from_1__module;

    CHECK_OBJECT( tmp_import_name_from_3 );
    tmp_assign_source_10 = IMPORT_NAME( tmp_import_name_from_3, const_str_plain_print_function );
    if ( tmp_assign_source_10 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 4;

        goto try_except_handler_1;
    }
    UPDATE_STRING_DICT1( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain_print_function, tmp_assign_source_10 );
    goto try_end_1;
    // Exception handler code:
    try_except_handler_1:;
    exception_keeper_type_1 = exception_type;
    exception_keeper_value_1 = exception_value;
    exception_keeper_tb_1 = exception_tb;
    exception_keeper_lineno_1 = exception_lineno;
    exception_type = NULL;
    exception_value = NULL;
    exception_tb = NULL;
    exception_lineno = 0;

    Py_XDECREF( tmp_import_from_1__module );
    tmp_import_from_1__module = NULL;

    // Re-raise.
    exception_type = exception_keeper_type_1;
    exception_value = exception_keeper_value_1;
    exception_tb = exception_keeper_tb_1;
    exception_lineno = exception_keeper_lineno_1;

    goto frame_exception_exit_1;
    // End of try:
    try_end_1:;

    // Restore frame exception if necessary.
#if 0
    RESTORE_FRAME_EXCEPTION( frame_371bf123e74debd7ee112cab5f4f9987 );
#endif
    popFrameStack();

    assertFrameObject( frame_371bf123e74debd7ee112cab5f4f9987 );

    goto frame_no_exception_1;
    frame_exception_exit_1:;
#if 0
    RESTORE_FRAME_EXCEPTION( frame_371bf123e74debd7ee112cab5f4f9987 );
#endif

    if ( exception_tb == NULL )
    {
        exception_tb = MAKE_TRACEBACK( frame_371bf123e74debd7ee112cab5f4f9987, exception_lineno );
    }
    else if ( exception_tb->tb_frame != &frame_371bf123e74debd7ee112cab5f4f9987->m_frame )
    {
        exception_tb = ADD_TRACEBACK( exception_tb, frame_371bf123e74debd7ee112cab5f4f9987, exception_lineno );
    }

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto module_exception_exit;
    frame_no_exception_1:;
    Py_XDECREF( tmp_import_from_1__module );
    tmp_import_from_1__module = NULL;

    tmp_assign_source_11 = LIST_COPY( const_list_b5215a344cdfe40170e16c947ed7b43b_list );
    UPDATE_STRING_DICT1( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain___all__, tmp_assign_source_11 );
    tmp_assign_source_12 = const_str_plain_packaging;
    UPDATE_STRING_DICT0( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain___title__, tmp_assign_source_12 );
    tmp_assign_source_13 = const_str_digest_983fc705caa3f427e09b821a1e270e4d;
    UPDATE_STRING_DICT0( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain___summary__, tmp_assign_source_13 );
    tmp_assign_source_14 = const_str_digest_05e8c38d628b3aba8abcc5d43ea8d8ea;
    UPDATE_STRING_DICT0( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain___uri__, tmp_assign_source_14 );
    tmp_assign_source_15 = const_str_digest_24af0d29525b682afb17c2d2cf4f025f;
    UPDATE_STRING_DICT0( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain___version__, tmp_assign_source_15 );
    tmp_assign_source_16 = const_str_digest_7e8039b2a5190b84eaba8e3668438234;
    UPDATE_STRING_DICT0( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain___author__, tmp_assign_source_16 );
    tmp_assign_source_17 = const_str_digest_43f96eca3406fd8074d16bbbe21aef95;
    UPDATE_STRING_DICT0( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain___email__, tmp_assign_source_17 );
    tmp_assign_source_18 = const_str_digest_d4542d2880d54a4b54551867fac03d07;
    UPDATE_STRING_DICT0( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain___license__, tmp_assign_source_18 );
    tmp_assign_source_19 = const_str_digest_894ad454fad7a3546de1b3ebcc4ddb55;
    UPDATE_STRING_DICT0( moduledict_packaging$__about__, (Nuitka_StringObject *)const_str_plain___copyright__, tmp_assign_source_19 );

    return MOD_RETURN_VALUE( module_packaging$__about__ );
    module_exception_exit:
    RESTORE_ERROR_OCCURRED( exception_type, exception_value, exception_tb );
    return MOD_RETURN_VALUE( NULL );
}
