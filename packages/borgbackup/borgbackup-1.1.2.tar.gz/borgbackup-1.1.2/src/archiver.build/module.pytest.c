/* Generated code for Python source for module 'pytest'
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

/* The _module_pytest is a Python object pointer of module type. */

/* Note: For full compatibility with CPython, every module variable access
 * needs to go through it except for cases where the module cannot possibly
 * have changed in the mean time.
 */

PyObject *module_pytest;
PyDictObject *moduledict_pytest;

/* The module constants used, if any. */
static PyObject *const_tuple_8e5b640cbf43e5ab24980bca3c2f84eb_tuple;
extern PyObject *const_str_plain_MARK_GEN;
static PyObject *const_tuple_str_plain_fillfixtures_tuple;
extern PyObject *const_str_digest_faf8202d3f6da8ef7f383dafc7c899ef;
static PyObject *const_tuple_6c57a551da69e6caa3a9902af9bfa8f9_tuple;
static PyObject *const_tuple_str_plain_warns_str_plain_deprecated_call_tuple;
extern PyObject *const_str_plain_ModuleSpec;
extern PyObject *const_str_plain___spec__;
extern PyObject *const_str_plain___package__;
extern PyObject *const_str_plain_main;
extern PyObject *const_str_digest_80eb686e282e8673946e705cb33eeda1;
extern PyObject *const_str_plain_warns;
extern PyObject *const_str_plain_freeze_includes;
extern PyObject *const_str_plain_Module;
extern PyObject *const_str_plain_Item;
extern PyObject *const_str_plain_skip;
extern PyObject *const_str_digest_7b5c8649f8daec52e9fa88bdd5c7ccdc;
static PyObject *const_tuple_str_plain__setup_collect_fakemodule_tuple;
extern PyObject *const_str_plain___all__;
extern PyObject *const_str_plain_fail;
extern PyObject *const_str_plain__preloadplugins;
static PyObject *const_str_digest_d767552924f31d1bb455c5b57fc6f922;
extern PyObject *const_str_digest_e2198bbf03f762749d69f082a8deaceb;
static PyObject *const_tuple_str_plain_pytestPDB_tuple;
extern PyObject *const_str_plain___file__;
extern PyObject *const_str_plain_fixture;
extern PyObject *const_str_plain_yield_fixture;
static PyObject *const_tuple_str_plain_register_assert_rewrite_tuple;
extern PyObject *const_str_plain___version__;
extern PyObject *const_str_plain_fillfixtures;
extern PyObject *const_str_plain_Function;
extern PyObject *const_int_0;
extern PyObject *const_str_plain_Session;
static PyObject *const_tuple_str_plain_fixture_str_plain_yield_fixture_tuple;
extern PyObject *const_str_plain_pytestPDB;
extern PyObject *const_str_digest_06040c1773aa3897cbdd53bf1f3b77cd;
extern PyObject *const_str_plain_Generator;
extern PyObject *const_str_plain_importorskip;
static PyObject *const_str_digest_f078010068591366b639d8536f68c2e6;
extern PyObject *const_str_plain___doc__;
extern PyObject *const_str_plain__setup_collect_fakemodule;
extern PyObject *const_str_digest_fd2a182399f1af236a945e51b4ae6780;
static PyObject *const_str_digest_9627c07a75b2f6fe239c2a1996591d5c;
extern PyObject *const_str_plain_File;
extern PyObject *const_str_plain_param;
extern PyObject *const_str_plain_Class;
extern PyObject *const_str_plain_register_assert_rewrite;
static PyObject *const_tuple_e16e1cfe85916ebb0b4b718008f1b571_tuple;
extern PyObject *const_str_plain_set_trace;
static PyObject *const_tuple_str_plain_freeze_includes_tuple;
extern PyObject *const_str_plain_xfail;
extern PyObject *const_tuple_empty;
extern PyObject *const_str_plain_pytest;
extern PyObject *const_str_plain_mark;
extern PyObject *const_str_plain__fillfuncargs;
extern PyObject *const_str_plain_Instance;
extern PyObject *const_str_digest_85276b092395087e8b17a3dbbb26c3fe;
static PyObject *const_str_plain___pytestPDB;
extern PyObject *const_str_plain_deprecated_call;
extern PyObject *const_str_plain_cmdline;
extern PyObject *const_str_digest_697519b333303d87961e335e5cc1410d;
extern PyObject *const_str_plain_UsageError;
extern PyObject *const_str_digest_b2b81f822fe941d00debcfb05534128e;
extern PyObject *const_tuple_str_plain___version___tuple;
extern PyObject *const_str_plain___loader__;
extern PyObject *const_str_digest_e76028b31cdbeb19174540661a998fab;
static PyObject *const_tuple_str_plain_MARK_GEN_str_plain_param_tuple;
static PyObject *const_tuple_str_plain_approx_str_plain_raises_tuple;
static PyObject *const_list_ed7164bf5feb489fae584c24800196dd_list;
extern PyObject *const_str_plain_approx;
extern PyObject *const_str_digest_9771cbb3646ea84961e9853ca850451d;
extern PyObject *const_str_plain_raises;
extern PyObject *const_str_plain_hookspec;
extern PyObject *const_str_plain_Collector;
extern PyObject *const_str_plain_hookimpl;
extern PyObject *const_str_plain___cached__;
extern PyObject *const_str_plain_exit;
static PyObject *const_tuple_6f7a3ee769ddaf265fd13050628cb485_tuple;
extern PyObject *const_str_digest_376381e08dd7407f681d8448db3d2021;
extern PyObject *const_str_plain__pytest;
static PyObject *module_filename_obj;

static bool constants_created = false;

