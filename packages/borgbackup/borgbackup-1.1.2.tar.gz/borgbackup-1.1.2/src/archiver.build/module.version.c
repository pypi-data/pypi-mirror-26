/* Generated code for Python source for module 'version'
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

/* The _module_version is a Python object pointer of module type. */

/* Note: For full compatibility with CPython, every module variable access
 * needs to go through it except for cases where the module cannot possibly
 * have changed in the mean time.
 */

PyObject *module_version;
PyDictObject *moduledict_version;

/* The module constants used, if any. */
static PyObject *const_str_plain_p_type;
extern PyObject *const_str_plain_b;
extern PyObject *const_str_plain_match;
static PyObject *const_str_digest_6c29bb23c35346eba1909ca992181577;
static PyObject *const_tuple_d86ec3fe0d38719b72699837636e9eb9_tuple;
static PyObject *const_list_int_neg_1_list;
extern PyObject *const_str_plain_ModuleSpec;
extern PyObject *const_str_plain___spec__;
extern PyObject *const_str_plain___package__;
extern PyObject *const_str_plain_it;
static PyObject *const_str_plain_p_num;
static PyObject *const_tuple_str_plain_version_str_plain_f_str_plain_it_str_plain_part_tuple;
extern PyObject *const_str_plain_f;
extern PyObject *const_dict_empty;
extern PyObject *const_str_plain___file__;
extern PyObject *const_str_plain_minor;
extern PyObject *const_int_neg_2;
extern PyObject *const_str_plain_parse_version;
extern PyObject *const_str_plain_VERBOSE;
extern PyObject *const_int_0;
static PyObject *const_str_plain_lastgroup;
static PyObject *const_str_digest_edb57ac2b82afc9f2e257f6aafd4ed5f;
static PyObject *const_str_plain_version_re;
extern PyObject *const_str_plain_rc;
extern PyObject *const_int_neg_4;
extern PyObject *const_str_plain_a;
static PyObject *const_str_plain_prerelease;
extern PyObject *const_str_plain_re;
static PyObject *const_str_digest_067d690937347332ae13b114537e7807;
extern PyObject *const_int_neg_1;
static PyObject *const_dict_dfabb327337056b623c0221f231c5cfc;
static PyObject *const_dict_b60c8b0b9237abeea956a42240bbf9a1;
extern PyObject *const_str_plain_m;
static PyObject *const_str_digest_4092d6c8937db39dca7fc19d3b776402;
extern PyObject *const_str_plain_part;
static PyObject *const_str_plain_patch;
extern PyObject *const_tuple_empty;
extern PyObject *const_str_plain_version;
extern PyObject *const_str_plain_format_version;
static PyObject *const_str_digest_17cce42d204419594950eb80f688c691;
extern PyObject *const_str_plain_append;
static PyObject *const_str_plain_pnum;
static PyObject *const_str_plain_gd;
extern PyObject *const_str_plain_major;
extern PyObject *const_str_plain___loader__;
extern PyObject *const_str_plain_join;
extern PyObject *const_int_neg_3;
static PyObject *const_str_plain_groupdict;
static PyObject *const_str_plain_ptype;
extern PyObject *const_str_plain___doc__;
extern PyObject *const_str_plain___cached__;
extern PyObject *const_str_dot;
static PyObject *const_str_digest_5825fd5fe71a47af9eeda157752b06a3;
static PyObject *module_filename_obj;

static bool constants_created = false;

static void createModuleConstants( void )
{
    const_str_plain_p_type = UNSTREAM_STRING( &constant_bin[ 268627 ], 6, 1 );
    const_str_digest_6c29bb23c35346eba1909ca992181577 = UNSTREAM_STRING( &constant_bin[ 268633 ], 71, 0 );
    const_tuple_d86ec3fe0d38719b72699837636e9eb9_tuple = PyTuple_New( 6 );
    PyTuple_SET_ITEM( const_tuple_d86ec3fe0d38719b72699837636e9eb9_tuple, 0, const_str_plain_version ); Py_INCREF( const_str_plain_version );
    const_str_plain_version_re = UNSTREAM_STRING( &constant_bin[ 268704 ], 10, 1 );
    PyTuple_SET_ITEM( const_tuple_d86ec3fe0d38719b72699837636e9eb9_tuple, 1, const_str_plain_version_re ); Py_INCREF( const_str_plain_version_re );
    PyTuple_SET_ITEM( const_tuple_d86ec3fe0d38719b72699837636e9eb9_tuple, 2, const_str_plain_m ); Py_INCREF( const_str_plain_m );
    const_str_plain_gd = UNSTREAM_STRING( &constant_bin[ 18842 ], 2, 1 );
    PyTuple_SET_ITEM( const_tuple_d86ec3fe0d38719b72699837636e9eb9_tuple, 3, const_str_plain_gd ); Py_INCREF( const_str_plain_gd );
    PyTuple_SET_ITEM( const_tuple_d86ec3fe0d38719b72699837636e9eb9_tuple, 4, const_str_plain_p_type ); Py_INCREF( const_str_plain_p_type );
    const_str_plain_p_num = UNSTREAM_STRING( &constant_bin[ 268714 ], 5, 1 );
    PyTuple_SET_ITEM( const_tuple_d86ec3fe0d38719b72699837636e9eb9_tuple, 5, const_str_plain_p_num ); Py_INCREF( const_str_plain_p_num );
    const_list_int_neg_1_list = PyList_New( 1 );
    PyList_SET_ITEM( const_list_int_neg_1_list, 0, const_int_neg_1 ); Py_INCREF( const_int_neg_1 );
    const_tuple_str_plain_version_str_plain_f_str_plain_it_str_plain_part_tuple = PyTuple_New( 4 );
    PyTuple_SET_ITEM( const_tuple_str_plain_version_str_plain_f_str_plain_it_str_plain_part_tuple, 0, const_str_plain_version ); Py_INCREF( const_str_plain_version );
    PyTuple_SET_ITEM( const_tuple_str_plain_version_str_plain_f_str_plain_it_str_plain_part_tuple, 1, const_str_plain_f ); Py_INCREF( const_str_plain_f );
    PyTuple_SET_ITEM( const_tuple_str_plain_version_str_plain_f_str_plain_it_str_plain_part_tuple, 2, const_str_plain_it ); Py_INCREF( const_str_plain_it );
    PyTuple_SET_ITEM( const_tuple_str_plain_version_str_plain_f_str_plain_it_str_plain_part_tuple, 3, const_str_plain_part ); Py_INCREF( const_str_plain_part );
    const_str_plain_lastgroup = UNSTREAM_STRING( &constant_bin[ 268719 ], 9, 1 );
    const_str_digest_edb57ac2b82afc9f2e257f6aafd4ed5f = UNSTREAM_STRING( &constant_bin[ 268728 ], 25, 0 );
    const_str_plain_prerelease = UNSTREAM_STRING( &constant_bin[ 268753 ], 10, 1 );
    const_str_digest_067d690937347332ae13b114537e7807 = UNSTREAM_STRING( &constant_bin[ 268763 ], 187, 0 );
    const_dict_dfabb327337056b623c0221f231c5cfc = _PyDict_NewPresized( 3 );
    PyDict_SetItem( const_dict_dfabb327337056b623c0221f231c5cfc, const_str_plain_a, const_int_neg_4 );
    PyDict_SetItem( const_dict_dfabb327337056b623c0221f231c5cfc, const_str_plain_b, const_int_neg_3 );
    PyDict_SetItem( const_dict_dfabb327337056b623c0221f231c5cfc, const_str_plain_rc, const_int_neg_2 );
    assert( PyDict_Size( const_dict_dfabb327337056b623c0221f231c5cfc ) == 3 );
    const_dict_b60c8b0b9237abeea956a42240bbf9a1 = _PyDict_NewPresized( 3 );
    PyDict_SetItem( const_dict_b60c8b0b9237abeea956a42240bbf9a1, const_int_neg_4, const_str_plain_a );
    PyDict_SetItem( const_dict_b60c8b0b9237abeea956a42240bbf9a1, const_int_neg_3, const_str_plain_b );
    PyDict_SetItem( const_dict_b60c8b0b9237abeea956a42240bbf9a1, const_int_neg_2, const_str_plain_rc );
    assert( PyDict_Size( const_dict_b60c8b0b9237abeea956a42240bbf9a1 ) == 3 );
    const_str_digest_4092d6c8937db39dca7fc19d3b776402 = UNSTREAM_STRING( &constant_bin[ 268950 ], 16, 0 );
    const_str_plain_patch = UNSTREAM_STRING( &constant_bin[ 21662 ], 5, 1 );
    const_str_digest_17cce42d204419594950eb80f688c691 = UNSTREAM_STRING( &constant_bin[ 268966 ], 692, 0 );
    const_str_plain_pnum = UNSTREAM_STRING( &constant_bin[ 268888 ], 4, 1 );
    const_str_plain_groupdict = UNSTREAM_STRING( &constant_bin[ 269658 ], 9, 1 );
    const_str_plain_ptype = UNSTREAM_STRING( &constant_bin[ 268871 ], 5, 1 );
    const_str_digest_5825fd5fe71a47af9eeda157752b06a3 = UNSTREAM_STRING( &constant_bin[ 6501 ], 10, 0 );

    constants_created = true;
}

