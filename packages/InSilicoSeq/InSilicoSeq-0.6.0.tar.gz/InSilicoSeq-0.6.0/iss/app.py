#!/usr/bin/env python
# -*- coding: utf-8 -*-

from iss import bam
from iss import util
from iss import download
from iss import abundance
from iss import generator
from Bio import SeqIO
from joblib import Parallel, delayed

import os
import sys
import logging
import argparse


def generate_reads(args):
    """Main function for the `iss generate` submodule

    This submodule generates reads from an ErrorModel and write them to
        args.output + _R(1|2).fastq

    Args:
        args (object): the command-line arguments from argparse
    """
    logger = logging.getLogger(__name__)
    logger.debug('Using verbose logger')

    try:  # try to import and load the correct error model
        logger.info('Starting iss generate')
        logger.info('Using %s ErrorModel' % args.model)
        if args.model == 'kde':
            from iss.error_models import kde, two_dim
            if args.model_file == 'HiSeq2500':
                npz = os.path.join(
                    os.path.dirname(__file__),
                    'profiles/HiSeq2500')
            elif args.model_file == 'MiSeq':
                npz = os.path.join(
                    os.path.dirname(__file__),
                    'profiles/MiSeq')
            else:
                npz = args.model_file
            err_mod = two_dim.MultiKDErrorModel(npz)
        elif args.model == 'basic':
            from iss.error_models import basic
            err_mod = basic.BasicErrorModel()
    except ImportError as e:
        logger.error('Failed to import ErrorModel module: %s' % e)
        sys.exit(1)

    try:  # try to read genomes and generate reads
        if args.genomes:
            genome_file = args.genomes
        elif args.ncbi and args.n_genomes:
            genomes = download.ncbi(args.ncbi, args.n_genomes)
            genome_file = download.to_fasta(genomes, args.output)
        else:
            logger.error('Invalid input')  # TODO better error handling here
            sys.exit(1)

        assert os.stat(genome_file).st_size != 0
        f = open(genome_file, 'r')
        with f:  # count the number of records
            record_list = util.count_records(f)
    except IOError as e:
        logger.error('Failed to open genome(s) file:%s' % e)
        sys.exit(1)
    except AssertionError as e:
        logger.error('Genome(s) file seems empty: %s' % genome_file)
        sys.exit(1)
    else:
        # read the abundance file
        if args.abundance_file:
            logger.info('Using abundance file:%s' % args.abundance_file)
            abundance_dic = abundance.parse_abundance_file(args.abundance_file)
        elif args.abundance == 'uniform':
            logger.info('Using %s abundance distribution' % args.abundance)
            abundance_dic = abundance.uniform(record_list)
        elif args.abundance == 'halfnormal':
            logger.info('Using %s abundance distribution' % args.abundance)
            abundance_dic = abundance.halfnormal(record_list)
        elif args.abundance == 'exponential':
            logger.info('Using %s abundance distribution' % args.abundance)
            abundance_dic = abundance.exponential(record_list)
        elif args.abundance == 'lognormal':
            logger.info('Using %s abundance distribution' % args.abundance)
            abundance_dic = abundance.lognormal(record_list)
        elif args.abundance == 'zero_inflated_lognormal':
            logger.info('Using %s abundance distribution' % args.abundance)
            abundance_dic = abundance.zero_inflated_lognormal(record_list)
        else:
            logger.error('Could not get abundance')
            sys.exit(1)

        cpus = args.cpus
        logger.info('Using %s cpus for read generation' % cpus)

        temp_file_list = []  # list holding the name prefix of all temp files
        f = open(genome_file, 'r')  # re-opens the file
        with f:
            fasta_file = SeqIO.parse(f, 'fasta')
            for record in fasta_file:  # generate set of reads for each record
                try:
                    species_abundance = abundance_dic[record.id]
                except KeyError as e:
                    logger.error(
                        'Fasta record not found in abundance file: %s' % e)
                    sys.exit(1)
                else:
                    logger.info('Generating reads for record: %s' % record.id)
                    genome_size = len(record.seq)
                    coverage = abundance.to_coverage(
                        args.n_reads,
                        species_abundance,
                        err_mod.read_length,
                        genome_size
                        )
                    n_pairs = int(round(
                        (coverage *
                            len(record.seq)) / err_mod.read_length) / 2)

                    # will correct approximation later
                    n_pairs_per_cpu = int(round(n_pairs / cpus))

                    record_file_name_list = Parallel(n_jobs=cpus)(
                        delayed(generator.reads)(
                            record, err_mod,
                            n_pairs_per_cpu, i) for i in range(cpus))
                    temp_file_list.extend(record_file_name_list)

        generator.concatenate(temp_file_list, args.output)
        generator.cleanup(temp_file_list)
        logger.info('Read generation complete')


def model_from_bam(args):
    """Main function for the `iss model` submodule

    This submodule write all variables necessary for building an ErrorModel
    to args.output + .npz

    Args:
        args (object): the command-line arguments from argparse
    """
    logger = logging.getLogger(__name__)
    logger.debug('Using verbose logger')

    try:  # try to import bam module and write model data to file
        logger.info('Starting iss model')
        from iss import bam
    except ImportError as e:
        logger.error('Failed to import bam module: %s' % e)
        sys.exit(1)
    else:
        logger.info('Using KDE ErrorModel')
        bam.to_model(args.bam, args.output)
        logger.info('Model generation complete')


