#!/usr/bin/env python3

import argparse
import os
import pypdf

def read_existing_words(args):
    words_by_length = {}
    if not args.append:
        return words_by_length
    for dirpath, _, filenames in os.walk(args.outdir):
        for filename in filenames: 
            try:
                l = int(filename.removesuffix('.' + args.outfile_extension).removeprefix(args.outfile_basename + '-'))
                words_by_length[l] = { l.strip() for l in open(os.path.join(dirpath, filename)).readlines() }
            except Exception as e:
                print(f'Error when reading file {dirpath}/{filename}: {e}')
                continue
    return words_by_length

def main(args):
    os.makedirs(args.outdir, exist_ok=True)
    words_by_length = read_existing_words(args)
    reader = pypdf.PdfReader(args.input)
    for page in reader.pages:
        for w in page.extract_text().split():
            w = ''.join([ l for l in w if l.isalpha() ])
            l = len(w)
            if l == 0:
                continue
            if l not in words_by_length:
                words_by_length[l] = set()
            words_by_length[l].add(w[::-1] if args.reverse else w)
    for length, words in words_by_length.items():
        with open(f'{args.outdir}/{args.outfile_basename}-{length}.{args.outfile_extension}', 'w') as output:
            output.write('\n'.join(sorted(words)))

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        "Extract all the words from a PDF into multiple sorted lists of words. "
        "Each list contains words of the same length")
    parser.add_argument('input', help='Input PDF file')
    parser.add_argument('outdir', help='Output file with each line containing one word', default='wordlist.txt')
    parser.add_argument('-b', '--outfile-basename', default='words',
                        help='Basename for each of the files containing one of the word lists. The file name will be '
                        'made up the length of each word in the contained list concatenated to this base.')
    parser.add_argument('-x', '--outfile-extension', default='txt',
                        help='File name extension for each of the word list files')
    parser.add_argument('-a', '--append', default=True, action='store_true',
                        help='Whether the new word from the PDF should be added to the existing list')
    parser.add_argument('-r', '--reverse', default=False, action='store_true',
                        help='Reverse each of the words after reading')
    return parser.parse_args()

if __name__ == "__main__":
    main(parse_args())
