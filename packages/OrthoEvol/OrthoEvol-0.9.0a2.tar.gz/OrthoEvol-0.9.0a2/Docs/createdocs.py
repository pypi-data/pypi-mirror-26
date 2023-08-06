#from shutil import copyfile
#import os
#from os.path import join
#
#try:
#    import pypandoc
#except Exception:
#    from pypandoc.pandoc_download import download_pandoc
#    download_pandoc()
#
#from OrthoEvol.Tools.logit import LogIt
#
#
#class PandocConverter(object):
#    """Convert files using the pypandoc wrapper.
#
#    :param infile:  path to the input file
#    :param outfile_path:  output path
#    """
#    def __init__(self, infile, outfile_path):
#        self.infile = infile
#        self.outfile_path = outfile_path
#        self.pandoc_log = LogIt().default('pandoc converter', None)
#        self.md2rst()
#
#    def md2rst(self):
#        infile = str(self.infile)
#        filepath, ext = infile.split('.')
#        splitfilepath = filepath.split(os.sep)
#        initial_filename = splitfilepath[-1]
#        final_filename = str(splitfilepath[-2] + initial_filename).lower()
#        outfile = join(self.outfile_path, final_filename + ".rst")
#        if ext == 'md':
#            pypandoc.convert_file(infile, 'rst',  outputfile=outfile)
#            self.pandoc_log.info('%s.md converted to %s.rst.' %
#                                 (infile, final_filename))
#        else:
#            self.pandoc_log.error('%s not supported by this function.' % ext)
#
#
#class CreateDocs(object):
#    def __init__(self):
#        """"Initialize this class."""
#        self.createdocs_log = LogIt().default('create docs', None)
#        self.current_dir = os.path.dirname(os.path.realpath(__file__))
#        self._docsdir = os.path.join(self.current_dir, 'docs')
#        self.up = '..'
#        self.docs_source = os.path.join(self._docsdir, 'source')
#        self.main_readme = self._pathtomainreadme()
#        self.readme2index()
#        self.packagename = 'OrthoEvol'
#        self.convertfiles()
#
#    def _append_toc_info(self):
#        """Write TOC info to the README.rst when copied as index.rst."""
#        tocinfo = "\nContents\n" \
#            "--------\n"\
#            ".. toctree::\n    " \
#            ":hidden:\n    " \
#            ":maxdepth: 3\n\n    " \
#            "orthoevolreadme\n    cookiesreadme\n    managerreadme\n    " \
#            "orthologsreadme\n    pipelinereadme\n    toolsreadme\n" \
#            "\nIndices and tables\n" \
#            "==================\n" \
#            "* :ref:`genindex`\n" \
#            "* :ref:`modindex`\n" \
#            "* :ref:`search`"
#
#        return tocinfo
#
#    def readme2index(self):
#        """Copy README.rst from the top level of your repo to docs source."""
#        indexpath = os.path.join(self.docs_source, 'index.rst')
#        copyfile(self.main_readme, indexpath)
#        log_msg = '%s copied to %s.' % (self.main_readme, indexpath)
#        self.createdocs_log.info(log_msg)
#
#        with open(indexpath, 'a') as index:
#            toctree = self._append_toc_info()
#            index.write(toctree)
#            index.close()
#            self.createdocs_log.info('TOC written to index.rst')
#
#    def _pathtomainreadme(self):
#        """Return the path to the main README.rst."""
#        os.chdir(self.current_dir)
#        os.chdir(self.up)
#        readmedir = os.getcwd()
#        main_readme = os.path.join(readmedir, 'README.rst')
#        os.chdir(self.current_dir)
#        return main_readme
#
#    def getfiles2convert(self):
#        """Get a list of files to convert."""
#        os.chdir(self.current_dir)
#        os.chdir(self.up)
#        datasnakesdir = os.path.join(os.getcwd(), self.packagename)
#
#        # Skip these folders when looking for README.md
#        # Most of these are folders in the cookiecutter repository
#        skip = ['new_basic_project', 'new_repository', 'new_database_repo',
#                'index', 'new_research', 'new_user', 'web', 'data',
#                'new_website', 'config', 'utils']
#
#        files2convert = []
#
#        # Use os.walk to walk from the datasnakes/package directory and down
#        # to find README.md files in each main submodule.
#        for dirname, subdirlist, filelist in os.walk(datasnakesdir):
#            subdirlist[:] = [d for d in subdirlist if d not in skip]
#            for filename in filelist:
#                if filename == 'README.md':
#                    file = os.path.join(dirname, filename)
#                    files2convert.append(file)
#
#        return files2convert
#
#    def convertfiles(self):
#        """Convert a list of files from .md to .rst."""
#        files2convert = self.getfiles2convert()
#        for file2convert in files2convert:
#            PandocConverter(file2convert, self.docs_source)
#        self.createdocs_log.info('Your docs were converted to .rst format.')
#
#
#if __name__ == "__main__":
#    CreateDocs()
