import sys

# https://en.wikipedia.org/wiki/BMP_file_format
# starting location of pixel array is f[10:14], bit depth in f[28:30], little-endian

def little_endian_range_to_int(group):
    return int(''.join(f'{bin(d)[2:]:>08}' for d in group[::-1]), 2) # per spec
    
def int_to_little_endian_range(number, bits):
    group = bin(number)[2:]
    group = '0' * (bits-len(group)) + group
    return [int(group[n:n+8], 2) for n in range(0, len(group)-1, 8)][::-1]

input_file = sys.argv[1]
output_file = sys.argv[2]
fg_color = sys.argv[3]
fg_colors = int(fg_color[4:], 16), int(fg_color[2:4], 16), int(fg_color[0:2], 16) # reversed for little-endian
bg_color = sys.argv[4]
bg_colors = int(bg_color[4:], 16), int(bg_color[2:4], 16), int(bg_color[0:2], 16) # reversed for little-endian

with open(input_file, 'rb') as f:
    f = f.read()

img_data_start = little_endian_range_to_int(f[10:14])
bit_depth = little_endian_range_to_int(f[28:30])
bits_per_channel = 8
channels = bit_depth // bits_per_channel
pix_width = little_endian_range_to_int(f[18:22])
filesize = little_endian_range_to_int(f[2:6])

if channels == 3: # create list and add alpha channel
    padding = pix_width * 3 % 4 # remainder
    padding = padding and 4 - padding # remainder to padding, 0 is okay
    lf = list(f)
    if padding:
        for rowstart in range(len(f) - pix_width*3 - padding, img_data_start-1, -(pix_width*3 + padding)):
            del lf[rowstart + pix_width*3 : rowstart + pix_width*3 + padding] # remove padding
    lf = lf[:img_data_start] + [item for r in range(img_data_start, len(lf)-1, 3) for item in (lf[r],lf[r+1],lf[r+2],255)] # add alpha channel
    lf[28:30] = int_to_little_endian_range(32, bits=16) # bpp
    lf[2:6] = int_to_little_endian_range(len(lf), bits=32) # file size
    lf[34:38] = int_to_little_endian_range(len(lf)-img_data_start, bits=32) # image data size
elif channels == 4: # alpha channel already exists
    lf = list(f)
else:
    input('Input must be 24-bit RGB or 32-bit RGBA. Press Enter to exit.')
    sys.exit()

for i in range(img_data_start, len(lf)-1, 4):
    b,g,r,opacity = lf[i:i+4] # BGR instead of RGB because little-endian
    determinant = int(
                        (
                            (r+g+b - sum(fg_colors)) / (sum(bg_colors) - sum(fg_colors))
                        ) * 255
                    )
    lf[i+3] = max(0, min(255 - determinant, 255))
    if lf[i+3]: # if there's any opacity
        if determinant >= 0:
            colors = fg_colors # already reversed on creation, for little-endian
        else: # use current color if it's even darker than fg
            colors = b,g,r # BGR instead of RGB because little-endian
    else:
        colors = bg_colors
    lf[i:i+3] = colors

with open(output_file, 'wb') as output:
    output.write(bytearray(lf))