# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#*** nmeta - Network Metadata - REST API Class and Methods

"""
This module is part of the nmeta suite running on top of Ryu SDN
controller to provide network identity and flow metadata.
It provides methods for RESTful API connectivity.
"""

import logging
import logging.handlers

class Api(object):
    """
    This class is instantiated by nmeta.py and provides methods
    for RESTful API connectivity.
    """
    #*** Constants for REST API:
    url_flowtable = '/nmeta/flowtable/'
    url_flowtable_by_ip = '/nmeta/flowtable/{ip}'
    url_identity_nic_table = '/nmeta/identity/nictable/'
    url_identity_system_table = '/nmeta/identity/systemtable/'
    #*** Measurement APIs:
    url_flowtable_size_rows = '/nmeta/measurement/tablesize/rows/'
    url_measure_event_rates = '/nmeta/measurement/eventrates/'
    url_measure_pkt_time = '/nmeta/measurement/metrics/packet_time/'
    #
    IP_PATTERN = r'\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$){4}\b'
    _CONTEXTS = {'wsgi': WSGIApplication}

    def __init__(self, _nmeta, _config):
        #*** Get logging config values from config class:
        _logging_level_s = _config.get_value \
                                    ('api_logging_level_s')
        _logging_level_c = _config.get_value \
                                    ('api_logging_level_c')
        _syslog_enabled = _config.get_value('syslog_enabled')
        _loghost = _config.get_value('loghost')
        _logport = _config.get_value('logport')
        _logfacility = _config.get_value('logfacility')
        _syslog_format = _config.get_value('syslog_format')
        _console_log_enabled = _config.get_value('console_log_enabled')
        _console_format = _config.get_value('console_format')
        #*** Set up Logging:
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        #*** Syslog:
        if _syslog_enabled:
            #*** Log to syslog on host specified in config.yaml:
            self.syslog_handler = logging.handlers.SysLogHandler(address=(
                                                _loghost, _logport), 
                                                facility=_logfacility)
            syslog_formatter = logging.Formatter(_syslog_format)
            self.syslog_handler.setFormatter(syslog_formatter)
            self.syslog_handler.setLevel(_logging_level_s)
            #*** Add syslog log handler to logger:
            self.logger.addHandler(self.syslog_handler)
        #*** Console logging:
        if _console_log_enabled:
            #*** Log to the console:
            self.console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(_console_format)
            self.console_handler.setFormatter(console_formatter)
            self.console_handler.setLevel(_logging_level_c)
            #*** Add console log handler to logger:
            self.logger.addHandler(self.console_handler)
