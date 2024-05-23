import argparse

def create_argument_parser():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(required=True, dest='subparser')

    parser_cluster = subparsers.add_parser('job-setup', add_help=False)
    parser_cluster.add_argument("--container", required=True, help='.sif container ID. To list available containers use cjobs --list-containers')
    parser_cluster.add_argument("--send-files", nargs='+', required=False, help='send files from local to remote directory')
    parser_cluster.add_argument("--array", action='store_true', help='request a job array for multiple jobs')
    parser_cluster.add_argument("-c", "--cores", type=int, required=True, help='number of cores (CPUs) to be allocated')
    parser_cluster.add_argument("-m", "--memory-per-core", type=int, required=True, help='memory in MB per core required')
    parser_cluster.add_argument("-t", "--time", type=float, required=True, help='allocation time in hours')

    parser_containers = subparsers.add_parser('config', help='Create the configuration directory for cjobs and initialize the settings with default options. IMPORTANT: Please review the default options carefully and make necessary adjustments before using the program.')

    parser_containers = subparsers.add_parser('listcontainers', help='list all available containers')

    parser_gaussian = subparsers.add_parser('gaussian', help='setup a Gaussian calculation', parents=[parser_cluster])
    parser_gaussian.add_argument('-j','--job', nargs='+', required=True, help='gaussian input file')

    parser_gaussian = subparsers.add_parser('orca', help='setup a Gaussian calculation', parents=[parser_cluster])
    parser_gaussian.add_argument('-j','--job', nargs='+', required=True, help='gaussian input file')

    parser_xtb = subparsers.add_parser('xtb', help="setup a xTB calculation", parents=[parser_cluster])
    parser_xtb.add_argument('-j','--job', nargs='+', required=True, help='coordinates file')
    parser_xtb.add_argument('-f','--flags', type=str, default='', help='xTB flags')
    parser_xtb.add_argument('--standalone', action='store_true', help='Swap first flag with job input for standalone usage')

    parser_crest = subparsers.add_parser('crest', help="setup crest calculation", parents=[parser_cluster])
    parser_crest.add_argument('-j','--job', nargs='+', required=True, help='coordinates file')
    parser_crest.add_argument('-f','--flags', type=str, default='', help='crest flags')
    parser_crest.add_argument('--standalone', action='store_true', help='Swap first flag with job input for standalone usage')

    return parser