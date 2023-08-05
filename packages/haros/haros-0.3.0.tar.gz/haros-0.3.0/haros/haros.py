
#Copyright (c) 2016 Andre Santos
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

"""
HAROS directory (data folder) structure:

+ ~/.haros
|-- index.yaml
|-+ plugins
  |-+ ...
|-+ repositories
  |-+ ...
|-+ viz
  |-+ ...
  |-+ data
    |-- packages.json
    |-- rules.json
    |-- summary.json
    |-+ compliance
      |-- ...
    |-+ metrics
      |-- ...
  |-- index.html
|-+ export
  |-- metrics.csv
"""

# start with init
# init creates the default data dir
# viz is copied to init dir

# analysis grabs previous db and index from data dir
# analysis may accept import option to use another db

# export receives a dir where it will generate the export files
# export still generates files in the data dir
# export uses db from analysis step or loads it from data dir

# viz uses data from the data dir


import argparse
import logging
import os
import subprocess
import sys
import tempfile

from shutil import copyfile, rmtree
from pkg_resources import Requirement, resource_filename

from .data_manager import DataManager
from . import plugin_manager as plugman
from .analysis_manager import AnalysisManager
from . import export_manager as expoman
from . import visualiser as viz


HAROS_DIR       = os.path.join(os.path.expanduser("~"), ".haros")
REPOSITORY_DIR  = os.path.join(HAROS_DIR, "repositories")
EXPORT_DIR      = os.path.join(HAROS_DIR, "export")
PLUGIN_DIR      = os.path.join(HAROS_DIR, "plugins")
VIZ_DIR         = os.path.join(HAROS_DIR, "viz")
DB_PATH         = os.path.join(HAROS_DIR, "haros.db")
ANALYSIS_PATH   = os.path.join(HAROS_DIR, "analysis.db")
LOG_PATH        = os.path.join(HAROS_DIR, "log.txt")
PLUGIN_REPOSITORY = "https://github.com/git-afsantos/haros_plugins.git"

_log = logging.getLogger()

# Options:
#   --debug sets the logging level to debug
#   haros init
#       initialises the data directory
#   haros analyse [args]
#       runs update, analysis and export
#       -k  keep previous analyses (run analysis only for new packages)
#       -r  also register and analyse repositories
#       -w  whitelist plugins
#       -b  blacklist plugins
#       -p  package filter
#       -d  db to import
#   haros export [args]
#       runs export only
#       -d export dir (output)
#   haros viz [args]
#       runs visualiser only
#       -s host
#       -d export dir (input)
#   haros full [args]
#       full run (analyse + viz)
def parse_arguments(argv, source_runner):
    parser = argparse.ArgumentParser(prog="haros",
            description="ROS quality assurance.")
    parser.add_argument("--debug", action = "store_true",
                        help = "set debug logging")
    parser.add_argument("-C", dest = "dir",
            help = "change current directory to DIR before running")
    subparsers = parser.add_subparsers()

    parser_init = subparsers.add_parser("init")
    parser_init.set_defaults(func = command_init, source_runner = source_runner)

    parser_full = subparsers.add_parser("full")
    parser_full.add_argument("-r", "--repositories", dest = "use_repos",
                             action = "store_true", help = "use repositories")
    parser_full.add_argument("-s", "--server-host", dest = "host",
                             default = "localhost:8080",
                             help = "visualisation host " \
                                    "(default: \"localhost:8080\")")
    parser_full.add_argument("-p", "--package-index", dest = "pkg_filter",
                             help = ("package index file (default: "
                                     "workspace packages below current dir)"))
    parser_full.add_argument("-t", "--target-dir", default = VIZ_DIR,
                             help = "export reports to target DIR")
    group = parser_full.add_mutually_exclusive_group()
    group.add_argument("-w", "--whitelist", nargs = "*", dest = "whitelist",
                       help = "execute only these plugins")
    group.add_argument("-b", "--blacklist", nargs = "*", dest = "blacklist",
                       help = "skip these plugins")
    parser_full.set_defaults(func = command_full, source_runner = source_runner)

    parser_analyse = subparsers.add_parser("analyse")
    parser_analyse.add_argument("-r", "--repositories", dest = "use_repos",
                                action = "store_true",
                                help = "use repositories")
    parser_analyse.add_argument("-p", "--package-index", dest = "pkg_filter",
                                help = ("package index file (default: workspace"
                                        " packages below current dir)"))
    parser_analyse.add_argument("-t", "--target-dir", default = VIZ_DIR,
                                help = "export reports to target DIR")
    group = parser_analyse.add_mutually_exclusive_group()
    group.add_argument("-w", "--whitelist", nargs = "*", dest = "whitelist",
                       help="execute only these plugins")
    group.add_argument("-b", "--blacklist", nargs = "*", dest = "blacklist",
                       help="skip these plugins")
    parser_analyse.set_defaults(func = command_analyse,
                                source_runner = source_runner)

    parser_export = subparsers.add_parser("export")
    parser_export.add_argument("-v", "--export-viz", action = "store_true",
                                help = "export HTML viz files")
    parser_export.add_argument("target_dir", metavar = "dir",
                               help = "where to export data")
    parser_export.set_defaults(func = command_export,
                               source_runner = source_runner)

    parser_viz = subparsers.add_parser("viz")
    parser_viz.add_argument("-d", "--server-dir", default = VIZ_DIR,
                            help = "served data directory")
    parser_viz.add_argument("-s", "--server-host", dest = "host",
                            default = "localhost:8080",
                            help = ("visualisation host "
                                    "(default: \"localhost:8080\")"))
    parser_viz.set_defaults(func = command_viz, source_runner = source_runner)

    return parser.parse_args() if argv is None else parser.parse_args(argv)


