import click
import json
import os
import json
import subprocess
import sqlite3
from jinja2 import Environment, PackageLoader, select_autoescape
from shutil import make_archive, rmtree

@click.group()
@click.option('--config-dir', default="~/.config/energy-dashboard", help="config file directory")
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, config_dir, debug):
    """
    Command Line Interface for the Energy Dashboard. This tooling 
    collects information from a number of data feeds, imports that data, 
    transforms it, and inserts it into a database.
    """
    ctx.obj = {
            'config-dir': config_dir,
            'debug': debug
            }

#------------------------------------------------------------------------------
# License
#------------------------------------------------------------------------------
@cli.command()
def license():
    """
    Show the license (GPL v3).
    """
    print("""    
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
    """)

#------------------------------------------------------------------------------
# Configure
#------------------------------------------------------------------------------
@cli.group()
@click.pass_context
def config(ctx):
    pass

@config.command('update', short_help="Update config")
@click.option('--path',                 '-p',   help="Path to Energy Dashboard, e.g. ~/repos/energy-dashboard")
@click.option('--verbose/--no-verbose',         help="Enable/disable debug logging", default=False)
@click.pass_context
def config_update(ctx, path, verbose):
    """
    Configure the CLI

    path : path to the energy dashboard
    """
    debug = ctx.obj['debug']
    config_dir = os.path.expanduser(ctx.obj['config-dir'])
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        if debug: click.echo("created config dir: %s" % config_dir)
    cfg_file_path = os.path.join(config_dir, 'energy-dashboard-client.config')
    if os.path.exists(cfg_file_path):
        config = Config.load(cfg_file_path)
        if debug: click.echo("loaded config file: %s" % cfg_file_path)
    else:
        config = Config()
        if debug: click.echo("loaded empty config")
    # override prev values
    config._debug   = verbose
    config._ed_path = path
    config.save()

@config.command('show')
@click.pass_context
def config_show(ctx):
    """
    Show the config
    """
    cfg = Config.from_ctx(ctx)
    click.echo(cfg)

#------------------------------------------------------------------------------
# Feeds (plural)
#------------------------------------------------------------------------------
@cli.group()
@click.pass_context
def feeds(ctx):
    """
    Manage the full set of data 'feeds' (plural).
    """
    pass

@feeds.command('list', short_help='list feeds')
@click.pass_context
def feeds_list(ctx):
    """
    List feeds by name. Feeds are implemented as submodules under the energy-dashboard/data directory.
    """
    cfg = Config.from_ctx(ctx)
    items = os.listdir(os.path.join(cfg.ed_path(), "data"))
    for item in items:
        click.echo(item)

@feeds.command('search', short_help='search feeds (NYI)')
def feeds_search():
    pass

#------------------------------------------------------------------------------
# Feed (singular)
#------------------------------------------------------------------------------
@cli.group()
def feed():
    """
    Manage individual 'feed' (singular).
    """
    pass

@feed.command('create', short_help='create new feed')
@click.argument('name')
@click.argument('maintainer')
@click.argument('company')
@click.argument('email')
@click.argument('url')
@click.option('--start-date-tuple', '-sdt', 
        help="Start date for the data feed (YYYY,MM, DD), e.g. (2013, 1,1)", 
        default=(2013,1,1))
