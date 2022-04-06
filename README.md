# Lazy Prices for CAC40

This project is influenced by a paper published in 2019 by 3 americans researchers[^1] which introduce the idea of stock prices predictions based on language changing in financial report. Throught this porject, we are trying to replicate this investment strategy on french listed companies in the CAC40 indice.

## Directory Architecture

```
root
  |_ dataset      ## .csv issu de la base de données
  |_ HMI
      |_ assets
  |_ Models
      |_ 0-main-script.py
      |_ 1-conversion-pdf-txt.php
      |_ 2-retraitement-txt.php
      |_ 3-nettoyageDocument.py
      |_ 4-analyse_sentiment.py
      |_ ...
  |_ Services  ## pour se connecter à la BD
      |_ lectureBD.php
      |_ transformer_BD_en_CSV.php
      |_ cotations_cac40.py
      |_ ...
  |_ txt-files
      |_ ...
README
```

### HMI

A directory where you can find all our front-end code.

### Models

This directory host our back-end treasure chests 💰🏴‍☠ !!

### text-files

A directory where all the financial documentation in .txt fornat is located.

--- 

[^1] Lauren Cohen, Christopher Malloy & Quoc Nguyen
