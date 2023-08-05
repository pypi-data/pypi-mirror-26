fastq-anonymous
===============

Change the sequence and identifier of a fastq file to enable sharing of
confidential information for troubleshooting

USAGE
-----

| Reads from stdin and writes to stdout. Sequences are by default
  replaced by random nucleotides.
| Fastq identifiers and description are also anonymized.
| Read lengths and quality strings are preserverd.

::

    optional arguments:
      -h, --help     show this help message and exit
      -v, --version  Print version and exit.
      -m, --mask     Mask all nucleotides using N

EXAMPLES
--------

.. code:: bash

    cat reads.fastq.gz | fastq-anonymous > anonymous_reads.fastq

    gunzip -c reads.fastq.gz | fastq-anonymous > anonymous_reads.fastq

    gunzip -c reads.fastq.gz | fastq-anonymous | gzip > anonymous_reads.fastq.gz
