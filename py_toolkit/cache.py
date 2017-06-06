# -*- coding: utf-8 -*-

"""
Provide a simple cache framework, 

A user implement a subclass of Cache implementing the on_miss function, to load data into the cache. 

After that they simply call lookup to get data from the cache, loading it on demand as needed. 

Cache retention policy is set during construction to allow either item expiry a set time after loading, or a set time 
after the last read. 

Items are refreshed if they are older than the expiry time and still present in the cache. Items left in the cache 
beyond their expiry time are removed by a pruner thread that runs on an interval set at construction time. 

The cache is thread safe

The goal of the CacheMonitor thread is to free memory, not ensure cache objects are refreshed in a timely fashion, if 
an existing key is expired it is refreshed on lookup, the pruning effort yields after each key is released in order to 
minimise the amount of time it is blocking other threads that have actual work to do. 
"""

import time
import threading

class CacheEntry(object):
    """
    CacheEntry that can track it's own access time
    """
    def __init__(self, value):
        self.value = value
        self.accessed = time.time()

    def get_value(self, update_accessed):
        if update_accessed:
            self.accessed = time.time()
        return self.value

    def expired(self, now, max_age):
        return now > (self.accessed + max_age)

class CacheMonitor(threading.Thread):
    def __init__(self, cache, prune_interval):
        """
        Starts a background thread to scan the cache at the specified interval and remove any expired entries. 
        :param cache: 
        :param prune_interval: 
        """
        super(CacheMonitor, self).__init__()
        self.daemon = True
        self.cache = cache
        self.prune_interval = prune_interval

    def run(self):
        while True:
            prune_time = time.time()
            # Get a list of items that have potentially expired, without the lock
            expired_items = [k for k,v in filter(lambda (key,value) : value.expired(prune_time,
                                                                                    self.cache.expiry_time_secs),
                                                 self.cache.cache_items.viewitems())]
            for k in expired_items:
                # For each potential, get the lock, check the key still exists, check it's still expired
                # if it's still viable for expiration then delete the key
                with self.cache.lock:
                    if k in self.cache.cache_items and self.cache.cache_items[k].expired(prune_time, self.cache.expiry_time_secs):
                        del self.cache.cache_items[k]
                # Yield to any actual activity
                time.sleep(0)
            # Sleep until the next interval is due, or continue if we took too long (really unlikely)
            time.sleep(max(0, self.prune_interval - (time.time() - prune_time)))

class Cache(object):
    def __init__(self, expiry_time_secs=1800, refresh_expiry_on_read=False, prune_interval=600):
        """
        Create a cache instance, with an expiry time, default of 30 minutes, and specify if reading the record extends
        the expiry time or not. Default behaviour is to not extend expiry times on reading. And specify the interval 
        of the cache pruning thread that removes items that haven't been accessed in along time
        :param expiry_time_secs: 
        :param refresh_expiry_on_read: 
        :param prune_interval: Number of seconds between pruning thread loops
        """
        self.refresh_expiry_on_read = refresh_expiry_on_read
        self.expiry_time_secs = expiry_time_secs
        self.cache_items = {}
        self.lock = threading.RLock()
        self.prune_thread = CacheMonitor(self, prune_interval)
        self.prune_thread.start()

    def __len__(self):
        return len(self.cache_items)

    def drop(self, key):
        with self.lock:
            self.cache_items.pop(key, None)

    def lookup(self, key):
        """
        Lookup key from the cache, if not present it will be loaded, if present but expired it will be reloaded, 
        otherwise it is returned directly from the cache
        :param key: 
        :return: 
        """
        with self.lock:
            now = time.time()
            if not key in self.cache_items:
                self.cache_items[key] = CacheEntry(self.on_miss(key))
            elif self.cache_items[key].expired(now, self.expiry_time_secs):
                self.cache_items[key] = CacheEntry(self.on_miss(key))
            return self.cache_items[key].get_value(self.refresh_expiry_on_read)

    def on_miss(self, key):
        """
        Instance implemented on_miss, load the entry for the key, implementation should make the decision about whether 
        to return a default value, the original key, or raise an error in the event the key can't be found. 
        :param key:  
        :return: 
        """
        raise NotImplementedError("Missing on_miss, please implement me otherwise I can't load any data into my cache")