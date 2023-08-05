"""Schevo database."""

# Copyright (c) 2001-2009 ElevenCraft Inc.
# Copyright (c) 2010 Etienne Robillard <robillard.etienne@gmail.com>
# See LICENSE for details.

import sys
import os

from schevo.lib import optimize

# from schevo import database1
from schevo import database2
from schevo.error import (
    DatabaseAlreadyExists, DatabaseDoesNotExist, DatabaseFormatMismatch)
from schevo.field import not_fget
from schevo import icon
from schevo.label import relabel
from schevo.store.connection import Connection
from schevo.store.file_storage import FileStorage
from schevo.trace import log
from schevo.url import make_url

format_dbclass = {
    # Default database class.
    None: database2.Database,

    # Format-specific database classes.
#     1: database1.Database,
    2: database2.Database,
    }


format_converter = {
    2: database2.convert_from_format1,
    }


def convert_format(url, backend_args={}, format=None):
    """Convert database to a new internal structure format.

    - `url`: URL of the database to convert.
    - `backend_args`: (optional) Additional arguments to pass to the backend.
    - `format`: (optional) Format to convert internal structure to.
      If not given, the most recent format available will be used.
    """
    backend = new_backend(url, backend_args)
    # Check the format of the database.
    root = backend.get_root()
    # XXX: Better error checking might be handy.
    # XXX: So might data structure verification.
    schevo = root['SCHEVO']
    original_format = schevo['format']
    if format is None:
        format = max(format_converter)
    # Convert one version at a time, ensuring that failures result in a
    # rollback to the database's original state.
    try:
        for new_format in xrange(original_format + 1, format + 1):
            converter = format_converter[new_format]
            converter(backend)
    except:
        backend.rollback()
        raise
    else:
        backend.commit()
    backend.close()


def copy(src_url, dest_url, src_backend_args={}, dest_backend_args={}):
    """Copy internal structures verbatim from a source database to a
    new destination database.

    To see progress of the copy operation, turn on tracing as
    described in `schevo.trace`

    - `src_url`: URL of the source database.
    - `dest_url`: URL of the destination database. This database
      may exist if it is in the format used by the destination
      backend, but must not already contain a Schevo database.
    - `src_backend_args`: (optional) Additional arguments to pass to
      the source backend.
    - `dest_backend_args`: (optional) Additional arguments to pass to the
      destination backend.
    """
    src_backend = new_backend(src_url, src_backend_args)
    # Make sure the source backend is in the proper format.
    assert log(1, 'Checking source', src_url)
    src_root = src_backend.get_root()
    if 'SCHEVO' not in src_root:
        src_backend.close()
        raise DatabaseDoesNotExist(src_url)
    current_format = src_root['SCHEVO']['format']
    required_format = 2
    if current_format != required_format:
        src_backend.close()
        raise DatabaseFormatMismatch(current_format, required_format)
    # Make sure the destination backend does not have a database.
    assert log(1, 'Checking destination', dest_url)
    dest_backend = new_backend(dest_url, dest_backend_args)
    dest_root = dest_backend.get_root()
    if 'SCHEVO' in dest_root:
        src_backend.close()
        dest_backend.close()
        raise DatabaseAlreadyExists(dest_url)
    assert log(1, 'Start copying structures.')
    d_btree = dest_backend.BTree
    d_pdict = dest_backend.PDict
    d_plist = dest_backend.PList
    s_btree = src_backend.BTree
    assert log(2, 'Creating SCHEVO key.')
    src_SCHEVO = src_root['SCHEVO']
    dest_SCHEVO = dest_root['SCHEVO'] = d_pdict()
    assert log(2, 'Copying lightweight structures.')
    if 'label' in src_SCHEVO:
        dest_SCHEVO['label'] = src_SCHEVO['label']
    dest_SCHEVO['format'] = 2
    dest_SCHEVO['version'] = src_SCHEVO['version']
    dest_SCHEVO['schema_source'] = src_SCHEVO['schema_source']
    dest_SCHEVO['extent_name_id'] = d_pdict(
        src_SCHEVO['extent_name_id'].iteritems())
    assert log(2, 'Copying extents.')
    dest_extents = dest_SCHEVO['extents'] = d_pdict()
    def copy_btree(src):
        """Used for copying indices structure."""
        copy = d_btree()
        for key, value in src.iteritems():
            if isinstance(value, s_btree):
                value = copy_btree(value)
            copy[key] = value
        return copy
    for extent_id, src_extent in src_SCHEVO['extents'].iteritems():
        extent_name = src_extent['name']
        assert log(2, 'Creating extent', extent_name)
        dest_extent = dest_extents[extent_id] = d_pdict()
        assert log(2, 'Copying lightweight structures for', extent_name)
        dest_extent['entity_field_ids'] = src_extent['entity_field_ids']
        dest_extent['field_id_name'] = d_pdict(
            src_extent['field_id_name'].iteritems())
        dest_extent['field_name_id'] = d_pdict(
            src_extent['field_name_id'].iteritems())
        dest_extent['id'] = src_extent['id']
        dest_extent['len'] = src_extent['len']
        dest_extent['name'] = src_extent['name']
        dest_extent['next_oid'] = src_extent['next_oid']
        assert log(2, 'Copying', len(src_extent['entities']), 'entities in',
            extent_name)
        dest_entities = dest_extent['entities'] = d_btree()
        for entity_oid, src_entity in src_extent['entities'].iteritems():
            assert log(3, 'Copying', entity_oid)
            dest_entity = dest_entities[entity_oid] = d_pdict()
            dest_entity['rev'] = src_entity['rev']
            dest_entity['fields'] = d_pdict(src_entity['fields'].iteritems())
            dest_entity['link_count'] = src_entity['link_count']
            src_links = src_entity['links']
            dest_links = dest_entity['links'] = d_pdict()
            for key, value in src_links.iteritems():
                links = dest_links[key] = d_btree()
                # Do not use update() since schevo.store, durus, and zodb
                # all have slightly different, incompatible, versions.
                for k, v in src_links[key].iteritems():
                    links[k] = v
            dest_entity['related_entities'] = d_pdict(
                src_entity['related_entities'].iteritems())
        assert log(2, 'Copying indices for', extent_name)
        dest_extent['index_map'] = d_pdict(
            (k, d_plist(v))
            for k, v
            in src_extent['index_map'].iteritems()
            )
        dest_extent['normalized_index_map'] = d_pdict(
            (k, d_plist(v))
            for k, v
            in src_extent['normalized_index_map'].iteritems()
            )
        dest_indices = dest_extent['indices'] = d_btree()
        for index_spec, src_index_data in src_extent['indices'].iteritems():
            unique, src_index_tree = src_index_data
            dest_indices[index_spec] = (unique, copy_btree(src_index_tree))
        assert log(2, 'Done copying', extent_name, '-- committing to disk')
        dest_backend.commit()
    # Finalize.
    assert log(1, 'Close source.')
    src_backend.close()
    assert log(1, 'Pack destination.')
    dest_backend.pack()
    assert log(1, 'Close destination.')
    dest_backend.close()


