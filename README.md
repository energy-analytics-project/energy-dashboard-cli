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
pip install -U energy-dashboard-client
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

Verify that you have files:

```bash
$ tree -L 1
.
├── data
├── docs
├── LICENSE
├── notebooks
├── README.md
└── run.sh
```

Verify that `edc` works:

```bash
`$ edc --help
Usage: edc [OPTIONS] COMMAND [ARGS]...

  Command Line Interface for the Energy Dashboard. This tooling  collects
  information from a number of data feeds, imports that data,  transforms
  it, and inserts it into a database.

Options:
  --ed-dir TEXT                   Energy Dashboard directory (defaults to cwd)
  --log-level [CRITICAL|ERROR|WARNING|INFO|DEBUG]
  --help                          Show this message and exit.

Commands:
  clone    Clone energy-dashboard locally
  feed     Manage individual 'feed' (singular).
  feeds    Manage the full set of data 'feeds' (plural).
  license  Show the license (GPL v3).
  update   Update the submodules
```

Verify that you can list out the data feeds:

```bash
$ edc feeds list | head
data-oasis-atl-ruc-zone-map
data-oasis-cbd-nodal-grp-cnstr-prc
data-oasis-cmmt-rmr-dam
data-oasis-atl-sp-tie
data-oasis-prc-mpm-cnstr-cmp-dam
data-oasis-trns-curr-usage-all-all
data-oasis-ene-baa-mkt-events-rtd-all
data-oasis-ene-eim-transfer-limit-all-all
data-oasis-as-results-dam
data-oasis-ene-wind-solar-summary
```

Using `find` we can verify that we don't have any data files 
such as .zip, .xml, or .sql in the tree, but that we _do_ have
the state files:

```
$ find data/ | grep state | head
data/data-oasis-atl-ruc-zone-map/sql/state.txt
data/data-oasis-atl-ruc-zone-map/xml/state.txt
data/data-oasis-atl-ruc-zone-map/zip/state.txt
data/data-oasis-cbd-nodal-grp-cnstr-prc/sql/state.txt
data/data-oasis-cbd-nodal-grp-cnstr-prc/xml/state.txt
data/data-oasis-cbd-nodal-grp-cnstr-prc/zip/state.txt
data/data-oasis-cmmt-rmr-dam/sql/state.txt
data/data-oasis-cmmt-rmr-dam/xml/state.txt
data/data-oasis-cmmt-rmr-dam/zip/state.txt
data/data-oasis-atl-sp-tie/sql/state.txt
```

Now verify what databases you have downloaded...

```bash
$ find data/ | grep "\.db$" | head
data/data-oasis-atl-gen-cap-lst/db/data-oasis-atl-gen-cap-lst_00.db
data/data-oasis-sld-adv-fcst-rtd/db/data-oasis-sld-adv-fcst-rtd_01.db
data/data-oasis-sld-adv-fcst-rtd/db/data-oasis-sld-adv-fcst-rtd_00.db
data/data-oasis-sld-sf-eval-dmd-fcst/db/data-oasis-sld-sf-eval-dmd-fcst_00.db
data/data-oasis-sld-sf-eval-dmd-fcst/db/data-oasis-sld-sf-eval-dmd-fcst_03.db
data/data-oasis-sld-sf-eval-dmd-fcst/db/data-oasis-sld-sf-eval-dmd-fcst_01.db
data/data-oasis-sld-sf-eval-dmd-fcst/db/data-oasis-sld-sf-eval-dmd-fcst_05.db
data/data-oasis-sld-sf-eval-dmd-fcst/db/data-oasis-sld-sf-eval-dmd-fcst_04.db
data/data-oasis-sld-sf-eval-dmd-fcst/db/data-oasis-sld-sf-eval-dmd-fcst_02.db
data/data-oasis-ene-flex-ramp-dc-rtd-all/db/data-oasis-ene-flex-ramp-dc-rtd-all_00.db
```

I'll go over this in more detail below, but the reason there are multiple database files 
for a given data feed is because the feed has multiple formats (argh!) and I 
have not yet sorted out how to deal with that. More on this later.


## Use Cases

### Create Jupyter Notebook

TODO

This is what most of the users of this project want to do.

### Process Data Feeds

At a high level, a data feed is simply a url and some instructions for processing
it. The url is stored in the `manifest.json`, and the processing instructions
are stored in the `./src` directory. The `./src` directory contains python files
that handle downloading, parsing, constructing sql insert statements, and inserting
the data into a sqlite3 database. See the section on `Add New Data Feed` for more
details on the construction of a data feed.

Data feeds are processed in stages, and you can think of this as a vertical to
horizontal processing.

Horizontally, the process is very simple, we move from downloading a resource
through the stages until we insert the records into a database. The DATABASE 
is the final product.

```bash
DOWNLOAD -> EXTRACT -> PARSE -> SQL -> INSERT -> *DATABASE*
```

Vertically, the process is also very simple. Each stage processes all the artifacts
from the previous stage. However, we need this to be robust and re-startable. No idea
if that's a word, but it's a real thing. Machines crash, or you may need to stop
for some reason. I've also had the case where I had an error in the logic in a given
stage, and needed to start over from scratch. How do we do this here? Easy. A `state`
file:

```bash
DOWNLOAD        -> EXTRACT     -> PARSE SQL     -> INSERT       -> *DATABASE*
./zip/          ./xml/          ./sql/          ./db/
    state.txt       state.txt       state.txt       state.txt
