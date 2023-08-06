/* Generated code for Python source for module 'borg.helpers.msgpack'
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

/* The _module_borg$helpers$msgpack is a Python object pointer of module type. */

/* Note: For full compatibility with CPython, every module variable access
 * needs to go through it except for cases where the module cannot possibly
 * have changed in the mean time.
 */

PyObject *module_borg$helpers$msgpack;
PyDictObject *moduledict_borg$helpers$msgpack;

/* The module constants used, if any. */
extern PyObject *const_str_digest_bdc1a971b462566afd65a1f634717d97;
extern PyObject *const_str_plain_max_array_len;
extern PyObject *const_str_plain_fallback;
extern PyObject *const_str_plain_BUFSIZE;
extern PyObject *const_str_plain_ModuleSpec;
extern PyObject *const_str_plain___spec__;
extern PyObject *const_str_plain___package__;
extern PyObject *const_str_plain_datastruct;
extern PyObject *const_str_plain_kind;
static PyObject *const_str_digest_fbcbc0962c569e60944e990076b07e8a;
extern PyObject *const_str_plain_value;
extern PyObject *const_str_plain_max_str_len;
extern PyObject *const_str_plain_constants;
extern PyObject *const_str_plain_use_list;
extern PyObject *const_int_pos_1;
extern PyObject *const_str_plain_update;
extern PyObject *const_dict_empty;
extern PyObject *const_str_plain_msgpack;
static PyObject *const_dict_856ad4ad04f4b1f3ed6830e3dac24f83;
extern PyObject *const_int_pos_63;
extern PyObject *const_str_plain___file__;
extern PyObject *const_str_plain_MAX_OBJECT_SIZE;
static PyObject *const_str_plain_bit_length;
extern PyObject *const_str_plain_max_ext_len;
extern PyObject *const_int_pos_9;
static PyObject *const_str_digest_89caf116f40c695b6bb920b8484fa4eb;
static PyObject *const_str_digest_e935d50786a37c4692c57bc9563b6d8a;
extern PyObject *const_str_plain_LIST_SCAN_LIMIT;
extern PyObject *const_str_plain_StableDict;
extern PyObject *const_str_plain_bigint_to_int;
extern PyObject *const_str_plain_max;
extern PyObject *const_int_0;
extern PyObject *const_tuple_str_chr_42_tuple;
extern PyObject *const_str_plain_key;
static PyObject *const_dict_572050117e2cfc8c656df66eb5790338;
static PyObject *const_str_digest_fa0dca0529b0df98590638b6970f9269;
static PyObject *const_str_digest_8934cf5a483ff31655447816b42b1638;
extern PyObject *const_str_plain_int_to_bigint;
static PyObject *const_tuple_str_plain_kind_str_plain_args_tuple;
static PyObject *const_str_plain_signed;
extern PyObject *const_int_pos_3;
extern PyObject *const_str_plain_server;
extern PyObject *const_str_plain_client;
extern PyObject *const_str_plain_max_map_len;
extern PyObject *const_str_plain_surrogateescape;
extern PyObject *const_tuple_str_plain_StableDict_tuple;
extern PyObject *const_str_plain_unicode_errors;
extern PyObject *const_int_pos_255;
extern PyObject *const_str_plain_max_buffer_size;
extern PyObject *const_tuple_str_plain_value_tuple;
extern PyObject *const_str_plain_args;
extern PyObject *const_str_plain_get_limited_unpacker;
extern PyObject *const_str_plain_Packer;
extern PyObject *const_str_plain_Unpacker;
extern PyObject *const_int_pos_8;
extern PyObject *const_str_chr_42;
extern PyObject *const_str_plain_object_hook;
static PyObject *const_str_digest_e9d431b2d489df608ece1fd4d40a35ea;
extern PyObject *const_str_plain_is_slow_msgpack;
extern PyObject *const_str_plain_manifest;
extern PyObject *const_tuple_empty;
extern PyObject *const_str_plain_mtime;
extern PyObject *const_str_plain_max_bin_len;
static PyObject *const_str_digest_298de95f784432487bc69c8bab59661a;
extern PyObject *const_int_pos_2;
extern PyObject *const_str_plain_to_bytes;
extern PyObject *const_str_plain_from_bytes;
extern PyObject *const_str_plain___loader__;
extern PyObject *const_str_digest_527f08c4556a3fc2d6f530aa1e4611db;
static PyObject *const_int_pos_4000;
extern PyObject *const_str_plain_little;
static PyObject *const_tuple_str_plain_mtime_tuple;
extern PyObject *const_str_plain_MAX_ARCHIVES;
extern PyObject *const_int_pos_10;
extern PyObject *const_int_pos_100;
extern PyObject *const_str_plain___doc__;
extern PyObject *const_str_plain___cached__;
static PyObject *module_filename_obj;

static bool constants_created = false;

static void createModuleConstants( void )
{
    const_str_digest_fbcbc0962c569e60944e990076b07e8a = UNSTREAM_STRING( &constant_bin[ 151360 ], 52, 0 );
    const_dict_856ad4ad04f4b1f3ed6830e3dac24f83 = _PyDict_NewPresized( 2 );
    PyDict_SetItem( const_dict_856ad4ad04f4b1f3ed6830e3dac24f83, const_str_plain_max_map_len, const_int_pos_100 );
    PyDict_SetItem( const_dict_856ad4ad04f4b1f3ed6830e3dac24f83, const_str_plain_max_array_len, const_int_pos_100 );
    assert( PyDict_Size( const_dict_856ad4ad04f4b1f3ed6830e3dac24f83 ) == 2 );
    const_str_plain_bit_length = UNSTREAM_STRING( &constant_bin[ 151412 ], 10, 1 );
    const_str_digest_89caf116f40c695b6bb920b8484fa4eb = UNSTREAM_STRING( &constant_bin[ 151422 ], 23, 0 );
    const_str_digest_e935d50786a37c4692c57bc9563b6d8a = UNSTREAM_STRING( &constant_bin[ 151445 ], 20, 0 );
    const_dict_572050117e2cfc8c656df66eb5790338 = _PyDict_NewPresized( 1 );
    const_str_plain_signed = UNSTREAM_STRING( &constant_bin[ 67656 ], 6, 1 );
    PyDict_SetItem( const_dict_572050117e2cfc8c656df66eb5790338, const_str_plain_signed, Py_True );
    assert( PyDict_Size( const_dict_572050117e2cfc8c656df66eb5790338 ) == 1 );
    const_str_digest_fa0dca0529b0df98590638b6970f9269 = UNSTREAM_STRING( &constant_bin[ 151465 ], 29, 0 );
    const_str_digest_8934cf5a483ff31655447816b42b1638 = UNSTREAM_STRING( &constant_bin[ 151494 ], 29, 0 );
    const_tuple_str_plain_kind_str_plain_args_tuple = PyTuple_New( 2 );
    PyTuple_SET_ITEM( const_tuple_str_plain_kind_str_plain_args_tuple, 0, const_str_plain_kind ); Py_INCREF( const_str_plain_kind );
    PyTuple_SET_ITEM( const_tuple_str_plain_kind_str_plain_args_tuple, 1, const_str_plain_args ); Py_INCREF( const_str_plain_args );
    const_str_digest_e9d431b2d489df608ece1fd4d40a35ea = UNSTREAM_STRING( &constant_bin[ 151523 ], 91, 0 );
    const_str_digest_298de95f784432487bc69c8bab59661a = UNSTREAM_STRING( &constant_bin[ 151614 ], 87, 0 );
    const_int_pos_4000 = PyLong_FromUnsignedLong( 4000ul );
    const_tuple_str_plain_mtime_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_mtime_tuple, 0, const_str_plain_mtime ); Py_INCREF( const_str_plain_mtime );

    constants_created = true;
}

#ifndef __NUITKA_NO_ASSERT__
void checkModuleConstants_borg$helpers$msgpack( void )
{
    // The module may not have been used at all.
    if (constants_created == false) return;


}
#endif

// The module code objects.
static PyCodeObject *codeobj_fd1a2420d53b3d03ceeaf317dca35c3a;
static PyCodeObject *codeobj_04aff8f40657a7831dc1ccc733d37c7b;
static PyCodeObject *codeobj_54d425feb5194dbe94589e64977bbc02;
static PyCodeObject *codeobj_166775609088984b2202587d5d940cbc;
static PyCodeObject *codeobj_472efd5ff00f1ee09db1945e53c348ab;

