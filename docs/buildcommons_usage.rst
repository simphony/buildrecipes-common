Usage of buildcommons in a distribution
---------------------------------------

Buildcommons provides convenience routines to create the EDM egg. In the following, we assume your 
distribution has a traditional ``python setup.py install`` approach to deployment.

1. copy the files under ``templates`` to the root of your distribution directory. 
   There are three files

    - edmsetup.py: similar to a setup, but packages the egg. It provides the command ``egg`` to build the EDM egg,
      and ``upload_egg`` to send the egg to the EDM server. You cannot perform this last operation unless you have
      valid credentials. 

    - endist.dat: provides information to edm to repack the egg. In contains the package dependencies, the additional
      files to package, etc.
   
    - packageinfo.py: contains python vars for NAME, VERSION and BUILD. The first two are self-explanatory and should
      be reused in your setup.py for deduplication. The third is the egg build number. It is incremented when you want
      to upload the same version a second time (for example, you noticed you specified incorrect dependencies).

2. (if needed) modify the above files to your specific needs. This varies from distribution to distribution.
   
