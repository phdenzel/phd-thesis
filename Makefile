SHELL := /bin/bash

main:
	pdflatex main \
	&& makeindex main \
	&& biber main \
	&& pdflatex main \
	&& pdflatex main

.PHONY: main

clean:
	rm -f *.aux *.blg *.log *.out *.bcf *.fdb_latexmk *.fls *.run.xml *.synctex.gz *.glo *.idx *.ilg *.ind *.nlo *.lof *.lot *.toc
