import click
import json
import os
import json
import subprocess

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
@cli.command()
@click.argument('path')
@click.pass_context
def config(ctx, path):
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
        config = load_config(cfg_file_path)
        if debug: click.echo("loaded config file: %s" % cfg_file_path)
    else:
        config = empty_config()
        if debug: click.echo("loaded empty config")
    # override prev values
    config2 = Config(config, {Config.ED_PATH: path, Config.CFG_FILE: cfg_file_path})
    config2.save()
    if debug: click.echo("saved config to: %s" % config2.cfg_file())



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
    cfg = config_from_ctx(ctx)
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

@feed.command('add', short_help='add new feed (NYI)')
def feed_add():
    pass

@feed.command('invoke', short_help='invoke a shell command in the feed directory')
@click.argument('feed')
@click.option('--command', '-c', multiple=True)
@click.pass_context
def feed_invoke(ctx, feed, command):
    """
    CD to feed directory, and invoke command.

    Coupled with the `feeds list` command, the `feed invoke` command allows advanced
    processing on the feeds in the data directory:

    Example:
    # print the 'url' of all the feeds with 'atl' in the name

    $ edc feeds list | grep atl | xargs -L 1 -I {} edc feed invoke {} -c "jq .url < manifest.json"
    "http://oasis.caiso.com/oasisapi/SingleZip?queryname=ATL_GEN_CAP_LST&startdatetime=_START_T07:00-0000&enddatetime=_END_T07:00-0000&version=4"
    "http://oasis.caiso.com/oasisapi/SingleZip?queryname=ATL_HUB&startdatetime=_START_T07:00-0000&enddatetime=_END_T07:00-0000&version=1"
    "http://oasis.caiso.com/oasisapi/SingleZip?queryname=ATL_OSM&msg_severity=ALL&startdatetime=_START_T07:00-0000&enddatetime=_END_T07:00-0000&version=1"
    "http://oasis.caiso.com/oasisapi/SingleZip?queryname=ATL_PEAK_ON_OFF&startdatetime=_START_T07:00-0000&enddatetime=_END_T07:00-0000&version=1"
    
    Example:
    # dump record count
    $ edc feeds list | grep mileage | xargs -L 1 -I {} edc feed invoke {} -c "echo {}; sqlite3 db/{}.db 'select count(*) from oasis'"
    data-oasis-as-mileage-calc-all
    42
    """
    cfg = config_from_ctx(ctx)
    target_dir = os.path.join(cfg.ed_path(), 'data', feed)
    if not os.path.exists(target_dir):
        raise Exception("Feed does not exist at: %s" % target_dir)
    subprocess.run(*command, cwd=target_dir, shell=True)

@feeds.command('status', short_help='show feeds status (NYI)')
def feeds_status():
    pass


#------------------------------------------------------------------------------
# Config Stuff
#------------------------------------------------------------------------------
class Config():
    ED_PATH='ed_path'
    CFG_FILE='cfg_file'
    def __init__(self, config, m):
        """
        config  : Config instance
        m       : map of overrides
        """
        self._ed_path    = os.path.expanduser(m[Config.ED_PATH]  or config.ed_path())
        self._cfg_file   = os.path.expanduser(m[Config.CFG_FILE] or config.cfg_file())

    def save(self) -> None:
        m               = {}
        m[Config.ED_PATH]   = os.path.expanduser(self._ed_path)
        m[Config.CFG_FILE]  = os.path.expanduser(self._cfg_file)
        with open(self._cfg_file, 'w') as outfile:
            json.dump(m, outfile, indent=4, sort_keys=True)

    def ed_path(self):
        return self._ed_path

    def cfg_file(self):
        return self._cfg_file

def empty_config() -> Config:
    return Config(None, {Config.ED_PATH:"", Config.CFG_FILE:""})

def load_config(f:str) -> Config:
    with open(f, 'r') as json_cfg_file:
        m = json.load(json_cfg_file)
        return Config(None, m)

def config_from_ctx(ctx):
    cfg = load_config(os.path.join(os.path.expanduser(ctx.obj['config-dir']), 'energy-dashboard-client.config'))
    return cfg
