all:
	make dl
	make data
	make cls
	make tex
	make bib
	make tex
	make tex
tex:
	pdflatex cv
bib:
	biber cv
dl:
	Rscript data/code/download.r
data:
	python3.8 data/code/main.py
cls:
	cp ~/dev/tex/pkg/nacv/nacv/nacv.cls .
clean:
	texclean .
.PHONY: data
