/* Generated code for Python source for module 'borg.platform'
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

/* The _module_borg$platform is a Python object pointer of module type. */

/* Note: For full compatibility with CPython, every module variable access
 * needs to go through it except for cases where the module cannot possibly
 * have changed in the mean time.
 */

PyObject *module_borg$platform;
PyDictObject *moduledict_borg$platform;

/* The module constants used, if any. */
extern PyObject *const_str_plain_OS_API_VERSION;
extern PyObject *const_str_digest_f9c3ced894ae0bca8d377c046b26a23c;
extern PyObject *const_str_plain_API_VERSION;
extern PyObject *const_str_plain_sync_dir;
extern PyObject *const_str_plain_environ;
extern PyObject *const_str_plain_ModuleSpec;
extern PyObject *const_str_plain___spec__;
extern PyObject *const_str_plain___package__;
extern PyObject *const_str_plain_sys;
extern PyObject *const_str_plain_local_pid_alive;
extern PyObject *const_str_plain_linux;
extern PyObject *const_str_plain_posix;
static PyObject *const_tuple_str_plain_freebsd_tuple;
static PyObject *const_str_plain_NUITKA_PACKAGE_borg_platform;
extern PyObject *const_int_pos_1;
extern PyObject *const_str_plain_process_alive;
extern PyObject *const_str_plain_freebsd;
extern PyObject *const_str_plain_safe_fadvise;
extern PyObject *const_str_plain___file__;
static PyObject *const_tuple_str_plain_swidth_str_plain_API_VERSION_tuple;
extern PyObject *const_str_plain_set_flags;
extern PyObject *const_str_plain_path;
extern PyObject *const_int_0;
static PyObject *const_tuple_tuple_str_plain_win32_tuple_tuple;
static PyObject *const_str_digest_f5b46308634bbcc98c3369ca3ea6e5c8;
extern PyObject *const_tuple_str_plain_linux_tuple;
extern PyObject *const_str_plain_acl_get;
extern PyObject *const_str_plain_fdatasync;
extern PyObject *const_str_plain_acl_set;
extern PyObject *const_str_plain_SyncFile;
static PyObject *const_tuple_4c000fd0a4eda37d35c9e905fc6754b5_tuple;
extern PyObject *const_str_plain_NUITKA_PACKAGE_borg;
extern PyObject *const_str_digest_5bfaf90dbd407b4fc29090c8f6415242;
extern PyObject *const_str_plain_get_process_id;
static PyObject *const_tuple_b6e40ced9400ffe10d9dcece75ea755c_tuple;
extern PyObject *const_str_plain___path__;
static PyObject *const_tuple_str_plain_set_flags_str_plain_get_flags_tuple;
extern PyObject *const_str_plain_SaveFile;
extern PyObject *const_str_plain_swidth;
extern PyObject *const_str_plain_get;
extern PyObject *const_tuple_empty;
extern PyObject *const_str_plain_base;
static PyObject *const_tuple_str_plain_SyncFile_tuple;
extern PyObject *const_str_plain_darwin;
extern PyObject *const_tuple_str_plain_swidth_tuple;
static PyObject *const_tuple_str_plain_acl_get_str_plain_acl_set_tuple;
extern PyObject *const_str_plain___loader__;
extern PyObject *const_str_plain_join;
extern PyObject *const_tuple_e0ce4c5c7e89f213a98997732caffbd9_tuple;
extern PyObject *const_str_plain_startswith;
static PyObject *const_tuple_61fa58ed5b974afe0eb97eba740b7a4b_tuple;
extern PyObject *const_str_plain_dirname;
extern PyObject *const_tuple_str_plain_win32_tuple;
extern PyObject *const_str_plain_platform;
static PyObject *const_str_digest_8a45406680b4b7e2dc0967307a8441cb;
extern PyObject *const_str_plain_win32;
extern PyObject *const_str_plain___doc__;
extern PyObject *const_str_plain___cached__;
extern PyObject *const_str_plain_get_flags;
static PyObject *const_tuple_str_plain_API_VERSION_tuple;
static PyObject *module_filename_obj;

static bool constants_created = false;

static void createModuleConstants( void )
{
    const_tuple_str_plain_freebsd_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_freebsd_tuple, 0, const_str_plain_freebsd ); Py_INCREF( const_str_plain_freebsd );
    const_str_plain_NUITKA_PACKAGE_borg_platform = UNSTREAM_STRING( &constant_bin[ 164353 ], 28, 1 );
    const_tuple_str_plain_swidth_str_plain_API_VERSION_tuple = PyTuple_New( 2 );
    PyTuple_SET_ITEM( const_tuple_str_plain_swidth_str_plain_API_VERSION_tuple, 0, const_str_plain_swidth ); Py_INCREF( const_str_plain_swidth );
    PyTuple_SET_ITEM( const_tuple_str_plain_swidth_str_plain_API_VERSION_tuple, 1, const_str_plain_API_VERSION ); Py_INCREF( const_str_plain_API_VERSION );
    const_tuple_tuple_str_plain_win32_tuple_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_tuple_str_plain_win32_tuple_tuple, 0, const_tuple_str_plain_win32_tuple ); Py_INCREF( const_tuple_str_plain_win32_tuple );
    const_str_digest_f5b46308634bbcc98c3369ca3ea6e5c8 = UNSTREAM_STRING( &constant_bin[ 164381 ], 22, 0 );
    const_tuple_4c000fd0a4eda37d35c9e905fc6754b5_tuple = PyTuple_New( 2 );
    PyTuple_SET_ITEM( const_tuple_4c000fd0a4eda37d35c9e905fc6754b5_tuple, 0, const_str_plain_NUITKA_PACKAGE_borg_platform ); Py_INCREF( const_str_plain_NUITKA_PACKAGE_borg_platform );
    PyTuple_SET_ITEM( const_tuple_4c000fd0a4eda37d35c9e905fc6754b5_tuple, 1, const_str_digest_5bfaf90dbd407b4fc29090c8f6415242 ); Py_INCREF( const_str_digest_5bfaf90dbd407b4fc29090c8f6415242 );
    const_tuple_b6e40ced9400ffe10d9dcece75ea755c_tuple = PyTuple_New( 5 );
    PyTuple_SET_ITEM( const_tuple_b6e40ced9400ffe10d9dcece75ea755c_tuple, 0, const_str_plain_SaveFile ); Py_INCREF( const_str_plain_SaveFile );
    PyTuple_SET_ITEM( const_tuple_b6e40ced9400ffe10d9dcece75ea755c_tuple, 1, const_str_plain_SyncFile ); Py_INCREF( const_str_plain_SyncFile );
    PyTuple_SET_ITEM( const_tuple_b6e40ced9400ffe10d9dcece75ea755c_tuple, 2, const_str_plain_sync_dir ); Py_INCREF( const_str_plain_sync_dir );
    PyTuple_SET_ITEM( const_tuple_b6e40ced9400ffe10d9dcece75ea755c_tuple, 3, const_str_plain_fdatasync ); Py_INCREF( const_str_plain_fdatasync );
    PyTuple_SET_ITEM( const_tuple_b6e40ced9400ffe10d9dcece75ea755c_tuple, 4, const_str_plain_safe_fadvise ); Py_INCREF( const_str_plain_safe_fadvise );
    const_tuple_str_plain_set_flags_str_plain_get_flags_tuple = PyTuple_New( 2 );
    PyTuple_SET_ITEM( const_tuple_str_plain_set_flags_str_plain_get_flags_tuple, 0, const_str_plain_set_flags ); Py_INCREF( const_str_plain_set_flags );
    PyTuple_SET_ITEM( const_tuple_str_plain_set_flags_str_plain_get_flags_tuple, 1, const_str_plain_get_flags ); Py_INCREF( const_str_plain_get_flags );
    const_tuple_str_plain_SyncFile_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_SyncFile_tuple, 0, const_str_plain_SyncFile ); Py_INCREF( const_str_plain_SyncFile );
    const_tuple_str_plain_acl_get_str_plain_acl_set_tuple = PyTuple_New( 2 );
    PyTuple_SET_ITEM( const_tuple_str_plain_acl_get_str_plain_acl_set_tuple, 0, const_str_plain_acl_get ); Py_INCREF( const_str_plain_acl_get );
    PyTuple_SET_ITEM( const_tuple_str_plain_acl_get_str_plain_acl_set_tuple, 1, const_str_plain_acl_set ); Py_INCREF( const_str_plain_acl_set );
    const_tuple_61fa58ed5b974afe0eb97eba740b7a4b_tuple = PyTuple_New( 3 );
    PyTuple_SET_ITEM( const_tuple_61fa58ed5b974afe0eb97eba740b7a4b_tuple, 0, const_str_plain_process_alive ); Py_INCREF( const_str_plain_process_alive );
    PyTuple_SET_ITEM( const_tuple_61fa58ed5b974afe0eb97eba740b7a4b_tuple, 1, const_str_plain_get_process_id ); Py_INCREF( const_str_plain_get_process_id );
    PyTuple_SET_ITEM( const_tuple_61fa58ed5b974afe0eb97eba740b7a4b_tuple, 2, const_str_plain_local_pid_alive ); Py_INCREF( const_str_plain_local_pid_alive );
    const_str_digest_8a45406680b4b7e2dc0967307a8441cb = UNSTREAM_STRING( &constant_bin[ 164403 ], 25, 0 );
    const_tuple_str_plain_API_VERSION_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_API_VERSION_tuple, 0, const_str_plain_API_VERSION ); Py_INCREF( const_str_plain_API_VERSION );

    constants_created = true;
}