def create(url, backend_args={},
           schema_source=None, schema_version=None, initialize=True,
           format=None, label=u'Schevo Database'):
    """Create a new database and return it.

    - `url`: URL of the new database.
    - `backend_args`: (optional) Additional arguments to pass to the backend.
    - `schema_source`: (optional) Schema source code to synchronize
      the new database with. If `None` is given, the database will
      exist but will contain no extents.
    - `schema_version`: (optional) Version of the schema being used to
      create the database.  If `None` is given, `1` is assumed.
    - `initialize`: `True` (default) if the new database should be
      populated with initial values defined in the schema.
    - `format`: (optional) Internal structure format to use.  If
      `None` is given, the latest format will be used.
    - `label`: (optional) The label to give the new database.
    """
    backend = new_backend(url, backend_args)
    # Make sure the database doesn't already exist.
    root = backend.get_root()
    if 'SCHEVO' in root:
        backend.close()
        raise DatabaseAlreadyExists(url)
    # Continue creating the new database.
    Database = format_dbclass[format]
    db = Database(backend)
    db._sync(
        schema_source=schema_source,
        schema_version=schema_version,
        initialize=initialize,
        )
    # Apply label.
    relabel(db, label)
    # Install icon support.
    icon.install(db)
    return db


def equivalent(db1, db2, require_identical_schema_source=True):
    """Return True if `db1` and `db2` are functionally equivalent, or False
    if they differ.

    - `db1` and `db2`: The open databases to compare.
    - `require_identical_schema_source`: True if `db1` and `db2` must have
      identical schema. This is typical, since this function is intended to test
      equivalence between a database that has been created at version `n` and a
      database that has been created at version 1 and then evolved to version
      `n`. Set to False if the schemata are non-identical, as in the unit tests
      for this function.  **BE CAREFUL** when doing so, and in particular,
      make sure field names are declared in the same order in each schema.

    "Functionally equivalent" in this scenario means that details meant to
    be used internally are ignored by this tool.  Rather, it performs a
    higher-level comparison of the database.  For example, the following
    details are ignored:

    - Entity OIDs
    - Entity revision numbers
    - Order of results when iterating over an extent
    """
    if require_identical_schema_source:
        if db1.schema_source != db2.schema_source:
            return False
    # Create value count dictionaries for each extent in each database.
    extents1, extents2 = {}, {}
    for extents, db in [(extents1, db1), (extents2, db2)]:
        for extent in db.extents():
            counts = {
                # value-tuple: instance-count,
                }
            extents[extent.name] = counts
            # Get field values for each entity in the extent, and increment
            # value counts.
            for entity in extent:
                field_map = entity.s.field_map(not_fget)
                stop_entities = frozenset([entity])
                values = tuple(
                    field.db_equivalence_value(stop_entities)
                    for field in field_map.itervalues()
                    )
                counts[values] = counts.get(values, 0) + 1
    # Now that the structures are filled in, they can be directly compared.
    return extents1 == extents2