```

Each state.txt contains a list of artifacts that have already been processed. 
Originally I called these: ./zip/downloaded.txt, ./xml/unzipped.txt, etc. But 
after working with this for a few days, it is easier to just `cat` out [dir]/state.txt
rather than remembering what each state file is named.

Each stage in the pipeline looks at the artifacts in the previous stage and compares
that list with the list of previously processed artifacts in it's `state.txt` file, and
then gives the delta of new files to the processing code.

So, to restart a given stage, you just delete the stage directory. This deletes all 
the generated artifacts *and* the state file. Voila. You are ready to start over.

Note: if you delete a stage, you may want to delete the subsequent stages, too.

Here's the command that does this for you:

```bash
edc feed [feed name] reset [stage]
```

And to process a given stage:

```bash
edc feed [feed name] proc [stage]
```

Here's the scenario. I've been writing the code for this project on my laptop. But it does
not have the horsepower to crunch all this data into the various sqlite databases in
a reasonable amount of time. So I'm firing up a desktop machine to perform the heavy
lifting. Here's what that process looks like. This is the same process any researcher 
that wanted to replicate my work would want to do.

Clone and update

```bash
mkdir foo
edc clone
cd energy-dashboard
edc update
```

At this point, we have the energy-dashboard project, but we don't want to re-download
all the previously downloaded files from their original source. In the case of CAISO
OASIS, that would simply take too long (I've calculated the upper bound as 152 days, 
though in reality it took about 3 weeks to download the resources here). Instead, we
can pull these previously downloaded artifacts from one of the public S3 buckets that
I've mirrored them on...

Example:

```bash
edc feed data-oasis-atl-ruc-zone-map s3restore
```

To grab the artifacts from the entire set of feeds:

```bash
edc feeds list | xargs -L 1 -I {} edc feed {} s3restore
```

Even though these are replicated on S3 and the download times are reasonable, you'll want
to grab a coffee, take a walk, etc. while the raw dataset downloads.

At the current time, only the original zip files will be downloaded.

    TODO: give the s3restore command more fidelity to control what get's restored. Currently
    it is hardwired to just download the zip files, but it's possible someone would want to
    select any of the stage artifacts [zip, xml, sql, db].

Ok, so you had coffee, took a walk, and stuff is still downloading. No problem. Pulling stuff
off of S3 is compressing what it took me weeks to accumulate down to hour(s). Let's continue...

We're downloading the feeds in this order, so the top few should have zip files:

```bash
$ edc feeds list | head
data-oasis-atl-ruc-zone-map
data-oasis-cbd-nodal-grp-cnstr-prc
data-oasis-cmmt-rmr-dam
data-oasis-atl-sp-tie
data-oasis-prc-mpm-cnstr-cmp-dam
data-oasis-trns-curr-usage-all-all
data-oasis-ene-baa-mkt-events-rtd-all
data-oasis-ene-eim-transfer-limit-all-all
data-oasis-as-results-dam
data-oasis-ene-wind-solar-summary
```

So let's process the first feed in the list and make sure everything in the tool chain works...

First, let's use the `invoke` commannd to execute arbitrary commands from that directory:

```bash
edc feed data-oasis-atl-ruc-zone-map invoke 'ls zip' | head

