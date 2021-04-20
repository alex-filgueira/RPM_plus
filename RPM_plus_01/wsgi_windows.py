import os
import sys
import site
from django.core.wsgi import get_wsgi_application

# add python site packages, you can use virtualenvs also
site.addsitedir("C:/Program files/python36/Lib/site-packages")

# Add the app's directory to the PYTHONPATH 
sys.path.append('D:/Datos_Alexandre/Software/ws_Tools/ReleasePlanMker_Plus/projects/RPM_plus/RPM_plus_01') 
sys.path.append('D:/Datos_Alexandre/Software/ws_Tools/ReleasePlanMker_Plus/projects/RPM_plus/RPM_plus_01/RPM_plus_01')  

os.environ['DJANGO_SETTINGS_MODULE'] = 'RPM_plus_01.settings' 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RPM_plus_01.settings")  
 
application = get_wsgi_application()


