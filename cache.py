from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
import configuration

def get_cache(name):
	cache_opts = {
	    'cache.type': 'file',
	    'cache.data_dir': configuration.DATA_FOLDER+'cache',
	    'cache.lock_dir': configuration.DATA_FOLDER+'cache-lock'
	}

	cache_manager = CacheManager(**parse_cache_config_options(cache_opts))
	cache = cache_manager.get_cache(name, type='file', expire=60)
	return cache