oasis_SZ_q_ATL_RUC_ZONE_MAP_sdt_20130101T07_00-0000_edt_20130102T07_00-0000_v_1.zip
oasis_SZ_q_ATL_RUC_ZONE_MAP_sdt_20130102T07_00-0000_edt_20130103T07_00-0000_v_1.zip
oasis_SZ_q_ATL_RUC_ZONE_MAP_sdt_20130103T07_00-0000_edt_20130104T07_00-0000_v_1.zip
oasis_SZ_q_ATL_RUC_ZONE_MAP_sdt_20130104T07_00-0000_edt_20130105T07_00-0000_v_1.zip
oasis_SZ_q_ATL_RUC_ZONE_MAP_sdt_20130105T07_00-0000_edt_20130106T07_00-0000_v_1.zip
oasis_SZ_q_ATL_RUC_ZONE_MAP_sdt_20130106T07_00-0000_edt_20130107T07_00-0000_v_1.zip
oasis_SZ_q_ATL_RUC_ZONE_MAP_sdt_20130107T07_00-0000_edt_20130108T07_00-0000_v_1.zip
oasis_SZ_q_ATL_RUC_ZONE_MAP_sdt_20130108T07_00-0000_edt_20130109T07_00-0000_v_1.zip
oasis_SZ_q_ATL_RUC_ZONE_MAP_sdt_20130109T07_00-0000_edt_20130110T07_00-0000_v_1.zip
oasis_SZ_q_ATL_RUC_ZONE_MAP_sdt_20130110T07_00-0000_edt_20130111T07_00-0000_v_1.zip
```

```bash
edc feed data-oasis-atl-ruc-zone-map invoke 'ls zip' | wc

    2451    2450  205727
```

Cool, so we have 2451 zip files to play with. That should match the number of lines
in the ./xml/state.txt file:

```bash
edc feed data-oasis-atl-ruc-zone-map invoke 'cat zip/state.txt' | wc

    2450    2449  355106
```

Close enough. Let's try to generate the database, which is done
with the `proc` command:

```bash
edc feed data-oasis-atl-ruc-zone-map proc --help
Usage: edc feed proc [OPTIONS] STAGE

  Process the feed through the stage procesing files in the './src'  directory, in lexical order.

  Stages are: ['download', 'unzip', 'parse', 'insert']

Options:
  --help  Show this message and exit.
```

TODO: add the 'all' stage and the 'save' stage.

Let's run through them one at a time to make sure everything
works as expected...


```bash
edc feed data-oasis-atl-ruc-zone-map proc download

{"ts":"09/18/2019 01:33:16 PM", "msg":{"src": "data-oasis-atl-ruc-zone-map", "action": "download", "url": "http://oasis.caiso.com/oasisapi/SingleZip?queryname=ATL_RUC_ZONE_MAP&startdatetime=20190916T07:00-0000&enddatetime=20190917T07:00-0000&version=1", "file": "oasis_SZ_q_ATL_RUC_ZONE_MAP_sdt_20190916T07_00-0000_edt_20190917T07_00-0000_v_1.zip"}}
```

Ok, so we downloaded a single file. This make sense. I ran this yesterday so I'd only expect to see a single new file. Today is:

```bash
date

Wed Sep 18 13:34:51 PDT 2019
```

The start date on that download is: sdt_20190916T07_00-0000
The end date is: edt_20190917T07_00-0000

'sdt' : abbreviation for 'start date'
'edt' : abbreviation for 'end date'

So today is 9/18, so the latest it can grab a report for is 9/17. Looks good.

What got modified on the local system?

```bash
edc feed data-oasis-atl-ruc-zone-map invoke 'git status'

HEAD detached at ca440b3
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

	modified:   zip/state.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

Notice that the zip file, which is in the ./zip directory, is not showing up. In 
fact it is explicitly excluded from the git repository. So are the other intermediate
files like .sql and .xml. These files are expected to be replicated to the S3 buckets,
but not stored in the git repository. Only the sqlite3 .db files are stored in 
git using git-lfs, and even that might change in the future if it's a pain. Time will tell.


So what changed in the zip/state.txt file?

```bash
$ edc feed data-oasis-atl-ruc-zone-map invoke 'git diff'

diff --git a/zip/state.txt b/zip/state.txt
index 92e0f63..b394e8f 100644
--- a/zip/state.txt
+++ b/zip/state.txt
@@ -2447,3 +2447,4 @@ http://oasis.caiso.com/oasisapi/SingleZip?queryname=ATL_RUC_ZONE_MAP&startdateti
 http://oasis.caiso.com/oasisapi/SingleZip?queryname=ATL_RUC_ZONE_MAP&startdatetime=20190913T07:00-0000&enddatetime=20190914T07:00-0000&version=1
 http://oasis.caiso.com/oasisapi/SingleZip?queryname=ATL_RUC_ZONE_MAP&startdatetime=20190914T07:00-0000&enddatetime=20190915T07:00-0000&version=1
 http://oasis.caiso.com/oasisapi/SingleZip?queryname=ATL_RUC_ZONE_MAP&startdatetime=20190915T07:00-0000&enddatetime=20190916T07:00-0000&version=1
+http://oasis.caiso.com/oasisapi/SingleZip?queryname=ATL_RUC_ZONE_MAP&startdatetime=20190916T07:00-0000&enddatetime=20190917T07:00-0000&version=1
```

*The zip/state.txt file contains the urls for the artifacts that have been downloaded.*