#ifndef __NUITKA_NO_ASSERT__
void checkModuleConstants_version( void )
{
    // The module may not have been used at all.
    if (constants_created == false) return;


}
#endif

// The module code objects.
static PyCodeObject *codeobj_12b9e3738990323f637c8485671cca55;
static PyCodeObject *codeobj_f15070edf5cffa5f3d631433d469eb20;
static PyCodeObject *codeobj_b10b191363399559174f9259fa7211f2;

static void createModuleCodeObjects(void)
{
    module_filename_obj = MAKE_RELATIVE_PATH( const_str_digest_5825fd5fe71a47af9eeda157752b06a3 );
    codeobj_12b9e3738990323f637c8485671cca55 = MAKE_CODEOBJ( module_filename_obj, const_str_digest_4092d6c8937db39dca7fc19d3b776402, 1, const_tuple_empty, 0, 0, CO_NOFREE );
    codeobj_f15070edf5cffa5f3d631433d469eb20 = MAKE_CODEOBJ( module_filename_obj, const_str_plain_format_version, 36, const_tuple_str_plain_version_str_plain_f_str_plain_it_str_plain_part_tuple, 1, 0, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE );
    codeobj_b10b191363399559174f9259fa7211f2 = MAKE_CODEOBJ( module_filename_obj, const_str_plain_parse_version, 4, const_tuple_d86ec3fe0d38719b72699837636e9eb9_tuple, 1, 0, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE );
}

// The module function declarations.
static PyObject *MAKE_FUNCTION_version$$$function_1_parse_version(  );


static PyObject *MAKE_FUNCTION_version$$$function_2_format_version(  );