static void createModuleCodeObjects(void)
{
    module_filename_obj = MAKE_RELATIVE_PATH( const_str_digest_89caf116f40c695b6bb920b8484fa4eb );
    codeobj_fd1a2420d53b3d03ceeaf317dca35c3a = MAKE_CODEOBJ( module_filename_obj, const_str_digest_fa0dca0529b0df98590638b6970f9269, 1, const_tuple_empty, 0, 0, CO_NOFREE );
    codeobj_04aff8f40657a7831dc1ccc733d37c7b = MAKE_CODEOBJ( module_filename_obj, const_str_plain_bigint_to_int, 49, const_tuple_str_plain_mtime_tuple, 1, 0, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE );
    codeobj_54d425feb5194dbe94589e64977bbc02 = MAKE_CODEOBJ( module_filename_obj, const_str_plain_get_limited_unpacker, 12, const_tuple_str_plain_kind_str_plain_args_tuple, 1, 0, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE );
    codeobj_166775609088984b2202587d5d940cbc = MAKE_CODEOBJ( module_filename_obj, const_str_plain_int_to_bigint, 57, const_tuple_str_plain_value_tuple, 1, 0, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE );
    codeobj_472efd5ff00f1ee09db1945e53c348ab = MAKE_CODEOBJ( module_filename_obj, const_str_plain_is_slow_msgpack, 8, const_tuple_empty, 0, 0, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE );
}

// The module function declarations.
NUITKA_CROSS_MODULE PyObject *impl___internal__$$$function_6_complex_call_helper_star_dict( PyObject **python_pars );


static PyObject *MAKE_FUNCTION_borg$helpers$msgpack$$$function_1_is_slow_msgpack(  );


static PyObject *MAKE_FUNCTION_borg$helpers$msgpack$$$function_2_get_limited_unpacker(  );


static PyObject *MAKE_FUNCTION_borg$helpers$msgpack$$$function_3_bigint_to_int(  );


static PyObject *MAKE_FUNCTION_borg$helpers$msgpack$$$function_4_int_to_bigint(  );


// The module function definitions.
static PyObject *impl_borg$helpers$msgpack$$$function_1_is_slow_msgpack( struct Nuitka_FunctionObject const *self, PyObject **python_pars )
{
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    PyObject *tmp_compexpr_left_1;
    PyObject *tmp_compexpr_right_1;
    PyObject *tmp_return_value;
    PyObject *tmp_source_name_1;
    PyObject *tmp_source_name_2;
    PyObject *tmp_source_name_3;
    static struct Nuitka_FrameObject *cache_frame_472efd5ff00f1ee09db1945e53c348ab = NULL;

    struct Nuitka_FrameObject *frame_472efd5ff00f1ee09db1945e53c348ab;

    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    tmp_return_value = NULL;

    // Actual function code.
    MAKE_OR_REUSE_FRAME( cache_frame_472efd5ff00f1ee09db1945e53c348ab, codeobj_472efd5ff00f1ee09db1945e53c348ab, module_borg$helpers$msgpack, 0 );
    frame_472efd5ff00f1ee09db1945e53c348ab = cache_frame_472efd5ff00f1ee09db1945e53c348ab;

    // Push the new frame as the currently active one.
    pushFrameStack( frame_472efd5ff00f1ee09db1945e53c348ab );

    // Mark the frame object as in use, ref count 1 will be up for reuse.
    assert( Py_REFCNT( frame_472efd5ff00f1ee09db1945e53c348ab ) == 2 ); // Frame stack

    // Framed code:
    tmp_source_name_1 = GET_STRING_DICT_VALUE( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain_msgpack );

    if (unlikely( tmp_source_name_1 == NULL ))
    {
        tmp_source_name_1 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_msgpack );
    }

    if ( tmp_source_name_1 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "msgpack" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 9;

        goto frame_exception_exit_1;
    }

    tmp_compexpr_left_1 = LOOKUP_ATTRIBUTE( tmp_source_name_1, const_str_plain_Packer );
    if ( tmp_compexpr_left_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 9;

        goto frame_exception_exit_1;
    }
    tmp_source_name_3 = GET_STRING_DICT_VALUE( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain_msgpack );

    if (unlikely( tmp_source_name_3 == NULL ))
    {
        tmp_source_name_3 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_msgpack );
    }

    if ( tmp_source_name_3 == NULL )
    {
        Py_DECREF( tmp_compexpr_left_1 );
        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "msgpack" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 9;

        goto frame_exception_exit_1;
    }

    tmp_source_name_2 = LOOKUP_ATTRIBUTE( tmp_source_name_3, const_str_plain_fallback );
    if ( tmp_source_name_2 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_compexpr_left_1 );

        exception_lineno = 9;

        goto frame_exception_exit_1;
    }
    tmp_compexpr_right_1 = LOOKUP_ATTRIBUTE( tmp_source_name_2, const_str_plain_Packer );
    Py_DECREF( tmp_source_name_2 );
    if ( tmp_compexpr_right_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_compexpr_left_1 );

        exception_lineno = 9;

        goto frame_exception_exit_1;
    }
    tmp_return_value = BOOL_FROM( tmp_compexpr_left_1 == tmp_compexpr_right_1 );
    Py_DECREF( tmp_compexpr_left_1 );
    Py_DECREF( tmp_compexpr_right_1 );
    Py_INCREF( tmp_return_value );
    goto frame_return_exit_1;

#if 0
    RESTORE_FRAME_EXCEPTION( frame_472efd5ff00f1ee09db1945e53c348ab );
#endif

    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;

    frame_return_exit_1:;
#if 0
    RESTORE_FRAME_EXCEPTION( frame_472efd5ff00f1ee09db1945e53c348ab );
#endif

    // Put the previous frame back on top.
    popFrameStack();

    goto function_return_exit;

    frame_exception_exit_1:;

#if 0
    RESTORE_FRAME_EXCEPTION( frame_472efd5ff00f1ee09db1945e53c348ab );
#endif

    if ( exception_tb == NULL )
    {
        exception_tb = MAKE_TRACEBACK( frame_472efd5ff00f1ee09db1945e53c348ab, exception_lineno );
    }
    else if ( exception_tb->tb_frame != &frame_472efd5ff00f1ee09db1945e53c348ab->m_frame )
    {
        exception_tb = ADD_TRACEBACK( exception_tb, frame_472efd5ff00f1ee09db1945e53c348ab, exception_lineno );
    }

    // Attachs locals to frame if any.
    Nuitka_Frame_AttachLocals(
        (struct Nuitka_FrameObject *)frame_472efd5ff00f1ee09db1945e53c348ab,
        type_description_1
    );


    // Release cached frame.
    if ( frame_472efd5ff00f1ee09db1945e53c348ab == cache_frame_472efd5ff00f1ee09db1945e53c348ab )
    {
        Py_DECREF( frame_472efd5ff00f1ee09db1945e53c348ab );
    }
    cache_frame_472efd5ff00f1ee09db1945e53c348ab = NULL;

    assertFrameObject( frame_472efd5ff00f1ee09db1945e53c348ab );

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;

    frame_no_exception_1:;


    // Return statement must have exited already.
    NUITKA_CANNOT_GET_HERE( borg$helpers$msgpack$$$function_1_is_slow_msgpack );
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


