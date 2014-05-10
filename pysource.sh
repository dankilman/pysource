#! /usr/bin/env bash
# Copyright 2014 Dan Kilman
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__pysource_python=python

pysource()
{
    case "$1" in
        daemon|list-registered)
            __pysource_main $@
            ;;
        source-registered)
            __pysource_source_registered $@
            ;;
        *)
            __pysource_source $@
            ;;
    esac
}

__pysource_main()
{
    ${__pysource_python} -m pysource.main $@
}


__pysource_source_registered()
{
    local output="$(${__pysource_python} -m pysource.main source-registered $@)"
    __pysource_source_impl "$output"
}

__pysource_source()
{
    local output="$(${__pysource_python} -m pysource.main source $@)"
    __pysource_source_impl "$output"
}

__pysource_source_impl()
{
    local output="$1"
    if [[ $output == \#GENERATED_BY_PYSOURCE* ]]
    then
        if [[ $output == \#GENERATED_BY_PYSOURCE_VERBOSE* ]]
        then
            echo "Sourcing:"
            echo "$output"
        fi
        eval "$output"
    else
        echo "$output"
    fi
}

__pysource_run()
{
    ${__pysource_python} -m pysource.main run "$@"
}

def()
{
    local definition="$1"
    local fulldefinition="import pysource
@pysource.function
def $definition
"
    __pysource_source <(echo "$fulldefinition")
}
