# Energy Dashboard Command Line Interface (edc)

Command Line Interface for the Energy Dashboard.

!!!PRE-ALPHA!!!

While this is the master branch, this project is not released yet. Stand by...

All examples commands, install, etc. assume a linux (ubuntu) installation
and use the `apt` package manager, etc.

## Prerequisites

### Install basic deps

```bash
sudo apt install parallel
sudo apt install build-essential
sudo apt install git
```

### Install git-lfs (git large file store)

*git-lfs* is used for storing the database files, which are basically binary blobs
that are updated periodically. Rather than store all the db blob revisions in the 
git repository, which would bloat it considerably, the db blobs are offloaded
to git-lfs.

For installation instructions, go here:

* https://git-lfs.github.com/

Example:

```bash
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
```

### Install conda/anaconda

You don't strictly _need_ anaconda for this toolchain to work. If you prefer
mucking with python virtualenv directly, then go for it. I find that anaconda
works really well with other parts of this toolchain, namely Jupyter Notebooks. 
All the examples and documentation will assume you are using anaconda.

Example, see the website for current instructions:

* https://www.anaconda.com/distribution/#download-section

Example:

```bash
wget https://repo.anaconda.com/archive/Anaconda3-2019.07-Linux-x86_64.sh
chmod +x Anaconda3-2019.07-Linux-x86_64.sh 
./Anaconda3-2019.07-Linux-x86_64.sh 
```

## Installation

This webpage has a great tutorial on how to use conda. It's what I use
when I forget the commands and concepts:

* https://geohackweek.github.io/Introductory/01-conda-tutorial/

First, create a conda environment, it can be named anything, I'll call
this `edc-cli`:

```bash
conda update conda
conda create -n edc-cli python=3 numpy jupyter pandas
conda activate edc-cli
```

Then install the energy-dashboard-client:

```bash
pip install energy-dashboard-client
```


## Setup

The energy-dashboard-client has two commands to get you up and running with an
energy-dashboard:

* clone : this will literally use git to clone the energy-dashboard repo to your local machine
* update : this will pull down all the submodules to your local machine

Note: if you only want a subset of the submodules installed on your local machine, then you
can use the `git submodule deinit data/[name-of-submodule-to-remove]`.

As always, let me know if you need better tooling around this or any other aspect of this project.

```bash
mkdir foo
cd foo
edc clone
cd energy-dashboard
edc update
```

At this point you should have a working environment:

```
foo/energy-dashboard/data/[...about ~91 submodules here ...]
```

## Use Cases

### Create Jupyter Notebook

TODO

### Process Data Feeds



### Add New Data Feed

TODO



## Show Help


## edc

```bash
Usage: edc [OPTIONS] COMMAND [ARGS]...

  Command Line Interface for the Energy Dashboard. This tooling  collects
  information from a number of data feeds, imports that data,  transforms
  it, and inserts it into a database.

Options:
  --config-dir TEXT     Config file directory
  --debug / --no-debug  Enable debug logging
  --help                Show this message and exit.

Commands:
  config   Manage config file.
  feed     Manage individual 'feed' (singular).
  feeds    Manage the full set of data 'feeds' (plural).
  license  Show the license (GPL v3).
```

### config

```bash
Usage: edc config [OPTIONS] COMMAND [ARGS]...

  Manage config file.

Options:
  --help  Show this message and exit.

Commands:
  show    Show the config
  update  Update config
```

### feed

```bash
Usage: edc feed [OPTIONS] COMMAND [ARGS]...

  Manage individual 'feed' (singular).

Options:
  --help  Show this message and exit.

Commands:
  archive    Archive feed to tar.gz
  create     Create new feed
  download   Download from source url
  invoke     Invoke a shell command in the feed directory
  proc       Process a feed through the stages
  reset      Reset feed to reprocess stage
  restore    Restore feed from tar.gz
  s3archive  Archive feed to S3 bucket
  s3restore  Restore feed zip files from from S3 bucket
  status     Show feed status
```

### feeds

```bash
Usage: edc feeds [OPTIONS] COMMAND [ARGS]...

  Manage the full set of data 'feeds' (plural).

Options:
  --help  Show this message and exit.

Commands:
  list    List feeds
  search  Search feeds (NYI)
```

### license

```bash
    
    edc : Energy Dashboard Command Line Interface
    Copyright (C) 2019  Todd Greenwood-Geer (Enviro Software Solutions, LLC)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    
```


##Usage

### Examples

```bash
edc feed invoke data-oasis-atl-lap-all "git st"
edc feed invoke data-oasis-atl-lap-all "ls"
edc feed invoke data-oasis-atl-lap-all "cat manifest.json"
edc feed invoke data-oasis-atl-lap-all "head manifest.json"
edc feeds list
edc feeds list | grep atl
edc feeds list | grep atl | edc feed invoke "head manifest.json"
edc feeds list | grep atl | edc feed invoke "head manifest.json" -
edc feeds list | grep atl | xargs -L 1 -I {} edc feed invoke {} "head manifest.json"
edc feeds list | grep atl | xargs -L 1 -I {} edc feed invoke {} "jq . < manifest.json"
edc feeds list | grep atl | xargs -L 1 -I {} edc feed invoke {} "jq .url < manifest.json"
edc feeds list | grep mileage | xargs -L 1 -I {} edc feed invoke {} "echo {}; sqlite3 db/{}.db 'select count(*) from oasis'"
edc feeds list | grep atl | xargs -L 1 -I {} edc feed invoke {} "jq .url < manifest.json"
edc feeds list| xargs -L 1 -I {} edc feed invoke {} "echo {}; sqlite3 db/{}.db 'select count(*) from oasis'"
edc feeds list | grep atl | xargs -L 1 -I {} edc feed status {}
edc feeds list | grep atl | xargs -L 1 -I {} edc feed status --header {}
edc feeds list | grep atl | xargs -L 1 -I {} edc feed status --header {}
edc feeds list | grep mileage | xargs -L 1 -I {} edc feed status --header {}
edc feeds list | xargs -L 1 -I {} edc feed invoke {} "./src/10_down.py"
edc feed archive data-oasis-as-mileage-calc-all
edc feed archive data-oasis-as-mileage-calc-all | xargs -L 1 -I {} tar -tvf {}
edc feed reset data-oasis-as-mileage-calc-all --stage xml --stage db
edc feed s3restore data-oasis-as-mileage-calc-all --outdir=temp --service=wasabi
edc feed s3archive data-oasis-as-mileage-calc-all
```

### Onboarding

Some quick notes on how I onboarded 'data-oasis-as-mileage-calc-all':

```bash
edc feed proc data-oasis-as-mileage-calc-all
edc feed s3archive data-oasis-as-mileage-calc-all --service wasabi
edc feed s3archive data-oasis-as-mileage-calc-all --service digitalocean
edc feed status data-oasis-as-mileage-calc-all --header
edc feed invoke data-oasis-as-mileage-calc-all "git st"
edc feed invoke data-oasis-as-mileage-calc-all "git log"
edc feed invoke data-oasis-as-mileage-calc-all "git show HEAD"
```

## Author
Todd Greenwood-Geer (Enviro Software Solutions, LLC)

## Notes
This project uses submodules, and this page has been useful:
https://github.blog/2016-02-01-working-with-submodules/

