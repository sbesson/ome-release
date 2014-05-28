OME release scripts
===================

These scripts are used during release to generate the downloads pages for each
release of OME, i.e.:
- [OMERO](http://downloads.openmicroscopy.org/omero)
- [Bio-Formats](http://downloads.openmicroscopy.org/bio-formats).

They are also used for each release of the following partner projects:
- [FLIMFit](http://downloads.openmicroscopy.org/flimfit)
- [u-track](http://downloads.openmicroscopy.org/u-track)
- [OMERO.webtagging](http://downloads.openmicroscopy.org/webtagging)
- [OMERO.searcher](http://downloads.openmicroscopy.org/searcher)
- [OMERO.figure](http://downloads.openmicroscopy.org/figure)
- [OMERO.mtools](http://downloads.openmicroscopy.org/mtools)

and some custom third-party packages:
- [Ice](http://downloads.openmicroscopy.org/ice).

Prior to the downloads page generation, the artifacts for the corresponding
release must have been copied under the root folder of the downloads page
published at `http://downloads.microscroscopy.org`.

Several environment variables can be configured for the downloads page
generation:

- `RELEASE` is the number of the upcoming release for example 4.4.7

- for the OMERO or the OMERO.searcher downloads page generation, `OMERO_BUILD`
  or `BUILDNUM` determines the build number of the job used to produce the
  release artifacts.

- for the OMERO.searcher downloads page generation, `PYSLIDVERSION` and
  `RICERCAVERSION` determine the version numbers of the pyslid and ricerca
  modules.

- for OMERO, OMERO.figure, OMERO.searcher and OMERO.webtagging,
  `ANNOUCEMENT_URL` specifies the URL of the announcement post to be used in
  the downloads page.

- for OMERO, `MILESTONE` is the name of the Trac milestone associated with the
  release.

To clean the target folder, run:

   ```
   make clean
   ```


To generate a downloads page, run the corresponding target (see table below),
e.g.:

  ```
  make omero
  ```

The output of the target will be located under the `content/` subfolder and
can be copied over to the release folder.


Name             | Target
-----------------|----------
OMERO            | omero
Bio-Formats      | bf
FLIMFit          | flimfit
u-track          | u-track
OMERO.webtagging | webtagging
OMERO.searcher   | searcher
OMERO.figure     | figure
OMERO.mtools     | mtools
Ice              | ice

Additional environment variables are defined in the scripts but should not
need to be modified:

- `RSYNC_PATH` and `PREFIX` are the root folder and the prefix of the folder
  where the release artifacts and downloads page.
