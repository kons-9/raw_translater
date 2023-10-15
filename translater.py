from struct import pack, unpack, calcsize, iter_unpack
from sys import argv, byteorder

def main():
    if len(argv) != 8:
        print("Invalid number of arguments: " + str(len(argv) - 1), "expected 7")
        print("Usage: python translater.py <input_file> <width> <height> <split_width> <split_height> <ratio> <output_file>")
        return

    input_file = argv[1]
    width = int(argv[2])
    height = int(argv[3])
    split_width = int(argv[4])
    split_height = int(argv[5])
    ratio = int(argv[6])
    output_file = argv[7]

    with open(input_file, "rb") as f:
        data = f.read()
        # data is rgb565
        # so each pixel is 2 bytes
        # the total number of pixels is width * height
        # the total number of bytes is width * height * 2
        # the total number of bytes is len(data)
        if len(data) != width * height * 2:
            print("Invalid file size")
            return

        # zoom in
        data = zoom_int(data, width, height, ratio)

        with open(output_file + "_zoom.raw", "wb") as f:
            f.write(data)

        width *= ratio
        height *= ratio

        # split
        chunks = split(data, width, height, split_width, split_height)

        # write to files
        for i in range(len(chunks)):
            with open(output_file + str(i) + ".raw", "wb") as f:
                f.write(chunks[i])

def zoom_int(data, width, height, ratio):
    extra_width = int(width * ratio)
    extra_height = int(height * ratio)
    extra_data = bytearray(extra_width * extra_height * 2)

    # iterate through the extra data
    for i in range(extra_height):
        for j in range(extra_width):
            # find the corresponding pixel in the original data
            original_i = i // ratio
            original_j = j // ratio
            index = (i * extra_width + j) * 2
            original_index = (original_i * width + original_j) * 2
            extra_data[index:index + 2] = data[original_index:original_index + 2]

    return extra_data

def split(data, width, height, split_width, split_height):
    # check if width and height are divisible by split_width and split_height
    if width % split_width != 0:
        print("Width is not divisible by split_width")
        return
    if height % split_height != 0:
        print("Height is not divisible by split_height")
        return

    width_chunks = width // split_width
    height_chunks = height // split_height

    # split the data into chunks
    chunks = []
    for i in range(height_chunks):
        index = i * split_height * width
        for j in range(width_chunks):
            chunks.append(data[index:index + split_width * split_height])
            index += split_width

    return chunks

if __name__ == "__main__":
    main()