static PyObject *impl_borg$helpers$msgpack$$$function_2_get_limited_unpacker( struct Nuitka_FunctionObject const *self, PyObject **python_pars )
{
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_kind = python_pars[ 0 ];
    PyObject *var_args = NULL;
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
    PyObject *tmp_args_element_name_4;
    PyObject *tmp_args_element_name_5;
    PyObject *tmp_assign_source_1;
    PyObject *tmp_call_arg_element_1;
    PyObject *tmp_called_instance_1;
    PyObject *tmp_called_name_1;
    PyObject *tmp_called_name_2;
    PyObject *tmp_called_name_3;
    PyObject *tmp_called_name_4;
    int tmp_cmp_Eq_1;
    int tmp_cmp_Eq_2;
    int tmp_cmp_Eq_3;
    int tmp_cmp_Eq_4;
    PyObject *tmp_compare_left_1;
    PyObject *tmp_compare_left_2;
    PyObject *tmp_compare_left_3;
    PyObject *tmp_compare_left_4;
    PyObject *tmp_compare_right_1;
    PyObject *tmp_compare_right_2;
    PyObject *tmp_compare_right_3;
    PyObject *tmp_compare_right_4;
    PyObject *tmp_dict_key_1;
    PyObject *tmp_dict_key_2;
    PyObject *tmp_dict_key_3;
    PyObject *tmp_dict_key_4;
    PyObject *tmp_dict_key_5;
    PyObject *tmp_dict_key_6;
    PyObject *tmp_dict_key_7;
    PyObject *tmp_dict_key_8;
    PyObject *tmp_dict_key_9;
    PyObject *tmp_dict_key_10;
    PyObject *tmp_dict_key_11;
    PyObject *tmp_dict_key_12;
    PyObject *tmp_dict_key_13;
    PyObject *tmp_dict_key_14;
    PyObject *tmp_dict_key_15;
    PyObject *tmp_dict_key_16;
    PyObject *tmp_dict_key_17;
    PyObject *tmp_dict_key_18;
    PyObject *tmp_dict_key_19;
    PyObject *tmp_dict_value_1;
    PyObject *tmp_dict_value_2;
    PyObject *tmp_dict_value_3;
    PyObject *tmp_dict_value_4;
    PyObject *tmp_dict_value_5;
    PyObject *tmp_dict_value_6;
    PyObject *tmp_dict_value_7;
    PyObject *tmp_dict_value_8;
    PyObject *tmp_dict_value_9;
    PyObject *tmp_dict_value_10;
    PyObject *tmp_dict_value_11;
    PyObject *tmp_dict_value_12;
    PyObject *tmp_dict_value_13;
    PyObject *tmp_dict_value_14;
    PyObject *tmp_dict_value_15;
    PyObject *tmp_dict_value_16;
    PyObject *tmp_dict_value_17;
    PyObject *tmp_dict_value_18;
    PyObject *tmp_dict_value_19;
    PyObject *tmp_dircall_arg1_1;
    PyObject *tmp_dircall_arg2_1;
    PyObject *tmp_left_name_1;
    PyObject *tmp_make_exception_arg_1;
    PyObject *tmp_raise_type_1;
    int tmp_res;
    PyObject *tmp_return_value;
    PyObject *tmp_right_name_1;
    PyObject *tmp_source_name_1;
    PyObject *tmp_source_name_2;
    PyObject *tmp_source_name_3;
    PyObject *tmp_source_name_4;
    NUITKA_MAY_BE_UNUSED PyObject *tmp_unused;
    static struct Nuitka_FrameObject *cache_frame_54d425feb5194dbe94589e64977bbc02 = NULL;

    struct Nuitka_FrameObject *frame_54d425feb5194dbe94589e64977bbc02;

    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    tmp_return_value = NULL;

    // Actual function code.
    // Tried code:
    MAKE_OR_REUSE_FRAME( cache_frame_54d425feb5194dbe94589e64977bbc02, codeobj_54d425feb5194dbe94589e64977bbc02, module_borg$helpers$msgpack, sizeof(void *)+sizeof(void *) );
    frame_54d425feb5194dbe94589e64977bbc02 = cache_frame_54d425feb5194dbe94589e64977bbc02;

    // Push the new frame as the currently active one.
    pushFrameStack( frame_54d425feb5194dbe94589e64977bbc02 );

    // Mark the frame object as in use, ref count 1 will be up for reuse.
    assert( Py_REFCNT( frame_54d425feb5194dbe94589e64977bbc02 ) == 2 ); // Frame stack

    // Framed code:
    tmp_assign_source_1 = _PyDict_NewPresized( 5 );
    tmp_dict_key_1 = const_str_plain_use_list;
    tmp_dict_value_1 = Py_False;
    tmp_res = PyDict_SetItem( tmp_assign_source_1, tmp_dict_key_1, tmp_dict_value_1 );
    assert( !(tmp_res != 0) );
    tmp_dict_key_2 = const_str_plain_max_bin_len;
    tmp_dict_value_2 = const_int_0;
    tmp_res = PyDict_SetItem( tmp_assign_source_1, tmp_dict_key_2, tmp_dict_value_2 );
    assert( !(tmp_res != 0) );
    tmp_dict_key_3 = const_str_plain_max_ext_len;
    tmp_dict_value_3 = const_int_0;
    tmp_res = PyDict_SetItem( tmp_assign_source_1, tmp_dict_key_3, tmp_dict_value_3 );
    assert( !(tmp_res != 0) );
    tmp_dict_key_4 = const_str_plain_max_buffer_size;
    tmp_left_name_1 = const_int_pos_3;
    tmp_called_name_1 = LOOKUP_BUILTIN( const_str_plain_max );
    assert( tmp_called_name_1 != NULL );
    tmp_args_element_name_1 = GET_STRING_DICT_VALUE( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain_BUFSIZE );

    if (unlikely( tmp_args_element_name_1 == NULL ))
    {
        tmp_args_element_name_1 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_BUFSIZE );
    }

    if ( tmp_args_element_name_1 == NULL )
    {
        Py_DECREF( tmp_assign_source_1 );
        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "BUFSIZE" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 17;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }

    tmp_args_element_name_2 = GET_STRING_DICT_VALUE( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain_MAX_OBJECT_SIZE );

    if (unlikely( tmp_args_element_name_2 == NULL ))
    {
        tmp_args_element_name_2 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_MAX_OBJECT_SIZE );
    }

    if ( tmp_args_element_name_2 == NULL )
    {
        Py_DECREF( tmp_assign_source_1 );
        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "MAX_OBJECT_SIZE" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 17;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }

    frame_54d425feb5194dbe94589e64977bbc02->m_frame.f_lineno = 17;
    {
        PyObject *call_args[] = { tmp_args_element_name_1, tmp_args_element_name_2 };
        tmp_right_name_1 = CALL_FUNCTION_WITH_ARGS2( tmp_called_name_1, call_args );
    }

    if ( tmp_right_name_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_1 );

        exception_lineno = 17;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }
    tmp_dict_value_4 = BINARY_OPERATION_MUL( tmp_left_name_1, tmp_right_name_1 );
    Py_DECREF( tmp_right_name_1 );
    if ( tmp_dict_value_4 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_1 );

        exception_lineno = 17;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }
    tmp_res = PyDict_SetItem( tmp_assign_source_1, tmp_dict_key_4, tmp_dict_value_4 );
    Py_DECREF( tmp_dict_value_4 );
    assert( !(tmp_res != 0) );
    tmp_dict_key_5 = const_str_plain_max_str_len;
    tmp_dict_value_5 = GET_STRING_DICT_VALUE( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain_MAX_OBJECT_SIZE );

    if (unlikely( tmp_dict_value_5 == NULL ))
    {
        tmp_dict_value_5 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_MAX_OBJECT_SIZE );
    }

    if ( tmp_dict_value_5 == NULL )
    {
        Py_DECREF( tmp_assign_source_1 );
        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "MAX_OBJECT_SIZE" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 18;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }

    tmp_res = PyDict_SetItem( tmp_assign_source_1, tmp_dict_key_5, tmp_dict_value_5 );
    assert( !(tmp_res != 0) );
    assert( var_args == NULL );
    var_args = tmp_assign_source_1;

    tmp_compare_left_1 = par_kind;

    if ( tmp_compare_left_1 == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "kind" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 20;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }

    tmp_compare_right_1 = const_str_plain_server;
    tmp_cmp_Eq_1 = RICH_COMPARE_BOOL_EQ( tmp_compare_left_1, tmp_compare_right_1 );
    if ( tmp_cmp_Eq_1 == -1 )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 20;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }
    if ( tmp_cmp_Eq_1 == 1 )
    {
        goto branch_yes_1;
    }
    else
    {
        goto branch_no_1;
    }
    branch_yes_1:;
    tmp_called_instance_1 = var_args;

    if ( tmp_called_instance_1 == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "args" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 21;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }

    tmp_call_arg_element_1 = PyDict_Copy( const_dict_856ad4ad04f4b1f3ed6830e3dac24f83 );
    frame_54d425feb5194dbe94589e64977bbc02->m_frame.f_lineno = 21;
    {
        PyObject *call_args[] = { tmp_call_arg_element_1 };
        tmp_unused = CALL_METHOD_WITH_ARGS1( tmp_called_instance_1, const_str_plain_update, call_args );
    }

    Py_DECREF( tmp_call_arg_element_1 );
    if ( tmp_unused == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 21;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }
    Py_DECREF( tmp_unused );
    goto branch_end_1;
    branch_no_1:;
    tmp_compare_left_2 = par_kind;

    if ( tmp_compare_left_2 == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "kind" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 24;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }

    tmp_compare_right_2 = const_str_plain_client;
    tmp_cmp_Eq_2 = RICH_COMPARE_BOOL_EQ( tmp_compare_left_2, tmp_compare_right_2 );
    if ( tmp_cmp_Eq_2 == -1 )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 24;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }
    if ( tmp_cmp_Eq_2 == 1 )
    {
        goto branch_yes_2;
    }
    else
    {
        goto branch_no_2;
    }
    branch_yes_2:;
    tmp_source_name_1 = var_args;

    if ( tmp_source_name_1 == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "args" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 25;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }

    tmp_called_name_2 = LOOKUP_ATTRIBUTE( tmp_source_name_1, const_str_plain_update );
    if ( tmp_called_name_2 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 25;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }
    tmp_args_element_name_3 = _PyDict_NewPresized( 2 );
    tmp_dict_key_6 = const_str_plain_max_array_len;
    tmp_dict_value_6 = GET_STRING_DICT_VALUE( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain_LIST_SCAN_LIMIT );

    if (unlikely( tmp_dict_value_6 == NULL ))
    {
        tmp_dict_value_6 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_LIST_SCAN_LIMIT );
    }

    if ( tmp_dict_value_6 == NULL )
    {
        Py_DECREF( tmp_called_name_2 );
        Py_DECREF( tmp_args_element_name_3 );
        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "LIST_SCAN_LIMIT" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 25;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }

    tmp_res = PyDict_SetItem( tmp_args_element_name_3, tmp_dict_key_6, tmp_dict_value_6 );
    assert( !(tmp_res != 0) );
    tmp_dict_key_7 = const_str_plain_max_map_len;
    tmp_dict_value_7 = const_int_pos_100;
    tmp_res = PyDict_SetItem( tmp_args_element_name_3, tmp_dict_key_7, tmp_dict_value_7 );
    assert( !(tmp_res != 0) );
    frame_54d425feb5194dbe94589e64977bbc02->m_frame.f_lineno = 25;
    {
        PyObject *call_args[] = { tmp_args_element_name_3 };
        tmp_unused = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_2, call_args );
    }

    Py_DECREF( tmp_called_name_2 );
    Py_DECREF( tmp_args_element_name_3 );
    if ( tmp_unused == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 25;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }
    Py_DECREF( tmp_unused );
    goto branch_end_2;
    branch_no_2:;
    tmp_compare_left_3 = par_kind;

    if ( tmp_compare_left_3 == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "kind" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 28;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }

    tmp_compare_right_3 = const_str_plain_manifest;
    tmp_cmp_Eq_3 = RICH_COMPARE_BOOL_EQ( tmp_compare_left_3, tmp_compare_right_3 );
    if ( tmp_cmp_Eq_3 == -1 )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 28;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }
    if ( tmp_cmp_Eq_3 == 1 )
    {
        goto branch_yes_3;
    }
    else
    {
        goto branch_no_3;
    }
    branch_yes_3:;
    tmp_source_name_2 = var_args;

    if ( tmp_source_name_2 == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "args" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 29;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }

    tmp_called_name_3 = LOOKUP_ATTRIBUTE( tmp_source_name_2, const_str_plain_update );
    if ( tmp_called_name_3 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 29;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }
    tmp_args_element_name_4 = _PyDict_NewPresized( 6 );
    tmp_dict_key_8 = const_str_plain_use_list;
    tmp_dict_value_8 = Py_True;
    tmp_res = PyDict_SetItem( tmp_args_element_name_4, tmp_dict_key_8, tmp_dict_value_8 );
    assert( !(tmp_res != 0) );
    tmp_dict_key_9 = const_str_plain_max_array_len;
    tmp_dict_value_9 = const_int_pos_100;
    tmp_res = PyDict_SetItem( tmp_args_element_name_4, tmp_dict_key_9, tmp_dict_value_9 );
    assert( !(tmp_res != 0) );
    tmp_dict_key_10 = const_str_plain_max_map_len;
    tmp_dict_value_10 = GET_STRING_DICT_VALUE( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain_MAX_ARCHIVES );

    if (unlikely( tmp_dict_value_10 == NULL ))
    {
        tmp_dict_value_10 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_MAX_ARCHIVES );
    }

    if ( tmp_dict_value_10 == NULL )
    {
        Py_DECREF( tmp_called_name_3 );
        Py_DECREF( tmp_args_element_name_4 );
        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "MAX_ARCHIVES" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 31;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }

    tmp_res = PyDict_SetItem( tmp_args_element_name_4, tmp_dict_key_10, tmp_dict_value_10 );
    assert( !(tmp_res != 0) );
    tmp_dict_key_11 = const_str_plain_max_str_len;
    tmp_dict_value_11 = const_int_pos_255;
    tmp_res = PyDict_SetItem( tmp_args_element_name_4, tmp_dict_key_11, tmp_dict_value_11 );
    assert( !(tmp_res != 0) );
    tmp_dict_key_12 = const_str_plain_object_hook;
    tmp_dict_value_12 = GET_STRING_DICT_VALUE( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain_StableDict );

    if (unlikely( tmp_dict_value_12 == NULL ))
    {
        tmp_dict_value_12 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_StableDict );
    }

    if ( tmp_dict_value_12 == NULL )
    {
        Py_DECREF( tmp_called_name_3 );
        Py_DECREF( tmp_args_element_name_4 );
        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "StableDict" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 33;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }

    tmp_res = PyDict_SetItem( tmp_args_element_name_4, tmp_dict_key_12, tmp_dict_value_12 );
    assert( !(tmp_res != 0) );
    tmp_dict_key_13 = const_str_plain_unicode_errors;
    tmp_dict_value_13 = const_str_plain_surrogateescape;
    tmp_res = PyDict_SetItem( tmp_args_element_name_4, tmp_dict_key_13, tmp_dict_value_13 );
    assert( !(tmp_res != 0) );
    frame_54d425feb5194dbe94589e64977bbc02->m_frame.f_lineno = 29;
    {
        PyObject *call_args[] = { tmp_args_element_name_4 };
        tmp_unused = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_3, call_args );
    }

    Py_DECREF( tmp_called_name_3 );
    Py_DECREF( tmp_args_element_name_4 );
    if ( tmp_unused == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 29;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }
    Py_DECREF( tmp_unused );
    goto branch_end_3;
    branch_no_3:;
    tmp_compare_left_4 = par_kind;

    if ( tmp_compare_left_4 == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "kind" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 36;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }

    tmp_compare_right_4 = const_str_plain_key;
    tmp_cmp_Eq_4 = RICH_COMPARE_BOOL_EQ( tmp_compare_left_4, tmp_compare_right_4 );
    if ( tmp_cmp_Eq_4 == -1 )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 36;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }
    if ( tmp_cmp_Eq_4 == 1 )
    {
        goto branch_yes_4;
    }
    else
    {
        goto branch_no_4;
    }
    branch_yes_4:;
    tmp_source_name_3 = var_args;

    if ( tmp_source_name_3 == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "args" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 37;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }

    tmp_called_name_4 = LOOKUP_ATTRIBUTE( tmp_source_name_3, const_str_plain_update );
    if ( tmp_called_name_4 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 37;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }
    tmp_args_element_name_5 = _PyDict_NewPresized( 6 );
    tmp_dict_key_14 = const_str_plain_use_list;
    tmp_dict_value_14 = Py_True;
    tmp_res = PyDict_SetItem( tmp_args_element_name_5, tmp_dict_key_14, tmp_dict_value_14 );
    assert( !(tmp_res != 0) );
    tmp_dict_key_15 = const_str_plain_max_array_len;
    tmp_dict_value_15 = const_int_0;
    tmp_res = PyDict_SetItem( tmp_args_element_name_5, tmp_dict_key_15, tmp_dict_value_15 );
    assert( !(tmp_res != 0) );
    tmp_dict_key_16 = const_str_plain_max_map_len;
    tmp_dict_value_16 = const_int_pos_10;
    tmp_res = PyDict_SetItem( tmp_args_element_name_5, tmp_dict_key_16, tmp_dict_value_16 );
    assert( !(tmp_res != 0) );
    tmp_dict_key_17 = const_str_plain_max_str_len;
    tmp_dict_value_17 = const_int_pos_4000;
    tmp_res = PyDict_SetItem( tmp_args_element_name_5, tmp_dict_key_17, tmp_dict_value_17 );
    assert( !(tmp_res != 0) );
    tmp_dict_key_18 = const_str_plain_object_hook;
    tmp_dict_value_18 = GET_STRING_DICT_VALUE( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain_StableDict );

    if (unlikely( tmp_dict_value_18 == NULL ))
    {
        tmp_dict_value_18 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_StableDict );
    }

    if ( tmp_dict_value_18 == NULL )
    {
        Py_DECREF( tmp_called_name_4 );
        Py_DECREF( tmp_args_element_name_5 );
        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "StableDict" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 41;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }

    tmp_res = PyDict_SetItem( tmp_args_element_name_5, tmp_dict_key_18, tmp_dict_value_18 );
    assert( !(tmp_res != 0) );
    tmp_dict_key_19 = const_str_plain_unicode_errors;
    tmp_dict_value_19 = const_str_plain_surrogateescape;
    tmp_res = PyDict_SetItem( tmp_args_element_name_5, tmp_dict_key_19, tmp_dict_value_19 );
    assert( !(tmp_res != 0) );
    frame_54d425feb5194dbe94589e64977bbc02->m_frame.f_lineno = 37;
    {
        PyObject *call_args[] = { tmp_args_element_name_5 };
        tmp_unused = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_4, call_args );
    }

    Py_DECREF( tmp_called_name_4 );
    Py_DECREF( tmp_args_element_name_5 );
    if ( tmp_unused == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 37;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }
    Py_DECREF( tmp_unused );
    goto branch_end_4;
    branch_no_4:;
    tmp_make_exception_arg_1 = const_str_digest_fbcbc0962c569e60944e990076b07e8a;
    frame_54d425feb5194dbe94589e64977bbc02->m_frame.f_lineno = 45;
    {
        PyObject *call_args[] = { tmp_make_exception_arg_1 };
        tmp_raise_type_1 = CALL_FUNCTION_WITH_ARGS1( PyExc_ValueError, call_args );
    }

    assert( tmp_raise_type_1 != NULL );
    exception_type = tmp_raise_type_1;
    exception_lineno = 45;
    RAISE_EXCEPTION_WITH_TYPE( &exception_type, &exception_value, &exception_tb );
    type_description_1 = "oo";
    goto frame_exception_exit_1;
    branch_end_4:;
    branch_end_3:;
    branch_end_2:;
    branch_end_1:;
    tmp_source_name_4 = GET_STRING_DICT_VALUE( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain_msgpack );

    if (unlikely( tmp_source_name_4 == NULL ))
    {
        tmp_source_name_4 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_msgpack );
    }

    if ( tmp_source_name_4 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "msgpack" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 46;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }

    tmp_dircall_arg1_1 = LOOKUP_ATTRIBUTE( tmp_source_name_4, const_str_plain_Unpacker );
    if ( tmp_dircall_arg1_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 46;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }
    tmp_dircall_arg2_1 = var_args;

    if ( tmp_dircall_arg2_1 == NULL )
    {
        Py_DECREF( tmp_dircall_arg1_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "args" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 46;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }

    Py_INCREF( tmp_dircall_arg2_1 );

    {
        PyObject *dir_call_args[] = {tmp_dircall_arg1_1, tmp_dircall_arg2_1};
        tmp_return_value = impl___internal__$$$function_6_complex_call_helper_star_dict( dir_call_args );
    }
    if ( tmp_return_value == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 46;
        type_description_1 = "oo";
        goto frame_exception_exit_1;
    }
    goto frame_return_exit_1;

#if 0
    RESTORE_FRAME_EXCEPTION( frame_54d425feb5194dbe94589e64977bbc02 );
#endif

    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;

    frame_return_exit_1:;
#if 0
    RESTORE_FRAME_EXCEPTION( frame_54d425feb5194dbe94589e64977bbc02 );
#endif

    // Put the previous frame back on top.
    popFrameStack();

    goto try_return_handler_1;

    frame_exception_exit_1:;

#if 0
    RESTORE_FRAME_EXCEPTION( frame_54d425feb5194dbe94589e64977bbc02 );
#endif

    if ( exception_tb == NULL )
    {
        exception_tb = MAKE_TRACEBACK( frame_54d425feb5194dbe94589e64977bbc02, exception_lineno );
    }
    else if ( exception_tb->tb_frame != &frame_54d425feb5194dbe94589e64977bbc02->m_frame )
    {
        exception_tb = ADD_TRACEBACK( exception_tb, frame_54d425feb5194dbe94589e64977bbc02, exception_lineno );
    }

    // Attachs locals to frame if any.
    Nuitka_Frame_AttachLocals(
        (struct Nuitka_FrameObject *)frame_54d425feb5194dbe94589e64977bbc02,
        type_description_1,
        par_kind,
        var_args
    );


    // Release cached frame.
    if ( frame_54d425feb5194dbe94589e64977bbc02 == cache_frame_54d425feb5194dbe94589e64977bbc02 )
    {
        Py_DECREF( frame_54d425feb5194dbe94589e64977bbc02 );
    }
    cache_frame_54d425feb5194dbe94589e64977bbc02 = NULL;

    assertFrameObject( frame_54d425feb5194dbe94589e64977bbc02 );

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto try_except_handler_1;

    frame_no_exception_1:;

    // tried codes exits in all cases
    NUITKA_CANNOT_GET_HERE( borg$helpers$msgpack$$$function_2_get_limited_unpacker );
    return NULL;
    // Return handler code:
    try_return_handler_1:;
    Py_XDECREF( par_kind );
    par_kind = NULL;

    Py_XDECREF( var_args );
    var_args = NULL;

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

    Py_XDECREF( par_kind );
    par_kind = NULL;

    Py_XDECREF( var_args );
    var_args = NULL;

    // Re-raise.
    exception_type = exception_keeper_type_1;
    exception_value = exception_keeper_value_1;
    exception_tb = exception_keeper_tb_1;
    exception_lineno = exception_keeper_lineno_1;

    goto function_exception_exit;
    // End of try:

    // Return statement must have exited already.
    NUITKA_CANNOT_GET_HERE( borg$helpers$msgpack$$$function_2_get_limited_unpacker );
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


static PyObject *impl_borg$helpers$msgpack$$$function_3_bigint_to_int( struct Nuitka_FunctionObject const *self, PyObject **python_pars )
{
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_mtime = python_pars[ 0 ];
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    PyObject *exception_keeper_type_1;
    PyObject *exception_keeper_value_1;
    PyTracebackObject *exception_keeper_tb_1;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_1;
    PyObject *tmp_args_name_1;
    PyObject *tmp_called_name_1;
    PyObject *tmp_isinstance_cls_1;
    PyObject *tmp_isinstance_inst_1;
    PyObject *tmp_kw_name_1;
    int tmp_res;
    PyObject *tmp_return_value;
    PyObject *tmp_source_name_1;
    PyObject *tmp_tuple_element_1;
    static struct Nuitka_FrameObject *cache_frame_04aff8f40657a7831dc1ccc733d37c7b = NULL;

    struct Nuitka_FrameObject *frame_04aff8f40657a7831dc1ccc733d37c7b;

    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    tmp_return_value = NULL;

    // Actual function code.
    // Tried code:
    MAKE_OR_REUSE_FRAME( cache_frame_04aff8f40657a7831dc1ccc733d37c7b, codeobj_04aff8f40657a7831dc1ccc733d37c7b, module_borg$helpers$msgpack, sizeof(void *) );
    frame_04aff8f40657a7831dc1ccc733d37c7b = cache_frame_04aff8f40657a7831dc1ccc733d37c7b;

    // Push the new frame as the currently active one.
    pushFrameStack( frame_04aff8f40657a7831dc1ccc733d37c7b );

    // Mark the frame object as in use, ref count 1 will be up for reuse.
    assert( Py_REFCNT( frame_04aff8f40657a7831dc1ccc733d37c7b ) == 2 ); // Frame stack

    // Framed code:
    tmp_isinstance_inst_1 = par_mtime;

    CHECK_OBJECT( tmp_isinstance_inst_1 );
    tmp_isinstance_cls_1 = (PyObject *)&PyBytes_Type;
    tmp_res = Nuitka_IsInstance( tmp_isinstance_inst_1, tmp_isinstance_cls_1 );
    if ( tmp_res == -1 )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 52;
        type_description_1 = "o";
        goto frame_exception_exit_1;
    }
    if ( tmp_res == 1 )
    {
        goto branch_yes_1;
    }
    else
    {
        goto branch_no_1;
    }
    branch_yes_1:;
    tmp_source_name_1 = (PyObject *)&PyLong_Type;
    tmp_called_name_1 = LOOKUP_ATTRIBUTE( tmp_source_name_1, const_str_plain_from_bytes );
    assert( tmp_called_name_1 != NULL );
    tmp_args_name_1 = PyTuple_New( 2 );
    tmp_tuple_element_1 = par_mtime;

    CHECK_OBJECT( tmp_tuple_element_1 );
    Py_INCREF( tmp_tuple_element_1 );
    PyTuple_SET_ITEM( tmp_args_name_1, 0, tmp_tuple_element_1 );
    tmp_tuple_element_1 = const_str_plain_little;
    Py_INCREF( tmp_tuple_element_1 );
    PyTuple_SET_ITEM( tmp_args_name_1, 1, tmp_tuple_element_1 );
    tmp_kw_name_1 = PyDict_Copy( const_dict_572050117e2cfc8c656df66eb5790338 );
    frame_04aff8f40657a7831dc1ccc733d37c7b->m_frame.f_lineno = 53;
    tmp_return_value = CALL_FUNCTION( tmp_called_name_1, tmp_args_name_1, tmp_kw_name_1 );
    Py_DECREF( tmp_called_name_1 );
    Py_DECREF( tmp_args_name_1 );
    Py_DECREF( tmp_kw_name_1 );
    if ( tmp_return_value == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 53;
        type_description_1 = "o";
        goto frame_exception_exit_1;
    }
    goto frame_return_exit_1;
    branch_no_1:;

#if 0
    RESTORE_FRAME_EXCEPTION( frame_04aff8f40657a7831dc1ccc733d37c7b );
#endif

    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;

    frame_return_exit_1:;
#if 0
    RESTORE_FRAME_EXCEPTION( frame_04aff8f40657a7831dc1ccc733d37c7b );
#endif

    // Put the previous frame back on top.
    popFrameStack();

    goto try_return_handler_1;

    frame_exception_exit_1:;

#if 0
    RESTORE_FRAME_EXCEPTION( frame_04aff8f40657a7831dc1ccc733d37c7b );
#endif

    if ( exception_tb == NULL )
    {
        exception_tb = MAKE_TRACEBACK( frame_04aff8f40657a7831dc1ccc733d37c7b, exception_lineno );
    }
    else if ( exception_tb->tb_frame != &frame_04aff8f40657a7831dc1ccc733d37c7b->m_frame )
    {
        exception_tb = ADD_TRACEBACK( exception_tb, frame_04aff8f40657a7831dc1ccc733d37c7b, exception_lineno );
    }

    // Attachs locals to frame if any.
    Nuitka_Frame_AttachLocals(
        (struct Nuitka_FrameObject *)frame_04aff8f40657a7831dc1ccc733d37c7b,
        type_description_1,
        par_mtime
    );


    // Release cached frame.
    if ( frame_04aff8f40657a7831dc1ccc733d37c7b == cache_frame_04aff8f40657a7831dc1ccc733d37c7b )
    {
        Py_DECREF( frame_04aff8f40657a7831dc1ccc733d37c7b );
    }
    cache_frame_04aff8f40657a7831dc1ccc733d37c7b = NULL;

    assertFrameObject( frame_04aff8f40657a7831dc1ccc733d37c7b );

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto try_except_handler_1;

    frame_no_exception_1:;

    tmp_return_value = par_mtime;

    CHECK_OBJECT( tmp_return_value );
    Py_INCREF( tmp_return_value );
    goto try_return_handler_1;
    // tried codes exits in all cases
    NUITKA_CANNOT_GET_HERE( borg$helpers$msgpack$$$function_3_bigint_to_int );
    return NULL;
    // Return handler code:
    try_return_handler_1:;
    Py_XDECREF( par_mtime );
    par_mtime = NULL;

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

    Py_XDECREF( par_mtime );
    par_mtime = NULL;

    // Re-raise.
    exception_type = exception_keeper_type_1;
    exception_value = exception_keeper_value_1;
    exception_tb = exception_keeper_tb_1;
    exception_lineno = exception_keeper_lineno_1;

    goto function_exception_exit;
    // End of try:

    // Return statement must have exited already.
    NUITKA_CANNOT_GET_HERE( borg$helpers$msgpack$$$function_3_bigint_to_int );
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


static PyObject *impl_borg$helpers$msgpack$$$function_4_int_to_bigint( struct Nuitka_FunctionObject const *self, PyObject **python_pars )
{
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_value = python_pars[ 0 ];
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    PyObject *exception_keeper_type_1;
    PyObject *exception_keeper_value_1;
    PyTracebackObject *exception_keeper_tb_1;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_1;
    PyObject *tmp_args_name_1;
    PyObject *tmp_called_instance_1;
    PyObject *tmp_called_instance_2;
    PyObject *tmp_called_name_1;
    int tmp_cmp_Gt_1;
    PyObject *tmp_compare_left_1;
    PyObject *tmp_compare_right_1;
    PyObject *tmp_kw_name_1;
    PyObject *tmp_left_name_1;
    PyObject *tmp_left_name_2;
    PyObject *tmp_return_value;
    PyObject *tmp_right_name_1;
    PyObject *tmp_right_name_2;
    PyObject *tmp_source_name_1;
    PyObject *tmp_tuple_element_1;
    static struct Nuitka_FrameObject *cache_frame_166775609088984b2202587d5d940cbc = NULL;

    struct Nuitka_FrameObject *frame_166775609088984b2202587d5d940cbc;

    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    tmp_return_value = NULL;

    // Actual function code.
    // Tried code:
    MAKE_OR_REUSE_FRAME( cache_frame_166775609088984b2202587d5d940cbc, codeobj_166775609088984b2202587d5d940cbc, module_borg$helpers$msgpack, sizeof(void *) );
    frame_166775609088984b2202587d5d940cbc = cache_frame_166775609088984b2202587d5d940cbc;

    // Push the new frame as the currently active one.
    pushFrameStack( frame_166775609088984b2202587d5d940cbc );

    // Mark the frame object as in use, ref count 1 will be up for reuse.
    assert( Py_REFCNT( frame_166775609088984b2202587d5d940cbc ) == 2 ); // Frame stack

    // Framed code:
    tmp_called_instance_1 = par_value;

    CHECK_OBJECT( tmp_called_instance_1 );
    frame_166775609088984b2202587d5d940cbc->m_frame.f_lineno = 62;
    tmp_compare_left_1 = CALL_METHOD_NO_ARGS( tmp_called_instance_1, const_str_plain_bit_length );
    if ( tmp_compare_left_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 62;
        type_description_1 = "o";
        goto frame_exception_exit_1;
    }
    tmp_compare_right_1 = const_int_pos_63;
    tmp_cmp_Gt_1 = RICH_COMPARE_BOOL_GT( tmp_compare_left_1, tmp_compare_right_1 );
    if ( tmp_cmp_Gt_1 == -1 )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_compare_left_1 );

        exception_lineno = 62;
        type_description_1 = "o";
        goto frame_exception_exit_1;
    }
    Py_DECREF( tmp_compare_left_1 );
    if ( tmp_cmp_Gt_1 == 1 )
    {
        goto branch_yes_1;
    }
    else
    {
        goto branch_no_1;
    }
    branch_yes_1:;
    tmp_source_name_1 = par_value;

    if ( tmp_source_name_1 == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "value" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 63;
        type_description_1 = "o";
        goto frame_exception_exit_1;
    }

    tmp_called_name_1 = LOOKUP_ATTRIBUTE( tmp_source_name_1, const_str_plain_to_bytes );
    if ( tmp_called_name_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 63;
        type_description_1 = "o";
        goto frame_exception_exit_1;
    }
    tmp_args_name_1 = PyTuple_New( 2 );
    tmp_called_instance_2 = par_value;

    if ( tmp_called_instance_2 == NULL )
    {
        Py_DECREF( tmp_called_name_1 );
        Py_DECREF( tmp_args_name_1 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "value" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 63;
        type_description_1 = "o";
        goto frame_exception_exit_1;
    }

    frame_166775609088984b2202587d5d940cbc->m_frame.f_lineno = 63;
    tmp_left_name_2 = CALL_METHOD_NO_ARGS( tmp_called_instance_2, const_str_plain_bit_length );
    if ( tmp_left_name_2 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_1 );
        Py_DECREF( tmp_args_name_1 );

        exception_lineno = 63;
        type_description_1 = "o";
        goto frame_exception_exit_1;
    }
    tmp_right_name_1 = const_int_pos_9;
    tmp_left_name_1 = BINARY_OPERATION_ADD( tmp_left_name_2, tmp_right_name_1 );
    Py_DECREF( tmp_left_name_2 );
    if ( tmp_left_name_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_1 );
        Py_DECREF( tmp_args_name_1 );

        exception_lineno = 63;
        type_description_1 = "o";
        goto frame_exception_exit_1;
    }
    tmp_right_name_2 = const_int_pos_8;
    tmp_tuple_element_1 = BINARY_OPERATION_FLOORDIV( tmp_left_name_1, tmp_right_name_2 );
    Py_DECREF( tmp_left_name_1 );
    if ( tmp_tuple_element_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_called_name_1 );
        Py_DECREF( tmp_args_name_1 );

        exception_lineno = 63;
        type_description_1 = "o";
        goto frame_exception_exit_1;
    }
    PyTuple_SET_ITEM( tmp_args_name_1, 0, tmp_tuple_element_1 );
    tmp_tuple_element_1 = const_str_plain_little;
    Py_INCREF( tmp_tuple_element_1 );
    PyTuple_SET_ITEM( tmp_args_name_1, 1, tmp_tuple_element_1 );
    tmp_kw_name_1 = PyDict_Copy( const_dict_572050117e2cfc8c656df66eb5790338 );
    frame_166775609088984b2202587d5d940cbc->m_frame.f_lineno = 63;
    tmp_return_value = CALL_FUNCTION( tmp_called_name_1, tmp_args_name_1, tmp_kw_name_1 );
    Py_DECREF( tmp_called_name_1 );
    Py_DECREF( tmp_args_name_1 );
    Py_DECREF( tmp_kw_name_1 );
    if ( tmp_return_value == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 63;
        type_description_1 = "o";
        goto frame_exception_exit_1;
    }
    goto frame_return_exit_1;
    branch_no_1:;
    tmp_return_value = par_value;

    if ( tmp_return_value == NULL )
    {

        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "value" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 64;
        type_description_1 = "o";
        goto frame_exception_exit_1;
    }

    Py_INCREF( tmp_return_value );
    goto frame_return_exit_1;

