from struct import pack, unpack, calcsize, iter_unpack
from sys import argv, byteorder

def main():
    if len(argv) != 9:
        print("Invalid number of arguments: " + str(len(argv) - 1), "expected 7")
        print("Usage: python translater.py <input_file> <original_width> <original_height> <screen_width> <screen_height> <split_width_num> <split_height_num> <output_file>")
        return

    input_file = argv[1]
    original_width = int(argv[2])
    original_height = int(argv[3])
    screen_width = int(argv[4])
    screen_height = int(argv[5])
    split_width_num = int(argv[6])
    split_height_num = int(argv[7])
    output_file = argv[8]

    with open(input_file, "rb") as f:
        data = f.read()
        # data is rgb565
        # so each pixel is 2 bytes
        # the total number of pixels is width * height
        # the total number of bytes is width * height * 2
        # the total number of bytes is len(data)
        if len(data) != original_width * original_height * 2:
            print("Invalid file size")
            return

        target_width = screen_width * split_width_num
        target_height = screen_height * split_height_num

        # zoom in
        data = zoom_int(data, original_width, original_height, target_width, target_height)


        with open(output_file + "_zoom.raw", "wb") as f:
            f.write(data)

        # split
        chunks = split(data, target_width, target_height, split_width_num, split_height_num)

        assert(len(chunks) == split_width_num * split_height_num)

        # write to files
        for i in range(split_height_num):
            for j in range(split_width_num):
                with open(output_file + "_" + str(j) + "_" + str(i) + ".raw", "wb") as f:
                    f.write(chunks[(split_height_num - i - 1) * split_width_num + j])


def add_padding(data, width, height, target_width, target_height):
    extra_width = target_width - width
    extra_height = target_height - height
    extra_data = bytearray(extra_width * extra_height * 2)

    # iterate through the extra data
    for i in range(extra_height):
        for j in range(extra_width):
            index = (i * extra_width + j) * 2
            extra_data[index:index + 2] = b'\x00\x00'

    # add the extra data to the original data
    data += extra_data

    return data



def zoom_int(data, original_width: int, original_height: int, target_width: int, target_height: int):
    ratio = calculate_ratio(original_width, original_height, target_width, target_height)
    padding_width, padding_height = calculate_padding(original_width, original_height, target_width, target_height, ratio)

    extra_width = int(original_width * ratio)
    extra_height = int(original_height * ratio)

    extra_data = bytearray((extra_width + padding_width) * (extra_height + padding_height) * 2)

    # iterate through the extra data
    for i in range(padding_height//2, extra_height + padding_height//2):
        original_i = (i - padding_height//2) // ratio
        for j in range(padding_width//2, extra_width + padding_width//2):
            # find the corresponding pixel in the original data
            original_j = (j - padding_width//2) // ratio
            index = (i * (extra_width + padding_width) + j) * 2
            original_index = (original_i * original_width + original_j) * 2
            extra_data[index:index + 2] = data[original_index:original_index + 2]

    return extra_data

def calculate_padding(original_width: int, original_height: int, target_width: int, target_height: int, ratio: int) -> tuple[int, int]:
    return (target_width - original_width * ratio, target_height - original_height * ratio)

def calculate_ratio(original_width: int, original_height: int, target_width: int, target_height: int) -> int:
    return min(target_width // original_width, target_height // original_height)

def split(data, target_width, target_height, split_width_num, split_height_num):
# def split(data, width, height, split_width, split_height):
    # check if width and height are divisible by split_width and split_height
    assert(target_width % split_width_num == 0)
    assert(target_height % split_height_num == 0)

    chunk_width = target_width // split_width_num
    chunk_height = target_height // split_height_num

    # split the data into chunks
    chunks = []
    # rgb565 has 2 bytes per pixel
    chunk_size = chunk_width * chunk_height * 2
    for i in range(split_height_num):
        for j in range(split_width_num):
            chunks.append(bytearray(chunk_size))

    for i in range(target_height):
        chunks_i = i // chunk_height
        chunk_i = i % chunk_height

        original_i = i 

        for j in range(split_width_num):
            chunks_j = j
            chunk_j = 0

            original_j = j * chunk_width

            chunks_index = chunks_i * split_width_num + chunks_j
            chunk_index = (chunk_i * chunk_width + chunk_j) * 2

            original_index = (original_i * target_width + original_j) * 2

            chunks[chunks_index][chunk_index:chunk_index + chunk_width * 2] = data[original_index:original_index + chunk_width * 2]

    return chunks

if __name__ == "__main__":
    main()

