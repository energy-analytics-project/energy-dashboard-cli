#! /usr/bin/env python3

# -----------------------------------------------------------------------------
# 30_inse.py : parse resources from an xml file and insert into database
# -----------------------------------------------------------------------------

import os
import logging
import xml.dom.minidom as md
import pprint
import datetime as dt
import sqlite3
from edl.resources import state

# -----------------------------------------------------------------------------
# Custom Glue Code
# -----------------------------------------------------------------------------
def xml2maps(xml_file):
    """Return a list of maps constructed from the xml file"""
    dom     = md.parse(xml_file)
    header  = get_element("MessageHeader",  dom)
    payload = get_element("MessagePayload", dom)
    rto     = get_element("RTO",            payload)
    name    = get_element("name",           rto)
    items   = get_elements("REPORT_ITEM",    rto)
    return [xml2map(header, name, item) for item in items] 

def xml2map(header, name, item):
    """Return map"""
    return {
        "timedate"                : value("TimeDate",           header),
        "timedate_posix"          : posix(value("TimeDate",     header)),
        "source"                  : value("Source",             header),
        "version"                 : value("Version",            header),
        "name"                    : value_of(name),
        "system"                  : value("SYSTEM",             item),
        "tz"                      : value("TZ",                 item),
        "report"                  : value("REPORT",             item),
        "mkt_type"                : value("MKT_TYPE",           item),
        "uom"                     : value("UOM",                item),
        "interval"                : value("INTERVAL",           item),
        "sec_per_interval"        : value("SEC_PER_INTERVAL",   item),
        "data_item"               : value("DATA_ITEM",          item),
        "resource_name"           : value("RESOURCE_NAME",      item),
        "opr_date"                : value("OPR_DATE",           item),
        "opr_date_8601"           : date_8601(value("OPR_DATE", item)),
        "interval_num"            : value("INTERVAL_NUM",       item),
        "interval_start_gmt"      : value("INTERVAL_START_GMT", item),
        "interval_start_posix"    : posix(value("INTERVAL_START_GMT", item)),
        "interval_end_gmt"        : value("INTERVAL_END_GMT",   item),
        "interval_end_posix"      : posix(value("INTERVAL_END_GMT", item)),
        "value"                   : value("VALUE",              item)
            }

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
def config():
    """
    config = {
            "source_dir"    : location of the xml files
            "working_dir"   : location of the database
            "state_file"    : fqpath to file that lists the inserted xml files
            }
    """
    cwd                     = os.path.abspath(os.path.curdir)
    xml_dir                 = os.path.join(cwd, "xml")
    db_dir                  = os.path.join(cwd, "db")
    state_file              = os.path.join(db_dir, "inserted.txt")
    config = {
            "source_dir"    : xml_dir,
            "working_dir"   : db_dir,
            "state_file"    : state_file
            }
    return config


# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
def run(manifest, config, logging_level=logging.INFO):
    log.configure_logging(logging_level)
    resource_name   = manifest['name']
    sql_insert      = manifest['sql_insert']
    ddl_create      = manifest['ddl_create']
    xml_dir         = config['source_dir']
    db_dir          = config['working_dir']
    state_file      = config['state_file']
    db_name         = "%s.db" % resource_name
    state.update(
            insert(
                resource_name,
                db_dir,
                db_name,
                ddl_create,
                sql_insert,
                parse(
                    resource_name,
                    new_xml_files(resource_name, state_file, xml_dir)
                    xml_dir,
                    xml2maps)))

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    with open('manifest.json', 'r') as json_file:
        m = json.load(json_file)
        run(m, config())
