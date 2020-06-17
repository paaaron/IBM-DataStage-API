# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from config import *
from ibm_datastage_api import DSAPI

hproj = None
hjob  = None

dsapi = DSAPI()

try:
   res, err = dsapi.DSLoadLibrary(API_LIB_FILE)
   if err:
      raise Exception("Loading the library failed: {}".format(err))

   print("Setting the parameters to connect to DataStage server")
   dsapi.DSSetServerParams(DS_DOMAIN_NAME, DS_USER_NAME, DS_PASSWORD, DS_SERVER)

   print("The list of available projects located on the server:")
   res, err = dsapi.DSGetProjectList()
   if err:
      raise Exception("Can't get the list of the projects: {}".format(err))

   print(res)

   DS_NEW_PROJECT_NAME = 'dsdev_api_project'

   print("Creating the project {}".format(DS_NEW_PROJECT_NAME))
   res, err = dsapi.DSAddProject(DS_NEW_PROJECT_NAME)
   if err:
      raise Exception("Can't create the project {}: {}".format(DS_NEW_PROJECT_NAME, err))

   print("The list of available projects located on the server:")
   res, err = dsapi.DSGetProjectList()
   if err:
      raise Exception("Can't get the list of the projects: {}".format(err))

   print(res)

   dsapi.DSUnloadLibrary()

except Exception as e:
   print("Runtime error: {}".format(str(e)))

   if hjob:
      print("Deblocking the job")
      dsapi.DSUnlockJob(hjob)

      print("Closing the job")
      dsapi.DSCloseJob(hjob)
      hjob = None

   if hproj:
      print("Closing the project")
      dsapi.DSCloseProject(hproj)
      hproj = None

   dsapi.DSUnloadLibrary()

print("Exit.")