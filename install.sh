#!/bin/bash


PYPI_INDEX=""
BUILDOUT_INDEX=""

HELP=0

#
# We need bash
#
if [ -z "$BASH_VERSION" ]; then
    echo -e "Error: BASH shell is required !"
    exit 1
fi

#
# install_openerp
#
function install_openerp {
    # TODO: Rework this test
    if [ -d py27 ]; then
        echo "install.sh has already been launched."
        echo "So you must either use bin/buildout to update or launch \"install.sh reset\" to remove all buildout installed items."
        exit -1
    fi
    wget https://raw.github.com/buildout/buildout/master/bootstrap/bootstrap.py
    virtualenv py27
    py27/bin/python bootstrap.py
    py27/bin/pip install $PYPI_INDEX --allow-all-external --allow-unverified bzr bzr==2.6.0
    bin/buildout install
    echo
    echo "Your commands are now available in ./bin"
    echo "Python is in ./py27. Don't forget to launch source py27/bin/activate"
    echo 
}

function remove_buildout_files {
    echo "Removing all buidout generated items..."
    echo "    Not removing downloads/ to avoid re-downloading openerp"
    rm -rf .installed.cfg
    rm -rf bin/
    rm -rf develop-eggs/
    rm -rf eggs/
    rm -rf etc/
    rm -rf py27/
    rm -rf bootstrap.py
    echo "    Done."
}


#
# Process command line options
#
while getopts "i:h" opt; do
    case $opt in
        i)
            PYPI_INDEX="-i ${OPTARG}"
            BUILDOUT_INDEX="index = ${OPTARG}"
            ;;

        h)
            HELP=1
            ;;

        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;

        :)
            echo "Option -$OPTARG requires an argument." >&2
            exit 1
            ;;
    esac
done

COMMAND=${@:$OPTIND:1}

echo
echo "install.sh - Inouk OpenERP Buildout Installer"
echo "(c) 2013, 2014, 2015 @cmorisse"

if [[ $COMMAND == "help"  ||  $HELP == 1 ]]; then
    echo "Available commands:"
    echo "  ./install.sh help                Prints this message."
    echo "  ./install.sh [-i ...] openerp    Install OpenERP using buildout (postgresql and prerequisites must"
    echo "  ./install.sh reset               Remove all buildout installed files."
    echo 
    echo "Available options:"
    echo "  -i   Pypi Index to use (default=""). See pip install --help"
    echo "  -h   Prints this message"
    echo 
    exit
fi

if [[ $COMMAND == "reset" ]]; then
    remove_buildout_files
    exit
elif [[ $COMMAND == "openerp" ]]; then
    install_openerp
    exit
fi

echo "use ./install.sh -h for usage instructions."
