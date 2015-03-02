IMAGESDIR=images/
BASEDIR=$(CURDIR)
OUTPUTDIR=$(BASEDIR)/output
CONTENTDIR=$(BASEDIR)/content

omero: gen

bf: bfgen

libbioformats: libbioformatsgen

figure: figuregen

flimfit: flimfitgen

searcher: searchergen

utrack: utrackgen

mtools: mtoolsgen

webtagging: webtagginggen

ice: icegen

gen:
	mkdir -p $(CONTENTDIR)
	python gen.py $(RELEASE) $(OMERO_BUILD) > $(CONTENTDIR)/index.html
	cp -r $(IMAGESDIR) $(CONTENTDIR)

bfgen:
	mkdir -p $(CONTENTDIR)
	python bfgen.py $(RELEASE) > $(CONTENTDIR)/index.html
	cp -r $(IMAGESDIR) $(CONTENTDIR)

libbioformatsgen:
	mkdir -p $(CONTENTDIR)
	python libbioformatsgen.py $(RELEASE) > $(CONTENTDIR)/index.html
	cp -r $(IMAGESDIR) $(CONTENTDIR)

figuregen:
	mkdir -p $(CONTENTDIR)
	python figuregen.py $(RELEASE) > $(CONTENTDIR)/index.html
	cp -r $(IMAGESDIR) $(CONTENTDIR)

flimfitgen:
	mkdir -p $(CONTENTDIR)
	python flimfitgen.py $(RELEASE) > $(CONTENTDIR)/index.html
	cp -r $(IMAGESDIR) $(CONTENTDIR)

searchergen:
	mkdir -p $(CONTENTDIR)
	python searchergen.py $(RELEASE) $(PYSLIDVERSION) $(RICERCAVERSION) $(BUILDNUM) > $(CONTENTDIR)/index.html
	cp -r $(IMAGESDIR) $(CONTENTDIR)

utrackgen:
	mkdir -p $(CONTENTDIR)
	python utrackgen.py $(RELEASE) > $(CONTENTDIR)/index.html
	cp -r $(IMAGESDIR) $(CONTENTDIR)

mtoolsgen:
	mkdir -p $(CONTENTDIR)
	python mtoolsgen.py $(RELEASE) > $(CONTENTDIR)/index.html
	cp -r $(IMAGESDIR) $(CONTENTDIR)

webtagginggen:
	mkdir -p $(CONTENTDIR)
	python webtagginggen.py $(RELEASE) > $(CONTENTDIR)/index.html
	cp -r $(IMAGESDIR) $(CONTENTDIR)

icegen:
	mkdir -p $(CONTENTDIR)
	python icegen.py $(RELEASE) $(ICE_BUILD) $(SOURCE_SUFFIX) > $(CONTENTDIR)/index.html
	cp -r $(IMAGESDIR) $(CONTENTDIR)

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

.PHONY: html help clean regenerate serve devserver publish ssh_upload rsync_upload dropbox_upload ftp_upload s3_upload cf_upload github
