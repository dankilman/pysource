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


def daemon(action):
    return 'pysource daemon {}'.format(action)


def list_registered():
    return 'pysource list-registered'


def source_def(def_content, piped=False, verbose=False):
    return "pysource source-def '{}' {} {}" \
           .format(def_content,
                   '-p' if piped else '',
                   '-v' if verbose else '')


def run_explicit(function_name, *args):
    return 'pysource run {}'.format(run(function_name, *args))


def run(function_name, *args):
    args = [str(arg) for arg in args]
    return '{} {}'.format(function_name, ' '.join(args))
