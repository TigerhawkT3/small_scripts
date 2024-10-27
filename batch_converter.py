from multiprocessing.pool import ThreadPool
import subprocess
import argparse
import glob
import os

parser = argparse.ArgumentParser(prog='Batch converter',
    description='Run a converter in parallel.',
    formatter_class=argparse.RawTextHelpFormatter,
    epilog='''Convert images in .\\vacation\\images to JXL in place:
  py batch_converter.py .\\vacation\\images "cjxl -j 0 -d 1" jxl -s png -s jpg jpeg -r -X -v 0
Convert videos with basename collisions in .\\vacation\\movies to a cloned directory,
hiding all of FFmpeg's console output:
  py batch_converter.py .\\vacation\\movies "ffmpeg -i" mp4 -s mov 3gpp `
  -c .\\vacation\\backup -v 3 -o="-c:v libx264 -crf 22 -c:a libopus -b:a 64k" -w 1 2>NUL
Convert some PNG images to WebP in place:
  py batch_converter.py gallery "cwebp -z 6" webp -s png -r -X -v 1 -o=-o
''')
parser.add_argument('directory', help='Source directory containing your files.') # C:\images
parser.add_argument('command', help='The conversion program to run, including options.') # "cjxl -j 0 -d 1"
parser.add_argument('target_extension', help='The file type extension to add to output files.') # jxl
parser.add_argument('-o', '--output-switch', default='',
    help='Any options inserted before the output name. Use = to start with -, e.g. -o=-o or -o=\'-c:v libx264\'.')
    # -o="-o" (when the output needs a switch, viz cwebp)
parser.add_argument('-w', '--workers', type=int, default=4, help='Number of simultaneous CPU workers.') # 4
parser.add_argument('-s', '--source-extensions', action='extend', nargs='+',
    help='File type extentions to convert (no leading period, case-insensitive).') # -s png -s jpg jpeg
# to get image.jxl instead of image.png.jxl
parser.add_argument('-r', '--replace-extension', action='store_true',
    help='Replace the file\'s original extension with the new one instead of simply appending.')
parser.add_argument('-X', '--delete-originals', action='store_true',
    help='Delete source files after conversion. Use with caution.') # delete original file, use caution
# save output files to specified directory instead of original, cloning original directory structure:
parser.add_argument('-c', '--clone', default='',
    help='Save converted files to a separate directory that will mirror the source directory\'s structure.')
# verbosity: 0 no output, 1 % \r, 2 x/y \r, 3 x/y filename.png \r, 4 x/y filename.png
parser.add_argument('-v', '--verbosity', type=int, default=3, help=('''\
0: Add no output.
1: Display percentage completion.
2: Display completion as a fraction.
3: Same as above, plus latest input file converted.
4: Same as above, on separate lines instead of updating a single line.'''))
args = parser.parse_args()
if args.directory.startswith('.\\'):
    args.directory = args.directory[2:]
if args.clone:
    args.clone = os.path.abspath(args.clone.strip('\\/'))
if args.clone.startswith('.\\'):
    args.clone = args.clone[2:]
args.directory = os.path.abspath(args.directory.strip('\\/'))
args.source_extensions = set(args.source_extensions)

# py batch_convert.py C:\images "cjxl -d 0" jxl -s png -s jpg jpeg -w 4
# py batch_convert.py C:\images "cwebp -z 6" webp -s png -o "-o" -w 4 -c D:\backup\images

clone = '''if (!(Test-Path -LiteralPath @"
{clone}
"@ `
)) {{
mkdir @"
{clone}
"@ `
'''
if args.verbosity < 4:
    clone += '| Out-Null '
clone += '''}}
'''
template = '''{command} @"
{inp}
"@ `
{output_switch} @"
{outp}
"@;
if ($?) {{ '''
delete_originals = '''rm -LiteralPath @"
{inp}
"@
'''
verbosity_update = '''write-host -NoNewLine @"
`r$(' '*($Host.UI.RawUI.WindowSize.Width-1))`r{status}
"@ `
 '''
verbosity_persist = '''write-host @"
{status}
"@ `
'''
end_template = '''
}}'''

if args.clone:
    template = clone + template
if args.delete_originals:
    template += delete_originals
if 1 <= args.verbosity < 4:
    template += verbosity_update
elif args.verbosity == 4:
    template += verbosity_persist
template += end_template

# adapted from https://stackoverflow.com/a/26783779/2617068
def work(inp, outp, status):
    command = template.format(
        command=args.command,
        inp=inp,
        outp=outp,
        output_switch=args.output_switch,
        clone=os.path.dirname(outp),
        status=status)
    result = subprocess.run(('powershell', '-noprofile', '-command', command))

tp = ThreadPool(args.workers)

files = [(base,ext.lstrip('.')) for base,ext in map(os.path.splitext,
            glob.iglob(os.path.join(args.directory, '**', '*.*'), recursive=True))
                if ext.lower().lstrip('.') in args.source_extensions]
num_files = len(files)

for idx,(base, ext) in enumerate(files, start=1):
    inp = base + f'.{ext}'
    outp = (os.path.join(args.clone,
                         base[len(args.directory)+1:])
                     if args.clone else base
            ) + ('' if args.replace_extension else f'.{ext}'
            ) + f'.{args.target_extension}'
    status = ('', # level 0
              f'{round(100*idx/len(files), 2)}%',
              f'{idx}/{num_files}',
              f'{idx}/{num_files} {base}.{ext}',
              f'{idx}/{num_files} {base}.{ext}')[args.verbosity]
    tp.apply_async(work, (inp, outp, status))

tp.close()
tp.join()
