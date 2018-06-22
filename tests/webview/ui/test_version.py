# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime, timedelta
from warnings import warn

from tests import markers

from pages.webview.version import Version
from pages.webview.history import History
from cli.git import Git


@markers.webview
@markers.nondestructive
def test_version(webview_base_url, selenium, record_property):
    # GIVEN the webview base url, the Selenium driver and the time 2 days ago
    two_days_ago = datetime.utcnow() - timedelta(days=2)

    # WHEN the version and history pages have been visited
    version = Version(selenium, webview_base_url).open()
    version_parser = version.version_parser

    history = History(selenium, webview_base_url).open()
    history_url = selenium.current_url
    release_parsers = history.release_parsers
    current_release_parser = release_parsers[0]
    current_version_parser = current_release_parser.version_parser

    # THEN - the release is less than 2 days old (warning only)
    #      - the tags for webview, archive and deploy are the latest tags (warning only)
    #      - the last 2 releases in history.txt are not exactly identical (warning only)
    #      - version.txt matches the JSON for the latest release in history.txt
    if current_version_parser.datetime < two_days_ago:
        warn('\n\nThe latest release in {url} ({date}) is more than 2 days old.'.format(
                 url=history_url, date=current_version_parser.date))

    tag_tests = [('webview', 'webview_tag'),
                 ('cnx-archive', 'cnx_archive'),
                 ('cnx-deploy', 'cnx_deploy')]
    for (repository_name, tag_property) in tag_tests:
        repository_url = 'https://github.com/Connexions/{repository_name}.git'.format(
            repository_name=repository_name)
        current_tag = Git.shorten_tag(getattr(current_version_parser, tag_property))
        with Git(repository_url) as git:
            latest_tag = git.latest_tag
            if current_tag != latest_tag and current_tag != git.latest_tag_hash:
                warn('\n\nThe {repository_name} tag for the latest release in {url} ({current_tag})'
                     ' does not match the latest tag in {repository_url} ({latest_tag})'.format(
                         repository_name=repository_name,
                         url=history_url,
                         current_tag=current_tag,
                         repository_url=repository_url,
                         latest_tag=latest_tag
                     ))

    for index in range(len(release_parsers) - 1):
        releases_ago = index + 1
        previous_release_parser = release_parsers[releases_ago]
        if not current_release_parser.has_same_versions_as(previous_release_parser):
            break
        elif releases_ago == 1:
            warn('\n\nAll versions in the previous release ({previous_release_date}) match'
                 ' the current release exactly. Release diff based on older release.\n'.format(
                     previous_release_date=previous_release_parser.version_parser.date
                 ))

    if releases_ago == 1:
        releases_ago_string = 'the previous release'
    else:
        releases_ago_string = '{releases_ago} releases ago'.format(releases_ago=releases_ago)
    record_property(
        'terminal_summary_message',
        '\nRelease diff from {releases_ago_string} to the current release:\n\n{diff}'.format(
            releases_ago_string=releases_ago_string,
            diff=current_release_parser.diff(previous_release_parser)))

    assert version_parser.dict == current_version_parser.dict
