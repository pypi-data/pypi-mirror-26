## pubpub

A package to turn Jupyter ipynb files into pdf files

```bash
pubpub --help
```

```bash
pubpub run \
      -f "./book_drafts/Chapter 1.ipynb" \
      -f "./book_drafts/Chapter 2.ipynb" \
      -f "./book_drafts/Chapter 3.ipynb" \
      -f "./book_drafts/Chapter 4.ipynb" \
      -o ./print.pdf \
      -v udeeply \
      --template ./fullstack.tplx
```

## How to run

Install the required dependencies:

```bash
# ubuntu
sudo apt-get update -yq && sudo apt-get install -yq texlive-latex-extra texlive-latex-base
```

## Install pubpub

```bash
pip install --upgrade pubpub
```



