"""retriever.lib contains the core EcoData Retriever modules."""

import os

def proxy_function():
    proxies = ["http_proxy","https_proxy","ftp_proxy","HTTP_PROXY","HTTPS_PROXY","FTP_PROXY"]
    for proxy in proxies:
        if os.getenv(proxy):
            if len(os.environ[proxy]) != 0:
                for i in proxies:                                # Setting the other proxies of the system.
                    os.environ[i] = os.environ[proxy]
                break