#ifndef __NUITKA_NO_ASSERT__
void checkModuleConstants_borg$platform( void )
{
    // The module may not have been used at all.
    if (constants_created == false) return;


}
#endif

// The module code objects.
static PyCodeObject *codeobj_75f99a300e3e0a7f2eef0ab8ed958352;

static void createModuleCodeObjects(void)
{
    module_filename_obj = MAKE_RELATIVE_PATH( const_str_digest_8a45406680b4b7e2dc0967307a8441cb );
    codeobj_75f99a300e3e0a7f2eef0ab8ed958352 = MAKE_CODEOBJ( module_filename_obj, const_str_digest_f5b46308634bbcc98c3369ca3ea6e5c8, 1, const_tuple_empty, 0, 0, CO_NOFREE );
}

// The module function declarations.


// The module function definitions.



#if PYTHON_VERSION >= 300
static struct PyModuleDef mdef_borg$platform =
{
    PyModuleDef_HEAD_INIT,
    "borg.platform",   /* m_name */
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

MOD_INIT_DECL( borg$platform )
{
#if defined(_NUITKA_EXE) || PYTHON_VERSION >= 300
    static bool _init_done = false;

    // Modules might be imported repeatedly, which is to be ignored.
    if ( _init_done )
    {
        return MOD_RETURN_VALUE( module_borg$platform );
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
    puts("borg.platform: Calling createModuleConstants().");
#endif
    createModuleConstants();

    /* The code objects used by this module are created now. */
#ifdef _NUITKA_TRACE
    puts("borg.platform: Calling createModuleCodeObjects().");
#endif
    createModuleCodeObjects();

    // puts( "in initborg$platform" );

    // Create the module object first. There are no methods initially, all are
    // added dynamically in actual code only.  Also no "__doc__" is initially
    // set at this time, as it could not contain NUL characters this way, they
    // are instead set in early module code.  No "self" for modules, we have no
    // use for it.
#if PYTHON_VERSION < 300
    module_borg$platform = Py_InitModule4(
        "borg.platform",       // Module Name
        NULL,                    // No methods initially, all are added
                                 // dynamically in actual module code only.
        NULL,                    // No __doc__ is initially set, as it could
                                 // not contain NUL this way, added early in
                                 // actual code.
        NULL,                    // No self for modules, we don't use it.
        PYTHON_API_VERSION
    );
#else
    module_borg$platform = PyModule_Create( &mdef_borg$platform );
#endif

    moduledict_borg$platform = MODULE_DICT( module_borg$platform );

    CHECK_OBJECT( module_borg$platform );

// Seems to work for Python2.7 out of the box, but for Python3, the module
// doesn't automatically enter "sys.modules", so do it manually.
#if PYTHON_VERSION >= 300
    {
        int r = PyObject_SetItem( PySys_GetObject( (char *)"modules" ), const_str_digest_f9c3ced894ae0bca8d377c046b26a23c, module_borg$platform );

        assert( r != -1 );
    }
#endif

    // For deep importing of a module we need to have "__builtins__", so we set
    // it ourselves in the same way than CPython does. Note: This must be done
    // before the frame object is allocated, or else it may fail.

    if ( GET_STRING_DICT_VALUE( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain___builtins__ ) == NULL )
    {
        PyObject *value = (PyObject *)builtin_module;

        // Check if main module, not a dict then but the module itself.
#if !defined(_NUITKA_EXE) || !0
        value = PyModule_GetDict( value );
#endif

        UPDATE_STRING_DICT0( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain___builtins__, value );
    }

#if PYTHON_VERSION >= 330
    UPDATE_STRING_DICT0( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain___loader__, metapath_based_loader );
#endif

    // Temp variables if any
    PyObject *tmp_import_from_10__module = NULL;
    PyObject *tmp_import_from_1__module = NULL;
    PyObject *tmp_import_from_2__module = NULL;
    PyObject *tmp_import_from_3__module = NULL;
    PyObject *tmp_import_from_4__module = NULL;
    PyObject *tmp_import_from_5__module = NULL;
    PyObject *tmp_import_from_6__module = NULL;
    PyObject *tmp_import_from_7__module = NULL;
    PyObject *tmp_import_from_8__module = NULL;
    PyObject *tmp_import_from_9__module = NULL;
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
    PyObject *exception_keeper_type_9;
    PyObject *exception_keeper_value_9;
    PyTracebackObject *exception_keeper_tb_9;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_9;
    PyObject *exception_keeper_type_10;
    PyObject *exception_keeper_value_10;
    PyTracebackObject *exception_keeper_tb_10;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_10;
    PyObject *tmp_args_element_name_1;
    PyObject *tmp_args_element_name_2;
    PyObject *tmp_args_element_name_3;
    PyObject *tmp_args_element_name_4;
    PyObject *tmp_args_element_name_5;
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
    PyObject *tmp_assign_source_51;
    PyObject *tmp_called_instance_1;
    PyObject *tmp_called_instance_2;
    PyObject *tmp_called_instance_3;
    PyObject *tmp_called_instance_4;
    PyObject *tmp_called_instance_5;
    PyObject *tmp_called_name_1;
    PyObject *tmp_called_name_2;
    PyObject *tmp_called_name_3;
    int tmp_cmp_Eq_1;
    PyObject *tmp_compare_left_1;
    PyObject *tmp_compare_right_1;
    int tmp_cond_truth_1;
    int tmp_cond_truth_2;
    int tmp_cond_truth_3;
    PyObject *tmp_cond_value_1;
    PyObject *tmp_cond_value_2;
    PyObject *tmp_cond_value_3;
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
    PyObject *tmp_fromlist_name_15;
    PyObject *tmp_fromlist_name_16;
    PyObject *tmp_fromlist_name_17;
    PyObject *tmp_fromlist_name_18;
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
    PyObject *tmp_globals_name_15;
    PyObject *tmp_globals_name_16;
    PyObject *tmp_globals_name_17;
    PyObject *tmp_globals_name_18;
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
    PyObject *tmp_level_name_15;
    PyObject *tmp_level_name_16;
    PyObject *tmp_level_name_17;
    PyObject *tmp_level_name_18;
    PyObject *tmp_list_element_1;
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
    PyObject *tmp_locals_name_15;
    PyObject *tmp_locals_name_16;
    PyObject *tmp_locals_name_17;
    PyObject *tmp_locals_name_18;
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
    PyObject *tmp_name_name_15;
    PyObject *tmp_name_name_16;
    PyObject *tmp_name_name_17;
    PyObject *tmp_name_name_18;
    PyObject *tmp_source_name_1;
    PyObject *tmp_source_name_2;
    PyObject *tmp_source_name_3;
    PyObject *tmp_source_name_4;
    PyObject *tmp_source_name_5;
    PyObject *tmp_source_name_6;
    struct Nuitka_FrameObject *frame_75f99a300e3e0a7f2eef0ab8ed958352;

    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;

    // Module code.
    tmp_assign_source_1 = Py_None;
    UPDATE_STRING_DICT0( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain___doc__, tmp_assign_source_1 );
    tmp_assign_source_2 = module_filename_obj;
    UPDATE_STRING_DICT0( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain___file__, tmp_assign_source_2 );
    // Frame without reuse.
    frame_75f99a300e3e0a7f2eef0ab8ed958352 = MAKE_MODULE_FRAME( codeobj_75f99a300e3e0a7f2eef0ab8ed958352, module_borg$platform );

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStack( frame_75f99a300e3e0a7f2eef0ab8ed958352 );
    assert( Py_REFCNT( frame_75f99a300e3e0a7f2eef0ab8ed958352 ) == 2 );

    // Framed code:
    tmp_assign_source_3 = PyList_New( 3 );
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 1;
    {
        PyObject *module = PyImport_ImportModule("os");
        if (likely( module != NULL ))
        {
            tmp_source_name_1 = PyObject_GetAttr( module, const_str_plain_path );
        }
        else
        {
            tmp_source_name_1 = NULL;
        }
    }

    if ( tmp_source_name_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_3 );

        exception_lineno = 1;

        goto frame_exception_exit_1;
    }
    tmp_called_name_1 = LOOKUP_ATTRIBUTE( tmp_source_name_1, const_str_plain_dirname );
    if ( tmp_called_name_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_3 );

        exception_lineno = 1;

        goto frame_exception_exit_1;
    }
    tmp_args_element_name_1 = module_filename_obj;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 1;
    {
        PyObject *call_args[] = { tmp_args_element_name_1 };
        tmp_list_element_1 = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_1, call_args );
    }

    Py_DECREF( tmp_called_name_1 );
    if ( tmp_list_element_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_3 );

        exception_lineno = 1;

        goto frame_exception_exit_1;
    }
    PyList_SET_ITEM( tmp_assign_source_3, 0, tmp_list_element_1 );
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 1;
    {
        PyObject *module = PyImport_ImportModule("os");
        if (likely( module != NULL ))
        {
            tmp_source_name_2 = PyObject_GetAttr( module, const_str_plain_path );
        }
        else
        {
            tmp_source_name_2 = NULL;
        }
    }

    if ( tmp_source_name_2 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_3 );

        exception_lineno = 1;

        goto frame_exception_exit_1;
    }
    tmp_called_name_2 = LOOKUP_ATTRIBUTE( tmp_source_name_2, const_str_plain_join );
    if ( tmp_called_name_2 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_3 );

        exception_lineno = 1;

        goto frame_exception_exit_1;
    }
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 1;
    {
        PyObject *module = PyImport_ImportModule("os");
        if (likely( module != NULL ))
        {
            tmp_called_instance_1 = PyObject_GetAttr( module, const_str_plain_environ );
        }
        else
        {
            tmp_called_instance_1 = NULL;
        }
    }

    if ( tmp_called_instance_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_3 );
        Py_DECREF( tmp_called_name_2 );

        exception_lineno = 1;

        goto frame_exception_exit_1;
    }
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 1;
    tmp_args_element_name_2 = CALL_METHOD_WITH_ARGS2( tmp_called_instance_1, const_str_plain_get, &PyTuple_GET_ITEM( const_tuple_e0ce4c5c7e89f213a98997732caffbd9_tuple, 0 ) );

    if ( tmp_args_element_name_2 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_3 );
        Py_DECREF( tmp_called_name_2 );

        exception_lineno = 1;

        goto frame_exception_exit_1;
    }
    tmp_args_element_name_3 = const_str_plain_platform;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 1;
    {
        PyObject *call_args[] = { tmp_args_element_name_2, tmp_args_element_name_3 };
        tmp_list_element_1 = CALL_FUNCTION_WITH_ARGS2( tmp_called_name_2, call_args );
    }

    Py_DECREF( tmp_called_name_2 );
    Py_DECREF( tmp_args_element_name_2 );
    if ( tmp_list_element_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_3 );

        exception_lineno = 1;

        goto frame_exception_exit_1;
    }
    PyList_SET_ITEM( tmp_assign_source_3, 1, tmp_list_element_1 );
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 1;
    {
        PyObject *module = PyImport_ImportModule("os");
        if (likely( module != NULL ))
        {
            tmp_called_instance_2 = PyObject_GetAttr( module, const_str_plain_environ );
        }
        else
        {
            tmp_called_instance_2 = NULL;
        }
    }

    if ( tmp_called_instance_2 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_3 );

        exception_lineno = 1;

        goto frame_exception_exit_1;
    }
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 1;
    tmp_list_element_1 = CALL_METHOD_WITH_ARGS2( tmp_called_instance_2, const_str_plain_get, &PyTuple_GET_ITEM( const_tuple_4c000fd0a4eda37d35c9e905fc6754b5_tuple, 0 ) );

    if ( tmp_list_element_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_3 );

        exception_lineno = 1;

        goto frame_exception_exit_1;
    }
    PyList_SET_ITEM( tmp_assign_source_3, 2, tmp_list_element_1 );
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain___path__, tmp_assign_source_3 );
    tmp_assign_source_4 = metapath_based_loader;
    UPDATE_STRING_DICT0( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain___loader__, tmp_assign_source_4 );
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 1;
    {
        PyObject *module = PyImport_ImportModule("importlib._bootstrap");
        if (likely( module != NULL ))
        {
            tmp_called_name_3 = PyObject_GetAttr( module, const_str_plain_ModuleSpec );
        }
        else
        {
            tmp_called_name_3 = NULL;
        }
    }

    if ( tmp_called_name_3 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 1;

        goto frame_exception_exit_1;
    }
    tmp_args_element_name_4 = const_str_digest_f9c3ced894ae0bca8d377c046b26a23c;
    tmp_args_element_name_5 = metapath_based_loader;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 1;
    {
        PyObject *call_args[] = { tmp_args_element_name_4, tmp_args_element_name_5 };
        tmp_assign_source_5 = CALL_FUNCTION_WITH_ARGS2( tmp_called_name_3, call_args );
    }

    if ( tmp_assign_source_5 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 1;

        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain___spec__, tmp_assign_source_5 );
    tmp_assign_source_6 = Py_None;
    UPDATE_STRING_DICT0( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain___cached__, tmp_assign_source_6 );
    tmp_assign_source_7 = const_str_digest_f9c3ced894ae0bca8d377c046b26a23c;
    UPDATE_STRING_DICT0( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain___package__, tmp_assign_source_7 );
    tmp_name_name_1 = const_str_plain_sys;
    tmp_globals_name_1 = (PyObject *)moduledict_borg$platform;
    tmp_locals_name_1 = Py_None;
    tmp_fromlist_name_1 = Py_None;
    tmp_level_name_1 = const_int_0;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 1;
    tmp_assign_source_8 = IMPORT_MODULE5( tmp_name_name_1, tmp_globals_name_1, tmp_locals_name_1, tmp_fromlist_name_1, tmp_level_name_1 );
    assert( tmp_assign_source_8 != NULL );
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_sys, tmp_assign_source_8 );
    tmp_name_name_2 = const_str_plain_base;
    tmp_globals_name_2 = (PyObject *)moduledict_borg$platform;
    tmp_locals_name_2 = Py_None;
    tmp_fromlist_name_2 = const_tuple_str_plain_acl_get_str_plain_acl_set_tuple;
    tmp_level_name_2 = const_int_pos_1;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 9;
    tmp_assign_source_9 = IMPORT_MODULE5( tmp_name_name_2, tmp_globals_name_2, tmp_locals_name_2, tmp_fromlist_name_2, tmp_level_name_2 );
    if ( tmp_assign_source_9 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 9;

        goto frame_exception_exit_1;
    }
    assert( tmp_import_from_1__module == NULL );
    tmp_import_from_1__module = tmp_assign_source_9;

    // Tried code:
    tmp_import_name_from_1 = tmp_import_from_1__module;

    CHECK_OBJECT( tmp_import_name_from_1 );
    tmp_assign_source_10 = IMPORT_NAME( tmp_import_name_from_1, const_str_plain_acl_get );
    if ( tmp_assign_source_10 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 9;

        goto try_except_handler_1;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_acl_get, tmp_assign_source_10 );
    tmp_import_name_from_2 = tmp_import_from_1__module;

    CHECK_OBJECT( tmp_import_name_from_2 );
    tmp_assign_source_11 = IMPORT_NAME( tmp_import_name_from_2, const_str_plain_acl_set );
    if ( tmp_assign_source_11 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 9;

        goto try_except_handler_1;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_acl_set, tmp_assign_source_11 );
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

    tmp_name_name_3 = const_str_plain_base;
    tmp_globals_name_3 = (PyObject *)moduledict_borg$platform;
    tmp_locals_name_3 = Py_None;
    tmp_fromlist_name_3 = const_tuple_str_plain_set_flags_str_plain_get_flags_tuple;
    tmp_level_name_3 = const_int_pos_1;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 10;
    tmp_assign_source_12 = IMPORT_MODULE5( tmp_name_name_3, tmp_globals_name_3, tmp_locals_name_3, tmp_fromlist_name_3, tmp_level_name_3 );
    if ( tmp_assign_source_12 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 10;

        goto frame_exception_exit_1;
    }
    assert( tmp_import_from_2__module == NULL );
    tmp_import_from_2__module = tmp_assign_source_12;

    // Tried code:
    tmp_import_name_from_3 = tmp_import_from_2__module;

    CHECK_OBJECT( tmp_import_name_from_3 );
    tmp_assign_source_13 = IMPORT_NAME( tmp_import_name_from_3, const_str_plain_set_flags );
    if ( tmp_assign_source_13 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 10;

        goto try_except_handler_2;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_set_flags, tmp_assign_source_13 );
    tmp_import_name_from_4 = tmp_import_from_2__module;

    CHECK_OBJECT( tmp_import_name_from_4 );
    tmp_assign_source_14 = IMPORT_NAME( tmp_import_name_from_4, const_str_plain_get_flags );
    if ( tmp_assign_source_14 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 10;

        goto try_except_handler_2;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_get_flags, tmp_assign_source_14 );
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

    tmp_name_name_4 = const_str_plain_base;
    tmp_globals_name_4 = (PyObject *)moduledict_borg$platform;
    tmp_locals_name_4 = Py_None;
    tmp_fromlist_name_4 = const_tuple_b6e40ced9400ffe10d9dcece75ea755c_tuple;
    tmp_level_name_4 = const_int_pos_1;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 11;
    tmp_assign_source_15 = IMPORT_MODULE5( tmp_name_name_4, tmp_globals_name_4, tmp_locals_name_4, tmp_fromlist_name_4, tmp_level_name_4 );
    if ( tmp_assign_source_15 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 11;

        goto frame_exception_exit_1;
    }
    assert( tmp_import_from_3__module == NULL );
    tmp_import_from_3__module = tmp_assign_source_15;

    // Tried code:
    tmp_import_name_from_5 = tmp_import_from_3__module;

    CHECK_OBJECT( tmp_import_name_from_5 );
    tmp_assign_source_16 = IMPORT_NAME( tmp_import_name_from_5, const_str_plain_SaveFile );
    if ( tmp_assign_source_16 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 11;

        goto try_except_handler_3;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_SaveFile, tmp_assign_source_16 );
    tmp_import_name_from_6 = tmp_import_from_3__module;

    CHECK_OBJECT( tmp_import_name_from_6 );
    tmp_assign_source_17 = IMPORT_NAME( tmp_import_name_from_6, const_str_plain_SyncFile );
    if ( tmp_assign_source_17 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 11;

        goto try_except_handler_3;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_SyncFile, tmp_assign_source_17 );
    tmp_import_name_from_7 = tmp_import_from_3__module;

    CHECK_OBJECT( tmp_import_name_from_7 );
    tmp_assign_source_18 = IMPORT_NAME( tmp_import_name_from_7, const_str_plain_sync_dir );
    if ( tmp_assign_source_18 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 11;

        goto try_except_handler_3;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_sync_dir, tmp_assign_source_18 );
    tmp_import_name_from_8 = tmp_import_from_3__module;

    CHECK_OBJECT( tmp_import_name_from_8 );
    tmp_assign_source_19 = IMPORT_NAME( tmp_import_name_from_8, const_str_plain_fdatasync );
    if ( tmp_assign_source_19 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 11;

        goto try_except_handler_3;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_fdatasync, tmp_assign_source_19 );
    tmp_import_name_from_9 = tmp_import_from_3__module;

    CHECK_OBJECT( tmp_import_name_from_9 );
    tmp_assign_source_20 = IMPORT_NAME( tmp_import_name_from_9, const_str_plain_safe_fadvise );
    if ( tmp_assign_source_20 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 11;

        goto try_except_handler_3;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_safe_fadvise, tmp_assign_source_20 );
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

    tmp_name_name_5 = const_str_plain_base;
    tmp_globals_name_5 = (PyObject *)moduledict_borg$platform;
    tmp_locals_name_5 = Py_None;
    tmp_fromlist_name_5 = const_tuple_str_plain_swidth_str_plain_API_VERSION_tuple;
    tmp_level_name_5 = const_int_pos_1;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 12;
    tmp_assign_source_21 = IMPORT_MODULE5( tmp_name_name_5, tmp_globals_name_5, tmp_locals_name_5, tmp_fromlist_name_5, tmp_level_name_5 );
    if ( tmp_assign_source_21 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 12;

        goto frame_exception_exit_1;
    }
    assert( tmp_import_from_4__module == NULL );
    tmp_import_from_4__module = tmp_assign_source_21;

    // Tried code:
    tmp_import_name_from_10 = tmp_import_from_4__module;

    CHECK_OBJECT( tmp_import_name_from_10 );
    tmp_assign_source_22 = IMPORT_NAME( tmp_import_name_from_10, const_str_plain_swidth );
    if ( tmp_assign_source_22 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 12;

        goto try_except_handler_4;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_swidth, tmp_assign_source_22 );
    tmp_import_name_from_11 = tmp_import_from_4__module;

    CHECK_OBJECT( tmp_import_name_from_11 );
    tmp_assign_source_23 = IMPORT_NAME( tmp_import_name_from_11, const_str_plain_API_VERSION );
    if ( tmp_assign_source_23 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 12;

        goto try_except_handler_4;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_API_VERSION, tmp_assign_source_23 );
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

    tmp_name_name_6 = const_str_plain_base;
    tmp_globals_name_6 = (PyObject *)moduledict_borg$platform;
    tmp_locals_name_6 = Py_None;
    tmp_fromlist_name_6 = const_tuple_61fa58ed5b974afe0eb97eba740b7a4b_tuple;
    tmp_level_name_6 = const_int_pos_1;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 13;
    tmp_assign_source_24 = IMPORT_MODULE5( tmp_name_name_6, tmp_globals_name_6, tmp_locals_name_6, tmp_fromlist_name_6, tmp_level_name_6 );
    if ( tmp_assign_source_24 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 13;

        goto frame_exception_exit_1;
    }
    assert( tmp_import_from_5__module == NULL );
    tmp_import_from_5__module = tmp_assign_source_24;

    // Tried code:
    tmp_import_name_from_12 = tmp_import_from_5__module;

    CHECK_OBJECT( tmp_import_name_from_12 );
    tmp_assign_source_25 = IMPORT_NAME( tmp_import_name_from_12, const_str_plain_process_alive );
    if ( tmp_assign_source_25 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 13;

        goto try_except_handler_5;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_process_alive, tmp_assign_source_25 );
    tmp_import_name_from_13 = tmp_import_from_5__module;

    CHECK_OBJECT( tmp_import_name_from_13 );
    tmp_assign_source_26 = IMPORT_NAME( tmp_import_name_from_13, const_str_plain_get_process_id );
    if ( tmp_assign_source_26 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 13;

        goto try_except_handler_5;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_get_process_id, tmp_assign_source_26 );
    tmp_import_name_from_14 = tmp_import_from_5__module;

    CHECK_OBJECT( tmp_import_name_from_14 );
    tmp_assign_source_27 = IMPORT_NAME( tmp_import_name_from_14, const_str_plain_local_pid_alive );
    if ( tmp_assign_source_27 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 13;

        goto try_except_handler_5;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_local_pid_alive, tmp_assign_source_27 );
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

    tmp_assign_source_28 = GET_STRING_DICT_VALUE( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_API_VERSION );

    if (unlikely( tmp_assign_source_28 == NULL ))
    {
        tmp_assign_source_28 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_API_VERSION );
    }

    if ( tmp_assign_source_28 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "API_VERSION" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 15;

        goto frame_exception_exit_1;
    }

    UPDATE_STRING_DICT0( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_OS_API_VERSION, tmp_assign_source_28 );
    tmp_source_name_3 = GET_STRING_DICT_VALUE( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_sys );

    if (unlikely( tmp_source_name_3 == NULL ))
    {
        tmp_source_name_3 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_sys );
    }

    if ( tmp_source_name_3 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "sys" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 17;

        goto frame_exception_exit_1;
    }

    tmp_called_instance_3 = LOOKUP_ATTRIBUTE( tmp_source_name_3, const_str_plain_platform );
    if ( tmp_called_instance_3 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 17;

        goto frame_exception_exit_1;
    }
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 17;
    tmp_cond_value_1 = CALL_METHOD_WITH_ARGS1( tmp_called_instance_3, const_str_plain_startswith, &PyTuple_GET_ITEM( const_tuple_tuple_str_plain_win32_tuple_tuple, 0 ) );

    Py_DECREF( tmp_called_instance_3 );
    if ( tmp_cond_value_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 17;

        goto frame_exception_exit_1;
    }
    tmp_cond_truth_1 = CHECK_IF_TRUE( tmp_cond_value_1 );
    if ( tmp_cond_truth_1 == -1 )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_cond_value_1 );

        exception_lineno = 17;

        goto frame_exception_exit_1;
    }
    Py_DECREF( tmp_cond_value_1 );
    if ( tmp_cond_truth_1 == 1 )
    {
        goto branch_no_1;
    }
    else
    {
        goto branch_yes_1;
    }
    branch_yes_1:;
    tmp_name_name_7 = const_str_plain_posix;
    tmp_globals_name_7 = (PyObject *)moduledict_borg$platform;
    tmp_locals_name_7 = Py_None;
    tmp_fromlist_name_7 = const_tuple_61fa58ed5b974afe0eb97eba740b7a4b_tuple;
    tmp_level_name_7 = const_int_pos_1;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 18;
    tmp_assign_source_29 = IMPORT_MODULE5( tmp_name_name_7, tmp_globals_name_7, tmp_locals_name_7, tmp_fromlist_name_7, tmp_level_name_7 );
    if ( tmp_assign_source_29 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 18;

        goto frame_exception_exit_1;
    }
    assert( tmp_import_from_6__module == NULL );
    tmp_import_from_6__module = tmp_assign_source_29;

    // Tried code:
    tmp_import_name_from_15 = tmp_import_from_6__module;

    CHECK_OBJECT( tmp_import_name_from_15 );
    tmp_assign_source_30 = IMPORT_NAME( tmp_import_name_from_15, const_str_plain_process_alive );
    if ( tmp_assign_source_30 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 18;

        goto try_except_handler_6;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_process_alive, tmp_assign_source_30 );
    tmp_import_name_from_16 = tmp_import_from_6__module;

    CHECK_OBJECT( tmp_import_name_from_16 );
    tmp_assign_source_31 = IMPORT_NAME( tmp_import_name_from_16, const_str_plain_get_process_id );
    if ( tmp_assign_source_31 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 18;

        goto try_except_handler_6;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_get_process_id, tmp_assign_source_31 );
    tmp_import_name_from_17 = tmp_import_from_6__module;

    CHECK_OBJECT( tmp_import_name_from_17 );
    tmp_assign_source_32 = IMPORT_NAME( tmp_import_name_from_17, const_str_plain_local_pid_alive );
    if ( tmp_assign_source_32 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 18;

        goto try_except_handler_6;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_local_pid_alive, tmp_assign_source_32 );
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

    branch_no_1:;
    tmp_source_name_4 = GET_STRING_DICT_VALUE( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_sys );

    if (unlikely( tmp_source_name_4 == NULL ))
    {
        tmp_source_name_4 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_sys );
    }

    if ( tmp_source_name_4 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "sys" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 20;

        goto frame_exception_exit_1;
    }

    tmp_called_instance_4 = LOOKUP_ATTRIBUTE( tmp_source_name_4, const_str_plain_platform );
    if ( tmp_called_instance_4 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 20;

        goto frame_exception_exit_1;
    }
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 20;
    tmp_cond_value_2 = CALL_METHOD_WITH_ARGS1( tmp_called_instance_4, const_str_plain_startswith, &PyTuple_GET_ITEM( const_tuple_str_plain_linux_tuple, 0 ) );

    Py_DECREF( tmp_called_instance_4 );
    if ( tmp_cond_value_2 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 20;

        goto frame_exception_exit_1;
    }
    tmp_cond_truth_2 = CHECK_IF_TRUE( tmp_cond_value_2 );
    if ( tmp_cond_truth_2 == -1 )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_cond_value_2 );

        exception_lineno = 20;

        goto frame_exception_exit_1;
    }
    Py_DECREF( tmp_cond_value_2 );
    if ( tmp_cond_truth_2 == 1 )
    {
        goto branch_yes_2;
    }
    else
    {
        goto branch_no_2;
    }
    branch_yes_2:;
    tmp_name_name_8 = const_str_plain_linux;
    tmp_globals_name_8 = (PyObject *)moduledict_borg$platform;
    tmp_locals_name_8 = Py_None;
    tmp_fromlist_name_8 = const_tuple_str_plain_API_VERSION_tuple;
    tmp_level_name_8 = const_int_pos_1;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 21;
    tmp_import_name_from_18 = IMPORT_MODULE5( tmp_name_name_8, tmp_globals_name_8, tmp_locals_name_8, tmp_fromlist_name_8, tmp_level_name_8 );
    if ( tmp_import_name_from_18 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 21;

        goto frame_exception_exit_1;
    }
    tmp_assign_source_33 = IMPORT_NAME( tmp_import_name_from_18, const_str_plain_API_VERSION );
    Py_DECREF( tmp_import_name_from_18 );
    if ( tmp_assign_source_33 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 21;

        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_OS_API_VERSION, tmp_assign_source_33 );
    tmp_name_name_9 = const_str_plain_linux;
    tmp_globals_name_9 = (PyObject *)moduledict_borg$platform;
    tmp_locals_name_9 = Py_None;
    tmp_fromlist_name_9 = const_tuple_str_plain_acl_get_str_plain_acl_set_tuple;
    tmp_level_name_9 = const_int_pos_1;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 22;
    tmp_assign_source_34 = IMPORT_MODULE5( tmp_name_name_9, tmp_globals_name_9, tmp_locals_name_9, tmp_fromlist_name_9, tmp_level_name_9 );
    if ( tmp_assign_source_34 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 22;

        goto frame_exception_exit_1;
    }
    assert( tmp_import_from_7__module == NULL );
    tmp_import_from_7__module = tmp_assign_source_34;

    // Tried code:
    tmp_import_name_from_19 = tmp_import_from_7__module;

    CHECK_OBJECT( tmp_import_name_from_19 );
    tmp_assign_source_35 = IMPORT_NAME( tmp_import_name_from_19, const_str_plain_acl_get );
    if ( tmp_assign_source_35 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 22;

        goto try_except_handler_7;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_acl_get, tmp_assign_source_35 );
    tmp_import_name_from_20 = tmp_import_from_7__module;

    CHECK_OBJECT( tmp_import_name_from_20 );
    tmp_assign_source_36 = IMPORT_NAME( tmp_import_name_from_20, const_str_plain_acl_set );
    if ( tmp_assign_source_36 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 22;

        goto try_except_handler_7;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_acl_set, tmp_assign_source_36 );
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

    tmp_name_name_10 = const_str_plain_linux;
    tmp_globals_name_10 = (PyObject *)moduledict_borg$platform;
    tmp_locals_name_10 = Py_None;
    tmp_fromlist_name_10 = const_tuple_str_plain_set_flags_str_plain_get_flags_tuple;
    tmp_level_name_10 = const_int_pos_1;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 23;
    tmp_assign_source_37 = IMPORT_MODULE5( tmp_name_name_10, tmp_globals_name_10, tmp_locals_name_10, tmp_fromlist_name_10, tmp_level_name_10 );
    if ( tmp_assign_source_37 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 23;

        goto frame_exception_exit_1;
    }
    assert( tmp_import_from_8__module == NULL );
    tmp_import_from_8__module = tmp_assign_source_37;

    // Tried code:
    tmp_import_name_from_21 = tmp_import_from_8__module;

    CHECK_OBJECT( tmp_import_name_from_21 );
    tmp_assign_source_38 = IMPORT_NAME( tmp_import_name_from_21, const_str_plain_set_flags );
    if ( tmp_assign_source_38 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 23;

        goto try_except_handler_8;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_set_flags, tmp_assign_source_38 );
    tmp_import_name_from_22 = tmp_import_from_8__module;

    CHECK_OBJECT( tmp_import_name_from_22 );
    tmp_assign_source_39 = IMPORT_NAME( tmp_import_name_from_22, const_str_plain_get_flags );
    if ( tmp_assign_source_39 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 23;

        goto try_except_handler_8;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_get_flags, tmp_assign_source_39 );
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

    tmp_name_name_11 = const_str_plain_linux;
    tmp_globals_name_11 = (PyObject *)moduledict_borg$platform;
    tmp_locals_name_11 = Py_None;
    tmp_fromlist_name_11 = const_tuple_str_plain_SyncFile_tuple;
    tmp_level_name_11 = const_int_pos_1;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 24;
    tmp_import_name_from_23 = IMPORT_MODULE5( tmp_name_name_11, tmp_globals_name_11, tmp_locals_name_11, tmp_fromlist_name_11, tmp_level_name_11 );
    if ( tmp_import_name_from_23 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 24;

        goto frame_exception_exit_1;
    }
    tmp_assign_source_40 = IMPORT_NAME( tmp_import_name_from_23, const_str_plain_SyncFile );
    Py_DECREF( tmp_import_name_from_23 );
    if ( tmp_assign_source_40 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 24;

        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_SyncFile, tmp_assign_source_40 );
    tmp_name_name_12 = const_str_plain_linux;
    tmp_globals_name_12 = (PyObject *)moduledict_borg$platform;
    tmp_locals_name_12 = Py_None;
    tmp_fromlist_name_12 = const_tuple_str_plain_swidth_tuple;
    tmp_level_name_12 = const_int_pos_1;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 25;
    tmp_import_name_from_24 = IMPORT_MODULE5( tmp_name_name_12, tmp_globals_name_12, tmp_locals_name_12, tmp_fromlist_name_12, tmp_level_name_12 );
    if ( tmp_import_name_from_24 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 25;

        goto frame_exception_exit_1;
    }
    tmp_assign_source_41 = IMPORT_NAME( tmp_import_name_from_24, const_str_plain_swidth );
    Py_DECREF( tmp_import_name_from_24 );
    if ( tmp_assign_source_41 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 25;

        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_swidth, tmp_assign_source_41 );
    goto branch_end_2;
    branch_no_2:;
    tmp_source_name_5 = GET_STRING_DICT_VALUE( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_sys );

    if (unlikely( tmp_source_name_5 == NULL ))
    {
        tmp_source_name_5 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_sys );
    }

    if ( tmp_source_name_5 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "sys" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 26;

        goto frame_exception_exit_1;
    }

    tmp_called_instance_5 = LOOKUP_ATTRIBUTE( tmp_source_name_5, const_str_plain_platform );
    if ( tmp_called_instance_5 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 26;

        goto frame_exception_exit_1;
    }
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 26;
    tmp_cond_value_3 = CALL_METHOD_WITH_ARGS1( tmp_called_instance_5, const_str_plain_startswith, &PyTuple_GET_ITEM( const_tuple_str_plain_freebsd_tuple, 0 ) );

    Py_DECREF( tmp_called_instance_5 );
    if ( tmp_cond_value_3 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 26;

        goto frame_exception_exit_1;
    }
    tmp_cond_truth_3 = CHECK_IF_TRUE( tmp_cond_value_3 );
    if ( tmp_cond_truth_3 == -1 )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_cond_value_3 );

        exception_lineno = 26;

        goto frame_exception_exit_1;
    }
    Py_DECREF( tmp_cond_value_3 );
    if ( tmp_cond_truth_3 == 1 )
    {
        goto branch_yes_3;
    }
    else
    {
        goto branch_no_3;
    }
    branch_yes_3:;
    tmp_name_name_13 = const_str_plain_freebsd;
    tmp_globals_name_13 = (PyObject *)moduledict_borg$platform;
    tmp_locals_name_13 = Py_None;
    tmp_fromlist_name_13 = const_tuple_str_plain_API_VERSION_tuple;
    tmp_level_name_13 = const_int_pos_1;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 27;
    tmp_import_name_from_25 = IMPORT_MODULE5( tmp_name_name_13, tmp_globals_name_13, tmp_locals_name_13, tmp_fromlist_name_13, tmp_level_name_13 );
    if ( tmp_import_name_from_25 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 27;

        goto frame_exception_exit_1;
    }
    tmp_assign_source_42 = IMPORT_NAME( tmp_import_name_from_25, const_str_plain_API_VERSION );
    Py_DECREF( tmp_import_name_from_25 );
    if ( tmp_assign_source_42 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 27;

        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_OS_API_VERSION, tmp_assign_source_42 );
    tmp_name_name_14 = const_str_plain_freebsd;
    tmp_globals_name_14 = (PyObject *)moduledict_borg$platform;
    tmp_locals_name_14 = Py_None;
    tmp_fromlist_name_14 = const_tuple_str_plain_acl_get_str_plain_acl_set_tuple;
    tmp_level_name_14 = const_int_pos_1;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 28;
    tmp_assign_source_43 = IMPORT_MODULE5( tmp_name_name_14, tmp_globals_name_14, tmp_locals_name_14, tmp_fromlist_name_14, tmp_level_name_14 );
    if ( tmp_assign_source_43 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 28;

        goto frame_exception_exit_1;
    }
    assert( tmp_import_from_9__module == NULL );
    tmp_import_from_9__module = tmp_assign_source_43;

    // Tried code:
    tmp_import_name_from_26 = tmp_import_from_9__module;

    CHECK_OBJECT( tmp_import_name_from_26 );
    tmp_assign_source_44 = IMPORT_NAME( tmp_import_name_from_26, const_str_plain_acl_get );
    if ( tmp_assign_source_44 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 28;

        goto try_except_handler_9;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_acl_get, tmp_assign_source_44 );
    tmp_import_name_from_27 = tmp_import_from_9__module;

    CHECK_OBJECT( tmp_import_name_from_27 );
    tmp_assign_source_45 = IMPORT_NAME( tmp_import_name_from_27, const_str_plain_acl_set );
    if ( tmp_assign_source_45 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 28;

        goto try_except_handler_9;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_acl_set, tmp_assign_source_45 );
    goto try_end_9;
    // Exception handler code:
    try_except_handler_9:;
    exception_keeper_type_9 = exception_type;
    exception_keeper_value_9 = exception_value;
    exception_keeper_tb_9 = exception_tb;
    exception_keeper_lineno_9 = exception_lineno;
    exception_type = NULL;
    exception_value = NULL;
    exception_tb = NULL;
    exception_lineno = 0;

    Py_XDECREF( tmp_import_from_9__module );
    tmp_import_from_9__module = NULL;

    // Re-raise.
    exception_type = exception_keeper_type_9;
    exception_value = exception_keeper_value_9;
    exception_tb = exception_keeper_tb_9;
    exception_lineno = exception_keeper_lineno_9;

    goto frame_exception_exit_1;
    // End of try:
    try_end_9:;
    Py_XDECREF( tmp_import_from_9__module );
    tmp_import_from_9__module = NULL;

    tmp_name_name_15 = const_str_plain_freebsd;
    tmp_globals_name_15 = (PyObject *)moduledict_borg$platform;
    tmp_locals_name_15 = Py_None;
    tmp_fromlist_name_15 = const_tuple_str_plain_swidth_tuple;
    tmp_level_name_15 = const_int_pos_1;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 29;
    tmp_import_name_from_28 = IMPORT_MODULE5( tmp_name_name_15, tmp_globals_name_15, tmp_locals_name_15, tmp_fromlist_name_15, tmp_level_name_15 );
    if ( tmp_import_name_from_28 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 29;

        goto frame_exception_exit_1;
    }
    tmp_assign_source_46 = IMPORT_NAME( tmp_import_name_from_28, const_str_plain_swidth );
    Py_DECREF( tmp_import_name_from_28 );
    if ( tmp_assign_source_46 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 29;

        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_swidth, tmp_assign_source_46 );
    goto branch_end_3;
    branch_no_3:;
    tmp_source_name_6 = GET_STRING_DICT_VALUE( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_sys );

    if (unlikely( tmp_source_name_6 == NULL ))
    {
        tmp_source_name_6 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_sys );
    }

    if ( tmp_source_name_6 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "sys" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 30;

        goto frame_exception_exit_1;
    }

    tmp_compare_left_1 = LOOKUP_ATTRIBUTE( tmp_source_name_6, const_str_plain_platform );
    if ( tmp_compare_left_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 30;

        goto frame_exception_exit_1;
    }
    tmp_compare_right_1 = const_str_plain_darwin;
    tmp_cmp_Eq_1 = RICH_COMPARE_BOOL_EQ_NORECURSE( tmp_compare_left_1, tmp_compare_right_1 );
    if ( tmp_cmp_Eq_1 == -1 )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_compare_left_1 );

        exception_lineno = 30;

        goto frame_exception_exit_1;
    }
    Py_DECREF( tmp_compare_left_1 );
    if ( tmp_cmp_Eq_1 == 1 )
    {
        goto branch_yes_4;
    }
    else
    {
        goto branch_no_4;
    }
    branch_yes_4:;
    tmp_name_name_16 = const_str_plain_darwin;
    tmp_globals_name_16 = (PyObject *)moduledict_borg$platform;
    tmp_locals_name_16 = Py_None;
    tmp_fromlist_name_16 = const_tuple_str_plain_API_VERSION_tuple;
    tmp_level_name_16 = const_int_pos_1;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 31;
    tmp_import_name_from_29 = IMPORT_MODULE5( tmp_name_name_16, tmp_globals_name_16, tmp_locals_name_16, tmp_fromlist_name_16, tmp_level_name_16 );
    if ( tmp_import_name_from_29 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 31;

        goto frame_exception_exit_1;
    }
    tmp_assign_source_47 = IMPORT_NAME( tmp_import_name_from_29, const_str_plain_API_VERSION );
    Py_DECREF( tmp_import_name_from_29 );
    if ( tmp_assign_source_47 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 31;

        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_OS_API_VERSION, tmp_assign_source_47 );
    tmp_name_name_17 = const_str_plain_darwin;
    tmp_globals_name_17 = (PyObject *)moduledict_borg$platform;
    tmp_locals_name_17 = Py_None;
    tmp_fromlist_name_17 = const_tuple_str_plain_acl_get_str_plain_acl_set_tuple;
    tmp_level_name_17 = const_int_pos_1;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 32;
    tmp_assign_source_48 = IMPORT_MODULE5( tmp_name_name_17, tmp_globals_name_17, tmp_locals_name_17, tmp_fromlist_name_17, tmp_level_name_17 );
    if ( tmp_assign_source_48 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 32;

        goto frame_exception_exit_1;
    }
    assert( tmp_import_from_10__module == NULL );
    tmp_import_from_10__module = tmp_assign_source_48;

    // Tried code:
    tmp_import_name_from_30 = tmp_import_from_10__module;

    CHECK_OBJECT( tmp_import_name_from_30 );
    tmp_assign_source_49 = IMPORT_NAME( tmp_import_name_from_30, const_str_plain_acl_get );
    if ( tmp_assign_source_49 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 32;

        goto try_except_handler_10;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_acl_get, tmp_assign_source_49 );
    tmp_import_name_from_31 = tmp_import_from_10__module;

    CHECK_OBJECT( tmp_import_name_from_31 );
    tmp_assign_source_50 = IMPORT_NAME( tmp_import_name_from_31, const_str_plain_acl_set );
    if ( tmp_assign_source_50 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 32;

        goto try_except_handler_10;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_acl_set, tmp_assign_source_50 );
    goto try_end_10;
    // Exception handler code:
    try_except_handler_10:;
    exception_keeper_type_10 = exception_type;
    exception_keeper_value_10 = exception_value;
    exception_keeper_tb_10 = exception_tb;
    exception_keeper_lineno_10 = exception_lineno;
    exception_type = NULL;
    exception_value = NULL;
    exception_tb = NULL;
    exception_lineno = 0;

    Py_XDECREF( tmp_import_from_10__module );
    tmp_import_from_10__module = NULL;

    // Re-raise.
    exception_type = exception_keeper_type_10;
    exception_value = exception_keeper_value_10;
    exception_tb = exception_keeper_tb_10;
    exception_lineno = exception_keeper_lineno_10;

    goto frame_exception_exit_1;
    // End of try:
    try_end_10:;
    Py_XDECREF( tmp_import_from_10__module );
    tmp_import_from_10__module = NULL;

    tmp_name_name_18 = const_str_plain_darwin;
    tmp_globals_name_18 = (PyObject *)moduledict_borg$platform;
    tmp_locals_name_18 = Py_None;
    tmp_fromlist_name_18 = const_tuple_str_plain_swidth_tuple;
    tmp_level_name_18 = const_int_pos_1;
    frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame.f_lineno = 33;
    tmp_import_name_from_32 = IMPORT_MODULE5( tmp_name_name_18, tmp_globals_name_18, tmp_locals_name_18, tmp_fromlist_name_18, tmp_level_name_18 );
    if ( tmp_import_name_from_32 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 33;

        goto frame_exception_exit_1;
    }
    tmp_assign_source_51 = IMPORT_NAME( tmp_import_name_from_32, const_str_plain_swidth );
    Py_DECREF( tmp_import_name_from_32 );
    if ( tmp_assign_source_51 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 33;

        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_borg$platform, (Nuitka_StringObject *)const_str_plain_swidth, tmp_assign_source_51 );
    branch_no_4:;
    branch_end_3:;
    branch_end_2:;

    // Restore frame exception if necessary.
#if 0
    RESTORE_FRAME_EXCEPTION( frame_75f99a300e3e0a7f2eef0ab8ed958352 );
#endif
    popFrameStack();

    assertFrameObject( frame_75f99a300e3e0a7f2eef0ab8ed958352 );

    goto frame_no_exception_1;
    frame_exception_exit_1:;
#if 0
    RESTORE_FRAME_EXCEPTION( frame_75f99a300e3e0a7f2eef0ab8ed958352 );
#endif

    if ( exception_tb == NULL )
    {
        exception_tb = MAKE_TRACEBACK( frame_75f99a300e3e0a7f2eef0ab8ed958352, exception_lineno );
    }
    else if ( exception_tb->tb_frame != &frame_75f99a300e3e0a7f2eef0ab8ed958352->m_frame )
    {
        exception_tb = ADD_TRACEBACK( exception_tb, frame_75f99a300e3e0a7f2eef0ab8ed958352, exception_lineno );
    }

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto module_exception_exit;
    frame_no_exception_1:;

    return MOD_RETURN_VALUE( module_borg$platform );
    module_exception_exit:
    RESTORE_ERROR_OCCURRED( exception_type, exception_value, exception_tb );
    return MOD_RETURN_VALUE( NULL );
}