def _check_haros_directory():
    if not os.path.isdir(HAROS_DIR):
        raise RuntimeError("HAROS directory was not initialised.")

def _empty_dir(dir_path):
    _log.debug("Emptying directory %s", dir_path)
    for f in os.listdir(dir_path):
        path = os.path.join(dir_path, f)
        if os.path.isfile(path):
            _log.debug("Removing file %s", path)
            os.unlink(path)

def command_init(args):
    print "[HAROS] Creating directories..."
    if os.path.exists(HAROS_DIR) and not os.path.isdir(HAROS_DIR):
        raise RuntimeError("Could not init; " + HAROS_DIR \
                           + " already exists and is not a directory.")
    if not os.path.exists(HAROS_DIR):
        _log.info("Creating %s", HAROS_DIR)
        os.makedirs(HAROS_DIR)
        _log.info("Creating %s", os.path.join(HAROS_DIR, "index.yaml"))
        with open(os.path.join(HAROS_DIR, "index.yaml"), "w") as f:
            f.write("%YAML 1.1\n---\npackages: []\n")
    if not os.path.exists(REPOSITORY_DIR):
        _log.info("Creating %s", REPOSITORY_DIR)
        os.mkdir(REPOSITORY_DIR)
    if not os.path.exists(EXPORT_DIR):
        _log.info("Creating %s", EXPORT_DIR)
        os.mkdir(EXPORT_DIR)
    viz.install(VIZ_DIR, args.source_runner)
    if not os.path.exists(PLUGIN_DIR):
        _log.info("Creating %s", PLUGIN_DIR)
        os.mkdir(PLUGIN_DIR)
        _log.info("Cloning plugin repository.")
        subprocess.check_call(["git", "clone", PLUGIN_REPOSITORY, PLUGIN_DIR])
    else:
        _log.info("Updating plugin repository.")
        wd = os.getcwd()
        os.chdir(PLUGIN_DIR)
        if subprocess.call(["git", "branch"], stderr = subprocess.STDOUT,
                           stdout = open(os.devnull, 'w')) == 0:
            _log.info("%s is a git repository. Executing git pull.", PLUGIN_DIR)
            subprocess.check_call(["git", "pull"])
        os.chdir(wd)


def command_full(args):
    if command_analyse(args):
        args.server_dir = args.target_dir
        return command_viz(args)
    return False


