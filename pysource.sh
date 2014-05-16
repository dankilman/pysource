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


export PYSOURCE_PYTHON=${PYSOURCE_PYTHON="$(command \which python)"}

pysource()
{
    case "$1" in
        daemon|list-registered|run|run-piped)
            __pysource_main "$@"
            ;;
        source|source-registered|source-named)
            __pysource_source "$@"
            ;;
        *)
            __pysource_source source "$@"
            ;;
    esac
}

__pysource_main()
{
    ${PYSOURCE_PYTHON} -m pysource.main "$@"
}

__pysource_source()
{
    local output="$(__pysource_main $@)"
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

def()
{
    local definition="$1"
    local fulldefinition="import pysource
@pysource.function
def $definition
"
    __pysource_source source <(echo "$fulldefinition")
}
