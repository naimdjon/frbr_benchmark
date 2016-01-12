import os
import sys
from subprocess import call


def main(argv):
    vfrbr_persist = "/data/vfrbr/vfrbr-persist"
    vfrbr_frbrize_marc = "/data/vfrbr/vfrbr-frbrize-marc"
    vfrbr_export = "/data/vfrbr/vfrbr-export"
    sql = os.path.join(vfrbr_persist, "src/main/resources/sql/ddl")
    print sql
    if argv.__len__() != 1:
        print "Usage rerun_experiments <mrc_files>"
        sys.exit(1)
    for path, subdirs, files in os.walk(argv[0]):
        for ffile in files:
            print "processing ", os.path.abspath(path), ",", ffile
            print "recreating DB schema..."
            call(["bash", "script-recreate.sql"], cwd=sql)
            call(["bash", "batch-load.sh", "-Dmarc_data_path=" + os.path.abspath(path)], cwd=vfrbr_frbrize_marc)
            call(["bash", "rdf-export.sh", "-Dexport.path=" + os.path.abspath(path)], cwd=vfrbr_export)


if __name__ == "__main__":
    main(sys.argv[1:])
