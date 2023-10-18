#!/bin/bash

# python translater.py <input_file> <original_width> <original_height> <screen_width> <screen_height> <split_width_num> <split_height_num> <output_file>")
#
# <input_file>         : asset/ferris.raw
# <original_width>     : 86
# <original_height>    : 64
# <screen_width>       : 128
# <screen_height>      : 128
# <split_width_num>    : 4
# <split_height_num>   : 4
# <output_file>        : out/test
#
mkdir -p out
python3.10 translater.py asset/acm.raw 480 480 128 128 4 4 out/test_acm