// The module function definitions.
static PyObject *impl_version$$$function_1_parse_version( struct Nuitka_FunctionObject const *self, PyObject **python_pars )
{
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_version = python_pars[ 0 ];
    PyObject *var_version_re = NULL;
    PyObject *var_m = NULL;
    PyObject *var_gd = NULL;
    PyObject *var_p_type = NULL;
    PyObject *var_p_num = NULL;
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
    PyObject *tmp_args_element_name_3;
    PyObject *tmp_assign_source_1;
    PyObject *tmp_assign_source_2;
    PyObject *tmp_assign_source_3;
    PyObject *tmp_assign_source_4;
    PyObject *tmp_assign_source_5;
    PyObject *tmp_assign_source_6;
    PyObject *tmp_assign_source_7;
    PyObject *tmp_assign_source_8;
    PyObject *tmp_called_instance_1;
    PyObject *tmp_called_name_1;
    int tmp_cmp_Eq_1;
    PyObject *tmp_compare_left_1;
    PyObject *tmp_compare_left_2;
    PyObject *tmp_compare_right_1;
    PyObject *tmp_compare_right_2;
    PyObject *tmp_int_arg_1;
    PyObject *tmp_int_arg_2;
    PyObject *tmp_int_arg_3;
    PyObject *tmp_int_arg_4;
    bool tmp_is_1;
    PyObject *tmp_left_name_1;
    PyObject *tmp_left_name_2;
    PyObject *tmp_left_name_3;
    PyObject *tmp_list_element_1;
    PyObject *tmp_list_element_2;
    PyObject *tmp_make_exception_arg_1;
    PyObject *tmp_raise_type_1;
    bool tmp_result;
    PyObject *tmp_return_value;
    PyObject *tmp_right_name_1;
    PyObject *tmp_right_name_2;
    PyObject *tmp_right_name_3;
    PyObject *tmp_source_name_1;
    PyObject *tmp_source_name_2;
    PyObject *tmp_source_name_3;
    PyObject *tmp_subscribed_name_1;
    PyObject *tmp_subscribed_name_2;
    PyObject *tmp_subscribed_name_3;
    PyObject *tmp_subscribed_name_4;
    PyObject *tmp_subscribed_name_5;
    PyObject *tmp_subscribed_name_6;
    PyObject *tmp_subscript_name_1;
    PyObject *tmp_subscript_name_2;
    PyObject *tmp_subscript_name_3;
    PyObject *tmp_subscript_name_4;
    PyObject *tmp_subscript_name_5;
    PyObject *tmp_subscript_name_6;
    PyObject *tmp_tuple_arg_1;
    static struct Nuitka_FrameObject *cache_frame_b10b191363399559174f9259fa7211f2 = NULL;

    struct Nuitka_FrameObject *frame_b10b191363399559174f9259fa7211f2;

    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    tmp_return_value = NULL;

    // Actual function code.
    tmp_assign_source_1 = const_str_digest_067d690937347332ae13b114537e7807;
    assert( var_version_re == NULL );
    Py_INCREF( tmp_assign_source_1 );
    var_version_re = tmp_assign_source_1;

    // Tried code:
    MAKE_OR_REUSE_FRAME( cache_frame_b10b191363399559174f9259fa7211f2, codeobj_b10b191363399559174f9259fa7211f2, module_version, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *) );
    frame_b10b191363399559174f9259fa7211f2 = cache_frame_b10b191363399559174f9259fa7211f2;

    // Push the new frame as the currently active one.
    pushFrameStack( frame_b10b191363399559174f9259fa7211f2 );

    // Mark the frame object as in use, ref count 1 will be up for reuse.
    assert( Py_REFCNT( frame_b10b191363399559174f9259fa7211f2 ) == 2 ); // Frame stack

    // Framed code:
    tmp_source_name_1 = GET_STRING_DICT_VALUE( moduledict_version, (Nuitka_StringObject *)const_str_plain_re );

    if (unlikely( tmp_source_name_1 == NULL ))
    {
        tmp_source_name_1 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_re );
    }

    if ( tmp_source_name_1 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "re" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 22;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }

    tmp_called_name_1 = LOOKUP_ATTRIBUTE( tmp_source_name_1, const_str_plain_match );
    if ( tmp_called_name_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 22;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }
    tmp_args_element_name_1 = var_version_re;

    if ( tmp_args_element_name_1 == NULL )
    {
        Py_DECREF( tmp_called_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "version_re" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 22;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }

    tmp_args_element_name_2 = par_version;

    if ( tmp_args_element_name_2 == NULL )
    {
        Py_DECREF( tmp_called_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "version" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 22;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }

    tmp_source_name_2 = GET_STRING_DICT_VALUE( moduledict_version, (Nuitka_StringObject *)const_str_plain_re );

    if (unlikely( tmp_source_name_2 == NULL ))
    {
        tmp_source_name_2 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_re );
    }

    if ( tmp_source_name_2 == NULL )
    {
        Py_DECREF( tmp_called_name_1 );
        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "re" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 22;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }

    tmp_args_element_name_3 = LOOKUP_ATTRIBUTE( tmp_source_name_2, const_str_plain_VERBOSE );
    if ( tmp_args_element_name_3 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_1 );

        exception_lineno = 22;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }
    frame_b10b191363399559174f9259fa7211f2->m_frame.f_lineno = 22;
    {
        PyObject *call_args[] = { tmp_args_element_name_1, tmp_args_element_name_2, tmp_args_element_name_3 };
        tmp_assign_source_2 = CALL_FUNCTION_WITH_ARGS3( tmp_called_name_1, call_args );
    }

    Py_DECREF( tmp_called_name_1 );
    Py_DECREF( tmp_args_element_name_3 );
    if ( tmp_assign_source_2 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 22;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }
    assert( var_m == NULL );
    var_m = tmp_assign_source_2;

    tmp_compare_left_1 = var_m;

    CHECK_OBJECT( tmp_compare_left_1 );
    tmp_compare_right_1 = Py_None;
    tmp_is_1 = ( tmp_compare_left_1 == tmp_compare_right_1 );
    if ( tmp_is_1 )
    {
        goto branch_yes_1;
    }
    else
    {
        goto branch_no_1;
    }
    branch_yes_1:;
    tmp_left_name_1 = const_str_digest_edb57ac2b82afc9f2e257f6aafd4ed5f;
    tmp_right_name_1 = par_version;

    if ( tmp_right_name_1 == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "version" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 24;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }

    tmp_make_exception_arg_1 = BINARY_OPERATION_REMAINDER( tmp_left_name_1, tmp_right_name_1 );
    if ( tmp_make_exception_arg_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 24;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }
    frame_b10b191363399559174f9259fa7211f2->m_frame.f_lineno = 24;
    {
        PyObject *call_args[] = { tmp_make_exception_arg_1 };
        tmp_raise_type_1 = CALL_FUNCTION_WITH_ARGS1( PyExc_ValueError, call_args );
    }

    Py_DECREF( tmp_make_exception_arg_1 );
    assert( tmp_raise_type_1 != NULL );
    exception_type = tmp_raise_type_1;
    exception_lineno = 24;
    RAISE_EXCEPTION_WITH_TYPE( &exception_type, &exception_value, &exception_tb );
    type_description_1 = "oooooo";
    goto frame_exception_exit_1;
    branch_no_1:;
    tmp_called_instance_1 = var_m;

    if ( tmp_called_instance_1 == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "m" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 25;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }

    frame_b10b191363399559174f9259fa7211f2->m_frame.f_lineno = 25;
    tmp_assign_source_3 = CALL_METHOD_NO_ARGS( tmp_called_instance_1, const_str_plain_groupdict );
    if ( tmp_assign_source_3 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 25;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }
    assert( var_gd == NULL );
    var_gd = tmp_assign_source_3;

    tmp_assign_source_4 = PyList_New( 3 );
    tmp_subscribed_name_1 = var_gd;

    CHECK_OBJECT( tmp_subscribed_name_1 );
    tmp_subscript_name_1 = const_str_plain_major;
    tmp_int_arg_1 = LOOKUP_SUBSCRIPT( tmp_subscribed_name_1, tmp_subscript_name_1 );
    if ( tmp_int_arg_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_4 );

        exception_lineno = 26;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }
    tmp_list_element_1 = PyNumber_Int( tmp_int_arg_1 );
    Py_DECREF( tmp_int_arg_1 );
    if ( tmp_list_element_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_4 );

        exception_lineno = 26;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }
    PyList_SET_ITEM( tmp_assign_source_4, 0, tmp_list_element_1 );
    tmp_subscribed_name_2 = var_gd;

    if ( tmp_subscribed_name_2 == NULL )
    {
        Py_DECREF( tmp_assign_source_4 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "gd" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 26;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }

    tmp_subscript_name_2 = const_str_plain_minor;
    tmp_int_arg_2 = LOOKUP_SUBSCRIPT( tmp_subscribed_name_2, tmp_subscript_name_2 );
    if ( tmp_int_arg_2 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_4 );

        exception_lineno = 26;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }
    tmp_list_element_1 = PyNumber_Int( tmp_int_arg_2 );
    Py_DECREF( tmp_int_arg_2 );
    if ( tmp_list_element_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_4 );

        exception_lineno = 26;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }
    PyList_SET_ITEM( tmp_assign_source_4, 1, tmp_list_element_1 );
    tmp_subscribed_name_3 = var_gd;

    if ( tmp_subscribed_name_3 == NULL )
    {
        Py_DECREF( tmp_assign_source_4 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "gd" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 26;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }

    tmp_subscript_name_3 = const_str_plain_patch;
    tmp_int_arg_3 = LOOKUP_SUBSCRIPT( tmp_subscribed_name_3, tmp_subscript_name_3 );
    if ( tmp_int_arg_3 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_4 );

        exception_lineno = 26;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }
    tmp_list_element_1 = PyNumber_Int( tmp_int_arg_3 );
    Py_DECREF( tmp_int_arg_3 );
    if ( tmp_list_element_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_4 );

        exception_lineno = 26;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }
    PyList_SET_ITEM( tmp_assign_source_4, 2, tmp_list_element_1 );
    {
        PyObject *old = par_version;
        par_version = tmp_assign_source_4;
        Py_XDECREF( old );
    }

    tmp_source_name_3 = var_m;

    if ( tmp_source_name_3 == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "m" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 27;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }

    tmp_compare_left_2 = LOOKUP_ATTRIBUTE( tmp_source_name_3, const_str_plain_lastgroup );
    if ( tmp_compare_left_2 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 27;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }
    tmp_compare_right_2 = const_str_plain_prerelease;
    tmp_cmp_Eq_1 = RICH_COMPARE_BOOL_EQ( tmp_compare_left_2, tmp_compare_right_2 );
    if ( tmp_cmp_Eq_1 == -1 )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_compare_left_2 );

        exception_lineno = 27;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }
    Py_DECREF( tmp_compare_left_2 );
    if ( tmp_cmp_Eq_1 == 1 )
    {
        goto branch_yes_2;
    }
    else
    {
        goto branch_no_2;
    }
    branch_yes_2:;
    tmp_subscribed_name_4 = PyDict_Copy( const_dict_dfabb327337056b623c0221f231c5cfc );
    tmp_subscribed_name_5 = var_gd;

    if ( tmp_subscribed_name_5 == NULL )
    {
        Py_DECREF( tmp_subscribed_name_4 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "gd" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 28;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }

    tmp_subscript_name_5 = const_str_plain_ptype;
    tmp_subscript_name_4 = LOOKUP_SUBSCRIPT( tmp_subscribed_name_5, tmp_subscript_name_5 );
    if ( tmp_subscript_name_4 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_subscribed_name_4 );

        exception_lineno = 28;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }
    tmp_assign_source_5 = LOOKUP_SUBSCRIPT( tmp_subscribed_name_4, tmp_subscript_name_4 );
    Py_DECREF( tmp_subscribed_name_4 );
    Py_DECREF( tmp_subscript_name_4 );
    if ( tmp_assign_source_5 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 28;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }
    assert( var_p_type == NULL );
    var_p_type = tmp_assign_source_5;

    tmp_subscribed_name_6 = var_gd;

    if ( tmp_subscribed_name_6 == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "gd" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 29;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }

    tmp_subscript_name_6 = const_str_plain_pnum;
    tmp_int_arg_4 = LOOKUP_SUBSCRIPT( tmp_subscribed_name_6, tmp_subscript_name_6 );
    if ( tmp_int_arg_4 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 29;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }
    tmp_assign_source_6 = PyNumber_Int( tmp_int_arg_4 );
    Py_DECREF( tmp_int_arg_4 );
    if ( tmp_assign_source_6 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 29;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }
    assert( var_p_num == NULL );
    var_p_num = tmp_assign_source_6;

    tmp_left_name_2 = par_version;

    if ( tmp_left_name_2 == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "version" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 30;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }

    tmp_right_name_2 = PyList_New( 2 );
    tmp_list_element_2 = var_p_type;

    if ( tmp_list_element_2 == NULL )
    {
        Py_DECREF( tmp_right_name_2 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "p_type" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 30;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }

    Py_INCREF( tmp_list_element_2 );
    PyList_SET_ITEM( tmp_right_name_2, 0, tmp_list_element_2 );
    tmp_list_element_2 = var_p_num;

    CHECK_OBJECT( tmp_list_element_2 );
    Py_INCREF( tmp_list_element_2 );
    PyList_SET_ITEM( tmp_right_name_2, 1, tmp_list_element_2 );
    tmp_result = BINARY_OPERATION_ADD_INPLACE( &tmp_left_name_2, tmp_right_name_2 );
    tmp_assign_source_7 = tmp_left_name_2;
    Py_DECREF( tmp_right_name_2 );
    if ( tmp_result == false )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 30;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }
    par_version = tmp_assign_source_7;

    goto branch_end_2;
    branch_no_2:;
    tmp_left_name_3 = par_version;

    if ( tmp_left_name_3 == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "version" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 32;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }

    tmp_right_name_3 = LIST_COPY( const_list_int_neg_1_list );
    tmp_result = BINARY_OPERATION_ADD_INPLACE( &tmp_left_name_3, tmp_right_name_3 );
    tmp_assign_source_8 = tmp_left_name_3;
    Py_DECREF( tmp_right_name_3 );
    if ( tmp_result == false )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 32;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }
    par_version = tmp_assign_source_8;

    branch_end_2:;
    tmp_tuple_arg_1 = par_version;

    CHECK_OBJECT( tmp_tuple_arg_1 );
    tmp_return_value = PySequence_Tuple( tmp_tuple_arg_1 );
    if ( tmp_return_value == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 33;
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }
    goto frame_return_exit_1;