#if 0
    RESTORE_FRAME_EXCEPTION( frame_166775609088984b2202587d5d940cbc );
#endif

    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;

    frame_return_exit_1:;
#if 0
    RESTORE_FRAME_EXCEPTION( frame_166775609088984b2202587d5d940cbc );
#endif

    // Put the previous frame back on top.
    popFrameStack();

    goto try_return_handler_1;

    frame_exception_exit_1:;

#if 0
    RESTORE_FRAME_EXCEPTION( frame_166775609088984b2202587d5d940cbc );
#endif

    if ( exception_tb == NULL )
    {
        exception_tb = MAKE_TRACEBACK( frame_166775609088984b2202587d5d940cbc, exception_lineno );
    }
    else if ( exception_tb->tb_frame != &frame_166775609088984b2202587d5d940cbc->m_frame )
    {
        exception_tb = ADD_TRACEBACK( exception_tb, frame_166775609088984b2202587d5d940cbc, exception_lineno );
    }

    // Attachs locals to frame if any.
    Nuitka_Frame_AttachLocals(
        (struct Nuitka_FrameObject *)frame_166775609088984b2202587d5d940cbc,
        type_description_1,
        par_value
    );


    // Release cached frame.
    if ( frame_166775609088984b2202587d5d940cbc == cache_frame_166775609088984b2202587d5d940cbc )
    {
        Py_DECREF( frame_166775609088984b2202587d5d940cbc );
    }
    cache_frame_166775609088984b2202587d5d940cbc = NULL;

    assertFrameObject( frame_166775609088984b2202587d5d940cbc );

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto try_except_handler_1;

    frame_no_exception_1:;

    // tried codes exits in all cases
    NUITKA_CANNOT_GET_HERE( borg$helpers$msgpack$$$function_4_int_to_bigint );
    return NULL;
    // Return handler code:
    try_return_handler_1:;
    Py_XDECREF( par_value );
    par_value = NULL;

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

    Py_XDECREF( par_value );
    par_value = NULL;

    // Re-raise.
    exception_type = exception_keeper_type_1;
    exception_value = exception_keeper_value_1;
    exception_tb = exception_keeper_tb_1;
    exception_lineno = exception_keeper_lineno_1;

    goto function_exception_exit;
    // End of try:

    // Return statement must have exited already.
    NUITKA_CANNOT_GET_HERE( borg$helpers$msgpack$$$function_4_int_to_bigint );
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