def command_analyse(args):
    _check_haros_directory()
    _log.debug("Creating new data manager.")
    dataman = DataManager()
    # path = os.path.join(args.datadir, "haros.db")
    # if os.path.isfile(path):
        # dataman = DataManager.load_state()
    print "[HAROS] Indexing source code..."
    path = args.pkg_filter \
           if args.pkg_filter and os.path.isfile(args.pkg_filter) \
           else os.path.join(HAROS_DIR, "index.yaml")
    _log.debug("Package index file %s", path)
    dataman.index_source(path, REPOSITORY_DIR, args.use_repos)
    if not dataman.packages:
        _log.warning("There are no packages to analyse.")
        return False
    print "[HAROS] Loading common definitions..."
    if args.source_runner:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                               "definitions.yaml"))
    else:
        path = resource_filename(Requirement.parse("haros"),
                                 "haros/definitions.yaml")
    dataman.load_definitions(path)
    print "[HAROS] Loading plugins..."
    plugins = plugman.load_plugins(PLUGIN_DIR, args.whitelist, args.blacklist)
    if not plugins:
        _log.warning("There are no analysis plugins.")
        return False
    for plugin in plugins:
        dataman.extend_definitions(plugin.name, plugin.rules, plugin.metrics)
    print "[HAROS] Running analysis..."
    _empty_dir(EXPORT_DIR)
    if os.path.isfile(ANALYSIS_PATH):
        anaman = AnalysisManager.load_state(ANALYSIS_PATH)
    else:
        anaman = AnalysisManager()
    temppath = tempfile.mkdtemp()
    anaman.run_analysis_and_processing(temppath, plugins, dataman, EXPORT_DIR)
    rmtree(temppath)
    print "[HAROS] Saving analysis results..."
    dataman.save_state(DB_PATH)
    anaman.save_state(ANALYSIS_PATH)
    index_file = os.path.join(args.target_dir, "index.html")
    args.export_viz = (args.target_dir != VIZ_DIR
                       and not os.path.isfile(index_file))
    command_export(args, dataman, anaman)
    return True


def command_export(args, dataman = None, anaman = None):
    assert (dataman is None) == (anaman is None)
    _check_haros_directory()
    print "[HAROS] Exporting analysis results..."
    if args.export_viz:
        viz.install(args.target_dir, args.source_runner)
    viz_data_dir = os.path.join(args.target_dir, "data")
    if dataman:
        _log.debug("Exporting on-memory data manager.")
        json_path   = viz_data_dir
        csv_path    = EXPORT_DIR
        db_path     = None
        ana_path    = None
        _empty_dir(os.path.join(viz_data_dir, "compliance"))
        _empty_dir(os.path.join(viz_data_dir, "metrics"))
    elif os.path.isdir(args.target_dir):
        _log.debug("Exporting data manager from file.")
        if os.path.isfile(DB_PATH):
            dataman = DataManager.load_state(DB_PATH)
        else:
            _log.warning("There is no analysis data to export.")
            return False
        if os.path.isfile(ANALYSIS_PATH):
            anaman = AnalysisManager.load_state(ANALYSIS_PATH)
        else:
            _log.warning("There is no analysis data to export.")
            return False
        if args.export_viz:
            json_path = viz_data_dir
        else:
            json_path = os.path.join(args.target_dir, "json")
        if not os.path.exists(json_path):
            _log.info("Creating directory %s", json_path)
            os.mkdir(json_path)
        csv_path = os.path.join(args.target_dir, "csv")
        if not os.path.exists(csv_path):
            _log.info("Creating directory %s", csv_path)
            os.mkdir(csv_path)
        db_path = os.path.join(args.target_dir, "haros.db")
        ana_path = os.path.join(args.target_dir, "analysis.db")
    else:
        _log.error("%s is not a directory!", args.target_dir)
        return False
    expoman.export_packages(json_path, dataman.packages)
    expoman.export_rules(json_path, dataman.rules)
    expoman.export_metrics(json_path, dataman.metrics)
    expoman.export_summary(json_path, anaman)
    path = os.path.join(json_path, "compliance")
    if not os.path.exists(path):
        _log.info("Creating directory %s", path)
        os.mkdir(path)
    expoman.export_violations(path, dataman.packages)
    path = os.path.join(json_path, "metrics")
    if not os.path.exists(path):
        _log.info("Creating directory %s", path)
        os.mkdir(path)
    expoman.export_measurements(path, dataman.packages)
    path = os.path.join(json_path, "models")
    if not os.path.exists(path):
        _log.info("Creating directory %s", path)
        os.mkdir(path)
    expoman.export_configurations(path, dataman.packages)
    if db_path:
        _log.debug("Copying data DB from %s to %s", DB_PATH, db_path)
        copyfile(DB_PATH, db_path)
    if ana_path:
        _log.debug("Copying analysis DB from %s to %s", ANALYSIS_PATH, ana_path)
        copyfile(ANALYSIS_PATH, ana_path)
    return True


def command_viz(args):
    _check_haros_directory()
    viz.serve(args.server_dir, args.host)


def main(argv = None, source_runner = False):
    args = parse_arguments(argv, source_runner)
    if args.debug:
        logging.basicConfig(filename = LOG_PATH, filemode = "w",
                            level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.WARNING)

    original_path = os.getcwd()
    try:
        if args.dir:
            os.chdir(args.dir)
        _log.info("Executing selected command.")
        args.func(args)
        return 0

    except RuntimeError as err:
        _log.error(str(err))
        return 1

    finally:
        os.chdir(original_path)
