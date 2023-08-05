#!/usr/bin/python
# ----------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  Licensed under the MIT License. See LICENSE.rst in the
#  project root for license information. If LICENSE.rst
#  is missing, see https://opensource.org/licenses/MIT
# ----------------------------------------------------------

"""Microsoft Genomics command-line client - allows submission and management
 of genomics workflows on the Microsoft Genomics platform"""

import sys
import malibuworkflow
import malibuargs

# Version must be valid form for StrictVersion <d>.<d>.<d> for the sort
# to work properly and find the latest version.  More details at:
# http://epydoc.sourceforge.net/stdlib/distutils.version.StrictVersion-class.html
VERSION = '0.7.2'

def warn_for_package_update():
    """Check for updated version of msgen and warn if a newer version is available"""

    try:
        import requests
        from distutils.version import StrictVersion

        # Construct the URL to get the msgen package information from pypi
        url = "https://pypi.python.org/pypi/{0}/json".format(malibuargs.PACKAGE_NAME)
        versions = requests.get(url).json()["releases"].keys()
        versions.sort(key=StrictVersion, reverse=True)
        if VERSION < versions[0]:
            print ("\nThere is a newer version of msgen available."
                   "  Please consider upgrading to v%s."
                   "\nTo upgrade, run: pip install --upgrade msgen\n"
                  ) % versions[0]

    except:
        print "\nException during test for msgen update. Continuing\n"

    return

def _command(func, args):
    """Perform a command using command-line arguments
    func: A method of the malibuworkflow.WorkflowExecutor class"""
    args_output = malibuargs.ArgsOutput()
    args_output.fill(args)
    workflow_executor = malibuworkflow.WorkflowExecutor(args_output)
    func(workflow_executor)
    sys.exit(workflow_executor.current_exit_status)

def post_workflow(args):
    """Post a workflow using command-line arguments"""
    _command(malibuworkflow.WorkflowExecutor.post_workflow, args)

def get_workflow_status(args):
    """Get status of a workflow using command-line arguments"""
    _command(malibuworkflow.WorkflowExecutor.get_workflow_status, args)

def cancel_workflow(args):
    """Cancel a workflow using command-line arguments"""
    _command(malibuworkflow.WorkflowExecutor.cancel_workflow, args)

def list_workflows(args):
    """List workflows using command-line arguments"""
    _command(malibuworkflow.WorkflowExecutor.list_workflows, args)

def print_help(args, subparsers):
    """Print general help or help for a specific command"""
    if args.cmd is None or args.cmd == "help":
        malibuargs.print_generic_help()
    else:
        subparser = subparsers.choices.get(args.cmd, None)
        if subparser is None:
            malibuargs.print_generic_help()
        else:
            subparser.print_help()

def main():
    """Main execution flow"""

    # Display logon banner
    print "Microsoft Genomics command-line client v{0}".format(VERSION)
    print "Copyright (c) 2017 Microsoft. All rights reserved."

    warn_for_package_update()

    malibuargs.parse_and_run(sys.argv, post_workflow, list_workflows, cancel_workflow, get_workflow_status, print_help)

if __name__ == "__main__":
    main()
