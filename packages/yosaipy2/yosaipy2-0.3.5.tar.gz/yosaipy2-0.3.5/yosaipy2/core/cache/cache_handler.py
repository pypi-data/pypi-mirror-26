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

from abcs import CacheHandler
from dogpile.cache import make_region
from functools import partial
from dogpile.cache.api import NO_VALUE
from settings import CacheSettings


class DPCacheHandler(CacheHandler):
    def __init__(self, settings=None, serialization_manager=None):
        """
        You may either explicitly configure the CacheHandler or default to
        settings defined in a yaml file.
        """
        cache_settings = CacheSettings(settings)
        self.region_name = "dogpile"
        self.absolute_ttl = cache_settings.absolute_ttl
        self.credentials_ttl = cache_settings.credentials_ttl
        self.authz_info_ttl = cache_settings.authz_info_ttl
        self.session_ttl = cache_settings.session_abs_ttl
        self.region_name = cache_settings.region_name
        self.region_arguments = cache_settings.region_arguments
        if serialization_manager:
            self.serialization_manager = serialization_manager
        else:
            self._serializer = None
            self.cache_region = None

    @property
    def serialization_manager(self):
        return self._serializer

    @serialization_manager.setter
    def serialization_manager(self, manager):
        self._serializer = manager
        self.cache_region = self.create_cache_region(name=self.region_name)

    def create_cache_region(self, name):
        try:
            cache_region = make_region(name=name).configure(
                'dogpile.cache.redis',
                expiration_time=3600,
                arguments=self.region_arguments
            )
        except AttributeError:
            one = 'serialization_manager not set' if not self.serialization_manager else ''
            msg = 'Failed to Initialize a CacheRegion. {one}'.format(one=one)
            raise AttributeError(msg)
        return cache_region

    def get_ttl(self, key):
        return getattr(self, key + '_ttl', self.absolute_ttl)

    @staticmethod
    def generate_key(identifier, domain):
        # simple for now yet TBD:
        return "yosai:{0}:{1}".format(identifier, domain)

    def get(self, domain, identifier):
        if identifier is None:
            return
        full_key = self.generate_key(identifier, domain)
        result = self.cache_region.get(full_key)

        if result is NO_VALUE:
            return None
        else:
            return self._serializer.deserialize(result)

    def get_or_create(self, domain, identifier, creator_func, creator):
        """
        This method will try to obtain an object from cache.  If the object is
        not available from cache, the creator_func function is called to generate
        a new Serializable object and then the object is cached.  get_or_create
        uses dogpile locking to avoid race condition among competing get_or_create
        threads where by the first requesting thread obtains exclusive privilege
        to generate the new object while other requesting threads wait for the
        value and then return it.
        :param domain:
        :param identifier:
        :param creator_func: the function called to generate a new
                             Serializable object for cache
        :type creator_func:  function

        :param creator: the object calling get_or_create
        """
        if identifier is None:
            return
        full_key = self.generate_key(identifier, domain)
        ttl = self.get_ttl(domain)
        creator = partial(creator_func, creator)
        creator = partial(self._serialize_wrapper, creator)
        result = self.cache_region.get_or_create(
            key=full_key,
            creator=creator,
            expiration_time=ttl
        )
        if result is NO_VALUE:
            return None
        else:
            return self._serializer.deserialize(result)

    def hmget_or_create(self, domain, identifier, keys, creator_func, creator):
        """
        This method will try to obtain an object from cache.  If the object is
        not available from cache, the creator_func function is called to generate
        a new Serializable object and then the object is cached.  get_or_create
        uses dogpile locking to avoid race condition among competing get_or_create
        threads where by the first requesting thread obtains exclusive privilege
        to generate the new object while other requesting threads wait for the
        value and then return it.

        :param domain:

        :param identifier:

        :param keys:

        :param creator_func: the function called to generate a new
                             Serializable object for cache
        :type creator_func:  function

        :param creator: the object calling get_or_create
        """
        if identifier is None:
            return
        full_key = self.generate_key(identifier, domain)
        ttl = self.get_ttl(domain)
        creator = partial(creator_func, creator)
        creator = partial(self._hm_creator_wrapper, creator, keys)
        result = self.cache_region.get_or_create(
            key=full_key,
            creator=creator,
            expiration_time=ttl
        )
        return None if result is NO_VALUE else self._hm_get(keys, result)

    def set(self, domain, identifier, value):
        """
        :param domain:
        :param identifier:
        :param value:  the Serializable object to cache
        """
        if value is None:
            return
        full_key = self.generate_key(identifier, domain)
        value = self._serializer.serialize(value)
        self.cache_region.set(full_key, value)

    def delete(self, domain, identifier):
        """
        Removes an object from cache
        """
        if identifier is None:
            return
        full_key = self.generate_key(identifier, domain)
        self.cache_region.delete(full_key)

    def keys(self, pattern):
        """
        obtains keys from cache that match pattern

        CAUTION:  use for debugging only as it is taxes redis hard and is slow

        :returns: list of bytestrings
        """
        return self.cache_region.keys(pattern)

    def _hm_creator_wrapper(self, f, keys, *args):
        result = f(*args)
        store = {}
        for k in keys:
            if k in result:
                store[k] = result[k]
        store = self._serializer.serialize(store)
        return store

    def _hm_get(self, keys, data):
        data = self._serializer.deserialize(data)
        result = []
        for k in keys:
            if k in data:
                result.append(data[k])
        return result

    def _serialize_wrapper(self, f, *args, **kwargs):
        result = f(*args, **kwargs)
        return self._serializer.serialize(result)
