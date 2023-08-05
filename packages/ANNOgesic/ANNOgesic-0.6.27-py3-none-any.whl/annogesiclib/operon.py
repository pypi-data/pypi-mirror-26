import os
from annogesiclib.multiparser import Multiparser
from annogesiclib.helper import Helper
from annogesiclib.detect_operon import operon
from annogesiclib.stat_operon import stat
from annogesiclib.combine_gff import combine_gff


class OperonDetection(object):
    '''detection of operon'''

    def __init__(self, args_op):
        self.multiparser = Multiparser()
        self.helper = Helper()
        if args_op.tsss is not None:
            self.tss_path = os.path.join(args_op.tsss, "tmp")
        else:
            self.tss_path = None
        if args_op.utr5s is not None:
            self.utr5_path = os.path.join(args_op.utr5s, "tmp")
        else:
            self.utr5_path = None
        if args_op.utr3s is not None:
            self.utr3_path = os.path.join(args_op.utr3s, "tmp")
        else:
            self.utr3_path = None
        self.tran_path = os.path.join(args_op.trans, "tmp")
        self.table_path = os.path.join(args_op.output_folder, "tables")
        if args_op.terms is not None:
            self._check_gff(args_op.terms, "term")
            self.term_path = os.path.join(args_op.terms, "tmp")
        else:
            self.term_path = None

    def _check_gff(self, gffs, type_):
        for gff in os.listdir(gffs):
            if gff.endswith(".gff"):
                self.helper.check_uni_attributes(os.path.join(gffs, gff))

    def _detect_operon(self, prefixs, args_op):
        for prefix in prefixs:
            out_table = os.path.join(self.table_path,
                                     "_".join([prefix, "operon.csv"]))
            print("Detecting operons of {0}".format(prefix))
            if self.tss_path is None:
                tss = False
            else:
                tss = self.helper.get_correct_file(
                        self.tss_path, "_TSS.gff", prefix, None, None)
            tran = self.helper.get_correct_file(
                    self.tran_path, "_transcript.gff", prefix, None, None)
            gff = self.helper.get_correct_file(
                    args_op.gffs, ".gff", prefix, None, None)
            if self.term_path is None:
                term = False
            else:
                term = self.helper.get_correct_file(
                        self.term_path, "_term.gff", prefix, None, None)
            operon(tran, tss, gff, term, args_op.tss_fuzzy,
                   args_op.term_fuzzy, args_op.length, out_table)

    def _check_and_parser_gff(self, args_op):
        self._check_gff(args_op.gffs, "gff")
        self._check_gff(args_op.trans, "tran")
        self.multiparser.parser_gff(args_op.gffs, None)
        self.multiparser.parser_gff(args_op.trans, "transcript")
        self.multiparser.combine_gff(args_op.gffs, self.tran_path,
                                     None, "transcript")
        if args_op.tsss is not None:
            self._check_gff(args_op.tsss, "tss")
            self.multiparser.parser_gff(args_op.tsss, "TSS")
            self.multiparser.combine_gff(args_op.gffs, self.tss_path, None, "TSS")
        if args_op.utr5s is not None:
            self._check_gff(args_op.utr5s, "utr")
            self.multiparser.parser_gff(args_op.utr5s, "5UTR")
            self.multiparser.combine_gff(args_op.gffs, self.utr5_path,
                                         None, "5UTR")
        if args_op.utr3s is not None:
            self._check_gff(args_op.utr3s, "utr")
            self.multiparser.parser_gff(args_op.utr3s, "3UTR")
            self.multiparser.combine_gff(args_op.gffs, self.utr3_path,
                                         None, "3UTR")
        if args_op.terms is not None:
            self._check_gff(args_op.terms, "term")
            self.multiparser.parser_gff(args_op.terms, "term")
            self.multiparser.combine_gff(args_op.gffs, self.term_path,
                                         None, "term")

    def _stat(self, table_path, stat_folder):
        for table in os.listdir(table_path):
            if table.endswith("_operon.csv"):
                filename = "_".join(["stat", table])
                out_stat = os.path.join(stat_folder, filename)
                stat(os.path.join(table_path, table), out_stat)

    def _combine_gff(self, prefixs, args_op):
        '''combine all gff files of features which are associated with operon'''
        for prefix in prefixs:
            out_file = os.path.join(args_op.output_folder, "gffs",
                                    "_".join([prefix, "operon.gff"]))
            print("Generating the gff file of {0}".format(prefix))
            if args_op.tsss is not None:
                tss = self.helper.get_correct_file(
                        self.tss_path, "_TSS.gff", prefix, None, None)
            else:
                tss = None
            tran = self.helper.get_correct_file(
                    self.tran_path, "_transcript.gff", prefix, None, None)
            gff = self.helper.get_correct_file(
                    args_op.gffs, ".gff", prefix, None, None)
            if args_op.utr5s is not None:
                utr5 = self.helper.get_correct_file(
                        self.utr5_path, "_5UTR.gff", prefix, None, None)
            else:
                utr5 = None
            if args_op.utr3s is not None:
                utr3 = self.helper.get_correct_file(
                        self.utr3_path, "_3UTR.gff", prefix, None, None)
            else:
                utr3 = None
            if self.term_path is not None:
                term = self.helper.get_correct_file(
                        self.term_path, "_term.gff", prefix, None, None)
            else:
                term = None
            combine_gff(gff, tran, tss, utr5, utr3, term,
                        args_op.tss_fuzzy, args_op.term_fuzzy, out_file)

    def run_operon(self, args_op):
        self._check_and_parser_gff(args_op)
        prefixs = []
        for gff in os.listdir(args_op.gffs):
            if gff.endswith(".gff"):
                prefixs.append(gff.replace(".gff", ""))
        self._detect_operon(prefixs, args_op)
        self._stat(self.table_path, args_op.stat_folder)
        self._combine_gff(prefixs, args_op)
        self.helper.remove_tmp_dir(args_op.gffs)
        self.helper.remove_tmp_dir(args_op.utr3s)
        self.helper.remove_tmp_dir(args_op.utr5s)
        self.helper.remove_tmp_dir(args_op.tsss)
        self.helper.remove_tmp_dir(args_op.trans)
        if args_op.terms is not None:
            self.helper.remove_tmp_dir(args_op.terms)
