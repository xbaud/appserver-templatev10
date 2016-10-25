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
    if [ ! -f bootstrap.py ]; then    
        wget https://raw.github.com/buildout/buildout/master/bootstrap/bootstrap.py
    fi
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

function setup_c9_trusty_blank_container {
    
    # Set a UTF8 locale
    sudo locale-gen fr_FR fr_FR.UTF-8
    sudo update-locale    
    
    # Update bashrc with locale
    echo "#"
    echo "# Added by appserver-templatev10 install.sh"
    echo "export LANG=fr_FR.UTF-8" >> /home/ubuntu/.bashrc
    echo "export LANGUAGE=fr_FR" >> /home/ubuntu/.bashrc
    echo "export LC_ALL=fr_FR.UTF-8" >> /home/ubuntu/.bashrc
    echo "export LC_CTYPE=fr_FR.UTF-8" >> /home/ubuntu/.bashrc

    # Refresh index and install required index
    sudo apt-get update
    sudo apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev
    sudo apt-get install -y postgresql
    sudo pg_dropcluster 9.3 main
    sudo pg_createcluster --locale fr_FR.UTF-8 9.3 main
    sudo pg_ctlcluster 9.3 main start
    sudo su - postgres -c "psql -c \"CREATE ROLE ubuntu WITH LOGIN SUPERUSER CREATEDB CREATEROLE PASSWORD 'ubuntu';\"" 
    
    # Install recent setuptools
    wget https://bootstrap.pypa.io/ez_setup.py
    sudo python ez_setup.py
    rm ez_setup.py
    
    # Install recent virtualenv
    sudo easy_install virtualenv
    
    # create a basic buildout.cfg
    cat <<EOT >> buildout.cfg
[buildout]
extends = appserver.cfg
#          ../../../inouk.edofx

[openerp]
options.admin_passwd = admin
options.db_user = ubuntu
options.db_password = ubuntu
options.db_host = 127.0.0.1
options.xmlrpc_port = 8080    
EOT

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
    echo "  ./install.sh c9-trusty-setup     Install Prerequisites on c9 Ubuntu 14 blank container"
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
elif [[ $COMMAND == "c9-trusty-setup" ]]; then
    setup_c9_trusty_blank_container
    exit
fi

echo "use ./install.sh -h for usage instructions."
