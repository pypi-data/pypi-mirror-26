#!/usr/bin/env python
#     Copyright 2017, Kay Hayen, mailto:kay.hayen@gmail.com
#
#     Python tests originally created or extracted from other peoples work. The
#     parts were too small to be protected.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#

import os
import sys

# Find nuitka package relative to us.
sys.path.insert(
    0,
    os.path.normpath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            ".."
        )
    )
)
from nuitka.tools.testing.Common import (
    my_print,
    setup,
    compareWithCPython,
    createSearchMode,
    decideFilenameVersionSkip
)

python_version = setup(needs_io_encoding = True)

search_mode = createSearchMode()

for filename in sorted(os.listdir('.')):
    if not filename.endswith(".py"):
        continue

    if not decideFilenameVersionSkip(filename):
        continue

    active = search_mode.consider(
        dirname  = None,
        filename = filename
    )

    if active:
        extra_flags = ["expect_failure", "remove_output", "syntax_errors"]

        compareWithCPython(
            dirname     = None,
            filename    = filename,
            extra_flags = extra_flags,
            search_mode = search_mode,
            needs_2to3  = False
        )
    else:
        my_print("Skipping", filename)

search_mode.finish()
