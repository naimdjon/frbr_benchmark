import sys
import os

def main(argv):
    vfrbr_persist="/data/vfrbr/vfrbr-persist"
    vfrbr_frbrize_marc="/data/vfrbr/vfrbr-frbrize-marc"
    if argv.__len__() != 1:
        print "Usage rerun_experiments <mrc_files>"
        sys.exit(1)
    for path, subdirs, files in os.walk(argv[0]):
        for ffile in files:
            print os.path.abspath(path)


if __name__ == "__main__":
    main(sys.argv[1:])
