# pedastep
Persian Dada Steganographic Poetry utility creates templates to
steganographically wrap a Persian piece of text message into a piece of classic
Persian poetry.

When steganizing a piece of text, you provide the destination poem _rhyme_ and
_metre_ in a metadata file. The metadata file contains a simple JSON object
that specifies destination poem rhyme, metre, destination poem file, source 
clear text file, and the intermediate CSV file.

The encryption part of the utility uses the rhyme as the rotating encryption
key. It then uses the metre values to inflate the encrypted message by adding
corresponding numbers of spaces between the encrypted letters. This is then
written to the intermediate CSV file.

At this time, you will need to open the CSV file in your editor of choice and
replace the spaces with letters in such a way that it can be recited as a piece
of poetry with the same rhyme and metre. The letters in the rhyme plus their two
preceding letters do not fill any of the spaces in the CSV file. The rhyme 
is added where required without being constrained by the letters in the CSV.

You can place the finished piece of poetry in a separate file from the CSV as
plain text so that it can be later decrypted using the same utility.

The decryption part has not been implemented yet.
