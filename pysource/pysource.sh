#! /usr/bin/env bash

__pysource_python=python

pysource()
{
    case "$1" in
        daemon)
            __pysource_daemon $@
            ;;
        *)
            __pysource_source $@
            ;;
    esac
}

__pysource_daemon()
{
    ${__pysource_python} -m pysource.main $@
}

__pysource_source()
{
    eval "$(${__pysource_python} -m pysource.main source $@)"
}

__pysource_run()
{
    ${__pysource_python} -m pysource.main run $@
}
