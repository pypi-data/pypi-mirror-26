# coding=utf-8
# Copyright (c) 2017 Dell Inc. or its subsidiaries.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
from nagiosunity.lib import unity
from nagiosunity.lib import utils

_log = logging.getLogger(__name__)


class Dpe(unity.UnityWrapper):
    name = 'dpe'

    def __init__(self, options, **kwargs):
        super(Dpe, self).__init__(options)
        self.options = options
        self.kwargs = kwargs
        self._dpe = None

    @property
    def dpe(self):
        return self._dpe if self._dpe else (
            self.unity.get_dpe())

    def check(self):
        all_status = ok, warning, critical, unknown = utils.get_all_status(
            self.dpe)
        code = utils.max_if_not_empty(ok + warning + critical + unknown,
                                      key=lambda i: i[0])
        code = code[0]
        status_mark = utils.get_status_mark("DPE", code)
        first_line = "Total DPEs #{}, Failed DPE(ID): {}".format(
            len(ok + warning + critical + unknown), [c[1] for c in critical])
        # Status line
        print(status_mark + first_line + " | ")

        # Failed details
        utils.print_if_failure(all_status[code], self.dpe)
        # Performance detail
        for d in self.dpe:
            print("{}: Power(curr/avg/max)={}/{}/{} watts, "
                  "Temperature(curr/avg/max)={}/{}/{} degrees , "
                  "Speed(curr/max)={}/{} GB".format(
                   d.name,
                   d.current_power, d.avg_power, d.max_power,
                   d.current_temperature, d.avg_temperature,
                   d.max_temperature,
                   utils.byte_to_GB(d.current_speed),
                   utils.byte_to_GB(d.max_speed)))
        return code