@click.pass_context
def feed_create(ctx, name, maintainer, company, email, url, start_date_tuple):
    """
    Create a new data feed from a template.

    Arguments:

        name        : name of the data feed, lowerase, with dashes and no special chars
        maintainer  : name of the feed curator
        company     : name of the company or organization the owner belongs to
        url         : data feed url, with replacement strings in url (see below)

    URL Replacements:
        
        The default tooling generates a URL for each day between the _START_
        date, and today. This makes it trivial to download daily resources from
        a target URL for the past N years.  Other use cases are supported, too.
        The default tooling can be overriden in the generated `src/10_down.py`
        script. 
        
        For the default behaviour, ensure that the data feed URL has the
        following replacement strings:

        _START_
        _END_

        Example:

            "url": "http://oasis.caiso.com/oasisapi/SingleZip?queryname=AS_MILEAGE_CALC&anc_type=ALL&startdatetime=_START_T07:00-0000&enddatetime=_END_T07:00-0000&version=1",
    """
    cfg = Config.from_ctx(ctx)
    new_feed_dir = os.path.join(cfg.ed_path(), 'data', name)
    os.mkdir(new_feed_dir)
    if cfg.debug(): click.echo("Created directory: %s" % new_feed_dir)
    template_files = ["LICENSE","Makefile","README.md","src/10_down.py","src/20_unzp.py","src/30_inse.py","src/40_save.sh","manifest.json"]
    env = Environment(
        loader=PackageLoader('edc', 'templates'),
        autoescape=select_autoescape(['py'])
    )
    m = {
            'NAME'      : name,
            'MAINTAINER': maintainer,
            'COMPANY'   : company,
            'EMAIL'     : email,
            'DATA_URL'  : url,
            'REPO_URL'  : "https://github.com/energy-analytics-project/%s" % name,
            'START'     : start_date_tuple
    }
    for tf in template_files:
        template    = env.get_template(tf)
        target      = os.path.join(new_feed_dir, tf)
        path        = os.path.dirname(target)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(target, 'w') as f:
            f.write(template.render(m))
            if cfg.debug(): click.echo("Rendered '%s'" % target)

    hidden_files = ['gitignore', 'gitattributes']
    for hf in hidden_files:
        template    = env.get_template(hf)
        target      = os.path.join(new_feed_dir, ".%s" % hf)
        with open(target, 'w') as f:
            f.write(template.render(m))
            if cfg.debug(): click.echo("Rendered '%s'" % target)

    #subprocess.run(['git', 'init'], cwd=new_feed_dir, shell=True)
    #subprocess.run(['git', 'add', "*"], cwd=new_feed_dir, shell=True)
    #subprocess.run(['git', 'commit', "-m", "initial commit", "-m", "auto-generated via edc"], cwd=new_feed_dir, shell=True)



@feed.command('invoke', short_help='invoke a shell command in the feed directory')
@click.argument('feed')
@click.argument('command')
@click.pass_context
def feed_invoke(ctx, feed, command):
    """
    CD to feed directory, and invoke command.

    Coupled with the `feeds list` command, the `feed invoke` command allows advanced
    processing on the feeds in the data directory:

    Example:
    # print the 'url' of all the feeds with 'atl' in the name

    $ edc feeds list | grep atl | xargs -L 1 -I {} edc feed invoke {} "jq .url < manifest.json"
    "http://oasis.caiso.com/oasisapi/SingleZip?queryname=ATL_GEN_CAP_LST&startdatetime=_START_T07:00-0000&enddatetime=_END_T07:00-0000&version=4"
    "http://oasis.caiso.com/oasisapi/SingleZip?queryname=ATL_HUB&startdatetime=_START_T07:00-0000&enddatetime=_END_T07:00-0000&version=1"
    "http://oasis.caiso.com/oasisapi/SingleZip?queryname=ATL_OSM&msg_severity=ALL&startdatetime=_START_T07:00-0000&enddatetime=_END_T07:00-0000&version=1"
    "http://oasis.caiso.com/oasisapi/SingleZip?queryname=ATL_PEAK_ON_OFF&startdatetime=_START_T07:00-0000&enddatetime=_END_T07:00-0000&version=1"
    
    Example:
    # dump record count
    $ edc feeds list | grep mileage | xargs -L 1 -I {} edc feed invoke {} "echo {}; sqlite3 db/{}.db 'select count(*) from oasis'"
    data-oasis-as-mileage-calc-all
    42
    """
    cfg = Config.from_ctx(ctx)
    target_dir = os.path.join(cfg.ed_path(), 'data', feed)
    if not os.path.exists(target_dir):
        raise Exception("Feed does not exist at: %s" % target_dir)
    subprocess.run([command], cwd=target_dir, shell=True)


@feed.command('status', short_help='show feed status')
@click.argument('feed')
@click.option('--separator', '-s', default=',')
@click.option('--header/--no-header', default=False)
@click.pass_context
def feed_status(ctx, feed, separator, header):
    """
    Return the feed status as:

        "feed name","download count","unzipped count","inserted count", "db count"
    """
    cfg = Config.from_ctx(ctx)
    target_dir = os.path.join(cfg.ed_path(), 'data', feed)
    if not os.path.exists(target_dir):
        raise Exception("Feed does not exist at: %s" % target_dir)
    if header:
        click.echo(separator.join(["feed name","download count","unzipped count","inserted count", "db count"]))
    txtfiles = ["zip/downloaded.txt", "xml/unzipped.txt", "db/inserted.txt"]
    counts = [str(lines(os.path.join(target_dir, f))) for f in txtfiles]
    status = [feed]
    status.extend(counts)
    click.echo(separator.join(status))