#if 0
    RESTORE_FRAME_EXCEPTION( frame_b10b191363399559174f9259fa7211f2 );
#endif

    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;

    frame_return_exit_1:;
#if 0
    RESTORE_FRAME_EXCEPTION( frame_b10b191363399559174f9259fa7211f2 );
#endif

    // Put the previous frame back on top.
    popFrameStack();

    goto try_return_handler_1;

    frame_exception_exit_1:;

#if 0
    RESTORE_FRAME_EXCEPTION( frame_b10b191363399559174f9259fa7211f2 );
#endif

    if ( exception_tb == NULL )
    {
        exception_tb = MAKE_TRACEBACK( frame_b10b191363399559174f9259fa7211f2, exception_lineno );
    }
    else if ( exception_tb->tb_frame != &frame_b10b191363399559174f9259fa7211f2->m_frame )
    {
        exception_tb = ADD_TRACEBACK( exception_tb, frame_b10b191363399559174f9259fa7211f2, exception_lineno );
    }

    // Attachs locals to frame if any.
    Nuitka_Frame_AttachLocals(
        (struct Nuitka_FrameObject *)frame_b10b191363399559174f9259fa7211f2,
        type_description_1,
        par_version,
        var_version_re,
        var_m,
        var_gd,
        var_p_type,
        var_p_num
    );


    // Release cached frame.
    if ( frame_b10b191363399559174f9259fa7211f2 == cache_frame_b10b191363399559174f9259fa7211f2 )
    {
        Py_DECREF( frame_b10b191363399559174f9259fa7211f2 );
    }
    cache_frame_b10b191363399559174f9259fa7211f2 = NULL;

    assertFrameObject( frame_b10b191363399559174f9259fa7211f2 );

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto try_except_handler_1;

    frame_no_exception_1:;

    // tried codes exits in all cases
    NUITKA_CANNOT_GET_HERE( version$$$function_1_parse_version );
    return NULL;
    // Return handler code:
    try_return_handler_1:;
    CHECK_OBJECT( (PyObject *)par_version );
    Py_DECREF( par_version );
    par_version = NULL;

    Py_XDECREF( var_version_re );
    var_version_re = NULL;

    Py_XDECREF( var_m );
    var_m = NULL;

    Py_XDECREF( var_gd );
    var_gd = NULL;

    Py_XDECREF( var_p_type );
    var_p_type = NULL;

    Py_XDECREF( var_p_num );
    var_p_num = NULL;

    goto function_return_exit;
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

    Py_XDECREF( par_version );
    par_version = NULL;

    Py_XDECREF( var_version_re );
    var_version_re = NULL;

    Py_XDECREF( var_m );
    var_m = NULL;

    Py_XDECREF( var_gd );
    var_gd = NULL;

    Py_XDECREF( var_p_type );
    var_p_type = NULL;

    Py_XDECREF( var_p_num );
    var_p_num = NULL;

    // Re-raise.
    exception_type = exception_keeper_type_1;
    exception_value = exception_keeper_value_1;
    exception_tb = exception_keeper_tb_1;
    exception_lineno = exception_keeper_lineno_1;

    goto function_exception_exit;
    // End of try:

    // Return statement must have exited already.
    NUITKA_CANNOT_GET_HERE( version$$$function_1_parse_version );
    return NULL;

