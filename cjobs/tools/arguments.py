import argparse

def create_argument_parser():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(required=True, dest='subparser')

    # parser_settings #
    # this parser handles the configuration of cjobs
    parser_settings = subparsers.add_parser(
        'config', 
        help='create settings dir and settings file'
    )

    # parser_containers #
    # this parser handles containers-related operations
    parser_containers = subparsers.add_parser(
        'listcontainers', 
        help='list available containers'
    )
    
    # parser_cluster #
    # this parser interprets arguments related to resources allocation at runtime
    parser_cluster = subparsers.add_parser('job-setup', add_help=False)
    parser_cluster.add_argument(
        "--container", 
        required=True, 
        help='CONTAINER id. Use \'cjobs listcontainers\' to list available containers'
    )
    parser_cluster.add_argument(
        "-c", "--cores", 
        type=int, 
        required=True, 
        help='number of CPU cores to allocate'
    )
    parser_cluster.add_argument(
        "-m", "--memory-per-core",
        type=int,
        required=True,
        help='amount of memory in MB to allocate per CPU core'
    )
    parser_cluster.add_argument(
        "-t", "--time", 
        type=float, 
        required=True, 
        help='maximum allocation time in hours'
    )
    parser_cluster.add_argument(
        "--array", 
        action='store_true', 
        help='request a job array. Incompatible with --massive'
    )
    parser_cluster.add_argument(
        "--massive", 
        action='store_true', 
        help='request a massive job. Incompatible with --array'
    )

    # SOFTWARE-SPECIFIC PARSERS
    
    # gaussian16
    parser_gaussian = subparsers.add_parser('gaussian', help='setup a Gaussian calculation', parents=[parser_cluster])
    parser_gaussian.add_argument(
        '-j','--jobs', 
        nargs='+', 
        required=True, 
        help='gaussian input file'
    )
    parser_gaussian.add_argument(
        "--send-files", 
        nargs='+', 
        required=False, 
        help='send additional files files from local dir to calculation directory'
    )

    # orca
    parser_orca = subparsers.add_parser('orca', help='setup an Orca calculation', parents=[parser_cluster])
    parser_orca.add_argument(
        '-j','--jobs', 
        nargs='+', 
        required=True, 
        help='orca input file'
    )
    parser_orca.add_argument(
        "--send-files", 
        nargs='+', 
        required=False, 
        help='send additional files files from local dir to calculation directory'
    )

    # xtb
    parser_xtb = subparsers.add_parser('xtb', help="setup a xTB calculation", parents=[parser_cluster])
    parser_xtb.add_argument(
        '-j','--jobs', 
        nargs='+', 
        required=True, 
        help='xTB-compatible coordinates file'
    )
    parser_xtb.add_argument(
        '-f','--flags', 
        type=str, 
        default='', 
        help='xTB CLI options. See "https://xtb-docs.readthedocs.io/en/latest/commandline.html" for details'
    )
    parser_xtb.add_argument(
        "--send-files", 
        nargs='+', 
        required=False, 
        help='send additional files files from local dir to calculation directory'
    )
    parser_xtb.add_argument(
        '--use-input', 
        action='store_true', 
        help=(
            'Use the xTB detailed input file. '
            'The detailed input file should have the same name as the file provided in \'--job\' '
            'but with a .inp extension. The \'--send-files\' option is required'
        )
    )
    

    # crest
    parser_crest = subparsers.add_parser('crest', help="setup a crest calculation", parents=[parser_cluster])
    parser_crest.add_argument(
        '-j','--jobs', 
        nargs='+', 
        required=True, 
        help='coordinates file'
    )
    parser_crest.add_argument(
        '-f','--flags', 
        type=str, 
        default='', 
        help='crest CLI options. See "https://crest-lab.github.io/crest-docs/page/documentation/keywords.html" for details'
    )
    parser_crest.add_argument(
        '--standalone', 
        action='store_true', 
        help='Switch places of the first option with job input for standalone usage'
    )
    parser_crest.add_argument(
        "--send-files", 
        nargs='+', 
        required=False, 
        help='send additional files files from local dir to calculation directory'
    )
    parser_crest.add_argument(
        '--use-input', 
        action='store_true', 
        help=(
            'Use the crest detailed input file. '
            'The detailed input file should have the same name as the file provided in \'--job\' '
            'but with a .inp extension. The \'--send-files\' option is required'
        )
    )
    parser_crest.add_argument(
        '--use-reference', 
        action='store_true', 
        help=(
            'Request the use a reference geometry. '
            'The reference geometry file should have the same name as the file provided in \'--job\' '
            'but with a .coord extension. The \'--send-files\' option is required'
        )
    )
    return parser