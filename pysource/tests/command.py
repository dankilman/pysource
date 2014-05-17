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


def source_def_explicit(def_content, piped=False, verbose=False):
    return "pysource source-{}".format(source_def(def_content,
                                                  piped,
                                                  verbose))


def source_def(def_content, piped=False, verbose=False):
    return "def '{}' {} {}" \
        .format(def_content,
                '-p' if piped else '',
                '-v' if verbose else '')


def run_explicit(function_name, *args):
    return 'pysource run {}'.format(run(function_name, *args))


def run(function_name, *args):
    args = [str(arg) for arg in args]
    return '{} {}'.format(function_name, ' '.join(args))


def update_env(verbose=False, **env):
    return '{} pysource update-env {}'.format(
        ' '.join('{}={}'.format(key, value) for key, value in env.items()),
        '-v' if verbose else '')


def source_inline(source_content, verbose=False):
    return "pysource source-inline '{}' {}".format(
        source_content,
        '-v' if verbose else '')


def source_named(function_name, piped=False, verbose=False):
    return 'pysource source-named {} {} {}'.format(
        function_name,
        '-p' if piped else '',
        '-v' if verbose else '')


def source(source_path, verbose=False):
    return 'pysource {} {}'.format(source_path, '-v' if verbose else '')


def source_explicit(source_path, verbose=False):
    return 'pysource source {} {}'.format(source_path, '-v' if verbose else '')


def source_registered(verbose=False):
    return 'pysource source-registered {}'.format('-v' if verbose else '')
