# -*- coding: utf-8 -*-

from sphinx.util.compat import Directive
from docutils import nodes

import os
import re
import popen2


class releasenotes(nodes.General, nodes.Element):
    pass

class ReleasenotesDirective(Directive):
    has_content = True
    option_spec = {
        'sur': unicode,
        'app': unicode
    }

    def run(self):
        print self.options
        res = releasenotes('')
        res['sur'] = self.options['sur']
        res['app'] = self.options['app']
        return [res]


def visit_html_releasenotes(self, node):
    env = self.builder.env
    for docname in env.found_docs:
        filename = docname

    git_command = 'git log --date=short --name-status --decorate=full'
    stdout, stdin, stderr = popen2.popen3(git_command)

    list = []
    commit = {}
    commit_log = ""
    for log in stdout:
        match = re.match('commit', log)
        if not match == None:
            commit['log'] = commit_log + '</pre>'
            list.append(commit)
            commit = {}
            commit_log = "<pre>"

            commit['hash'] = log[match.end() + 1:match.end() + 8]
            # (refs/tags/0.1)
            #commit['tag'] = i[3]
        else:
            match = re.match('Author:', log)
            if not match == None:
                commit['author'] = log[match.end() + 1:]
                commit['survey'] = node['sur']
                commit['approval'] = node['app']
            else:
                match = re.match('Date:  ', log)
                if not match == None:
                    commit['date'] = log[match.end() + 1:]
                else:
                    commit_log += log
    commit['log'] = commit_log + '</pre>'
    list.append(commit)
    del list[0]

    self.body += insert_release_note(list)


def depart_releasenotes(self, node):
    pass


def setup(app):
    app.add_node(
        releasenotes, html=(visit_html_releasenotes, depart_releasenotes))

    app.add_directive('releasenotes', ReleasenotesDirective)


def insert_release_note(list):
    html_content = []
    html_content.append('<div class="section" id="release_notes">')
    html_content.append('<h2>')
    html_content.append(u'Release Note')
    html_content.append(u'<a class="headerlink" href="#release_notes" title="Permalink to this headline">¶</a>')
    html_content.append('</h2>')
    html_content.append('<table border="1" class="docutils"><thead valign="bottom"><tr>')
    html_content.append(u'<th class="head">Revision</th>')
    html_content.append(u'<th class="head">Date</th>')
    html_content.append(u'<th class="head">Commit log</th>')
    html_content.append(u'<th class="head">Author</th>')
    html_content.append(u'<th class="head">Survey</th>')
    html_content.append(u'<th class="head">Approval</th>')
    html_content.append('</tr></thead><tbody valign="top">')
    for i in list:
        html_content.append('<tr>')
        html_content.append('<td>%s</td>' % i['hash'].decode('utf-8'))
        html_content.append('<td>%s</td>' % i['date'].decode('utf-8'))
        html_content.append('<td>%s</td>' % i['log'].decode('utf-8'))
        html_content.append('<td>%s</td>' % i['author'].decode('utf-8'))
        html_content.append('<td>%s</td>' % i['survey'])
        html_content.append('<td>%s</td>' % i['approval'])
        html_content.append('</tr>')
    html_content.append('</tbody></table>')
    html_content.append('</div>')

    return html_content
