"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
__license__ = 'Apache 2.0'
__author__ = 'Darin Gordon'
__credits__ = ['Apache Shiro']
__maintainer__ = 'Darin Gordon'
__email__ = 'dkcdkg@gmail.com'
__status__ = 'Development'


from yosaipy2.web.subject import abcs as web_subject_abcs
from yosaipy2.web.registry import abcs as web_abcs  # since it is the primary api

from .exceptions import (
    CookieException,
    CSRFTokenException,
    YosaiWebException,
)


from yosaipy2.web.registry.registry_settings import (
    WebRegistrySettings,
)


from yosaipy2.web.session.session import (
    WebSessionStorageEvaluator,
    WebSessionManager,
    WebDelegatingSession,
    WebSimpleSession,
    WebSessionHandler,
    WebSessionKey,
)


from yosaipy2.web.subject.subject import (
    WebSubjectContext,
    WebDelegatingSubject,
    WebYosai,
    global_webregistry_context,
)

from yosaipy2.web.mgt.mgt import (
    WebSecurityManager,
    CookieRememberMeManager,
)