static void createModuleConstants( void )
{
    const_tuple_8e5b640cbf43e5ab24980bca3c2f84eb_tuple = PyTuple_New( 5 );
    PyTuple_SET_ITEM( const_tuple_8e5b640cbf43e5ab24980bca3c2f84eb_tuple, 0, const_str_plain_fail ); Py_INCREF( const_str_plain_fail );
    PyTuple_SET_ITEM( const_tuple_8e5b640cbf43e5ab24980bca3c2f84eb_tuple, 1, const_str_plain_skip ); Py_INCREF( const_str_plain_skip );
    PyTuple_SET_ITEM( const_tuple_8e5b640cbf43e5ab24980bca3c2f84eb_tuple, 2, const_str_plain_importorskip ); Py_INCREF( const_str_plain_importorskip );
    PyTuple_SET_ITEM( const_tuple_8e5b640cbf43e5ab24980bca3c2f84eb_tuple, 3, const_str_plain_exit ); Py_INCREF( const_str_plain_exit );
    PyTuple_SET_ITEM( const_tuple_8e5b640cbf43e5ab24980bca3c2f84eb_tuple, 4, const_str_plain_xfail ); Py_INCREF( const_str_plain_xfail );
    const_tuple_str_plain_fillfixtures_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_fillfixtures_tuple, 0, const_str_plain_fillfixtures ); Py_INCREF( const_str_plain_fillfixtures );
    const_tuple_6c57a551da69e6caa3a9902af9bfa8f9_tuple = PyTuple_New( 6 );
    PyTuple_SET_ITEM( const_tuple_6c57a551da69e6caa3a9902af9bfa8f9_tuple, 0, const_str_plain_main ); Py_INCREF( const_str_plain_main );
    PyTuple_SET_ITEM( const_tuple_6c57a551da69e6caa3a9902af9bfa8f9_tuple, 1, const_str_plain_UsageError ); Py_INCREF( const_str_plain_UsageError );
    PyTuple_SET_ITEM( const_tuple_6c57a551da69e6caa3a9902af9bfa8f9_tuple, 2, const_str_plain__preloadplugins ); Py_INCREF( const_str_plain__preloadplugins );
    PyTuple_SET_ITEM( const_tuple_6c57a551da69e6caa3a9902af9bfa8f9_tuple, 3, const_str_plain_cmdline ); Py_INCREF( const_str_plain_cmdline );
    PyTuple_SET_ITEM( const_tuple_6c57a551da69e6caa3a9902af9bfa8f9_tuple, 4, const_str_plain_hookspec ); Py_INCREF( const_str_plain_hookspec );
    PyTuple_SET_ITEM( const_tuple_6c57a551da69e6caa3a9902af9bfa8f9_tuple, 5, const_str_plain_hookimpl ); Py_INCREF( const_str_plain_hookimpl );
    const_tuple_str_plain_warns_str_plain_deprecated_call_tuple = PyTuple_New( 2 );
    PyTuple_SET_ITEM( const_tuple_str_plain_warns_str_plain_deprecated_call_tuple, 0, const_str_plain_warns ); Py_INCREF( const_str_plain_warns );
    PyTuple_SET_ITEM( const_tuple_str_plain_warns_str_plain_deprecated_call_tuple, 1, const_str_plain_deprecated_call ); Py_INCREF( const_str_plain_deprecated_call );
    const_tuple_str_plain__setup_collect_fakemodule_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain__setup_collect_fakemodule_tuple, 0, const_str_plain__setup_collect_fakemodule ); Py_INCREF( const_str_plain__setup_collect_fakemodule );
    const_str_digest_d767552924f31d1bb455c5b57fc6f922 = UNSTREAM_STRING( &constant_bin[ 223170 ], 15, 0 );
    const_tuple_str_plain_pytestPDB_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_pytestPDB_tuple, 0, const_str_plain_pytestPDB ); Py_INCREF( const_str_plain_pytestPDB );
    const_tuple_str_plain_register_assert_rewrite_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_register_assert_rewrite_tuple, 0, const_str_plain_register_assert_rewrite ); Py_INCREF( const_str_plain_register_assert_rewrite );
    const_tuple_str_plain_fixture_str_plain_yield_fixture_tuple = PyTuple_New( 2 );
    PyTuple_SET_ITEM( const_tuple_str_plain_fixture_str_plain_yield_fixture_tuple, 0, const_str_plain_fixture ); Py_INCREF( const_str_plain_fixture );
    PyTuple_SET_ITEM( const_tuple_str_plain_fixture_str_plain_yield_fixture_tuple, 1, const_str_plain_yield_fixture ); Py_INCREF( const_str_plain_yield_fixture );
    const_str_digest_f078010068591366b639d8536f68c2e6 = UNSTREAM_STRING( &constant_bin[ 223185 ], 50, 0 );
    const_str_digest_9627c07a75b2f6fe239c2a1996591d5c = UNSTREAM_STRING( &constant_bin[ 84351 ], 9, 0 );
    const_tuple_e16e1cfe85916ebb0b4b718008f1b571_tuple = PyTuple_New( 4 );
    PyTuple_SET_ITEM( const_tuple_e16e1cfe85916ebb0b4b718008f1b571_tuple, 0, const_str_plain_Item ); Py_INCREF( const_str_plain_Item );
    PyTuple_SET_ITEM( const_tuple_e16e1cfe85916ebb0b4b718008f1b571_tuple, 1, const_str_plain_Collector ); Py_INCREF( const_str_plain_Collector );
    PyTuple_SET_ITEM( const_tuple_e16e1cfe85916ebb0b4b718008f1b571_tuple, 2, const_str_plain_File ); Py_INCREF( const_str_plain_File );
    PyTuple_SET_ITEM( const_tuple_e16e1cfe85916ebb0b4b718008f1b571_tuple, 3, const_str_plain_Session ); Py_INCREF( const_str_plain_Session );
    const_tuple_str_plain_freeze_includes_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_freeze_includes_tuple, 0, const_str_plain_freeze_includes ); Py_INCREF( const_str_plain_freeze_includes );
    const_str_plain___pytestPDB = UNSTREAM_STRING( &constant_bin[ 223235 ], 11, 1 );
    const_tuple_str_plain_MARK_GEN_str_plain_param_tuple = PyTuple_New( 2 );
    PyTuple_SET_ITEM( const_tuple_str_plain_MARK_GEN_str_plain_param_tuple, 0, const_str_plain_MARK_GEN ); Py_INCREF( const_str_plain_MARK_GEN );
    PyTuple_SET_ITEM( const_tuple_str_plain_MARK_GEN_str_plain_param_tuple, 1, const_str_plain_param ); Py_INCREF( const_str_plain_param );
    const_tuple_str_plain_approx_str_plain_raises_tuple = PyTuple_New( 2 );
    PyTuple_SET_ITEM( const_tuple_str_plain_approx_str_plain_raises_tuple, 0, const_str_plain_approx ); Py_INCREF( const_str_plain_approx );
    PyTuple_SET_ITEM( const_tuple_str_plain_approx_str_plain_raises_tuple, 1, const_str_plain_raises ); Py_INCREF( const_str_plain_raises );
    const_list_ed7164bf5feb489fae584c24800196dd_list = PyMarshal_ReadObjectFromString( (char *)&constant_bin[ 223246 ], 327 );
    const_tuple_6f7a3ee769ddaf265fd13050628cb485_tuple = PyTuple_New( 5 );
    PyTuple_SET_ITEM( const_tuple_6f7a3ee769ddaf265fd13050628cb485_tuple, 0, const_str_plain_Module ); Py_INCREF( const_str_plain_Module );
    PyTuple_SET_ITEM( const_tuple_6f7a3ee769ddaf265fd13050628cb485_tuple, 1, const_str_plain_Class ); Py_INCREF( const_str_plain_Class );
    PyTuple_SET_ITEM( const_tuple_6f7a3ee769ddaf265fd13050628cb485_tuple, 2, const_str_plain_Instance ); Py_INCREF( const_str_plain_Instance );
    PyTuple_SET_ITEM( const_tuple_6f7a3ee769ddaf265fd13050628cb485_tuple, 3, const_str_plain_Function ); Py_INCREF( const_str_plain_Function );
    PyTuple_SET_ITEM( const_tuple_6f7a3ee769ddaf265fd13050628cb485_tuple, 4, const_str_plain_Generator ); Py_INCREF( const_str_plain_Generator );

    constants_created = true;
}

#ifndef __NUITKA_NO_ASSERT__
void checkModuleConstants_pytest( void )
{
    // The module may not have been used at all.
    if (constants_created == false) return;


}
#endif

// The module code objects.
static PyCodeObject *codeobj_531a1df80b944f2591c7ecbce6b9ae81;

static void createModuleCodeObjects(void)
{
    module_filename_obj = MAKE_RELATIVE_PATH( const_str_digest_9627c07a75b2f6fe239c2a1996591d5c );
    codeobj_531a1df80b944f2591c7ecbce6b9ae81 = MAKE_CODEOBJ( module_filename_obj, const_str_digest_d767552924f31d1bb455c5b57fc6f922, 1, const_tuple_empty, 0, 0, CO_NOFREE );
}

// The module function declarations.


// The module function definitions.