static PyObject *MAKE_FUNCTION_borg$helpers$msgpack$$$function_1_is_slow_msgpack(  )
{
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_borg$helpers$msgpack$$$function_1_is_slow_msgpack,
        const_str_plain_is_slow_msgpack,
#if PYTHON_VERSION >= 330
        NULL,
#endif
        codeobj_472efd5ff00f1ee09db1945e53c348ab,
        NULL,
#if PYTHON_VERSION >= 300
        NULL,
        const_dict_empty,
#endif
        module_borg$helpers$msgpack,
        Py_None,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_borg$helpers$msgpack$$$function_2_get_limited_unpacker(  )
{
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_borg$helpers$msgpack$$$function_2_get_limited_unpacker,
        const_str_plain_get_limited_unpacker,
#if PYTHON_VERSION >= 330
        NULL,
#endif
        codeobj_54d425feb5194dbe94589e64977bbc02,
        NULL,
#if PYTHON_VERSION >= 300
        NULL,
        const_dict_empty,
#endif
        module_borg$helpers$msgpack,
        const_str_digest_298de95f784432487bc69c8bab59661a,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_borg$helpers$msgpack$$$function_3_bigint_to_int(  )
{
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_borg$helpers$msgpack$$$function_3_bigint_to_int,
        const_str_plain_bigint_to_int,
#if PYTHON_VERSION >= 330
        NULL,
#endif
        codeobj_04aff8f40657a7831dc1ccc733d37c7b,
        NULL,
#if PYTHON_VERSION >= 300
        NULL,
        const_dict_empty,
#endif
        module_borg$helpers$msgpack,
        const_str_digest_8934cf5a483ff31655447816b42b1638,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_borg$helpers$msgpack$$$function_4_int_to_bigint(  )
{
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_borg$helpers$msgpack$$$function_4_int_to_bigint,
        const_str_plain_int_to_bigint,
#if PYTHON_VERSION >= 330
        NULL,
#endif
        codeobj_166775609088984b2202587d5d940cbc,
        NULL,
#if PYTHON_VERSION >= 300
        NULL,
        const_dict_empty,
#endif
        module_borg$helpers$msgpack,
        const_str_digest_e9d431b2d489df608ece1fd4d40a35ea,
        0
    );


    return (PyObject *)result;
}



#if PYTHON_VERSION >= 300
static struct PyModuleDef mdef_borg$helpers$msgpack =
{
    PyModuleDef_HEAD_INIT,
    "borg.helpers.msgpack",   /* m_name */
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

MOD_INIT_DECL( borg$helpers$msgpack )
{
#if defined(_NUITKA_EXE) || PYTHON_VERSION >= 300
    static bool _init_done = false;

    // Modules might be imported repeatedly, which is to be ignored.
    if ( _init_done )
    {
        return MOD_RETURN_VALUE( module_borg$helpers$msgpack );
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
    puts("borg.helpers.msgpack: Calling createModuleConstants().");
#endif
    createModuleConstants();

    /* The code objects used by this module are created now. */
#ifdef _NUITKA_TRACE
    puts("borg.helpers.msgpack: Calling createModuleCodeObjects().");
#endif
    createModuleCodeObjects();

    // puts( "in initborg$helpers$msgpack" );

    // Create the module object first. There are no methods initially, all are
    // added dynamically in actual code only.  Also no "__doc__" is initially
    // set at this time, as it could not contain NUL characters this way, they
    // are instead set in early module code.  No "self" for modules, we have no
    // use for it.
#if PYTHON_VERSION < 300
    module_borg$helpers$msgpack = Py_InitModule4(
        "borg.helpers.msgpack",       // Module Name
        NULL,                    // No methods initially, all are added
                                 // dynamically in actual module code only.
        NULL,                    // No __doc__ is initially set, as it could
                                 // not contain NUL this way, added early in
                                 // actual code.
        NULL,                    // No self for modules, we don't use it.
        PYTHON_API_VERSION
    );
#else
    module_borg$helpers$msgpack = PyModule_Create( &mdef_borg$helpers$msgpack );
#endif

    moduledict_borg$helpers$msgpack = MODULE_DICT( module_borg$helpers$msgpack );

    CHECK_OBJECT( module_borg$helpers$msgpack );

// Seems to work for Python2.7 out of the box, but for Python3, the module
// doesn't automatically enter "sys.modules", so do it manually.
#if PYTHON_VERSION >= 300
    {
        int r = PyObject_SetItem( PySys_GetObject( (char *)"modules" ), const_str_digest_e935d50786a37c4692c57bc9563b6d8a, module_borg$helpers$msgpack );

        assert( r != -1 );
    }
#endif

    // For deep importing of a module we need to have "__builtins__", so we set
    // it ourselves in the same way than CPython does. Note: This must be done
    // before the frame object is allocated, or else it may fail.

    if ( GET_STRING_DICT_VALUE( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain___builtins__ ) == NULL )
    {
        PyObject *value = (PyObject *)builtin_module;

        // Check if main module, not a dict then but the module itself.
#if !defined(_NUITKA_EXE) || !0
        value = PyModule_GetDict( value );
#endif

        UPDATE_STRING_DICT0( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain___builtins__, value );
    }

#if PYTHON_VERSION >= 330
    UPDATE_STRING_DICT0( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain___loader__, metapath_based_loader );
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
    PyObject *tmp_assign_source_10;
    PyObject *tmp_assign_source_11;
    PyObject *tmp_assign_source_12;
    PyObject *tmp_assign_source_13;
    PyObject *tmp_called_name_1;
    PyObject *tmp_fromlist_name_1;
    PyObject *tmp_fromlist_name_2;
    PyObject *tmp_fromlist_name_3;
    PyObject *tmp_fromlist_name_4;
    PyObject *tmp_globals_name_1;
    PyObject *tmp_globals_name_2;
    PyObject *tmp_globals_name_3;
    PyObject *tmp_globals_name_4;
    PyObject *tmp_import_name_from_1;
    PyObject *tmp_level_name_1;
    PyObject *tmp_level_name_2;
    PyObject *tmp_level_name_3;
    PyObject *tmp_level_name_4;
    PyObject *tmp_locals_name_1;
    PyObject *tmp_locals_name_2;
    PyObject *tmp_locals_name_3;
    PyObject *tmp_locals_name_4;
    PyObject *tmp_name_name_1;
    PyObject *tmp_name_name_2;
    PyObject *tmp_name_name_3;
    PyObject *tmp_name_name_4;
    bool tmp_result;
    PyObject *tmp_star_imported_1;
    struct Nuitka_FrameObject *frame_fd1a2420d53b3d03ceeaf317dca35c3a;

    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;

    // Module code.
    tmp_assign_source_1 = Py_None;
    UPDATE_STRING_DICT0( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain___doc__, tmp_assign_source_1 );
    tmp_assign_source_2 = module_filename_obj;
    UPDATE_STRING_DICT0( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain___file__, tmp_assign_source_2 );
    tmp_assign_source_3 = metapath_based_loader;
    UPDATE_STRING_DICT0( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain___loader__, tmp_assign_source_3 );
    // Frame without reuse.
    frame_fd1a2420d53b3d03ceeaf317dca35c3a = MAKE_MODULE_FRAME( codeobj_fd1a2420d53b3d03ceeaf317dca35c3a, module_borg$helpers$msgpack );

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStack( frame_fd1a2420d53b3d03ceeaf317dca35c3a );
    assert( Py_REFCNT( frame_fd1a2420d53b3d03ceeaf317dca35c3a ) == 2 );

    // Framed code:
    frame_fd1a2420d53b3d03ceeaf317dca35c3a->m_frame.f_lineno = 1;
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
    tmp_args_element_name_1 = const_str_digest_e935d50786a37c4692c57bc9563b6d8a;
    tmp_args_element_name_2 = metapath_based_loader;
    frame_fd1a2420d53b3d03ceeaf317dca35c3a->m_frame.f_lineno = 1;
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
    UPDATE_STRING_DICT1( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain___spec__, tmp_assign_source_4 );
    tmp_assign_source_5 = Py_None;
    UPDATE_STRING_DICT0( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain___cached__, tmp_assign_source_5 );
    tmp_assign_source_6 = const_str_digest_527f08c4556a3fc2d6f530aa1e4611db;
    UPDATE_STRING_DICT0( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain___package__, tmp_assign_source_6 );
    tmp_name_name_1 = const_str_plain_msgpack;
    tmp_globals_name_1 = (PyObject *)moduledict_borg$helpers$msgpack;
    tmp_locals_name_1 = Py_None;
    tmp_fromlist_name_1 = Py_None;
    tmp_level_name_1 = const_int_0;
    frame_fd1a2420d53b3d03ceeaf317dca35c3a->m_frame.f_lineno = 1;
    tmp_assign_source_7 = IMPORT_MODULE5( tmp_name_name_1, tmp_globals_name_1, tmp_locals_name_1, tmp_fromlist_name_1, tmp_level_name_1 );
    if ( tmp_assign_source_7 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 1;

        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain_msgpack, tmp_assign_source_7 );
    tmp_name_name_2 = const_str_digest_bdc1a971b462566afd65a1f634717d97;
    tmp_globals_name_2 = (PyObject *)moduledict_borg$helpers$msgpack;
    tmp_locals_name_2 = Py_None;
    tmp_fromlist_name_2 = Py_None;
    tmp_level_name_2 = const_int_0;
    frame_fd1a2420d53b3d03ceeaf317dca35c3a->m_frame.f_lineno = 2;
    tmp_assign_source_8 = IMPORT_MODULE5( tmp_name_name_2, tmp_globals_name_2, tmp_locals_name_2, tmp_fromlist_name_2, tmp_level_name_2 );
    if ( tmp_assign_source_8 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 2;

        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain_msgpack, tmp_assign_source_8 );
    tmp_name_name_3 = const_str_plain_datastruct;
    tmp_globals_name_3 = (PyObject *)moduledict_borg$helpers$msgpack;
    tmp_locals_name_3 = Py_None;
    tmp_fromlist_name_3 = const_tuple_str_plain_StableDict_tuple;
    tmp_level_name_3 = const_int_pos_1;
    frame_fd1a2420d53b3d03ceeaf317dca35c3a->m_frame.f_lineno = 4;
    tmp_import_name_from_1 = IMPORT_MODULE5( tmp_name_name_3, tmp_globals_name_3, tmp_locals_name_3, tmp_fromlist_name_3, tmp_level_name_3 );
    if ( tmp_import_name_from_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 4;

        goto frame_exception_exit_1;
    }
    tmp_assign_source_9 = IMPORT_NAME( tmp_import_name_from_1, const_str_plain_StableDict );
    Py_DECREF( tmp_import_name_from_1 );
    if ( tmp_assign_source_9 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 4;

        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain_StableDict, tmp_assign_source_9 );
    tmp_name_name_4 = const_str_plain_constants;
    tmp_globals_name_4 = (PyObject *)moduledict_borg$helpers$msgpack;
    tmp_locals_name_4 = (PyObject *)moduledict_borg$helpers$msgpack;
    tmp_fromlist_name_4 = const_tuple_str_chr_42_tuple;
    tmp_level_name_4 = const_int_pos_2;
    frame_fd1a2420d53b3d03ceeaf317dca35c3a->m_frame.f_lineno = 5;
    tmp_star_imported_1 = IMPORT_MODULE5( tmp_name_name_4, tmp_globals_name_4, tmp_locals_name_4, tmp_fromlist_name_4, tmp_level_name_4 );
    if ( tmp_star_imported_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 5;

        goto frame_exception_exit_1;
    }
    tmp_result = IMPORT_MODULE_STAR( module_borg$helpers$msgpack, true, tmp_star_imported_1 );
    Py_DECREF( tmp_star_imported_1 );
    if ( tmp_result == false )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 5;

        goto frame_exception_exit_1;
    }

    // Restore frame exception if necessary.
#if 0
    RESTORE_FRAME_EXCEPTION( frame_fd1a2420d53b3d03ceeaf317dca35c3a );
#endif
    popFrameStack();

    assertFrameObject( frame_fd1a2420d53b3d03ceeaf317dca35c3a );

    goto frame_no_exception_1;
    frame_exception_exit_1:;
#if 0
    RESTORE_FRAME_EXCEPTION( frame_fd1a2420d53b3d03ceeaf317dca35c3a );
#endif

    if ( exception_tb == NULL )
    {
        exception_tb = MAKE_TRACEBACK( frame_fd1a2420d53b3d03ceeaf317dca35c3a, exception_lineno );
    }
    else if ( exception_tb->tb_frame != &frame_fd1a2420d53b3d03ceeaf317dca35c3a->m_frame )
    {
        exception_tb = ADD_TRACEBACK( exception_tb, frame_fd1a2420d53b3d03ceeaf317dca35c3a, exception_lineno );
    }

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto module_exception_exit;
    frame_no_exception_1:;
    tmp_assign_source_10 = MAKE_FUNCTION_borg$helpers$msgpack$$$function_1_is_slow_msgpack(  );
    UPDATE_STRING_DICT1( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain_is_slow_msgpack, tmp_assign_source_10 );
    tmp_assign_source_11 = MAKE_FUNCTION_borg$helpers$msgpack$$$function_2_get_limited_unpacker(  );
    UPDATE_STRING_DICT1( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain_get_limited_unpacker, tmp_assign_source_11 );
    tmp_assign_source_12 = MAKE_FUNCTION_borg$helpers$msgpack$$$function_3_bigint_to_int(  );
    UPDATE_STRING_DICT1( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain_bigint_to_int, tmp_assign_source_12 );
    tmp_assign_source_13 = MAKE_FUNCTION_borg$helpers$msgpack$$$function_4_int_to_bigint(  );
    UPDATE_STRING_DICT1( moduledict_borg$helpers$msgpack, (Nuitka_StringObject *)const_str_plain_int_to_bigint, tmp_assign_source_13 );

    return MOD_RETURN_VALUE( module_borg$helpers$msgpack );
    module_exception_exit:
    RESTORE_ERROR_OCCURRED( exception_type, exception_value, exception_tb );
    return MOD_RETURN_VALUE( NULL );
}
