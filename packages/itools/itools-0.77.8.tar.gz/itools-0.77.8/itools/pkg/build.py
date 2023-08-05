# -*- coding: UTF-8 -*-
# Copyright (C) 2006, 2010 Hervé Cauwelier <herve@oursours.net>
# Copyright (C) 2006-2007, 2009-2011 J. David Ibáñez <jdavid.ibp@gmail.com>
# Copyright (C) 2007 Sylvain Taverne <taverne.sylvain@gmail.com>
# Copyright (C) 2009 David Versmisse <versmisse@lil.univ-littoral.fr>
# Copyright (C) 2009 Dumont Sébastien <sebastien.dumont@itaapy.com>
# Copyright (C) 2016 Sylvain Taverne <taverne.sylvain@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Import from standard library
from os.path import islink, exists
from subprocess import Popen
from json import dumps

from pygit2 import GitError

# Import from itools
from itools.fs import lfs
from itools.handlers import ro_database

# Import from here
from build_gulp import GulpBuilder
from git import open_worktree


def get_manifest():
    worktree = open_worktree('.')
    exclude = frozenset(['.gitignore'])
    return [ x for x in worktree.get_filenames() if x not in exclude ]


def make(worktree, rules, manifest, package_root):
    for source in worktree.get_filenames():
        # Exclude
        if 'docs/' in source:
            continue
        # Apply rules
        for source_ext, target_ext, f in rules:
            if source.endswith(source_ext):
                target = source[:-len(source_ext)] + target_ext
                if not lfs.exists(target) or \
                   lfs.get_mtime(source) > lfs.get_mtime(target):
                    f(package_root, source, target)     # 1. Compile
                    manifest.add(target)                # 2. Update manifest
                    print target                        # 3. Print


# PO => MO
def po2mo(package_root, source, target):
    Popen(['msgfmt', source, '-o', target])


# Translate templates
def make_template(package_root, source, target):
    # Import some packages so we can compile templates
    from itools.html import XHTMLFile
    from itools.xmlfile.errors import TranslationError
    import itools.gettext
    import itools.stl
    import itools.pdf
    # Get file
    source_handler = ro_database.get_handler(source, XHTMLFile)
    language = target.rsplit('.', 1)[1]
    po = ro_database.get_handler('%s/locale/%s.po' % (package_root, language))
    try:
        data = source_handler.translate(po)
    except TranslationError as e:
        # Override source and language
        raise TranslationError(line=e.line, source_file=source, language=language)
    with open(target, 'w') as f:
        f.write(data)


def get_file_path(package_root, filename):
    if package_root == '.':
        return filename
    return package_root + '/' + filename


def get_package_version(package_root):
    path = get_file_path(package_root, 'version.txt')
    if exists(path):
        version = open(path).read().strip()
    else:
        version = None
    return version


def make_version(worktree):
    """This function finds out the version number from the source, this will
    be written to the 'version.txt' file, which will be read once the software
    is installed to get the version number.
    """
    # Get the git description
    tag = None
    description = worktree.git_describe()

    # The version name
    if description:
        # n represent the number of commit between the tag and the ref
        tag, n, commit = description
        if n == 0:
            # Exact match
            return tag

    # Try to get the branch
    branch = worktree.get_branch_name()
    branch = branch or 'nobranch'
    if tag and tag.startswith(branch):
        branch = tag
    # Get the timestamp
    try:
        head = worktree.get_metadata()
        timestamp = head['committer_date']
        timestamp = timestamp.strftime('%Y%m%d%H%M')
    except KeyError:
        # XXX bug in docker ?
        timestamp = 'notimestamp'

    # Build a version from the branch and the timestamp
    return '{}.dev{}'.format(branch, timestamp)


def build(path, config, environment):
    # Get version path
    package_root = config.get_value('package_root')
    version_txt = get_file_path(package_root, 'version.txt')
    try:
        # Get git worktree
        worktree = open_worktree(path)
    except (GitError, KeyError):
        # Not in a git repostory
        return get_package_version(package_root)
    # Find out the version string
    version = make_version(worktree)
    # Initialize the manifest file
    manifest = set([ x for x in get_manifest() if not islink(x) ])
    manifest.add('MANIFEST')
    # Write version
    open(path + version_txt, 'w').write(version)
    print '**'*30
    print '* Version:', version
    manifest.add(version_txt)
    # Write environment.json file
    environment_json = get_file_path(package_root, 'environment.json')
    environment_kw = {'build_path': path, 'environment': environment}
    open(path + environment_json, 'w').write(dumps(environment_kw))
    manifest.add(environment_json)
    print '* Build environment.json'
    # (3) Rules
    rules = [('.po', '.mo', po2mo)]
    # Templates
    src_lang = config.get_value('source_language', default='en')
    for dst_lang in config.get_value('target_languages'):
        rules.append(
            ('.xml.%s' % src_lang, '.xml.%s' % dst_lang, make_template))
        rules.append(
            ('.xhtml.%s' % src_lang, '.xhtml.%s' % dst_lang, make_template))
    # (4) Make
    make(worktree, rules, manifest, package_root)
    # (5) Run gulp
    if environment == 'production':
        gulp_builder = GulpBuilder(worktree, manifest)
        gulp_builder.run()
    # (6) Write the manifest
    lines = [ x + '\n' for x in sorted(manifest) ]
    open(path + 'MANIFEST', 'w').write(''.join(lines))
    print '* Build MANIFEST file (list of files to install)'
    print '**'*30
    return version