function_exception_exit:
    assert( exception_type );
    RESTORE_ERROR_OCCURRED( exception_type, exception_value, exception_tb );

    return NULL;
    function_return_exit:

    CHECK_OBJECT( tmp_return_value );
    assert( had_error || !ERROR_OCCURRED() );
    return tmp_return_value;

}


static PyObject *impl_version$$$function_2_format_version( struct Nuitka_FunctionObject const *self, PyObject **python_pars )
{
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_version = python_pars[ 0 ];
    PyObject *var_f = NULL;
    PyObject *var_it = NULL;
    PyObject *var_part = NULL;
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
    PyObject *tmp_ass_subscribed_1;
    PyObject *tmp_ass_subscript_1;
    int tmp_ass_subscript_res_1;
    PyObject *tmp_ass_subvalue_1;
    PyObject *tmp_assign_source_1;
    PyObject *tmp_assign_source_2;
    PyObject *tmp_assign_source_3;
    PyObject *tmp_called_name_1;
    PyObject *tmp_called_name_2;
    int tmp_cmp_Eq_1;
    int tmp_cmp_GtE_1;
    PyObject *tmp_compare_left_1;
    PyObject *tmp_compare_left_2;
    PyObject *tmp_compare_right_1;
    PyObject *tmp_compare_right_2;
    PyObject *tmp_iter_arg_1;
    PyObject *tmp_left_name_1;
    PyObject *tmp_left_name_2;
    PyObject *tmp_return_value;
    PyObject *tmp_right_name_1;
    PyObject *tmp_right_name_2;
    PyObject *tmp_source_name_1;
    PyObject *tmp_source_name_2;
    PyObject *tmp_subscribed_name_1;
    PyObject *tmp_subscribed_name_2;
    PyObject *tmp_subscript_name_1;
    PyObject *tmp_subscript_name_2;
    PyObject *tmp_unicode_arg_1;
    PyObject *tmp_unicode_arg_2;
    NUITKA_MAY_BE_UNUSED PyObject *tmp_unused;
    PyObject *tmp_value_name_1;
    PyObject *tmp_value_name_2;
    static struct Nuitka_FrameObject *cache_frame_f15070edf5cffa5f3d631433d469eb20 = NULL;

    struct Nuitka_FrameObject *frame_f15070edf5cffa5f3d631433d469eb20;

    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    tmp_return_value = NULL;

    // Actual function code.
    tmp_assign_source_1 = PyList_New( 0 );
    assert( var_f == NULL );
    var_f = tmp_assign_source_1;

    // Tried code:
    MAKE_OR_REUSE_FRAME( cache_frame_f15070edf5cffa5f3d631433d469eb20, codeobj_f15070edf5cffa5f3d631433d469eb20, module_version, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *) );
    frame_f15070edf5cffa5f3d631433d469eb20 = cache_frame_f15070edf5cffa5f3d631433d469eb20;

    // Push the new frame as the currently active one.
    pushFrameStack( frame_f15070edf5cffa5f3d631433d469eb20 );

    // Mark the frame object as in use, ref count 1 will be up for reuse.
    assert( Py_REFCNT( frame_f15070edf5cffa5f3d631433d469eb20 ) == 2 ); // Frame stack

    // Framed code:
    tmp_iter_arg_1 = par_version;

    CHECK_OBJECT( tmp_iter_arg_1 );
    tmp_assign_source_2 = MAKE_ITERATOR( tmp_iter_arg_1 );
    if ( tmp_assign_source_2 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 39;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }
    assert( var_it == NULL );
    var_it = tmp_assign_source_2;

    loop_start_1:;
    tmp_value_name_1 = var_it;

    CHECK_OBJECT( tmp_value_name_1 );
    tmp_assign_source_3 = ITERATOR_NEXT( tmp_value_name_1 );
    if ( tmp_assign_source_3 == NULL )
    {
        if ( !ERROR_OCCURRED() )
        {
            exception_type = PyExc_StopIteration;
            Py_INCREF( exception_type );
            exception_value = NULL;
            exception_tb = NULL;
        }
        else
        {
            FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        }


        type_description_1 = "oooo";
        exception_lineno = 41;
        goto frame_exception_exit_1;
    }
    {
        PyObject *old = var_part;
        var_part = tmp_assign_source_3;
        Py_XDECREF( old );
    }

    tmp_compare_left_1 = var_part;

    CHECK_OBJECT( tmp_compare_left_1 );
    tmp_compare_right_1 = const_int_0;
    tmp_cmp_GtE_1 = RICH_COMPARE_BOOL_GE( tmp_compare_left_1, tmp_compare_right_1 );
    if ( tmp_cmp_GtE_1 == -1 )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 42;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }
    if ( tmp_cmp_GtE_1 == 1 )
    {
        goto branch_yes_1;
    }
    else
    {
        goto branch_no_1;
    }
    branch_yes_1:;
    tmp_source_name_1 = var_f;

    if ( tmp_source_name_1 == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "f" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 43;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }

    tmp_called_name_1 = LOOKUP_ATTRIBUTE( tmp_source_name_1, const_str_plain_append );
    if ( tmp_called_name_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 43;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }
    tmp_unicode_arg_1 = var_part;

    if ( tmp_unicode_arg_1 == NULL )
    {
        Py_DECREF( tmp_called_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "part" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 43;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }

    tmp_args_element_name_1 = PyObject_Unicode( tmp_unicode_arg_1 );
    if ( tmp_args_element_name_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_1 );

        exception_lineno = 43;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }
    frame_f15070edf5cffa5f3d631433d469eb20->m_frame.f_lineno = 43;
    {
        PyObject *call_args[] = { tmp_args_element_name_1 };
        tmp_unused = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_1, call_args );
    }

    Py_DECREF( tmp_called_name_1 );
    Py_DECREF( tmp_args_element_name_1 );
    if ( tmp_unused == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 43;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }
    Py_DECREF( tmp_unused );
    goto branch_end_1;
    branch_no_1:;
    tmp_compare_left_2 = var_part;

    if ( tmp_compare_left_2 == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "part" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 44;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }

    tmp_compare_right_2 = const_int_neg_1;
    tmp_cmp_Eq_1 = RICH_COMPARE_BOOL_EQ( tmp_compare_left_2, tmp_compare_right_2 );
    if ( tmp_cmp_Eq_1 == -1 )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 44;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }
    if ( tmp_cmp_Eq_1 == 1 )
    {
        goto branch_yes_2;
    }
    else
    {
        goto branch_no_2;
    }
    branch_yes_2:;
    goto loop_end_1;
    goto branch_end_2;
    branch_no_2:;
    tmp_subscribed_name_1 = var_f;

    if ( tmp_subscribed_name_1 == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "f" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 47;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }

    tmp_subscript_name_1 = const_int_neg_1;
    tmp_left_name_2 = LOOKUP_SUBSCRIPT( tmp_subscribed_name_1, tmp_subscript_name_1 );
    if ( tmp_left_name_2 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 47;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }
    tmp_subscribed_name_2 = PyDict_Copy( const_dict_b60c8b0b9237abeea956a42240bbf9a1 );
    tmp_subscript_name_2 = var_part;

    if ( tmp_subscript_name_2 == NULL )
    {
        Py_DECREF( tmp_left_name_2 );
        Py_DECREF( tmp_subscribed_name_2 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "part" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 47;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }

    tmp_right_name_1 = LOOKUP_SUBSCRIPT( tmp_subscribed_name_2, tmp_subscript_name_2 );
    Py_DECREF( tmp_subscribed_name_2 );
    if ( tmp_right_name_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_left_name_2 );

        exception_lineno = 47;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }
    tmp_left_name_1 = BINARY_OPERATION_ADD( tmp_left_name_2, tmp_right_name_1 );
    Py_DECREF( tmp_left_name_2 );
    Py_DECREF( tmp_right_name_1 );
    if ( tmp_left_name_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 47;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }
    tmp_value_name_2 = var_it;

    if ( tmp_value_name_2 == NULL )
    {
        Py_DECREF( tmp_left_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "it" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 47;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }

    tmp_unicode_arg_2 = ITERATOR_NEXT( tmp_value_name_2 );
    if ( tmp_unicode_arg_2 == NULL )
    {
        if ( !ERROR_OCCURRED() )
        {
            exception_type = PyExc_StopIteration;
            Py_INCREF( exception_type );
            exception_value = NULL;
            exception_tb = NULL;
        }
        else
        {
            FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        }
        Py_DECREF( tmp_left_name_1 );

        type_description_1 = "oooo";
        exception_lineno = 47;
        goto frame_exception_exit_1;
    }
    tmp_right_name_2 = PyObject_Unicode( tmp_unicode_arg_2 );
    Py_DECREF( tmp_unicode_arg_2 );
    if ( tmp_right_name_2 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_left_name_1 );

        exception_lineno = 47;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }
    tmp_ass_subvalue_1 = BINARY_OPERATION_ADD( tmp_left_name_1, tmp_right_name_2 );
    Py_DECREF( tmp_left_name_1 );
    Py_DECREF( tmp_right_name_2 );
    if ( tmp_ass_subvalue_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 47;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }
    tmp_ass_subscribed_1 = var_f;

    if ( tmp_ass_subscribed_1 == NULL )
    {
        Py_DECREF( tmp_ass_subvalue_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "f" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 47;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }

    tmp_ass_subscript_1 = const_int_neg_1;
    tmp_ass_subscript_res_1 = SET_SUBSCRIPT_CONST( tmp_ass_subscribed_1, tmp_ass_subscript_1, -1, tmp_ass_subvalue_1 );
    Py_DECREF( tmp_ass_subvalue_1 );
    if ( tmp_ass_subscript_res_1 == false )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 47;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }
    goto loop_end_1;
    branch_end_2:;
    branch_end_1:;
    if ( CONSIDER_THREADING() == false )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 40;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }
    goto loop_start_1;
    loop_end_1:;
    tmp_source_name_2 = const_str_dot;
    tmp_called_name_2 = LOOKUP_ATTRIBUTE( tmp_source_name_2, const_str_plain_join );
    assert( tmp_called_name_2 != NULL );
    tmp_args_element_name_2 = var_f;

    if ( tmp_args_element_name_2 == NULL )
    {
        Py_DECREF( tmp_called_name_2 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "f" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 49;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }

    frame_f15070edf5cffa5f3d631433d469eb20->m_frame.f_lineno = 49;
    {
        PyObject *call_args[] = { tmp_args_element_name_2 };
        tmp_return_value = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_2, call_args );
    }

    Py_DECREF( tmp_called_name_2 );
    if ( tmp_return_value == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 49;
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }
    goto frame_return_exit_1;