#if PYTHON_VERSION >= 300
static struct PyModuleDef mdef_pytest =
{
    PyModuleDef_HEAD_INIT,
    "pytest",   /* m_name */
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

MOD_INIT_DECL( pytest )
{
#if defined(_NUITKA_EXE) || PYTHON_VERSION >= 300
    static bool _init_done = false;

    // Modules might be imported repeatedly, which is to be ignored.
    if ( _init_done )
    {
        return MOD_RETURN_VALUE( module_pytest );
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
    puts("pytest: Calling createModuleConstants().");
#endif
    createModuleConstants();

    /* The code objects used by this module are created now. */
#ifdef _NUITKA_TRACE
    puts("pytest: Calling createModuleCodeObjects().");
#endif
    createModuleCodeObjects();

    // puts( "in initpytest" );

    // Create the module object first. There are no methods initially, all are
    // added dynamically in actual code only.  Also no "__doc__" is initially
    // set at this time, as it could not contain NUL characters this way, they
    // are instead set in early module code.  No "self" for modules, we have no
    // use for it.
#if PYTHON_VERSION < 300
    module_pytest = Py_InitModule4(
        "pytest",       // Module Name
        NULL,                    // No methods initially, all are added
                                 // dynamically in actual module code only.
        NULL,                    // No __doc__ is initially set, as it could
                                 // not contain NUL this way, added early in
                                 // actual code.
        NULL,                    // No self for modules, we don't use it.
        PYTHON_API_VERSION
    );
#else
    module_pytest = PyModule_Create( &mdef_pytest );
#endif

    moduledict_pytest = MODULE_DICT( module_pytest );

    CHECK_OBJECT( module_pytest );

// Seems to work for Python2.7 out of the box, but for Python3, the module
// doesn't automatically enter "sys.modules", so do it manually.
#if PYTHON_VERSION >= 300
    {
        int r = PyObject_SetItem( PySys_GetObject( (char *)"modules" ), const_str_plain_pytest, module_pytest );

        assert( r != -1 );
    }
#endif

    // For deep importing of a module we need to have "__builtins__", so we set
    // it ourselves in the same way than CPython does. Note: This must be done
    // before the frame object is allocated, or else it may fail.

    if ( GET_STRING_DICT_VALUE( moduledict_pytest, (Nuitka_StringObject *)const_str_plain___builtins__ ) == NULL )
    {
        PyObject *value = (PyObject *)builtin_module;

        // Check if main module, not a dict then but the module itself.
#if !defined(_NUITKA_EXE) || !0
        value = PyModule_GetDict( value );
#endif

        UPDATE_STRING_DICT0( moduledict_pytest, (Nuitka_StringObject *)const_str_plain___builtins__, value );
    }

#if PYTHON_VERSION >= 330
    UPDATE_STRING_DICT0( moduledict_pytest, (Nuitka_StringObject *)const_str_plain___loader__, metapath_based_loader );
#endif

    // Temp variables if any
    PyObject *tmp_import_from_1__module = NULL;
    PyObject *tmp_import_from_2__module = NULL;
    PyObject *tmp_import_from_3__module = NULL;
    PyObject *tmp_import_from_4__module = NULL;
    PyObject *tmp_import_from_5__module = NULL;
    PyObject *tmp_import_from_6__module = NULL;
    PyObject *tmp_import_from_7__module = NULL;
    PyObject *tmp_import_from_8__module = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    PyObject *exception_keeper_type_1;
    PyObject *exception_keeper_value_1;
    PyTracebackObject *exception_keeper_tb_1;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_1;
    PyObject *exception_keeper_type_2;
    PyObject *exception_keeper_value_2;
    PyTracebackObject *exception_keeper_tb_2;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_2;
    PyObject *exception_keeper_type_3;
    PyObject *exception_keeper_value_3;
    PyTracebackObject *exception_keeper_tb_3;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_3;
    PyObject *exception_keeper_type_4;
    PyObject *exception_keeper_value_4;
    PyTracebackObject *exception_keeper_tb_4;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_4;
    PyObject *exception_keeper_type_5;
    PyObject *exception_keeper_value_5;
    PyTracebackObject *exception_keeper_tb_5;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_5;
    PyObject *exception_keeper_type_6;
    PyObject *exception_keeper_value_6;
    PyTracebackObject *exception_keeper_tb_6;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_6;
    PyObject *exception_keeper_type_7;
    PyObject *exception_keeper_value_7;
    PyTracebackObject *exception_keeper_tb_7;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_7;
    PyObject *exception_keeper_type_8;
    PyObject *exception_keeper_value_8;
    PyTracebackObject *exception_keeper_tb_8;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_8;
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
    PyObject *tmp_assign_source_20;
    PyObject *tmp_assign_source_21;
    PyObject *tmp_assign_source_22;
    PyObject *tmp_assign_source_23;
    PyObject *tmp_assign_source_24;
    PyObject *tmp_assign_source_25;
    PyObject *tmp_assign_source_26;
    PyObject *tmp_assign_source_27;
    PyObject *tmp_assign_source_28;
    PyObject *tmp_assign_source_29;
    PyObject *tmp_assign_source_30;
    PyObject *tmp_assign_source_31;
    PyObject *tmp_assign_source_32;
    PyObject *tmp_assign_source_33;
    PyObject *tmp_assign_source_34;
    PyObject *tmp_assign_source_35;
    PyObject *tmp_assign_source_36;
    PyObject *tmp_assign_source_37;
    PyObject *tmp_assign_source_38;
    PyObject *tmp_assign_source_39;
    PyObject *tmp_assign_source_40;
    PyObject *tmp_assign_source_41;
    PyObject *tmp_assign_source_42;
    PyObject *tmp_assign_source_43;
    PyObject *tmp_assign_source_44;
    PyObject *tmp_assign_source_45;
    PyObject *tmp_assign_source_46;
    PyObject *tmp_assign_source_47;
    PyObject *tmp_assign_source_48;
    PyObject *tmp_assign_source_49;
    PyObject *tmp_assign_source_50;
    PyObject *tmp_called_name_1;
    PyObject *tmp_called_name_2;
    PyObject *tmp_called_name_3;
    PyObject *tmp_fromlist_name_1;
    PyObject *tmp_fromlist_name_2;
    PyObject *tmp_fromlist_name_3;
    PyObject *tmp_fromlist_name_4;
    PyObject *tmp_fromlist_name_5;
    PyObject *tmp_fromlist_name_6;
    PyObject *tmp_fromlist_name_7;
    PyObject *tmp_fromlist_name_8;
    PyObject *tmp_fromlist_name_9;
    PyObject *tmp_fromlist_name_10;
    PyObject *tmp_fromlist_name_11;
    PyObject *tmp_fromlist_name_12;
    PyObject *tmp_fromlist_name_13;
    PyObject *tmp_fromlist_name_14;
    PyObject *tmp_globals_name_1;
    PyObject *tmp_globals_name_2;
    PyObject *tmp_globals_name_3;
    PyObject *tmp_globals_name_4;
    PyObject *tmp_globals_name_5;
    PyObject *tmp_globals_name_6;
    PyObject *tmp_globals_name_7;
    PyObject *tmp_globals_name_8;
    PyObject *tmp_globals_name_9;
    PyObject *tmp_globals_name_10;
    PyObject *tmp_globals_name_11;
    PyObject *tmp_globals_name_12;
    PyObject *tmp_globals_name_13;
    PyObject *tmp_globals_name_14;
    PyObject *tmp_import_name_from_1;
    PyObject *tmp_import_name_from_2;
    PyObject *tmp_import_name_from_3;
    PyObject *tmp_import_name_from_4;
    PyObject *tmp_import_name_from_5;
    PyObject *tmp_import_name_from_6;
    PyObject *tmp_import_name_from_7;
    PyObject *tmp_import_name_from_8;
    PyObject *tmp_import_name_from_9;
    PyObject *tmp_import_name_from_10;
    PyObject *tmp_import_name_from_11;
    PyObject *tmp_import_name_from_12;
    PyObject *tmp_import_name_from_13;
    PyObject *tmp_import_name_from_14;
    PyObject *tmp_import_name_from_15;
    PyObject *tmp_import_name_from_16;
    PyObject *tmp_import_name_from_17;
    PyObject *tmp_import_name_from_18;
    PyObject *tmp_import_name_from_19;
    PyObject *tmp_import_name_from_20;
    PyObject *tmp_import_name_from_21;
    PyObject *tmp_import_name_from_22;
    PyObject *tmp_import_name_from_23;
    PyObject *tmp_import_name_from_24;
    PyObject *tmp_import_name_from_25;
    PyObject *tmp_import_name_from_26;
    PyObject *tmp_import_name_from_27;
    PyObject *tmp_import_name_from_28;
    PyObject *tmp_import_name_from_29;
    PyObject *tmp_import_name_from_30;
    PyObject *tmp_import_name_from_31;
    PyObject *tmp_import_name_from_32;
    PyObject *tmp_import_name_from_33;
    PyObject *tmp_import_name_from_34;
    PyObject *tmp_level_name_1;
    PyObject *tmp_level_name_2;
    PyObject *tmp_level_name_3;
    PyObject *tmp_level_name_4;
    PyObject *tmp_level_name_5;
    PyObject *tmp_level_name_6;
    PyObject *tmp_level_name_7;
    PyObject *tmp_level_name_8;
    PyObject *tmp_level_name_9;
    PyObject *tmp_level_name_10;
    PyObject *tmp_level_name_11;
    PyObject *tmp_level_name_12;
    PyObject *tmp_level_name_13;
    PyObject *tmp_level_name_14;
    PyObject *tmp_locals_name_1;
    PyObject *tmp_locals_name_2;
    PyObject *tmp_locals_name_3;
    PyObject *tmp_locals_name_4;
    PyObject *tmp_locals_name_5;
    PyObject *tmp_locals_name_6;
    PyObject *tmp_locals_name_7;
    PyObject *tmp_locals_name_8;
    PyObject *tmp_locals_name_9;
    PyObject *tmp_locals_name_10;
    PyObject *tmp_locals_name_11;
    PyObject *tmp_locals_name_12;
    PyObject *tmp_locals_name_13;
    PyObject *tmp_locals_name_14;
    PyObject *tmp_name_name_1;
    PyObject *tmp_name_name_2;
    PyObject *tmp_name_name_3;
    PyObject *tmp_name_name_4;
    PyObject *tmp_name_name_5;
    PyObject *tmp_name_name_6;
    PyObject *tmp_name_name_7;
    PyObject *tmp_name_name_8;
    PyObject *tmp_name_name_9;
    PyObject *tmp_name_name_10;
    PyObject *tmp_name_name_11;
    PyObject *tmp_name_name_12;
    PyObject *tmp_name_name_13;
    PyObject *tmp_name_name_14;
    PyObject *tmp_source_name_1;
    NUITKA_MAY_BE_UNUSED PyObject *tmp_unused;
    struct Nuitka_FrameObject *frame_531a1df80b944f2591c7ecbce6b9ae81;

    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;

    // Module code.
    tmp_assign_source_1 = const_str_digest_f078010068591366b639d8536f68c2e6;
    UPDATE_STRING_DICT0( moduledict_pytest, (Nuitka_StringObject *)const_str_plain___doc__, tmp_assign_source_1 );
    tmp_assign_source_2 = module_filename_obj;
    UPDATE_STRING_DICT0( moduledict_pytest, (Nuitka_StringObject *)const_str_plain___file__, tmp_assign_source_2 );
    tmp_assign_source_3 = metapath_based_loader;
    UPDATE_STRING_DICT0( moduledict_pytest, (Nuitka_StringObject *)const_str_plain___loader__, tmp_assign_source_3 );
    // Frame without reuse.
    frame_531a1df80b944f2591c7ecbce6b9ae81 = MAKE_MODULE_FRAME( codeobj_531a1df80b944f2591c7ecbce6b9ae81, module_pytest );

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStack( frame_531a1df80b944f2591c7ecbce6b9ae81 );
    assert( Py_REFCNT( frame_531a1df80b944f2591c7ecbce6b9ae81 ) == 2 );

    // Framed code:
    frame_531a1df80b944f2591c7ecbce6b9ae81->m_frame.f_lineno = 1;
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
    tmp_args_element_name_1 = const_str_plain_pytest;
    tmp_args_element_name_2 = metapath_based_loader;
    frame_531a1df80b944f2591c7ecbce6b9ae81->m_frame.f_lineno = 1;
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
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain___spec__, tmp_assign_source_4 );
    tmp_assign_source_5 = Py_None;
    UPDATE_STRING_DICT0( moduledict_pytest, (Nuitka_StringObject *)const_str_plain___cached__, tmp_assign_source_5 );
    tmp_assign_source_6 = Py_None;
    UPDATE_STRING_DICT0( moduledict_pytest, (Nuitka_StringObject *)const_str_plain___package__, tmp_assign_source_6 );
    tmp_name_name_1 = const_str_digest_85276b092395087e8b17a3dbbb26c3fe;
    tmp_globals_name_1 = (PyObject *)moduledict_pytest;
    tmp_locals_name_1 = Py_None;
    tmp_fromlist_name_1 = const_tuple_6c57a551da69e6caa3a9902af9bfa8f9_tuple;
    tmp_level_name_1 = const_int_0;
    frame_531a1df80b944f2591c7ecbce6b9ae81->m_frame.f_lineno = 9;
    tmp_assign_source_7 = IMPORT_MODULE5( tmp_name_name_1, tmp_globals_name_1, tmp_locals_name_1, tmp_fromlist_name_1, tmp_level_name_1 );
    if ( tmp_assign_source_7 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 9;

        goto frame_exception_exit_1;
    }
    assert( tmp_import_from_1__module == NULL );
    tmp_import_from_1__module = tmp_assign_source_7;

    // Tried code:
    tmp_import_name_from_1 = tmp_import_from_1__module;

    CHECK_OBJECT( tmp_import_name_from_1 );
    tmp_assign_source_8 = IMPORT_NAME( tmp_import_name_from_1, const_str_plain_main );
    if ( tmp_assign_source_8 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 9;

        goto try_except_handler_1;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_main, tmp_assign_source_8 );
    tmp_import_name_from_2 = tmp_import_from_1__module;

    CHECK_OBJECT( tmp_import_name_from_2 );
    tmp_assign_source_9 = IMPORT_NAME( tmp_import_name_from_2, const_str_plain_UsageError );
    if ( tmp_assign_source_9 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 9;

        goto try_except_handler_1;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_UsageError, tmp_assign_source_9 );
    tmp_import_name_from_3 = tmp_import_from_1__module;

    CHECK_OBJECT( tmp_import_name_from_3 );
    tmp_assign_source_10 = IMPORT_NAME( tmp_import_name_from_3, const_str_plain__preloadplugins );
    if ( tmp_assign_source_10 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 9;

        goto try_except_handler_1;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain__preloadplugins, tmp_assign_source_10 );
    tmp_import_name_from_4 = tmp_import_from_1__module;

    CHECK_OBJECT( tmp_import_name_from_4 );
    tmp_assign_source_11 = IMPORT_NAME( tmp_import_name_from_4, const_str_plain_cmdline );
    if ( tmp_assign_source_11 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 9;

        goto try_except_handler_1;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_cmdline, tmp_assign_source_11 );
    tmp_import_name_from_5 = tmp_import_from_1__module;

    CHECK_OBJECT( tmp_import_name_from_5 );
    tmp_assign_source_12 = IMPORT_NAME( tmp_import_name_from_5, const_str_plain_hookspec );
    if ( tmp_assign_source_12 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 9;

        goto try_except_handler_1;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_hookspec, tmp_assign_source_12 );
    tmp_import_name_from_6 = tmp_import_from_1__module;

    CHECK_OBJECT( tmp_import_name_from_6 );
    tmp_assign_source_13 = IMPORT_NAME( tmp_import_name_from_6, const_str_plain_hookimpl );
    if ( tmp_assign_source_13 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 9;

        goto try_except_handler_1;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_hookimpl, tmp_assign_source_13 );
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
    Py_XDECREF( tmp_import_from_1__module );
    tmp_import_from_1__module = NULL;

    tmp_name_name_2 = const_str_digest_697519b333303d87961e335e5cc1410d;
    tmp_globals_name_2 = (PyObject *)moduledict_pytest;
    tmp_locals_name_2 = Py_None;
    tmp_fromlist_name_2 = const_tuple_str_plain_fixture_str_plain_yield_fixture_tuple;
    tmp_level_name_2 = const_int_0;
    frame_531a1df80b944f2591c7ecbce6b9ae81->m_frame.f_lineno = 13;
    tmp_assign_source_14 = IMPORT_MODULE5( tmp_name_name_2, tmp_globals_name_2, tmp_locals_name_2, tmp_fromlist_name_2, tmp_level_name_2 );
    if ( tmp_assign_source_14 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 13;

        goto frame_exception_exit_1;
    }
    assert( tmp_import_from_2__module == NULL );
    tmp_import_from_2__module = tmp_assign_source_14;

    // Tried code:
    tmp_import_name_from_7 = tmp_import_from_2__module;

    CHECK_OBJECT( tmp_import_name_from_7 );
    tmp_assign_source_15 = IMPORT_NAME( tmp_import_name_from_7, const_str_plain_fixture );
    if ( tmp_assign_source_15 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 13;

        goto try_except_handler_2;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_fixture, tmp_assign_source_15 );
    tmp_import_name_from_8 = tmp_import_from_2__module;

    CHECK_OBJECT( tmp_import_name_from_8 );
    tmp_assign_source_16 = IMPORT_NAME( tmp_import_name_from_8, const_str_plain_yield_fixture );
    if ( tmp_assign_source_16 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 13;

        goto try_except_handler_2;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_yield_fixture, tmp_assign_source_16 );
    goto try_end_2;
    // Exception handler code:
    try_except_handler_2:;
    exception_keeper_type_2 = exception_type;
    exception_keeper_value_2 = exception_value;
    exception_keeper_tb_2 = exception_tb;
    exception_keeper_lineno_2 = exception_lineno;
    exception_type = NULL;
    exception_value = NULL;
    exception_tb = NULL;
    exception_lineno = 0;

    Py_XDECREF( tmp_import_from_2__module );
    tmp_import_from_2__module = NULL;

    // Re-raise.
    exception_type = exception_keeper_type_2;
    exception_value = exception_keeper_value_2;
    exception_tb = exception_keeper_tb_2;
    exception_lineno = exception_keeper_lineno_2;

    goto frame_exception_exit_1;
    // End of try:
    try_end_2:;
    Py_XDECREF( tmp_import_from_2__module );
    tmp_import_from_2__module = NULL;

    tmp_name_name_3 = const_str_digest_fd2a182399f1af236a945e51b4ae6780;
    tmp_globals_name_3 = (PyObject *)moduledict_pytest;
    tmp_locals_name_3 = Py_None;
    tmp_fromlist_name_3 = const_tuple_str_plain_register_assert_rewrite_tuple;
    tmp_level_name_3 = const_int_0;
    frame_531a1df80b944f2591c7ecbce6b9ae81->m_frame.f_lineno = 14;
    tmp_import_name_from_9 = IMPORT_MODULE5( tmp_name_name_3, tmp_globals_name_3, tmp_locals_name_3, tmp_fromlist_name_3, tmp_level_name_3 );
    if ( tmp_import_name_from_9 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 14;

        goto frame_exception_exit_1;
    }
    tmp_assign_source_17 = IMPORT_NAME( tmp_import_name_from_9, const_str_plain_register_assert_rewrite );
    Py_DECREF( tmp_import_name_from_9 );
    if ( tmp_assign_source_17 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 14;

        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_register_assert_rewrite, tmp_assign_source_17 );
    tmp_name_name_4 = const_str_digest_b2b81f822fe941d00debcfb05534128e;
    tmp_globals_name_4 = (PyObject *)moduledict_pytest;
    tmp_locals_name_4 = Py_None;
    tmp_fromlist_name_4 = const_tuple_str_plain_freeze_includes_tuple;
    tmp_level_name_4 = const_int_0;
    frame_531a1df80b944f2591c7ecbce6b9ae81->m_frame.f_lineno = 15;
    tmp_import_name_from_10 = IMPORT_MODULE5( tmp_name_name_4, tmp_globals_name_4, tmp_locals_name_4, tmp_fromlist_name_4, tmp_level_name_4 );
    if ( tmp_import_name_from_10 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 15;

        goto frame_exception_exit_1;
    }
    tmp_assign_source_18 = IMPORT_NAME( tmp_import_name_from_10, const_str_plain_freeze_includes );
    Py_DECREF( tmp_import_name_from_10 );
    if ( tmp_assign_source_18 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 15;

        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_freeze_includes, tmp_assign_source_18 );
    tmp_name_name_5 = const_str_plain__pytest;
    tmp_globals_name_5 = (PyObject *)moduledict_pytest;
    tmp_locals_name_5 = Py_None;
    tmp_fromlist_name_5 = const_tuple_str_plain___version___tuple;
    tmp_level_name_5 = const_int_0;
    frame_531a1df80b944f2591c7ecbce6b9ae81->m_frame.f_lineno = 16;
    tmp_import_name_from_11 = IMPORT_MODULE5( tmp_name_name_5, tmp_globals_name_5, tmp_locals_name_5, tmp_fromlist_name_5, tmp_level_name_5 );
    if ( tmp_import_name_from_11 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 16;

        goto frame_exception_exit_1;
    }
    tmp_assign_source_19 = IMPORT_NAME( tmp_import_name_from_11, const_str_plain___version__ );
    Py_DECREF( tmp_import_name_from_11 );
    if ( tmp_assign_source_19 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 16;

        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain___version__, tmp_assign_source_19 );
    tmp_name_name_6 = const_str_digest_80eb686e282e8673946e705cb33eeda1;
    tmp_globals_name_6 = (PyObject *)moduledict_pytest;
    tmp_locals_name_6 = Py_None;
    tmp_fromlist_name_6 = const_tuple_str_plain_pytestPDB_tuple;
    tmp_level_name_6 = const_int_0;
    frame_531a1df80b944f2591c7ecbce6b9ae81->m_frame.f_lineno = 17;
    tmp_import_name_from_12 = IMPORT_MODULE5( tmp_name_name_6, tmp_globals_name_6, tmp_locals_name_6, tmp_fromlist_name_6, tmp_level_name_6 );
    if ( tmp_import_name_from_12 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 17;

        goto frame_exception_exit_1;
    }
    tmp_assign_source_20 = IMPORT_NAME( tmp_import_name_from_12, const_str_plain_pytestPDB );
    Py_DECREF( tmp_import_name_from_12 );
    if ( tmp_assign_source_20 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 17;

        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain___pytestPDB, tmp_assign_source_20 );
    tmp_name_name_7 = const_str_digest_376381e08dd7407f681d8448db3d2021;
    tmp_globals_name_7 = (PyObject *)moduledict_pytest;
    tmp_locals_name_7 = Py_None;
    tmp_fromlist_name_7 = const_tuple_str_plain_warns_str_plain_deprecated_call_tuple;
    tmp_level_name_7 = const_int_0;
    frame_531a1df80b944f2591c7ecbce6b9ae81->m_frame.f_lineno = 18;
    tmp_assign_source_21 = IMPORT_MODULE5( tmp_name_name_7, tmp_globals_name_7, tmp_locals_name_7, tmp_fromlist_name_7, tmp_level_name_7 );
    if ( tmp_assign_source_21 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 18;

        goto frame_exception_exit_1;
    }
    assert( tmp_import_from_3__module == NULL );
    tmp_import_from_3__module = tmp_assign_source_21;

    // Tried code:
    tmp_import_name_from_13 = tmp_import_from_3__module;

    CHECK_OBJECT( tmp_import_name_from_13 );
    tmp_assign_source_22 = IMPORT_NAME( tmp_import_name_from_13, const_str_plain_warns );
    if ( tmp_assign_source_22 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 18;

        goto try_except_handler_3;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_warns, tmp_assign_source_22 );
    tmp_import_name_from_14 = tmp_import_from_3__module;

    CHECK_OBJECT( tmp_import_name_from_14 );
    tmp_assign_source_23 = IMPORT_NAME( tmp_import_name_from_14, const_str_plain_deprecated_call );
    if ( tmp_assign_source_23 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 18;

        goto try_except_handler_3;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_deprecated_call, tmp_assign_source_23 );
    goto try_end_3;
    // Exception handler code:
    try_except_handler_3:;
    exception_keeper_type_3 = exception_type;
    exception_keeper_value_3 = exception_value;
    exception_keeper_tb_3 = exception_tb;
    exception_keeper_lineno_3 = exception_lineno;
    exception_type = NULL;
    exception_value = NULL;
    exception_tb = NULL;
    exception_lineno = 0;

    Py_XDECREF( tmp_import_from_3__module );
    tmp_import_from_3__module = NULL;

    // Re-raise.
    exception_type = exception_keeper_type_3;
    exception_value = exception_keeper_value_3;
    exception_tb = exception_keeper_tb_3;
    exception_lineno = exception_keeper_lineno_3;

    goto frame_exception_exit_1;
    // End of try:
    try_end_3:;
    Py_XDECREF( tmp_import_from_3__module );
    tmp_import_from_3__module = NULL;

    tmp_name_name_8 = const_str_digest_06040c1773aa3897cbdd53bf1f3b77cd;
    tmp_globals_name_8 = (PyObject *)moduledict_pytest;
    tmp_locals_name_8 = Py_None;
    tmp_fromlist_name_8 = const_tuple_8e5b640cbf43e5ab24980bca3c2f84eb_tuple;
    tmp_level_name_8 = const_int_0;
    frame_531a1df80b944f2591c7ecbce6b9ae81->m_frame.f_lineno = 19;
    tmp_assign_source_24 = IMPORT_MODULE5( tmp_name_name_8, tmp_globals_name_8, tmp_locals_name_8, tmp_fromlist_name_8, tmp_level_name_8 );
    if ( tmp_assign_source_24 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 19;

        goto frame_exception_exit_1;
    }
    assert( tmp_import_from_4__module == NULL );
    tmp_import_from_4__module = tmp_assign_source_24;

    // Tried code:
    tmp_import_name_from_15 = tmp_import_from_4__module;

    CHECK_OBJECT( tmp_import_name_from_15 );
    tmp_assign_source_25 = IMPORT_NAME( tmp_import_name_from_15, const_str_plain_fail );
    if ( tmp_assign_source_25 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 19;

        goto try_except_handler_4;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_fail, tmp_assign_source_25 );
    tmp_import_name_from_16 = tmp_import_from_4__module;

    CHECK_OBJECT( tmp_import_name_from_16 );
    tmp_assign_source_26 = IMPORT_NAME( tmp_import_name_from_16, const_str_plain_skip );
    if ( tmp_assign_source_26 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 19;

        goto try_except_handler_4;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_skip, tmp_assign_source_26 );
    tmp_import_name_from_17 = tmp_import_from_4__module;

    CHECK_OBJECT( tmp_import_name_from_17 );
    tmp_assign_source_27 = IMPORT_NAME( tmp_import_name_from_17, const_str_plain_importorskip );
    if ( tmp_assign_source_27 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 19;

        goto try_except_handler_4;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_importorskip, tmp_assign_source_27 );
    tmp_import_name_from_18 = tmp_import_from_4__module;

    CHECK_OBJECT( tmp_import_name_from_18 );
    tmp_assign_source_28 = IMPORT_NAME( tmp_import_name_from_18, const_str_plain_exit );
    if ( tmp_assign_source_28 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 19;

        goto try_except_handler_4;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_exit, tmp_assign_source_28 );
    tmp_import_name_from_19 = tmp_import_from_4__module;

    CHECK_OBJECT( tmp_import_name_from_19 );
    tmp_assign_source_29 = IMPORT_NAME( tmp_import_name_from_19, const_str_plain_xfail );
    if ( tmp_assign_source_29 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 19;

        goto try_except_handler_4;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_xfail, tmp_assign_source_29 );
    goto try_end_4;
    // Exception handler code:
    try_except_handler_4:;
    exception_keeper_type_4 = exception_type;
    exception_keeper_value_4 = exception_value;
    exception_keeper_tb_4 = exception_tb;
    exception_keeper_lineno_4 = exception_lineno;
    exception_type = NULL;
    exception_value = NULL;
    exception_tb = NULL;
    exception_lineno = 0;

    Py_XDECREF( tmp_import_from_4__module );
    tmp_import_from_4__module = NULL;

    // Re-raise.
    exception_type = exception_keeper_type_4;
    exception_value = exception_keeper_value_4;
    exception_tb = exception_keeper_tb_4;
    exception_lineno = exception_keeper_lineno_4;

    goto frame_exception_exit_1;
    // End of try:
    try_end_4:;
    Py_XDECREF( tmp_import_from_4__module );
    tmp_import_from_4__module = NULL;

    tmp_name_name_9 = const_str_digest_e76028b31cdbeb19174540661a998fab;
    tmp_globals_name_9 = (PyObject *)moduledict_pytest;
    tmp_locals_name_9 = Py_None;
    tmp_fromlist_name_9 = const_tuple_str_plain_MARK_GEN_str_plain_param_tuple;
    tmp_level_name_9 = const_int_0;
    frame_531a1df80b944f2591c7ecbce6b9ae81->m_frame.f_lineno = 20;
    tmp_assign_source_30 = IMPORT_MODULE5( tmp_name_name_9, tmp_globals_name_9, tmp_locals_name_9, tmp_fromlist_name_9, tmp_level_name_9 );
    if ( tmp_assign_source_30 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 20;

        goto frame_exception_exit_1;
    }
    assert( tmp_import_from_5__module == NULL );
    tmp_import_from_5__module = tmp_assign_source_30;

    // Tried code:
    tmp_import_name_from_20 = tmp_import_from_5__module;

    CHECK_OBJECT( tmp_import_name_from_20 );
    tmp_assign_source_31 = IMPORT_NAME( tmp_import_name_from_20, const_str_plain_MARK_GEN );
    if ( tmp_assign_source_31 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 20;

        goto try_except_handler_5;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_mark, tmp_assign_source_31 );
    tmp_import_name_from_21 = tmp_import_from_5__module;

    CHECK_OBJECT( tmp_import_name_from_21 );
    tmp_assign_source_32 = IMPORT_NAME( tmp_import_name_from_21, const_str_plain_param );
    if ( tmp_assign_source_32 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 20;

        goto try_except_handler_5;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_param, tmp_assign_source_32 );
    goto try_end_5;
    // Exception handler code:
    try_except_handler_5:;
    exception_keeper_type_5 = exception_type;
    exception_keeper_value_5 = exception_value;
    exception_keeper_tb_5 = exception_tb;
    exception_keeper_lineno_5 = exception_lineno;
    exception_type = NULL;
    exception_value = NULL;
    exception_tb = NULL;
    exception_lineno = 0;

    Py_XDECREF( tmp_import_from_5__module );
    tmp_import_from_5__module = NULL;

    // Re-raise.
    exception_type = exception_keeper_type_5;
    exception_value = exception_keeper_value_5;
    exception_tb = exception_keeper_tb_5;
    exception_lineno = exception_keeper_lineno_5;

    goto frame_exception_exit_1;
    // End of try:
    try_end_5:;
    Py_XDECREF( tmp_import_from_5__module );
    tmp_import_from_5__module = NULL;

    tmp_name_name_10 = const_str_digest_9771cbb3646ea84961e9853ca850451d;
    tmp_globals_name_10 = (PyObject *)moduledict_pytest;
    tmp_locals_name_10 = Py_None;
    tmp_fromlist_name_10 = const_tuple_e16e1cfe85916ebb0b4b718008f1b571_tuple;
    tmp_level_name_10 = const_int_0;
    frame_531a1df80b944f2591c7ecbce6b9ae81->m_frame.f_lineno = 21;
    tmp_assign_source_33 = IMPORT_MODULE5( tmp_name_name_10, tmp_globals_name_10, tmp_locals_name_10, tmp_fromlist_name_10, tmp_level_name_10 );
    if ( tmp_assign_source_33 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 21;

        goto frame_exception_exit_1;
    }
    assert( tmp_import_from_6__module == NULL );
    tmp_import_from_6__module = tmp_assign_source_33;

    // Tried code:
    tmp_import_name_from_22 = tmp_import_from_6__module;

    CHECK_OBJECT( tmp_import_name_from_22 );
    tmp_assign_source_34 = IMPORT_NAME( tmp_import_name_from_22, const_str_plain_Item );
    if ( tmp_assign_source_34 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 21;

        goto try_except_handler_6;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_Item, tmp_assign_source_34 );
    tmp_import_name_from_23 = tmp_import_from_6__module;

    CHECK_OBJECT( tmp_import_name_from_23 );
    tmp_assign_source_35 = IMPORT_NAME( tmp_import_name_from_23, const_str_plain_Collector );
    if ( tmp_assign_source_35 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 21;

        goto try_except_handler_6;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_Collector, tmp_assign_source_35 );
    tmp_import_name_from_24 = tmp_import_from_6__module;

    CHECK_OBJECT( tmp_import_name_from_24 );
    tmp_assign_source_36 = IMPORT_NAME( tmp_import_name_from_24, const_str_plain_File );
    if ( tmp_assign_source_36 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 21;

        goto try_except_handler_6;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_File, tmp_assign_source_36 );
    tmp_import_name_from_25 = tmp_import_from_6__module;

    CHECK_OBJECT( tmp_import_name_from_25 );
    tmp_assign_source_37 = IMPORT_NAME( tmp_import_name_from_25, const_str_plain_Session );
    if ( tmp_assign_source_37 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 21;

        goto try_except_handler_6;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_Session, tmp_assign_source_37 );
    goto try_end_6;
    // Exception handler code:
    try_except_handler_6:;
    exception_keeper_type_6 = exception_type;
    exception_keeper_value_6 = exception_value;
    exception_keeper_tb_6 = exception_tb;
    exception_keeper_lineno_6 = exception_lineno;
    exception_type = NULL;
    exception_value = NULL;
    exception_tb = NULL;
    exception_lineno = 0;

    Py_XDECREF( tmp_import_from_6__module );
    tmp_import_from_6__module = NULL;

    // Re-raise.
    exception_type = exception_keeper_type_6;
    exception_value = exception_keeper_value_6;
    exception_tb = exception_keeper_tb_6;
    exception_lineno = exception_keeper_lineno_6;

    goto frame_exception_exit_1;
    // End of try:
    try_end_6:;
    Py_XDECREF( tmp_import_from_6__module );
    tmp_import_from_6__module = NULL;

    tmp_name_name_11 = const_str_digest_697519b333303d87961e335e5cc1410d;
    tmp_globals_name_11 = (PyObject *)moduledict_pytest;
    tmp_locals_name_11 = Py_None;
    tmp_fromlist_name_11 = const_tuple_str_plain_fillfixtures_tuple;
    tmp_level_name_11 = const_int_0;
    frame_531a1df80b944f2591c7ecbce6b9ae81->m_frame.f_lineno = 22;
    tmp_import_name_from_26 = IMPORT_MODULE5( tmp_name_name_11, tmp_globals_name_11, tmp_locals_name_11, tmp_fromlist_name_11, tmp_level_name_11 );
    if ( tmp_import_name_from_26 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 22;

        goto frame_exception_exit_1;
    }
    tmp_assign_source_38 = IMPORT_NAME( tmp_import_name_from_26, const_str_plain_fillfixtures );
    Py_DECREF( tmp_import_name_from_26 );
    if ( tmp_assign_source_38 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 22;

        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain__fillfuncargs, tmp_assign_source_38 );
    tmp_name_name_12 = const_str_digest_faf8202d3f6da8ef7f383dafc7c899ef;
    tmp_globals_name_12 = (PyObject *)moduledict_pytest;
    tmp_locals_name_12 = Py_None;
    tmp_fromlist_name_12 = const_tuple_6f7a3ee769ddaf265fd13050628cb485_tuple;
    tmp_level_name_12 = const_int_0;
    frame_531a1df80b944f2591c7ecbce6b9ae81->m_frame.f_lineno = 23;
    tmp_assign_source_39 = IMPORT_MODULE5( tmp_name_name_12, tmp_globals_name_12, tmp_locals_name_12, tmp_fromlist_name_12, tmp_level_name_12 );
    if ( tmp_assign_source_39 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 23;

        goto frame_exception_exit_1;
    }
    assert( tmp_import_from_7__module == NULL );
    tmp_import_from_7__module = tmp_assign_source_39;

    // Tried code:
    tmp_import_name_from_27 = tmp_import_from_7__module;

    CHECK_OBJECT( tmp_import_name_from_27 );
    tmp_assign_source_40 = IMPORT_NAME( tmp_import_name_from_27, const_str_plain_Module );
    if ( tmp_assign_source_40 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 23;

        goto try_except_handler_7;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_Module, tmp_assign_source_40 );
    tmp_import_name_from_28 = tmp_import_from_7__module;

    CHECK_OBJECT( tmp_import_name_from_28 );
    tmp_assign_source_41 = IMPORT_NAME( tmp_import_name_from_28, const_str_plain_Class );
    if ( tmp_assign_source_41 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 23;

        goto try_except_handler_7;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_Class, tmp_assign_source_41 );
    tmp_import_name_from_29 = tmp_import_from_7__module;

    CHECK_OBJECT( tmp_import_name_from_29 );
    tmp_assign_source_42 = IMPORT_NAME( tmp_import_name_from_29, const_str_plain_Instance );
    if ( tmp_assign_source_42 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 23;

        goto try_except_handler_7;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_Instance, tmp_assign_source_42 );
    tmp_import_name_from_30 = tmp_import_from_7__module;

    CHECK_OBJECT( tmp_import_name_from_30 );
    tmp_assign_source_43 = IMPORT_NAME( tmp_import_name_from_30, const_str_plain_Function );
    if ( tmp_assign_source_43 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 23;

        goto try_except_handler_7;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_Function, tmp_assign_source_43 );
    tmp_import_name_from_31 = tmp_import_from_7__module;

    CHECK_OBJECT( tmp_import_name_from_31 );
    tmp_assign_source_44 = IMPORT_NAME( tmp_import_name_from_31, const_str_plain_Generator );
    if ( tmp_assign_source_44 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 23;

        goto try_except_handler_7;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_Generator, tmp_assign_source_44 );
    goto try_end_7;
    // Exception handler code:
    try_except_handler_7:;
    exception_keeper_type_7 = exception_type;
    exception_keeper_value_7 = exception_value;
    exception_keeper_tb_7 = exception_tb;
    exception_keeper_lineno_7 = exception_lineno;
    exception_type = NULL;
    exception_value = NULL;
    exception_tb = NULL;
    exception_lineno = 0;

    Py_XDECREF( tmp_import_from_7__module );
    tmp_import_from_7__module = NULL;

    // Re-raise.
    exception_type = exception_keeper_type_7;
    exception_value = exception_keeper_value_7;
    exception_tb = exception_keeper_tb_7;
    exception_lineno = exception_keeper_lineno_7;

    goto frame_exception_exit_1;
    // End of try:
    try_end_7:;
    Py_XDECREF( tmp_import_from_7__module );
    tmp_import_from_7__module = NULL;

    tmp_name_name_13 = const_str_digest_e2198bbf03f762749d69f082a8deaceb;
    tmp_globals_name_13 = (PyObject *)moduledict_pytest;
    tmp_locals_name_13 = Py_None;
    tmp_fromlist_name_13 = const_tuple_str_plain_approx_str_plain_raises_tuple;
    tmp_level_name_13 = const_int_0;
    frame_531a1df80b944f2591c7ecbce6b9ae81->m_frame.f_lineno = 27;
    tmp_assign_source_45 = IMPORT_MODULE5( tmp_name_name_13, tmp_globals_name_13, tmp_locals_name_13, tmp_fromlist_name_13, tmp_level_name_13 );
    if ( tmp_assign_source_45 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 27;

        goto frame_exception_exit_1;
    }
    assert( tmp_import_from_8__module == NULL );
    tmp_import_from_8__module = tmp_assign_source_45;

    // Tried code:
    tmp_import_name_from_32 = tmp_import_from_8__module;

    CHECK_OBJECT( tmp_import_name_from_32 );
    tmp_assign_source_46 = IMPORT_NAME( tmp_import_name_from_32, const_str_plain_approx );
    if ( tmp_assign_source_46 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 27;

        goto try_except_handler_8;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_approx, tmp_assign_source_46 );
    tmp_import_name_from_33 = tmp_import_from_8__module;

    CHECK_OBJECT( tmp_import_name_from_33 );
    tmp_assign_source_47 = IMPORT_NAME( tmp_import_name_from_33, const_str_plain_raises );
    if ( tmp_assign_source_47 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 27;

        goto try_except_handler_8;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_raises, tmp_assign_source_47 );
    goto try_end_8;
    // Exception handler code:
    try_except_handler_8:;
    exception_keeper_type_8 = exception_type;
    exception_keeper_value_8 = exception_value;
    exception_keeper_tb_8 = exception_tb;
    exception_keeper_lineno_8 = exception_lineno;
    exception_type = NULL;
    exception_value = NULL;
    exception_tb = NULL;
    exception_lineno = 0;

    Py_XDECREF( tmp_import_from_8__module );
    tmp_import_from_8__module = NULL;

    // Re-raise.
    exception_type = exception_keeper_type_8;
    exception_value = exception_keeper_value_8;
    exception_tb = exception_keeper_tb_8;
    exception_lineno = exception_keeper_lineno_8;

    goto frame_exception_exit_1;
    // End of try:
    try_end_8:;
    Py_XDECREF( tmp_import_from_8__module );
    tmp_import_from_8__module = NULL;

    tmp_source_name_1 = GET_STRING_DICT_VALUE( moduledict_pytest, (Nuitka_StringObject *)const_str_plain___pytestPDB );

    if (unlikely( tmp_source_name_1 == NULL ))
    {
        tmp_source_name_1 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain___pytestPDB );
    }

