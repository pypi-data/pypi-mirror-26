// This provides the frozen (compiled bytecode) files that are included if
// any.
#include <Python.h>

#include "nuitka/constants_blob.h"

// Blob from which modules are unstreamed.
#define stream_data constant_bin

// These modules should be loaded as bytecode. They may e.g. have to be loadable
// during "Py_Initialize" already, or for irrelevance, they are only included
// in this un-optimized form. These are not compiled by Nuitka, and therefore
// are not accelerated at all, merely bundled with the binary or module, so
// that CPython library can start out finding them.

struct frozen_desc {
    char const *name;
    ssize_t start;
    int size;
};

void copyFrozenModulesTo( struct _frozen *destination )
{
    struct frozen_desc frozen_modules[] = {
        { "_bootlocale", 6283511, 1032 },
        { "_collections_abc", 6284543, 29625 },
        { "_compression", 6314168, 4422 },
        { "_weakrefset", 6318590, 8409 },
        { "abc", 6326999, 7853 },
        { "ast", 6334852, 12278 },
        { "base64", 6347130, 18399 },
        { "bz2", 6365529, 11757 },
        { "codecs", 6377286, 35291 },
        { "collections", 6412577, -48675 },
        { "collections.abc", 6284543, 29625 },
        { "copyreg", 6461252, 4553 },
        { "dis", 6465805, 14758 },
        { "encodings", 6480563, -3837 },
        { "encodings.aliases", 6484400, 7553 },
        { "encodings.ascii", 6491953, 1997 },
        { "encodings.base64_codec", 6493950, 2557 },
        { "encodings.big5", 6496507, 1555 },
        { "encodings.big5hkscs", 6498062, 1565 },
        { "encodings.bz2_codec", 6499627, 3467 },
        { "encodings.charmap", 6503094, 3079 },
        { "encodings.cp037", 6506173, 2534 },
        { "encodings.cp1006", 6508707, 2610 },
        { "encodings.cp1026", 6511317, 2538 },
        { "encodings.cp1125", 6513855, 7555 },
        { "encodings.cp1140", 6521410, 2524 },
        { "encodings.cp1250", 6523934, 2561 },
        { "encodings.cp1251", 6526495, 2558 },
        { "encodings.cp1252", 6529053, 2561 },
        { "encodings.cp1253", 6531614, 2574 },
        { "encodings.cp1254", 6534188, 2563 },
        { "encodings.cp1255", 6536751, 2582 },
        { "encodings.cp1256", 6539333, 2560 },
        { "encodings.cp1257", 6541893, 2568 },
        { "encodings.cp1258", 6544461, 2566 },
        { "encodings.cp273", 6547027, 2520 },
        { "encodings.cp424", 6549547, 2564 },
        { "encodings.cp437", 6552111, 7372 },
        { "encodings.cp500", 6559483, 2534 },
        { "encodings.cp720", 6562017, 2631 },
        { "encodings.cp737", 6564648, 7600 },
        { "encodings.cp775", 6572248, 7386 },
        { "encodings.cp850", 6579634, 7119 },
        { "encodings.cp852", 6586753, 7388 },
        { "encodings.cp855", 6594141, 7569 },
        { "encodings.cp856", 6601710, 2596 },
        { "encodings.cp857", 6604306, 7104 },
        { "encodings.cp858", 6611410, 7089 },
        { "encodings.cp860", 6618499, 7355 },
        { "encodings.cp861", 6625854, 7366 },
        { "encodings.cp862", 6633220, 7501 },
        { "encodings.cp863", 6640721, 7366 },
        { "encodings.cp864", 6648087, 7496 },
        { "encodings.cp865", 6655583, 7366 },
        { "encodings.cp866", 6662949, 7601 },
        { "encodings.cp869", 6670550, 7413 },
        { "encodings.cp874", 6677963, 2662 },
        { "encodings.cp875", 6680625, 2531 },
        { "encodings.cp932", 6683156, 1557 },
        { "encodings.cp949", 6684713, 1557 },
        { "encodings.cp950", 6686270, 1557 },
        { "encodings.euc_jis_2004", 6687827, 1571 },
        { "encodings.euc_jisx0213", 6689398, 1571 },
        { "encodings.euc_jp", 6690969, 1559 },
        { "encodings.euc_kr", 6692528, 1559 },
        { "encodings.gb18030", 6694087, 1561 },
        { "encodings.gb2312", 6695648, 1559 },
        { "encodings.gbk", 6697207, 1553 },
        { "encodings.hex_codec", 6698760, 2544 },
        { "encodings.hp_roman8", 6701304, 2735 },
        { "encodings.hz", 6704039, 1551 },
        { "encodings.idna", 6705590, 6447 },
        { "encodings.iso2022_jp", 6712037, 1572 },
        { "encodings.iso2022_jp_1", 6713609, 1576 },
        { "encodings.iso2022_jp_2", 6715185, 1576 },
        { "encodings.iso2022_jp_2004", 6716761, 1582 },
        { "encodings.iso2022_jp_3", 6718343, 1576 },
        { "encodings.iso2022_jp_ext", 6719919, 1580 },
        { "encodings.iso2022_kr", 6721499, 1572 },
        { "encodings.iso8859_1", 6723071, 2533 },
        { "encodings.iso8859_10", 6725604, 2538 },
        { "encodings.iso8859_11", 6728142, 2632 },
        { "encodings.iso8859_13", 6730774, 2541 },
        { "encodings.iso8859_14", 6733315, 2559 },
        { "encodings.iso8859_15", 6735874, 2538 },
        { "encodings.iso8859_16", 6738412, 2540 },
        { "encodings.iso8859_2", 6740952, 2533 },
        { "encodings.iso8859_3", 6743485, 2540 },
        { "encodings.iso8859_4", 6746025, 2533 },
        { "encodings.iso8859_5", 6748558, 2534 },
        { "encodings.iso8859_6", 6751092, 2578 },
        { "encodings.iso8859_7", 6753670, 2541 },
        { "encodings.iso8859_8", 6756211, 2572 },
        { "encodings.iso8859_9", 6758783, 2533 },
        { "encodings.johab", 6761316, 1557 },
        { "encodings.koi8_r", 6762873, 2585 },
        { "encodings.koi8_t", 6765458, 2496 },
        { "encodings.koi8_u", 6767954, 2571 },
        { "encodings.kz1048", 6770525, 2548 },
        { "encodings.latin_1", 6773073, 2009 },
        { "encodings.mac_arabic", 6775082, 7272 },
        { "encodings.mac_centeuro", 6782354, 2572 },
        { "encodings.mac_croatian", 6784926, 2580 },
        { "encodings.mac_cyrillic", 6787506, 2570 },
        { "encodings.mac_farsi", 6790076, 2514 },
        { "encodings.mac_greek", 6792590, 2554 },
        { "encodings.mac_iceland", 6795144, 2573 },
        { "encodings.mac_latin2", 6797717, 2714 },
        { "encodings.mac_roman", 6800431, 2571 },
        { "encodings.mac_romanian", 6803002, 2581 },
        { "encodings.mac_turkish", 6805583, 2574 },
        { "encodings.palmos", 6808157, 2561 },
        { "encodings.ptcp154", 6810718, 2655 },
        { "encodings.punycode", 6813373, 7082 },
        { "encodings.quopri_codec", 6820455, 2589 },
        { "encodings.raw_unicode_escape", 6823044, 1865 },
        { "encodings.rot_13", 6824909, 3081 },
        { "encodings.shift_jis", 6827990, 1565 },
        { "encodings.shift_jis_2004", 6829555, 1575 },
        { "encodings.shift_jisx0213", 6831130, 1575 },
        { "encodings.tis_620", 6832705, 2623 },
        { "encodings.undefined", 6835328, 2257 },
        { "encodings.unicode_escape", 6837585, 1845 },
        { "encodings.unicode_internal", 6839430, 1855 },
        { "encodings.utf_16", 6841285, 5229 },
        { "encodings.utf_16_be", 6846514, 1717 },
        { "encodings.utf_16_le", 6848231, 1717 },
        { "encodings.utf_32", 6849948, 5122 },
        { "encodings.utf_32_be", 6855070, 1610 },
        { "encodings.utf_32_le", 6856680, 1610 },
        { "encodings.utf_7", 6858290, 1638 },
        { "encodings.utf_8", 6859928, 1697 },
        { "encodings.utf_8_sig", 6861625, 4829 },
        { "encodings.uu_codec", 6866454, 3448 },
        { "encodings.zlib_codec", 6869902, 3309 },
        { "enum", 6873211, 16613 },
        { "functools", 6889824, 23610 },
        { "genericpath", 6913434, 3920 },
        { "heapq", 6917354, 15030 },
        { "importlib", 6932384, -3888 },
        { "importlib._bootstrap", 6936272, 31793 },
        { "importlib._bootstrap_external", 6968065, 41510 },
        { "importlib.machinery", 7009575, 1011 },
        { "inspect", 7010586, 84252 },
        { "io", 7094838, 3446 },
        { "keyword", 7098284, 1928 },
        { "linecache", 7100212, 4065 },
        { "locale", 7104277, 36519 },
        { "opcode", 7140796, 5673 },
        { "operator", 7146469, 14795 },
        { "os", 7161264, 31298 },
        { "posixpath", 7192562, 11123 },
        { "quopri", 7203685, 6374 },
        { "re", 7210059, 14440 },
        { "reprlib", 7224499, 5947 },
        { "sre_compile", 7230446, 10908 },
        { "sre_constants", 7241354, 5929 },
        { "sre_parse", 7247283, 22323 },
        { "stat", 7269606, 4150 },
        { "stringprep", 7273756, 12956 },
        { "struct", 7286712, 335 },
        { "threading", 7287047, 38884 },
        { "token", 7325931, 3661 },
        { "tokenize", 7329592, 20453 },
        { "traceback", 7350045, 20146 },
        { "types", 7370191, 8728 },
        { "warnings", 7378919, 13100 },
        { "weakref", 7392019, 20237 },
        { NULL, 0, 0 }
    };

    struct frozen_desc *current = frozen_modules;

    for(;;)
    {
        destination->name = (char *)current->name;
        destination->code = (unsigned char *)&constant_bin[ current->start ];
        destination->size = current->size;

        if (destination->name == NULL) break;

        current += 1;
        destination += 1;
    };
}
