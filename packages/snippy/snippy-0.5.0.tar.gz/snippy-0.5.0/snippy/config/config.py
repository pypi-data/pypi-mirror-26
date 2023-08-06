#!/usr/bin/env python3

"""config.py: Configuration management."""

import re
import os.path
import datetime
import pkg_resources
from snippy.config.constants import Constants as Const
from snippy.logger.logger import Logger
from snippy.cause.cause import Cause
from snippy.config.arguments import Arguments
from snippy.config.editor import Editor


class Config(object):  # pylint: disable=too-many-public-methods
    """Global configuration management."""

    args = {}
    config = {}
    logger = None

    def __init__(self):
        Config.logger = Logger(__name__).get()
        Config.args = Arguments()
        Config._set_config()

    @classmethod
    def _set_config(cls):
        Config.logger.info('initiating configuration')
        cls.config['root'] = os.path.realpath(os.path.join(os.getcwd()))
        cls.config['content'] = {}
        cls.config['content']['category'] = cls.args.get_content_category()
        cls.config['content']['data'] = cls._parse_content_data()
        cls.config['content']['brief'] = cls._parse_content_brief()
        cls.config['content']['group'] = cls._parse_content_group()
        cls.config['content']['tags'] = cls._parse_content_tags()
        cls.config['content']['links'] = cls._parse_content_links()
        cls.config['content']['filename'] = Const.EMPTY
        cls.config['options'] = {}
        cls.config['options']['no_ansi'] = cls.args.is_no_ansi()
        cls.config['options']['migrate_defaults'] = cls.args.is_defaults()
        cls.config['options']['migrate_template'] = cls.args.is_template()
        cls.config['options']['debug'] = cls.args.is_debug()
        cls.config['digest'] = cls._parse_digest()
        cls.config['operation'] = {}
        cls.config['operation']['task'] = cls.args.get_operation()
        cls.config['operation']['file'] = {}
        cls.config['operation']['file']['name'], cls.config['operation']['file']['type'] = cls._parse_operation_file()
        cls.config['search'] = {}
        cls.config['search']['field'], cls.config['search']['keywords'] = cls._parse_search()
        cls.config['search']['filter'] = cls._parse_search_filter()
        cls.config['input'] = {}
        cls.config['input']['editor'] = cls.args.get_editor()
        cls.config['storage'] = {}
        cls.config['storage']['path'] = pkg_resources.resource_filename('snippy', 'data/storage')
        cls.config['storage']['file'] = 'snippy.db'
        cls.config['storage']['schema'] = {}
        cls.config['storage']['schema']['path'] = pkg_resources.resource_filename('snippy', 'data/config')
        cls.config['storage']['schema']['file'] = 'database.sql'
        cls.config['storage']['in_memory'] = False

        cls.logger.debug('configured value from positional argument as "%s"', cls.config['operation']['task'])
        cls.logger.debug('configured value from content category as "%s"', cls.config['content']['category'])
        cls.logger.debug('configured value from --content as %s', cls.config['content']['data'])
        cls.logger.debug('configured value from --brief as "%s"', cls.config['content']['brief'])
        cls.logger.debug('configured value from --group as "%s"', cls.config['content']['group'])
        cls.logger.debug('configured value from --tags as %s', cls.config['content']['tags'])
        cls.logger.debug('configured value from --links as %s', cls.config['content']['links'])
        cls.logger.debug('configured value from --digest as "%s"', cls.config['digest'])
        cls.logger.debug('configured value from --editor as %s', cls.config['input']['editor'])
        cls.logger.debug('configured value from --file as "%s"', cls.config['operation']['file']['name'])
        cls.logger.debug('configured value from search field as %s', cls.config['search']['field'])
        cls.logger.debug('configured value from search keywords as %s', cls.config['search']['keywords'])
        cls.logger.debug('configured value from search filter as %s', cls.config['search']['filter'])
        cls.logger.debug('extracted file format from argument --file "%s"', cls.config['operation']['file']['type'])

    @classmethod
    def reset(cls):
        """Reset the configuration."""

        Config.args.reset()
        Config.args = {}
        Config.config = {}

        return Config()

    @classmethod
    def get_content(cls, content, use_editor=False):
        """Return content after it has been optionally edited."""

        if cls.is_editor() or use_editor:
            content = Config._get_edited_content(content)

        return content

    @classmethod
    def get_file_contents(cls, content, edited):
        """Return contents from specified text file."""

        contents = []
        editor = Editor(content, Config.get_utc_time(), edited)
        content.set((editor.get_edited_data(),
                     editor.get_edited_brief(),
                     editor.get_edited_group(),
                     editor.get_edited_tags(),
                     editor.get_edited_links(),
                     editor.get_edited_category(),
                     editor.get_edited_filename(),
                     editor.get_edited_date(),
                     content.get_digest(),
                     content.get_metadata(),
                     content.get_key()))
        content.update_digest()
        contents.append(content)

        return contents

    @classmethod
    def get_content_template(cls, content):
        """Return content in text template."""

        editor = Editor(content, Config.get_utc_time())
        template = editor.get_template()

        return template

    @classmethod
    def is_operation_create(cls):
        """Test if operation was create."""

        return True if cls.config['operation']['task'] == 'create' else False

    @classmethod
    def is_operation_search(cls):
        """Test if operation was search."""

        return True if cls.config['operation']['task'] == 'search' else False

    @classmethod
    def is_operation_update(cls):
        """Test if operation was update."""

        return True if cls.config['operation']['task'] == 'update' else False

    @classmethod
    def is_operation_delete(cls):
        """Test if operation was delete."""

        return True if cls.config['operation']['task'] == 'delete' else False

    @classmethod
    def is_operation_export(cls):
        """Test if operation was export."""

        return True if cls.config['operation']['task'] == 'export' else False

    @classmethod
    def is_operation_import(cls):
        """Test if operation was import."""

        return True if cls.config['operation']['task'] == 'import' else False

    @classmethod
    def is_migrate_defaults(cls):
        """Test if migrate operation was related to content defaults."""

        return True if cls.config['options']['migrate_defaults'] else False

    @classmethod
    def is_migrate_template(cls):
        """Test if migrate operation was related to content template."""

        return True if cls.config['options']['migrate_template'] else False

    @classmethod
    def is_category_snippet(cls):
        """Test if operation is applied to snippet category."""

        return True if cls.config['content']['category'] == Const.SNIPPET else False

    @classmethod
    def is_category_solution(cls):
        """Test if operation is applied to solution category."""

        return True if cls.config['content']['category'] == Const.SOLUTION else False

    @classmethod
    def is_category_all(cls):
        """Test if operation is applied to all content categories."""

        return True if cls.config['content']['category'] == 'all' else False

    @classmethod
    def get_category(cls):
        """Return content category."""

        return cls.config['content']['category']

    @classmethod
    def set_category(cls, category):
        """Set content category."""

        if category == Const.SOLUTION:
            cls.config['content']['category'] = Const.SOLUTION
        else:
            cls.config['content']['category'] = Const.SNIPPET

    @classmethod
    def get_content_data(cls):
        """Return content data."""

        return cls.config['content']['data']

    @classmethod
    def get_content_brief(cls):
        """Return content brief description."""

        return cls.config['content']['brief']

    @classmethod
    def get_content_group(cls):
        """Return content group."""

        return cls.config['content']['group']

    @classmethod
    def get_content_tags(cls):
        """Return content tags."""

        return cls.config['content']['tags']

    @classmethod
    def get_content_links(cls):
        """Return content reference links."""

        return cls.config['content']['links']

    @classmethod
    def get_content_digest(cls):
        """Return digest identifying the content."""

        return cls.config['digest']

    @classmethod
    def get_content_valid_digest(cls):
        """Return digest identifying the content."""

        digest = Const.EMPTY
        if len(cls.config['digest']) >= Const.DIGEST_MIN_LENGTH:
            digest = cls.config['digest']

        return digest

    @classmethod
    def get_filename(cls):
        """Return content filename."""

        return cls.config['content']['filename']

    @classmethod
    def is_search_all(cls):
        """Test if all fields are searched."""

        return True if cls.config['search']['field'] == Const.SEARCH_ALL else False

    @classmethod
    def is_search_grp(cls):
        """Test if search is made only from groups."""

        return True if cls.config['search']['field'] == Const.SEARCH_GRP else False

    @classmethod
    def is_search_tag(cls):
        """Test if search is made only from tags."""

        return True if cls.config['search']['field'] == Const.SEARCH_TAG else False

    @classmethod
    def get_search_keywords(cls):
        """Return list of search keywords."""

        return cls.config['search']['keywords']

    @classmethod
    def get_search_filter(cls):
        """Return search filter."""

        return cls.config['search']['filter']

    @classmethod
    def is_editor(cls):
        """Test if editor is used to input content."""

        return cls.config['input']['editor']

    @classmethod
    def get_operation_file(cls, content_filename=Const.EMPTY):
        """Return file for operation."""

        # Use the content filename only in case of export operation and
        # when the user did not define the target file from command line.
        filename = cls.config['operation']['file']['name']
        if cls.is_operation_export() and content_filename and not cls.args.get_operation_file():
            filename = content_filename

        return filename

    @classmethod
    def is_file_type_yaml(cls):
        """Test if file format is yaml."""

        return True if cls.config['operation']['file']['type'] == Const.FILE_TYPE_YAML else False

    @classmethod
    def is_file_type_json(cls):
        """Test if file format is json."""

        return True if cls.config['operation']['file']['type'] == Const.FILE_TYPE_JSON else False

    @classmethod
    def is_file_type_text(cls):
        """Test if file format is text."""

        return True if cls.config['operation']['file']['type'] == Const.FILE_TYPE_TEXT else False

    @classmethod
    def is_supported_file_format(cls):
        """Test if file format is supported."""

        return True if cls.is_file_type_yaml() or cls.is_file_type_json() or cls.is_file_type_text() else False

    @classmethod
    def use_ansi(cls):
        """Test if ANSI characters like colors are disabled in the command output."""

        return False if cls.config['options']['no_ansi'] else True

    @classmethod
    def get_storage_path(cls):
        """Return path of the persistent storage."""

        return cls.config['storage']['path']

    @classmethod
    def get_storage_file(cls):
        """Return path and file of the persistent storage."""

        return os.path.join(cls.config['storage']['path'], cls.config['storage']['file'])

    @classmethod
    def get_storage_schema(cls):
        """Return storage schema."""

        return os.path.join(cls.config['storage']['schema']['path'], cls.config['storage']['schema']['file'])

    @classmethod
    def set_storage_in_memory(cls, in_memory):
        """Set the storage to be in memory."""

        cls.config['storage']['in_memory'] = in_memory

    @classmethod
    def is_storage_in_memory(cls):
        """Test if storage is defined to be run in memory."""

        return cls.config['storage']['in_memory']

    @staticmethod
    def get_utc_time():
        """Get UTC time."""

        utc = datetime.datetime.utcnow()

        return utc.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def is_debug(cls):
        """Test if debug option was used."""

        return True if cls.config['options']['debug'] else False

    @classmethod
    def _parse_content_data(cls):
        """Process content data."""

        arg = cls.args.get_content_data()
        if arg:
            content = arg.split(Const.DELIMITER_DATA)

            return tuple(content)

        return Const.EMPTY_TUPLE

    @classmethod
    def _parse_content_brief(cls):
        """Process content brief description."""

        arg = cls.args.get_content_brief()
        if arg:
            return arg

        return Const.EMPTY

    @classmethod
    def _parse_content_group(cls):
        """Process content group."""

        arg = cls.args.get_content_group()
        if arg:
            return arg

        return Const.EMPTY

    @classmethod
    def _parse_content_tags(cls):
        """Process content tags."""

        arg = cls.args.get_content_tags()

        return Editor.get_keywords(arg)

    @classmethod
    def _parse_content_links(cls):
        """Process content reference links."""

        links = cls.args.get_content_links()
        # Examples: Support processing of:
        #           1. -l docker container cleanup # Space separated string of links
        link_list = links.split()
        link_list = sorted(link_list)

        return tuple(link_list)

    @classmethod
    def _parse_digest(cls):
        """Process message digest identifying the operation target."""

        arg = cls.args.get_content_digest()
        if arg:
            return arg

        return Const.EMPTY

    @classmethod
    def _parse_search(cls):
        """Process the user given search keywords and field."""

        arg = ()
        field = Const.NO_SEARCH
        if cls.args.is_search_all():
            arg = cls.args.get_search_all()
            field = Const.SEARCH_ALL
        elif cls.args.is_search_tag():
            arg = cls.args.get_search_tag()
            field = Const.SEARCH_TAG
        elif cls.args.is_search_grp():
            arg = cls.args.get_search_grp()
            field = Const.SEARCH_GRP

        if not arg and (field != Const.NO_SEARCH):
            cls.logger.info('listing all content from category because no keywords were provided')
            arg = ('.')

        return (field, Editor.get_keywords(arg))

    @classmethod
    def _parse_search_filter(cls):
        """Process the user given search keywords and field."""

        regexp = cls.args.get_search_filter()

        try:
            re.compile(regexp)
        except re.error:
            cls.logger.info('filter is not a valid regexp "%s"', regexp)
            regexp = Const.EMPTY

        return regexp

    @classmethod
    def _get_edited_content(cls, content):
        """Read and set the user provided values from editor."""

        editor = Editor(content, Config.get_utc_time())
        editor.read_content()
        cls.config['content']['data'] = editor.get_edited_data()
        cls.config['content']['brief'] = editor.get_edited_brief()
        cls.config['content']['group'] = editor.get_edited_group()
        cls.config['content']['tags'] = editor.get_edited_tags()
        cls.config['content']['links'] = editor.get_edited_links()
        cls.config['content']['filename'] = editor.get_edited_filename()
        content.set((cls.get_content_data(),
                     cls.get_content_brief(),
                     cls.get_content_group(),
                     cls.get_content_tags(),
                     cls.get_content_links(),
                     content.get_category(),
                     cls.get_filename(),
                     content.get_utc(),
                     content.get_digest(),
                     content.get_metadata(),
                     content.get_key()))

        return content

    @classmethod
    def _parse_operation_file(cls):
        """Return the filename and the format of the file."""

        filename = cls.args.get_operation_file()
        filetype = Const.FILE_TYPE_NONE

        defaults = 'snippets.yaml'
        template = 'snippet-template.txt'
        if Config.is_category_solution():
            defaults = 'solutions.yaml'
            template = 'solution-template.txt'

        # Run migrate operation with default content.
        if cls.is_migrate_defaults():
            filename = os.path.join(pkg_resources.resource_filename('snippy', 'data/default'), defaults)

        # Run migrate operation with content template.
        if cls.is_migrate_template():
            filename = os.path.join('./', template)

        # Run export operation with specified content without specifying
        # the operation file.
        if cls.is_operation_export() and cls.get_content_digest():
            if Config.is_category_snippet() and not filename:
                filename = 'snippet.' + Const.FILE_TYPE_TEXT
            elif Config.is_category_solution() and not filename:
                filename = 'solution.' + Const.FILE_TYPE_TEXT

        # In case user did not provide filename, set defaults. For example
        # if user defined export or import operation without the file, the
        # default files are used.
        if not filename:
            filename = os.path.join('./', defaults)

        # User defined content to/from user specified file.
        name, extension = os.path.splitext(filename)
        if name and ('yaml' in extension or 'yml' in extension):
            filetype = Const.FILE_TYPE_YAML
        elif name and 'json' in extension:
            filetype = Const.FILE_TYPE_JSON
        elif name and ('txt' in extension or 'text' in extension):
            filetype = Const.FILE_TYPE_TEXT
        else:
            Cause.set_text('cannot identify file format for file {}'.format(filename))

        return (filename, filetype)
