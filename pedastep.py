#!/usr/bin/env python3

import json
import os.path as path
import re
import string

class Pedastep:
    def __init__(self):
        self._alpha = 'ءابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
        self._alphaSize = len(self._alpha)
        self._letterIndex = dict(
            (self._alpha[i], i) for i in range(len(self._alpha)) )
        self._endOfMessageSeq = 'پپپپ'

    def encrypt(self, metre, rhyme, text):
        text = self._clean_non_alpha_chars(text) + self._endOfMessageSeq
        rhyme = self._clean_non_alpha_chars(rhyme)
        metreSize = len(metre)
        rhymeSize = len(rhyme)
        encrypted = ','.join([str(i) for i in metre]) + '\n'
        for i in range(len(text)):
            skipCount = metre[i % metreSize]
            keyValue = self._letterIndex[rhyme[i % rhymeSize]]
            letterIndex = self._letterIndex[text[i]]
            encryptedLetterIndex = (keyValue + letterIndex) % self._alphaSize
            encryptedLetter = self._alpha[encryptedLetterIndex]
            for j in range(skipCount):
                encrypted += ' ,'
            encrypted += encryptedLetter
            encrypted += '\n' if (i + 1) % metreSize == 0 else ','
        
        encrypted.strip(', ')
        return encrypted

    def decrypt(self, metre, rhyme, encrypted):
        encrypted = self._clean_non_alpha_chars(encrypted)
        rhyme = self._clean_non_alpha_chars(rhyme)
        text = ''
        textIndex = 0
        metreSize = len(metre)
        rhymeSize = len(rhyme)
        encrypted = re.sub('.{2}' + rhyme, '', encrypted)
        encryptedSize = len(encrypted)
        eomSize = len(self._endOfMessageSeq)
        i = 0
        while i < encryptedSize:
            skipCount = metre[textIndex % metreSize]
            i += skipCount
            if i >= encryptedSize:
                break
            keyValue = self._letterIndex[rhyme[textIndex % rhymeSize]]
            encryptedLetterIndex = self._letterIndex[encrypted[i]]
            letterIndex = (encryptedLetterIndex - keyValue) % self._alphaSize
            letter = self._alpha[letterIndex]
            text += letter
            if text[-eomSize:] == self._endOfMessageSeq:
                text = text[:-eomSize]
                break
            i += 1
            textIndex += 1
        return text

    def _clean_non_alpha_chars(self, text):
        output = ''
        for ch in text:
            if ch in self._alpha: output += ch
            elif ch in 'ؤئإأ': output += 'ء'
            elif ch == 'ي': output += 'ی'
            elif ch == 'ة': output += 'ه'
            elif ch == 'آ': output += 'ا'
        return output

class PedastepIO:
    def __init__(self, metaDataFilePath):
        self._ped = Pedastep()
        self.parse_metadata(metaDataFilePath)

    def encrypt(self):
        with open(self._clearTextFilePath) as clearTextFile:
            clearText = clearTextFile.read()
        csv = self._ped.encrypt(self._metre, self._rhyme, clearText)
        with open(self._csvFilePath, 'w') as csvFile:
            csvFile.write(csv)

    def decrypt(self):
        with open(self._poemFilePath) as poemFile:
            poem = poemFile.read()
        decrypted = self._ped.decrypt(self._metre, self._rhyme, poem)
        with open(self._clearTextFilePath, 'w') as clearTextFile:
            clearTextFile.write(decrypted)

    def parse_metadata(self, metaDataFilePath):
        metaDataFilePath = path.abspath(metaDataFilePath)
        self._metaDataDirPath = path.split(metaDataFilePath)[0]
        if not self._metaDataDirPath:
            self._metaDataDirPath = os.getcwd()
        with open(metaDataFilePath) as metaDataFile:
            meta = json.load(metaDataFile)
            self._clearTextFilePath = self.abs_path_rel_to_meta_data(
                meta['clearTextFile'])
            self._csvFilePath = self.abs_path_rel_to_meta_data(meta['csvFile'])
            self._poemFilePath = self.abs_path_rel_to_meta_data(
                meta['poemFile'])
            self._metre = meta['metre']
            self._rhyme = meta['rhyme']

    def abs_path_rel_to_meta_data(self, p):
        if path.isabs(p):
            return p
        else:
            return path.normpath(path.join(self._metaDataDirPath, p))

def parse_pedastep_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Operation to perform. Possible values are "encrypt" and "decrypt"')
    parser.add_argument('meta', help='The JSON file containing the poem metadata (encryption and decryption parametres)')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_pedastep_args()
    pedIo = PedastepIO(args.meta)
    if args.command == 'encrypt':
        pedIo.encrypt()
    elif args.command == 'decrypt':
        pedIo.decrypt()
