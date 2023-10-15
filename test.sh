#!/bin/bash

# python translater.py <input_file> <width> <height> <split_width> <split_height> <ratio> <output_file>
# input_file = asset/ferris.raw
# width = 86
# height = 64
# split_width = 86
# split_height = 64
# ratio = 4, which means output_width = 86 * 4 = 344, output_height = 64 * 4 = 256
# output_file = out/test
python translater.py asset/ferris.raw 86 64 86 64 4 out/test
