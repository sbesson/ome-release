OME release scripts
==================

These scripts are used during the OMER release to 1 - copy the build
artifacts to cvs.openmicroscopy.org and generate the
[OMERO](http://www.openmicroscopy.org/site/products/omero/downloads) and
[Bio-Formats](http://www.openmicroscopy.org/site/products/bio-formats/downloads)
download pages for each release.

Prerequisites
-------------

* Merge all PRs related to the current release

* Update all  submodules using the OMERO-submods-{stable, develop} jobs.

* Tag the VERSION of openmicroscopy.git and bioformats.git

	```
	git tag -u "Josh Moore (Glencoe Software, Inc.) <you@example.com>" -m "Release version VERSION" v.VERSION
	````

* Push the tag and the branch to GitHub

	```
	git push origin v.4.4.4 develop
	```

* After the BIOFORMATS-{stable, trunk}, OMERO-{stable,trunk} and
OMERO-{stable,trunk}-ice34 builds pass, promote them with "RELEASE".
This will transfer the files under /ome/data-repo/releases/$BUILD_NAME/$BUILD_NUMBER

Preparation
-----------

Run [prep.sh](prep.sh) as hudson. This performs the following:

- Create a omero/VERSION and a bioformats/RELEASE folders
under SNAPSHOT_PATH.

- Symlink all the promoted OMERO artifacts to omero/VERSION/

- Rename the OVA to include the version number (e.g. VERSION) and be sure to
modify the MD5 file to use the new name.

- Symlink all the promoted Bio-Formats artifacts to bioformats/VERSION/

Downloads page generation
-------------------------

* To generate the OMERO downloads page, run [gen.py](gen.py)::

	```
	python gen.py VERSION bBUILDNUMBER [bBUILDNUMBER_ICE34]
	```

* To generate the Bio-Formats downloads page, run [bfgen.py](bfgen.py)::

	```
     python bfgen.py VERSION bBUILDNUMBER
	```
