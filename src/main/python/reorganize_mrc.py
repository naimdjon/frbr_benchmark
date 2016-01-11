import os
import sys
from os.path import dirname


def main(argv):
    if argv.__len__() != 2:
        print "Usage reorganize_mrc <dataset_t42> <mrc_files>"
        sys.exit(1)
    if os.path.isdir(argv[0]):
        for path, subdirs, files in os.walk(argv[0]):
            # noinspection SpellCheckingInspection
            for ffile in files:
                if 'marc21.xml' in ffile:
                    mrc_file = os.path.join(argv[1], ffile.replace(".xml", ".mrc"))
                    if os.path.isfile(mrc_file):
                        parent = dirname(path)
                        copy_to_dir = os.path.join(os.path.abspath(os.path.join(mrc_file, os.pardir)), os.path.basename(
                                parent), os.path.basename(path))
                        os.makedirs(copy_to_dir)
                        os.rename(mrc_file, os.path.join(copy_to_dir, os.path.basename(
                                mrc_file)))
                    else:
                        print "NOT FOUND", mrc_file


if __name__ == "__main__":
    main(sys.argv[1:])