Let's move on to the next stage...

```bash
edc feed data-oasis-atl-ruc-zone-map proc unzip

$ edc feed data-oasis-atl-ruc-zone-map invoke 'ls xml'

20190916_20190917_ATL_RUC_ZONE_MAP_N_20190918_13_33_16_v1.xml
state.txt
```

There is only 1 file in the ./xml directory. This is because the `s3restore` command only restored the
zip file artifacts. Then, the `proc unzip` command only processed the new file that's not in the
./xml/state.txt file. Normally, this is fine, but right now, we want to re-run the entire pipeline from
scratch (but using the zip files we restored from s3). What to do? Reset the stage(s)...

```bash
$ edc feed data-oasis-atl-ruc-zone-map reset --help
Usage: edc feed reset [OPTIONS] STAGE

  !!!USE WITH CAUTION!!!

  Reset a stage. This is a destructive action, make backups first!. This
  will delete the stage directory, including the state file and all the
  processed resources.

  !!!USE WITH CAUTION!!!

  Stages are: ['download', 'unzip', 'parse', 'insert']

Options:
  --confirm / --no-confirm
  --help
```

In this case we want to reset the last 3 stages...

```bash
edc feed data-oasis-atl-ruc-zone-map reset unzip
About to delete: /home/toddg/proj/energy-dashboard/data/data-oasis-atl-ruc-zone-map/xml. Do you want to continue? [y/N]: y
/home/toddg/proj/energy-dashboard/data/data-oasis-atl-ruc-zone-map/xml


edc feed data-oasis-atl-ruc-zone-map reset parse
About to delete: /home/toddg/proj/energy-dashboard/data/data-oasis-atl-ruc-zone-map/sql. Do you want to continue? [y/N]: y
/home/toddg/proj/energy-dashboard/data/data-oasis-atl-ruc-zone-map/sql


edc feed data-oasis-atl-ruc-zone-map reset insert
About to delete: /home/toddg/proj/energy-dashboard/data/data-oasis-atl-ruc-zone-map/db. Do you want to continue? [y/N]: y
{"ts":"09/18/2019 01:44:54 PM", "msg":{"name": "edl.cli.feed", "method": "reset", "path": "/home/toddg/proj/energy-dashboard", "feed": "data-oasis-atl-ruc-zone-map", "target_dir": "/home/toddg/proj/energy-dashboard/data/data-oasis-atl-ruc-zone-map/db", "ERROR": "failed to remove target_dir", "exception": "[Errno 2] No such file or directory: '/home/toddg/proj/energy-dashboard/data/data-oasis-atl-ruc-zone-map/db'"}}
```

TODO: fix this error message when the directory does not exist.

Let's examine what the `status` of this feed is now:

```bash
edc feed data-oasis-atl-ruc-zone-map status

feed name,downloaded,unzipped,parsed,inserted
data-oasis-atl-ruc-zone-map,2450,0,0,0
```

We have 2450 records in the zip/state.txt file to play with.

Let's re-unzip and see what happens to the state:

```bash
edc feed data-oasis-atl-ruc-zone-map proc unzip

edc feed data-oasis-atl-ruc-zone-map status

feed name,downloaded,unzipped,parsed,inserted
data-oasis-atl-ruc-zone-map,2450,2450,0,0
```

Ok, so now we have 2450 downloaded zip files and 2450 extracted xml files (as tracked
by the respective state files). Onwards...

```bash
edc feed data-oasis-atl-ruc-zone-map proc parse

{"ts":"09/18/2019 01:49:30 PM", "msg":{"src": "data-oasis-atl-ruc-zone-map", "action": "parse_file", "infile": "20150201_20150202_ATL_RUC_ZONE_MAP_N_20190811_04_45_40_v1.xml", "outfile": "/home/toddg/proj/energy-dashboard/data/data-oasis-atl-ruc-zone-map/sql/20150201_20150202_ATL_RUC_ZONE_MAP_N_20190811_04_45_40_v1.sql", "total_ddl": 8, "total_sql": 7688}}
{"ts":"09/18/2019 01:49:34 PM", "msg":{"src": "data-oasis-atl-ruc-zone-map", "action": "parse_file", "infile": "20150717_20150718_ATL_RUC_ZONE_MAP_N_20190811_05_00_30_v1.xml", "outfile": "/home/toddg/proj/energy-dashboard/data/data-oasis-atl-ruc-zone-map/sql/20150717_20150718_ATL_RUC_ZONE_MAP_N_20190811_05_00_30_v1.sql", "total_ddl": 8, "total_sql": 7688}}
```

Now this is going to take awhile to process all of the xml files and generate these sql files. While that's running, let's take a look at 
a generated .sql file:





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

