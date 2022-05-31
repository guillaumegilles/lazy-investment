# Lazy Investments

Lazy investment is a *Machine Learning project* influenced by a paper published in 2019 by three American researchers, Lauren Cohen, Christopher J. Malloy, and Quoc Nguyen. They show that when firms make an active change in their reporting practices, this conveys an important signal about future firm operations. Changes to the language and construction of financial reports also have strong implications for firms’ future returns. Changes in language referring to the executive (CEO and CFO) team, regarding litigation, or in the risk factor section of the documents are especially informative for future returns.

Based on these researches, this Machine Learning project is designed to:

1. Collect firms' financial reports;
2. Process and clean data to generate CSV files;
3. Train Supervised Machine Learning algorithms to predict investment opportunities.

**Through a web-based interface, Lazy Investissement is a tool designed to help investors to make better financial decisions.**

### Table of contents

- [Lazy Investments](#lazy-investments)
  - [Directories Architecture](#directories-architecture)
    - [Dataset](#dataset)
    - [HMI](#hmi)
    - [Model](#model)
    - [Services](#services)
    - [text-files](#text-files)

## Directories Architecture

```shell
root
  |_ Dataset
  |_ HMI
      |_ assets
  |_ Models
  |_ Services
  |_ txt-files
README
```

[Back to the top](#lazy-investments)

### Dataset

Where `.csv` files storing all our data used in our models are located.

### HMI

A directory where you can find all the front-end source code.

### Models

This directory host our back-end treasure chests 💰🏴‍☠ !!

### Services

Source code to connect to the database of the project.

### text-files

A directory where all the financial documentation in .txt fornat is located.
