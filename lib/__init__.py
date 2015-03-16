
"""retriever.lib contains the core EcoData Retriever modules."""
<<<<<<< HEAD
import os

def set_proxy():
  proxies = ["https_proxy", "http_proxy", "ftp_proxy", "HTTP_PROXY", "HTTPS_PROXY", "FTP_PROXY"]
  for proxy in proxies:
    if os.getenv(proxy):
      if len(os.environ[proxy]) != 0:
        for i in proxies:
          os.environ[i] = os.environ[proxy]
        break

set_proxy()
=======
>>>>>>> 86ff72097da457fea60adaf5191513e3bb68622e
