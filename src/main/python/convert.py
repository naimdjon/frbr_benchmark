import fnmatch
import getopt
import os
import sys
from subprocess import call

conversion_xslt = "conversion.xslt"

def main(argv):
    classpath = os.getenv('CLASSPATH', 'lib/saxon.9.1.0.8.jar')
    make_xslt = "http://dijon.idi.ntnu.no/exist/rest/db/frbrizer/xsl/make.xslt"
    #rules_xslt = "http://dijon.idi.ntnu.no/exist/rest/db/norbok/rules/norbok.rules.xml"
    #rules_xslt = "http://dijon.idi.ntnu.no/exist/rest/db/data/rules/marc21.to.rda.xml"
    #rules_xslt = "http://dijon.idi.ntnu.no/exist/rest/db/data/rules/bib-r.enhanced.rules.xml"
    rules_xslt = "http://dijon.idi.ntnu.no/exist/rest/db/data/rules/bib-r.baseline.rules.xml"
    input = os.path.join(os.path.expanduser("~"), 'Downloads/dataset_5/')
    output = "output"
    filter = '*marc21.xml'
    clean = False
    try:
        opts, args = getopt.getopt(argv, 'cp:i:o:c')
    except getopt.GetoptError:
        print 'convert.py -i <input_dir|file> -o <output_dir|file>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'convert.py -i <input_dir|file> -o <output_dir|file>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input = arg
        elif opt in ("-o", "--ofile"):
            output = arg
        elif opt in ("-c", "--clean"):
            clean = True
    if clean:
        clean_converted_files(input)
    print 'classpath:', classpath
    print 'conversion_xslt:', conversion_xslt
    print 'make_xslt:', make_xslt
    print 'rules_xslt:', rules_xslt
    print 'input:', input
    print 'output:', output
    print '---------------------'
    print "Creating xslt conversion"
    check_classpath(classpath)

    call(["java", "-cp", classpath, "net.sf.saxon.Transform"
             , "-u"
             , "-s:" + rules_xslt
             , "-xsl:" + make_xslt
             , "-o:" + conversion_xslt])

    print "Running transformation"
    if os.path.isdir(input):
        for path, subdirs, files in os.walk(input):
            for file in files:
                abs_path = os.path.join(path, file)
                convert_file(abs_path, classpath, file, filter, path)
    else:
        convert_file(input, classpath, os.path.basename(input), filter, os.path.dirname(input))

def convert_file(abs_path, classpath, file, filter, path):
    print "converting a single file"
    if fnmatch.fnmatch(file, filter) and 'CONVERTED-' not in file:
        output_file = os.path.join(path, 'CONVERTED-' + file)
        print 'converting ', abs_path, " => ", output_file

        call(["java", "-cp", classpath, "net.sf.saxon.Transform"
                 , "-s:" + abs_path
                 , "-xsl:" + conversion_xslt
                 , "-o:" + output_file])



def check_classpath(classpath):
    if not os.path.isfile(classpath):
        print 'class path is not set correctly, ', classpath, ' does not exist'
        sys.exit(2)


def clean_converted_files(input):
    for path, subdirs, files in os.walk(input):
        for file in files:
            if 'CONVERTED-' in file:
                print 'removing file ', file
                os.remove(os.path.join(path, file))
    os.remove(conversion_xslt)
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