#if 0
    RESTORE_FRAME_EXCEPTION( frame_f15070edf5cffa5f3d631433d469eb20 );
#endif

    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;

    frame_return_exit_1:;
#if 0
    RESTORE_FRAME_EXCEPTION( frame_f15070edf5cffa5f3d631433d469eb20 );
#endif

    // Put the previous frame back on top.
    popFrameStack();

    goto try_return_handler_1;

    frame_exception_exit_1:;

#if 0
    RESTORE_FRAME_EXCEPTION( frame_f15070edf5cffa5f3d631433d469eb20 );
#endif

    if ( exception_tb == NULL )
    {
        exception_tb = MAKE_TRACEBACK( frame_f15070edf5cffa5f3d631433d469eb20, exception_lineno );
    }
    else if ( exception_tb->tb_frame != &frame_f15070edf5cffa5f3d631433d469eb20->m_frame )
    {
        exception_tb = ADD_TRACEBACK( exception_tb, frame_f15070edf5cffa5f3d631433d469eb20, exception_lineno );
    }

    // Attachs locals to frame if any.
    Nuitka_Frame_AttachLocals(
        (struct Nuitka_FrameObject *)frame_f15070edf5cffa5f3d631433d469eb20,
        type_description_1,
        par_version,
        var_f,
        var_it,
        var_part
    );


    // Release cached frame.
    if ( frame_f15070edf5cffa5f3d631433d469eb20 == cache_frame_f15070edf5cffa5f3d631433d469eb20 )
    {
        Py_DECREF( frame_f15070edf5cffa5f3d631433d469eb20 );
    }
    cache_frame_f15070edf5cffa5f3d631433d469eb20 = NULL;

    assertFrameObject( frame_f15070edf5cffa5f3d631433d469eb20 );

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto try_except_handler_1;

    frame_no_exception_1:;

    // tried codes exits in all cases
    NUITKA_CANNOT_GET_HERE( version$$$function_2_format_version );
    return NULL;
    // Return handler code:
    try_return_handler_1:;
    Py_XDECREF( par_version );
    par_version = NULL;

    Py_XDECREF( var_f );
    var_f = NULL;

    Py_XDECREF( var_it );
    var_it = NULL;

    Py_XDECREF( var_part );
    var_part = NULL;

    goto function_return_exit;
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

    Py_XDECREF( par_version );
    par_version = NULL;

    Py_XDECREF( var_f );
    var_f = NULL;

    Py_XDECREF( var_it );
    var_it = NULL;

    Py_XDECREF( var_part );
    var_part = NULL;

    // Re-raise.
    exception_type = exception_keeper_type_1;
    exception_value = exception_keeper_value_1;
    exception_tb = exception_keeper_tb_1;
    exception_lineno = exception_keeper_lineno_1;

    goto function_exception_exit;
    // End of try:

    // Return statement must have exited already.
    NUITKA_CANNOT_GET_HERE( version$$$function_2_format_version );
    return NULL;

