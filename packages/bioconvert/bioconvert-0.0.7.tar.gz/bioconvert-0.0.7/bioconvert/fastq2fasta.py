from Bio import SeqIO
from Bio.SeqIO import FastaIO
from bioconvert import ConvBase
# try:
#     # Let us make this optional for now because
#     # GATB cannot be install on RTD
#     from gatb import Bank
# except:
#     pass
from mappy import fastx_read


class Fastq2Fasta(ConvBase):
    """
    Convert :term:`FASTQ` to :term:`FASTA`
    """

    input_ext = ['.fastq', '.fq']
    output_ext = '.fasta'

    @staticmethod
    def just_name(record):
        """
        This method takes a Biopython sequence record *record*
        and returns its name. The comment part is not included.
        """
        return record.id

    @staticmethod
    def unwrap_fasta(infile, outfile, strip_comment=False):
        """
        This method reads fasta sequences from *infile*
        and writes them unwrapped in *outfile*.
        :param str infile: The path to the input FASTA file.
        :param str outfile: The path to the output file.
        """
        with open(outfile, "w") as fasta_out:
            if strip_comment:
                FastaIO.FastaWriter(
                    fasta_out,
                    wrap=None,
                    record2title=Fastq2Fasta.just_name).write_file(
                        SeqIO.parse(infile, 'fasta'))
            else:
                FastaIO.FastaWriter(fasta_out, wrap=None).write_file(
                    SeqIO.parse(infile, 'fasta'))

    # Adapted from the readfq code by Heng Li
    # (https://raw.githubusercontent.com/lh3/readfq/master/readfq.py)
    @staticmethod
    def readfq(fp):  # this is a generator function
        last = None  # this is a buffer keeping the last unprocessed line
        while True:  # mimic closure; is it a bad idea?
            if not last:  # the first record or a record following a fastq
                for l in fp:  # search for the start of the next record
                    if l[0] == "@":  # fastq header line
                        last = l[:-1]  # save this line
                        break
            if not last:
                break
            header, seqs, last = last[1:], [], None
            for l in fp:  # read the sequence
                if l[0] in '@+':
                    last = l[:-1]
                    break
                seqs.append(l[:-1])
            seq, leng, seqs = ''.join(seqs), 0, []
            for l in fp:  # read the quality
                seqs.append(l[:-1])
                leng += len(l) - 1
                if leng >= len(seq):  # have read enough quality
                    last = None
                    yield header, seq, ''.join(seqs)  # yield a fastq record
                    break

    def __init__(self, infile, outfile):
        """
        :param str infile: The path to the input FASTA file.
        :param str outfile: The path to the output file.
        """
        super().__init__(infile, outfile)
        # use readfq for now because pure python and fast enough
        # for production, could use seqtk which seems the fastest method
        self._default_method = "readfq"

    def _method_biopython(self, *args, **kwargs):
        records = SeqIO.parse(self.infile, 'fastq')
        SeqIO.write(records, self.outfile, 'fasta')

    def _method_seqtk(self, *args, **kwargs):
        cmd = "seqtk seq -A {} > {}".format(self.infile, self.outfile)
        self.execute(cmd)

#     def _method_GATB(self, *args, **kwargs):
#         with open(self.outfile, "w") as fasta:
#             for record in Bank(self.infile):
#                 fasta.write(">{}\n{}\n".format(
#                     record.comment.decode("utf-8"),
#                     record.sequence.decode("utf-8")))

    def _method_readfq(self, *args, **kwargs):
        with open(self.outfile, "w") as fasta, open(self.infile, "r") as fastq:
            for (name, seq, _) in Fastq2Fasta.readfq(fastq):
                fasta.write(">{}\n{}\n".format(name, seq))

    # Does not give access to the comment part of the header
    def _method_mappy(self, *args, **kwargs):
        with open(self.outfile, "w") as fasta:
            for (name, seq, _) in fastx_read(self.infile):
                fasta.write(">{}\n{}\n".format(name, seq))

    def _method_awk(self, *args, **kwargs):
        # Note1: since we use .format, we need to escape the { and } characters
        # Note2: the \n need to be escaped for Popen to work
        awkcmd = """awk '{{if(NR%4==1) {{printf(">%s\\n",substr($0,2));}} else if(NR%4==2) print;}}' """
        cmd = "{} {} > {}".format(awkcmd, self.infile, self.outfile)
        self.execute(cmd)

    def _method_mawk(self, *args, **kwargs):
        """This variant of the awk method uses mawk, a lighter and faster
        implementation of awk."""
        # Note1: since we use .format, we need to escape the { and } characters
        # Note2: the \n need to be escaped for Popen to work
        awkcmd = """mawk '{{if(NR%4==1) {{printf(">%s\\n",substr($0,2));}} else if(NR%4==2) print;}}' """
        cmd = "{} {} > {}".format(awkcmd, self.infile, self.outfile)
        self.execute(cmd)

    def _method_bioawk(self, *args, **kwargs):
        """This method uses bioawk, an implementation with convenient
        bioinformatics parsing features."""
        awkcmd = """bioawk -c fastx '{{print ">"$name" "$comment"\\n"$seq}}'"""
        cmd = "{} {} > {}".format(awkcmd, self.infile, self.outfile)
        self.execute(cmd)

    def _method_awk_v2(self, *args, **kwargs):

        awkcmd = """awk '{{print ">"substr($0,2);getline;print;getline;getline}}'"""
        cmd = "{} {} > {}".format(awkcmd, self.infile, self.outfile)
        self.execute(cmd)

    def _method_mawk_v2(self, *args, **kwargs):

        awkcmd = """mawk '{{print ">"substr($0,2);getline;print;getline;getline}}'"""
        cmd = "{} {} > {}".format(awkcmd, self.infile, self.outfile)
        self.execute(cmd)

    def _method_sed(self, *args, **kwargs):
        cmd = """sed -n '1~4s/^@/>/p;2~4p' """
        cmd = "{} {} > {}".format(cmd, self.infile, self.outfile)
        self.execute(cmd)