def main():
    parser = argparse.ArgumentParser(
        prog='InSilicoSeq',
        usage='iss [subcommand] [options]',
        description='InSilicoSeq: A sequencing simulator'
    )
    subparsers = parser.add_subparsers(
            title='available subcommands',
            metavar=''
    )

    parser_mod = subparsers.add_parser(
        'model',
        prog='iss model',
        description='generate an error model from a bam file',
        help='generate an error model from a bam file'
    )
    parser_gen = subparsers.add_parser(
        'generate',
        prog='iss generate',
        description='simulate reads from an error model',
        help='simulate reads from an error model'
    )

    # arguments form the read generator module
    param_logging = parser_gen.add_mutually_exclusive_group()
    input_genomes = parser_gen.add_mutually_exclusive_group()
    input_abundance = parser_gen.add_mutually_exclusive_group()
    param_logging.add_argument(
        '--quiet',
        '-q',
        action='store_true',
        default=False,
        help='Disable info logging. (default: %(default)s).'
    )
    param_logging.add_argument(
        '--debug',
        '-d',
        action='store_true',
        default=False,
        help='Enable debug logging. (default: %(default)s).'
    )
    parser_gen.add_argument(
        '--cpus',
        '-p',
        default=2,
        type=int,
        metavar='<int>',
        help='number of cpus to use. (default: %(default)s).'
    )
    input_genomes.add_argument(
        '--genomes',
        '-g',
        metavar='<genomes.fasta>',
        help='Input genome(s) from where the reads will originate'
    )
    input_genomes.add_argument(
        '--ncbi',
        '-k',
        choices=['bacteria', 'viruses', 'archaea'],
        metavar='<str>',
        help='Download input genomes from NCBI. Requires --n_genomes/-u\
            option. Can be bacteria, viruses or archaea.'
    )
    parser_gen.add_argument(
        '--n_genomes',
        '-u',
        type=int,
        metavar='<int>',
        help='How many genomes will be downloaded from NCBI. Required if\
            --ncbi/-k is set.'
    )
    input_abundance.add_argument(
        '--abundance',
        '-a',
        choices=['uniform', 'halfnormal',
                 'exponential', 'lognormal', 'zero_inflated_lognormal'],
        metavar='<str>',
        default='lognormal',
        help='abundance distribution (default: %(default)s). Can be uniform,\
            halfnormal, exponential, lognormal or zero-inflated-lognormal.'
    )
    input_abundance.add_argument(
        '--abundance_file',
        '-b',
        metavar='<abundance.txt>',
        help='abundance file for coverage calculations (default: %(default)s).'
    )
    parser_gen.add_argument(
        '--n_reads',
        '-n',
        metavar='<int>',
        type=int,
        default=1000000,
        help='Number of reads to generate (default: %(default)s)'
    )
    parser_gen.add_argument(
        '--model',
        '-m',
        metavar='<str>',
        choices=['cdf', 'basic'],
        default='kde',
        help='Error model. If not specified, using kernel density estimation \
        (default: %(default)s). Can be kde or basic.'
    )
    parser_gen.add_argument(
        '--model_file',
        '-f',
        metavar='<npz>',
        default=None,
        help='Error model file. If not specified, using a basic \
        error model instead (default: %(default)s). Use \'HiSeq2500\' or \
        \'MiSeq\'for a pre-computed error model provided with the software \
        (require --model kde)'
    )
    parser_gen.add_argument(
        '--gc_bias',
        '-c',
        action='store_true',
        default=False,
        help='If set, may fail to sequence reads with abnormal GC content. \
        Doesn\'t guarantee --n_reads (default: %(default)s)'
    )
    parser_gen.add_argument(
        '--output',
        '-o',
        metavar='<fastq>',
        help='Output file prefix (Required)',
        required=True
    )
    parser_gen._optionals.title = 'arguments'
    parser_gen.set_defaults(func=generate_reads)

    # arguments for the error model module
    parser_mod.add_argument(
        '--quiet',
        '-q',
        action='store_true',
        default=False,
        help='Disable info logging. (default: %(default)s).'
    )
    parser_mod.add_argument(
        '--debug',
        '-d',
        action='store_true',
        default=False,
        help='Enable debug logging. (default: %(default)s).'
    )
    parser_mod.add_argument(
        '--bam',
        '-b',
        metavar='<bam>',
        help='aligned reads from which the model will be inferred (Required)',
        required=True
    )
    parser_mod.add_argument(
        '--output',
        '-o',
        metavar='<npz>',
        help='Output file prefix (Required)',
        required=True
    )
    parser_mod._optionals.title = 'arguments'
    parser_mod.set_defaults(func=model_from_bam)
    args = parser.parse_args()

    # set logger
    try:
        if args.quiet:
            logging.basicConfig(level=logging.ERROR)
        elif args.debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        args.func(args)
        logging.shutdown()
    except AttributeError as e:
        logger = logging.getLogger(__name__)
        logger.debug(e)
        parser.print_help()
        # raise  # extra traceback to uncomment if all hell breaks lose
