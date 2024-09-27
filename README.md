# Funcnodes Module

This helper tool makes it easy to generate new modules for [Funcnodes](https://github.com/Linkdlab/funcnodes).

## Installation
```bash
pip install funcnodes-module
```

## Usage

### Create a New Module
To create a new module, simply run:
```bash
funcnodes-module new <name_of_your_package>
```
This will set up the required folder structure with template files and even prepare everything for publishing to GitHub (which is recommended).

### Update a Module
Funcnodes is still in early development, and new features are added regularly.  
To update your module, start a command line in the module folder and run:
```bash
funcnodes-module update
```

### Upgrade Templates
When new template options are added, `funcnodes-module` needs to be updated.  
This can be done via the standard pip upgrade path or through a self-updating method:
```bash
funcnodes-module upgrade
```

### Add Third-Party Notices
We wanted a simple way to automatically give credit to other packages we use. Keeping third-party notices up to date can be time-consuming, so we implemented:
```bash
funcnodes-module gen_third_party_notice
```
This command automatically generates the corresponding third-party notices.  
**IMPORTANT**: This is not legally valid as it may not cover every package and/or license. [IANAL](https://en.wikipedia.org/wiki/IANAL) applies here.