def evolve(db, schema_source, version):
    """Evolve database to new version and new schema source.

    - `db`: The database to evolve.
    - `schema_source`: The new schema source to evolve to.
    - `version`: The new version number of the database schema.
    """
    db._evolve(schema_source, version)


def inject(url, schema_source, version, backend_args=None):
    """Inject a new schema and schema version into a database
    file. DANGEROUS!

    PLEASE USE WITH CAUTION; this is not intended to be used in normal course
    of Schevo operation, but can be useful in some corner cases and during
    application development.

    Inject in **no way shape or form evolves data or updates internal
    structures** to reflect changes between the database's current schema and
    that provided in the `schema_source` argument.

    - `url`: URL of database to inject new schema into.
    - `schema_source`: The new schema source to inject into the
      database.
    - `version`: The new version number of the database schema to
      inject.
    - `backend_args`: (optional) Additional arguments to pass to the backend.
    """
    backend = new_backend(url, backend_args)
    root = backend.get_root()
    schevo = root['SCHEVO']
    schevo['schema_source'] = schema_source
    schevo['version'] = version
    backend.commit()
    backend.close()


def new_backend(url, backend_args=None):
    """Return a new database backend instance for a file.

    - `url`: URL of the database to open with the backend.  If given
      as just a filename, and the file already exists, then the
      backend is auto-detected if possible, or an exception is raised.
      If the file does not already exist and `None` is given, an
      exception is raised.
    - `backend_args`: (optional) Additional arguments to pass to the backend.
    """
    if backend_args is not None:
        backend_args = backend_args.copy()
    else:
        backend_args = {}
    if '://' not in url:
        # Assume filename, try to find backend.
        from schevo.backend import backends
        usable = False
        for backend_name, backend_class in backends.iteritems():
            try:
                usable = backend_class.usable_by_backend(url)
            except IOError:
                usable = False
            else:
                if usable:
                    usable, additional_args = usable
                    backend_args.update(additional_args)
                    # Convert to proper URL form.
                    url = '%s:///%s' % (backend_name, url)
                    break
        if not usable:
            raise IOError('No suitable backends found for %r' % url)
    # Convert to URL object.
    url = make_url(url)

    if url.backend_name == 'zodb':
        #XXX fix me
        return url.backend_class()(url.database)

    # Convert backend args to a dictionary.
    backend_args.update(url.translate_connect_args())
    return url.backend_class()(**backend_args)


def open(url, backend_args=None):
    """Open an existing database and return it.

    - `url`: URL of the database to open.
    - `backend_args`: (optional) Additional arguments to pass to the backend.
    """
    #def format_url(url):
    #    if not url.startswith('durus://'):
    #        #raise ValueError("URL not properly formatted. Should at least begin with durus:// prefix.")
    #        db = url
    #    else:
    #        db = url.split('durus://', 1)[1]
    #    return db    
    backend = new_backend(url, backend_args)
    # Make sure the database already exists.
    root = backend.get_root()
    
    if 'SCHEVO' not in root:
        backend.close()
        raise DatabaseDoesNotExist(url)
    # Determine the version of the database.

    schevo = root['SCHEVO']
    format = schevo['format']
    # Determine database class based on format number.
    Database = format_dbclass[format]
    # Create the Database instance.
    db = Database(backend)
    db._sync()
    # Install icon support and finalize opening of database.
    icon.install(db)
    return db

optimize.bind_all(sys.modules[__name__])  # Last line of module.
