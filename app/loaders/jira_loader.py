import os
from datetime import datetime

from jira import JIRA
from haystack import Document

class JiraLoader:
    def __init__(self, base_url, email, token, jql=None, max_results=50):
        self.client = JIRA(server=base_url.rstrip('/'), basic_auth=(email, token))
        self.jql = jql or ''
        self.max_results = max_results

    def load(self):
        issues = self._get_issues()
        documents = []
        for issue in issues:
            fields = issue.fields
            description = fields.description
            content = self._parse_description(description)
            metadata = {
                'id': issue.key,
                'title': fields.summary,
                'created_at': fields.created
            }
            documents.append(Document(id=issue.key, content=content, meta=metadata))
        documents.sort(key=lambda d: datetime.fromisoformat(d.meta['created_at'].replace('Z', '+00:00')), reverse=True)
        return documents

    def _get_issues(self):
        start_at = 0
        issues = []
        while True:
            batch = self.client.search_issues(
                self.jql,
                startAt=start_at,
                maxResults=self.max_results,
                fields='summary,description,created,status'
            )
            if not batch:
                break
            issues.extend(batch)
            if len(batch) < self.max_results:
                break
            start_at += self.max_results
        return issues

    def _parse_description(self, description):
        if not description:
            return ''
        if isinstance(description, str):
            return description
        texts = []
        def extract(node):
            if hasattr(node, 'text') and node.text:
                texts.append(node.text)
            if hasattr(node, 'content'):
                for child in node.content:
                    extract(child)
        extract(description)
        return '\n'.join(texts)