function_exception_exit:
    assert( exception_type );
    RESTORE_ERROR_OCCURRED( exception_type, exception_value, exception_tb );

    return NULL;
    function_return_exit:

    CHECK_OBJECT( tmp_return_value );
    assert( had_error || !ERROR_OCCURRED() );
    return tmp_return_value;

}



static PyObject *MAKE_FUNCTION_version$$$function_1_parse_version(  )
{
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_version$$$function_1_parse_version,
        const_str_plain_parse_version,
#if PYTHON_VERSION >= 330
        NULL,
#endif
        codeobj_b10b191363399559174f9259fa7211f2,
        NULL,
#if PYTHON_VERSION >= 300
        NULL,
        const_dict_empty,
#endif
        module_version,
        const_str_digest_17cce42d204419594950eb80f688c691,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_version$$$function_2_format_version(  )
{
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_version$$$function_2_format_version,
        const_str_plain_format_version,
#if PYTHON_VERSION >= 330
        NULL,
#endif
        codeobj_f15070edf5cffa5f3d631433d469eb20,
        NULL,
#if PYTHON_VERSION >= 300
        NULL,
        const_dict_empty,
#endif
        module_version,
        const_str_digest_6c29bb23c35346eba1909ca992181577,
        0
    );


    return (PyObject *)result;
}



