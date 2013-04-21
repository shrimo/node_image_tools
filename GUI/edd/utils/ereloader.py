import sys

DEFAULT_RELOAD_PACKAGES = ['edd', 'example']


def unload(silent=True, packages=None):
    """
        performs unloading.
            * silent flag specifies if utility should print the unloaded modules
            * packages: array of packages to unload. specify None to use 
                defaults (DEFAULT_RELOAD_PACKAGES variable)
    """
    
    if packages is None:
        packages = DEFAULT_RELOAD_PACKAGES
        
    # construct reload list
    reloadList = []
    for i in sys.modules.keys():
        for package in packages:
            if i.startswith(package):
                reloadList.append(i)

    # unload everything
    for i in reloadList:
        try:
            if sys.modules[i] is not None:
                del(sys.modules[i])
                if not silent:
                    print "unloaded: %s " % str(i)
        except:
            print "failed to unload: %s " % str(i)