    if ( tmp_source_name_1 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "__pytestPDB" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 29;

        goto frame_exception_exit_1;
    }

    tmp_assign_source_48 = LOOKUP_ATTRIBUTE( tmp_source_name_1, const_str_plain_set_trace );
    if ( tmp_assign_source_48 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 29;

        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain_set_trace, tmp_assign_source_48 );
    tmp_assign_source_49 = LIST_COPY( const_list_ed7164bf5feb489fae584c24800196dd_list );
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain___all__, tmp_assign_source_49 );
    tmp_name_name_14 = const_str_digest_7b5c8649f8daec52e9fa88bdd5c7ccdc;
    tmp_globals_name_14 = (PyObject *)moduledict_pytest;
    tmp_locals_name_14 = Py_None;
    tmp_fromlist_name_14 = const_tuple_str_plain__setup_collect_fakemodule_tuple;
    tmp_level_name_14 = const_int_0;
    frame_531a1df80b944f2591c7ecbce6b9ae81->m_frame.f_lineno = 76;
    tmp_import_name_from_34 = IMPORT_MODULE5( tmp_name_name_14, tmp_globals_name_14, tmp_locals_name_14, tmp_fromlist_name_14, tmp_level_name_14 );
    if ( tmp_import_name_from_34 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 76;

        goto frame_exception_exit_1;
    }
    tmp_assign_source_50 = IMPORT_NAME( tmp_import_name_from_34, const_str_plain__setup_collect_fakemodule );
    Py_DECREF( tmp_import_name_from_34 );
    if ( tmp_assign_source_50 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 76;

        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_pytest, (Nuitka_StringObject *)const_str_plain__setup_collect_fakemodule, tmp_assign_source_50 );
    tmp_called_name_2 = GET_STRING_DICT_VALUE( moduledict_pytest, (Nuitka_StringObject *)const_str_plain__preloadplugins );

    if (unlikely( tmp_called_name_2 == NULL ))
    {
        tmp_called_name_2 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain__preloadplugins );
    }

    if ( tmp_called_name_2 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "_preloadplugins" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 77;

        goto frame_exception_exit_1;
    }

    frame_531a1df80b944f2591c7ecbce6b9ae81->m_frame.f_lineno = 77;
    tmp_unused = CALL_FUNCTION_NO_ARGS( tmp_called_name_2 );
    if ( tmp_unused == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 77;

        goto frame_exception_exit_1;
    }
    Py_DECREF( tmp_unused );
    tmp_called_name_3 = GET_STRING_DICT_VALUE( moduledict_pytest, (Nuitka_StringObject *)const_str_plain__setup_collect_fakemodule );

    if (unlikely( tmp_called_name_3 == NULL ))
    {
        tmp_called_name_3 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain__setup_collect_fakemodule );
    }

    if ( tmp_called_name_3 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "_setup_collect_fakemodule" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 78;

        goto frame_exception_exit_1;
    }

    frame_531a1df80b944f2591c7ecbce6b9ae81->m_frame.f_lineno = 78;
    tmp_unused = CALL_FUNCTION_NO_ARGS( tmp_called_name_3 );
    if ( tmp_unused == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 78;

        goto frame_exception_exit_1;
    }
    Py_DECREF( tmp_unused );

    // Restore frame exception if necessary.
#if 0
    RESTORE_FRAME_EXCEPTION( frame_531a1df80b944f2591c7ecbce6b9ae81 );
#endif
    popFrameStack();

    assertFrameObject( frame_531a1df80b944f2591c7ecbce6b9ae81 );

    goto frame_no_exception_1;
    frame_exception_exit_1:;
#if 0
    RESTORE_FRAME_EXCEPTION( frame_531a1df80b944f2591c7ecbce6b9ae81 );
#endif

    if ( exception_tb == NULL )
    {
        exception_tb = MAKE_TRACEBACK( frame_531a1df80b944f2591c7ecbce6b9ae81, exception_lineno );
    }
    else if ( exception_tb->tb_frame != &frame_531a1df80b944f2591c7ecbce6b9ae81->m_frame )
    {
        exception_tb = ADD_TRACEBACK( exception_tb, frame_531a1df80b944f2591c7ecbce6b9ae81, exception_lineno );
    }

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto module_exception_exit;
    frame_no_exception_1:;

    return MOD_RETURN_VALUE( module_pytest );
    module_exception_exit:
    RESTORE_ERROR_OCCURRED( exception_type, exception_value, exception_tb );
    return MOD_RETURN_VALUE( NULL );
}
