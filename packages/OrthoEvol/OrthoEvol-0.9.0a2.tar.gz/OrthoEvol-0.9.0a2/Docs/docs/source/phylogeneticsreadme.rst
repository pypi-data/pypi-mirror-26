Phylogenetics Documentation
===========================

This documentation will provide information and guidelines about how we
use the Phylogenetics modules related to this package.

Overview
--------

Phylogenetics is best defined as the study of evolutionary relationships
among biological entities. In our case, those entities are species. We
are seeking to learn how mammals (more specifically primates) compare to
each other given a group of genes (GPCRs and addiction related).

PAML in particular is the best software for helping us to understand the
potentially significant differences in genes across different mammalian
species. From there, we can decide which genes we will further study in
cell culture projects or assays.

Examples
--------

In the beginning stages of our project, we tested various phylogenetic
programs to see which worked well for us.

In this module, we include classes and ways to use PAML, Phylip, PhyML,
IQTREE, and Biopython's Bio.Phylo class.

Example using PhyML and RelaxPhylip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from OrthoEvol.Orthologs import Phylogenetics

    # Find out what subclasses are available for use
    dir(Phylogenetics)

    Out[1]:
    ['AlignIO',
     'ETE3PAML',
     'IQTree',
     'IQTreeCommandline',
     'OrthologsWarning',
     'PAML',
     'PhyML',
     'Phylip',
     'PhyloTree',
     'RelaxPhylip',
     'TreeViz',
     '__all__',
     '__builtins__',
     '__cached__',
     '__doc__',
     '__file__',
     '__loader__',
     '__name__',
     '__package__',
     '__path__',
     '__spec__',
     'warnings']

    # Now you can import a class you want to utilize
    from OrthoEvol.Orthologs.Phylogenetics import PhyML, RelaxPhylip

    RelaxPhylip("HTR1A_aligned.fasta", "HTR1A_aligned.phy")

    # Generate a maximum likelihood tree from the phylip formatted alignment file.
    PhyML("HTR1A_aligned.phy")