#if PYTHON_VERSION >= 300
static struct PyModuleDef mdef_version =
{
    PyModuleDef_HEAD_INIT,
    "version",   /* m_name */
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

MOD_INIT_DECL( version )
{
#if defined(_NUITKA_EXE) || PYTHON_VERSION >= 300
    static bool _init_done = false;

    // Modules might be imported repeatedly, which is to be ignored.
    if ( _init_done )
    {
        return MOD_RETURN_VALUE( module_version );
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
    puts("version: Calling createModuleConstants().");
#endif
    createModuleConstants();

    /* The code objects used by this module are created now. */
#ifdef _NUITKA_TRACE
    puts("version: Calling createModuleCodeObjects().");
#endif
    createModuleCodeObjects();

    // puts( "in initversion" );

    // Create the module object first. There are no methods initially, all are
    // added dynamically in actual code only.  Also no "__doc__" is initially
    // set at this time, as it could not contain NUL characters this way, they
    // are instead set in early module code.  No "self" for modules, we have no
    // use for it.
#if PYTHON_VERSION < 300
    module_version = Py_InitModule4(
        "version",       // Module Name
        NULL,                    // No methods initially, all are added
                                 // dynamically in actual module code only.
        NULL,                    // No __doc__ is initially set, as it could
                                 // not contain NUL this way, added early in
                                 // actual code.
        NULL,                    // No self for modules, we don't use it.
        PYTHON_API_VERSION
    );
#else
    module_version = PyModule_Create( &mdef_version );
#endif

    moduledict_version = MODULE_DICT( module_version );

    CHECK_OBJECT( module_version );

// Seems to work for Python2.7 out of the box, but for Python3, the module
// doesn't automatically enter "sys.modules", so do it manually.
#if PYTHON_VERSION >= 300
    {
        int r = PyObject_SetItem( PySys_GetObject( (char *)"modules" ), const_str_plain_version, module_version );

        assert( r != -1 );
    }
#endif

    // For deep importing of a module we need to have "__builtins__", so we set
    // it ourselves in the same way than CPython does. Note: This must be done
    // before the frame object is allocated, or else it may fail.

    if ( GET_STRING_DICT_VALUE( moduledict_version, (Nuitka_StringObject *)const_str_plain___builtins__ ) == NULL )
    {
        PyObject *value = (PyObject *)builtin_module;

        // Check if main module, not a dict then but the module itself.
#if !defined(_NUITKA_EXE) || !0
        value = PyModule_GetDict( value );
#endif

        UPDATE_STRING_DICT0( moduledict_version, (Nuitka_StringObject *)const_str_plain___builtins__, value );
    }

#if PYTHON_VERSION >= 330
    UPDATE_STRING_DICT0( moduledict_version, (Nuitka_StringObject *)const_str_plain___loader__, metapath_based_loader );
#endif

    // Temp variables if any
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
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
    PyObject *tmp_called_name_1;
    PyObject *tmp_fromlist_name_1;
    PyObject *tmp_globals_name_1;
    PyObject *tmp_level_name_1;
    PyObject *tmp_locals_name_1;
    PyObject *tmp_name_name_1;
    struct Nuitka_FrameObject *frame_12b9e3738990323f637c8485671cca55;

    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;

    // Module code.
    tmp_assign_source_1 = Py_None;
    UPDATE_STRING_DICT0( moduledict_version, (Nuitka_StringObject *)const_str_plain___doc__, tmp_assign_source_1 );
    tmp_assign_source_2 = module_filename_obj;
    UPDATE_STRING_DICT0( moduledict_version, (Nuitka_StringObject *)const_str_plain___file__, tmp_assign_source_2 );
    tmp_assign_source_3 = metapath_based_loader;
    UPDATE_STRING_DICT0( moduledict_version, (Nuitka_StringObject *)const_str_plain___loader__, tmp_assign_source_3 );
    // Frame without reuse.
    frame_12b9e3738990323f637c8485671cca55 = MAKE_MODULE_FRAME( codeobj_12b9e3738990323f637c8485671cca55, module_version );

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStack( frame_12b9e3738990323f637c8485671cca55 );
    assert( Py_REFCNT( frame_12b9e3738990323f637c8485671cca55 ) == 2 );

    // Framed code:
    frame_12b9e3738990323f637c8485671cca55->m_frame.f_lineno = 1;
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
    tmp_args_element_name_1 = const_str_plain_version;
    tmp_args_element_name_2 = metapath_based_loader;
    frame_12b9e3738990323f637c8485671cca55->m_frame.f_lineno = 1;
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
    UPDATE_STRING_DICT1( moduledict_version, (Nuitka_StringObject *)const_str_plain___spec__, tmp_assign_source_4 );
    tmp_assign_source_5 = Py_None;
    UPDATE_STRING_DICT0( moduledict_version, (Nuitka_StringObject *)const_str_plain___cached__, tmp_assign_source_5 );
    tmp_assign_source_6 = Py_None;
    UPDATE_STRING_DICT0( moduledict_version, (Nuitka_StringObject *)const_str_plain___package__, tmp_assign_source_6 );
    tmp_name_name_1 = const_str_plain_re;
    tmp_globals_name_1 = (PyObject *)moduledict_version;
    tmp_locals_name_1 = Py_None;
    tmp_fromlist_name_1 = Py_None;
    tmp_level_name_1 = const_int_0;
    frame_12b9e3738990323f637c8485671cca55->m_frame.f_lineno = 1;
    tmp_assign_source_7 = IMPORT_MODULE5( tmp_name_name_1, tmp_globals_name_1, tmp_locals_name_1, tmp_fromlist_name_1, tmp_level_name_1 );
    if ( tmp_assign_source_7 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 1;

        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_version, (Nuitka_StringObject *)const_str_plain_re, tmp_assign_source_7 );

    // Restore frame exception if necessary.
#if 0
    RESTORE_FRAME_EXCEPTION( frame_12b9e3738990323f637c8485671cca55 );
#endif
    popFrameStack();

    assertFrameObject( frame_12b9e3738990323f637c8485671cca55 );

    goto frame_no_exception_1;
    frame_exception_exit_1:;
#if 0
    RESTORE_FRAME_EXCEPTION( frame_12b9e3738990323f637c8485671cca55 );
#endif

    if ( exception_tb == NULL )
    {
        exception_tb = MAKE_TRACEBACK( frame_12b9e3738990323f637c8485671cca55, exception_lineno );
    }
    else if ( exception_tb->tb_frame != &frame_12b9e3738990323f637c8485671cca55->m_frame )
    {
        exception_tb = ADD_TRACEBACK( exception_tb, frame_12b9e3738990323f637c8485671cca55, exception_lineno );
    }

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto module_exception_exit;
    frame_no_exception_1:;
    tmp_assign_source_8 = MAKE_FUNCTION_version$$$function_1_parse_version(  );
    UPDATE_STRING_DICT1( moduledict_version, (Nuitka_StringObject *)const_str_plain_parse_version, tmp_assign_source_8 );
    tmp_assign_source_9 = MAKE_FUNCTION_version$$$function_2_format_version(  );
    UPDATE_STRING_DICT1( moduledict_version, (Nuitka_StringObject *)const_str_plain_format_version, tmp_assign_source_9 );

    return MOD_RETURN_VALUE( module_version );
    module_exception_exit:
    RESTORE_ERROR_OCCURRED( exception_type, exception_value, exception_tb );
    return MOD_RETURN_VALUE( NULL );
}
