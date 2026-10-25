$pdf_mode = 1;         

$out_dir = '../build';

$pdflatex = 'pdflatex -interaction=nonstopmode -file-line-error -synctex=1 %O %S';

# Запускать BibTeX когда нужно и удалять .bbl при `latexmk -C`
$bibtex_use = 2;

$clean_ext = 'synctex.gz';