@feed.command('download', short_help='download from source url')
@click.argument('feed')
@click.pass_context
def feed_download(ctx, feed):
    """
    Download feed
    """
    cp = subprocess.run(["src/10_down.py"], cwd=target_dir, shell=True, capture_output=True)
    click.echo(cp.stdout)
    click.echo(cp.stderr)

#@feed.command('reset', short_help='reset feed to reprocess stage')
#@click.argument('feed')
#@click.option('--stage', type=click.Choice(['zip', 'xml', 'db'], multiple=True))
#@click.pass_context
#def feed_download(ctx, feed, stage):
#    """
#    Reset stages. This is a destructive action, but a backup will be made.
#    """
#    cfg = Config.from_ctx(ctx)
#     = os.path.join(cfg.ed_path(), 'data', feed, s)
#    archive_name = os.path.expanduser(os.path.join('~', 'myarchive'))
#    root_dir = os.path.expanduser(os.path.join('~', '.ssh'))
#    make_archive(archive_name, 'gztar', root_dir)
#'/Users/tarek/myarchive.tar.gz'
#    for s in stage:
#        p = os.path.join(cfg.ed_path(), 'data', feed, s)
#        if click.confirm('About to delete %s. Do you want to continue?'):
#            shutil.rmtree


@feed.command('archive', short_help='archive feed')
@click.argument('feed')
@click.option('--outdir', help="Output directory to write archive")
@click.pass_context
def feed_download(ctx, feed, outdir):
    """
    Archive a feed. Especially usefull before a destructive action like 
    resetting the feed state.
    """
    cfg = Config.from_ctx(ctx)
    if outdir is None:
        outdir = os.path.join(cfg.ed_path(), 'archive')
    archive_name = os.path.join(outdir, feed)
    root_dir = os.path.expanduser(os.path.join(cfg.ed_path(), 'data', feed))
    click.echo(make_archive(archive_name, 'gztar', root_dir))


@feed.command('backup', short_help='backup feed to S3 bucket(s)')
@click.argument('feed')
@click.pass_context
def feed_download(ctx, feed):
    """
    """
    pass

@feed.command('restore', short_help='restore feed from S3 bucket(s)')
@click.argument('feed')
@click.pass_context
def feed_download(ctx, feed):
    """
    """
    pass



def dbcount(feed):
    try:
        cnx = sqlite3.connect(os.path.join(target_dir, "db", "%s.db" % feed))
        for val in cnx.execute("select count(*) from oasis"):
            return val
    except:
        return 0


def lines(f):
    try:
        with open(f, 'r') as x:
            lines = x.readlines()
            return len(lines)
    except:
        return 0

#------------------------------------------------------------------------------
# Config Stuff
#------------------------------------------------------------------------------
class Config():
    M_ED_PATH       = 'ed_path'
    M_CFG_FILE      = 'cfg_file'
    M_DEBUG         = 'debug'
    DEF_CFG_PATH    = '~/.config'
    DEF_CFG_FILE    = 'energy-dashboard-client.config'
    DEF_ED_PATH     = '../energy-dashboard'
    def __init__(self, ed_path, cfg_file, debug):
        """
        """
        self._ed_path    = os.path.abspath(os.path.expanduser(ed_path   or  Config.DEF_ED_PATH))
        self._cfg_file   = os.path.abspath(os.path.expanduser(cfg_file  or  os.path.join(Config.DEF_CFG_PATH, Config.DEF_CFG_FILE)))
        self._debug      = debug or False

    def save(self) -> None:
        with open(self._cfg_file, 'w') as outfile:
            json.dump(self.to_map(), outfile, indent=4, sort_keys=True)

    def to_map(self):
        m               = {}
        m[Config.M_ED_PATH]   = self._ed_path
        m[Config.M_CFG_FILE]  = self._cfg_file
        m[Config.M_DEBUG]     = self._debug
        return m

    def from_map(m):
        ed_path    = m.get(Config.M_ED_PATH,     None)
        cfg_file   = m.get(Config.M_CFG_FILE,    None)
        debug      = m.get(Config.M_DEBUG,       None)
        return Config(ed_path, cfg_file, debug)

    def load(f:str):
        with open(f, 'r') as json_cfg_file:
            m = json.load(json_cfg_file)
            return Config.from_map(m)

    def from_ctx(ctx):
        cfg = Config.load(os.path.join(os.path.expanduser(ctx.obj['config-dir']), Config.DEF_CFG_FILE))
        return cfg

    def ed_path(self):
        return self._ed_path

    def cfg_file(self):
        return self._cfg_file

    def debug(self):
        return self._debug
    
    def __repr__(self):
        return json.dumps(self.to_map(), indent=4, sort_keys=True)

