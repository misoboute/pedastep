# pedastep
Persian Dada Steganographic Poetry utility creates templates to
steganographically wrap a Persian piece of text message into a piece of classic
Persian poetry.

When steganizing a piece of text, you provide the destination poem _rhyme_ and
_metre_ in a metadata file. The metadata file contains a simple JSON object
that specifies destination poem rhyme, metre, poem file path, 
clear text file path, and the intermediate CSV file path. Then invoke the 
`pedastep` script like the example below:

```sh
$ python3 pedastep.py encrypt metadat/001.json
```

The encryption part of the utility uses the rhyme as the rotating encryption
key. It then uses the metre values to inflate the encrypted message by adding
corresponding numbers of spaces between the encrypted letters. This is then
written to the intermediate CSV file. The CSV file contains sequences of 
letters and spaces. You will need to open the CSV file in your editor of 
choice (LibreOffice Calc, Microsoft Excel, Apple Numbers...) and
replace the spaces with letters in such a way that it can be recited as a piece
of poetry with the same rhyme and metre. Remember that you can only replace
the spaces. If you change any of the letters that the encryption step has
produced you will change the encrypted message and will not be able to decrypt
the original message afterwards from the final poem. The letters in the rhyme
plus their two preceding letters do not fill any of the spaces in the CSV file.
The rhyme is added where required without being constrained by the letters in 
the CSV.

You can place the finished piece of poetry in a separate file from the CSV as
plain text so that it can be later decrypted using the same utility.

To decrypt a message previously encrypted using pedastep, create a metadata 
file (the same json object with values for poem file path, metre, rhyme,
and clear text file path) and invoke the `pedastep` script like the example below:

```sh
$ python3 pedastep.py decrypt metadata/001.json
```
