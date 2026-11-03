"""Check public rules without node credentials."""
from pathlib import Path
import sys
import concurrent.futures
import urllib.request
import yaml

root = Path(__file__).resolve().parent
c = yaml.safe_load((root / 'clash-rules.yaml').read_text())
dns = yaml.safe_load((root / 'nikki-dns.yaml').read_text())['dns']
sr = (root / 'shadowrocket-rules.conf').read_text()
groups = {g['name']: g for g in c['proxy-groups']}
for name, expected in [('🤖 AI','🇩🇪 德国节点'),('🚀 节点选择','🇭🇰 上海电信')]:
    assert groups[name]['proxies'] == [expected]
    assert not groups[name].get('include-all-proxies')
    assert f'{name} = select,{expected}\n' in sr
rules = c['rules']
assert rules[-1] == 'MATCH,🚀 节点选择'
for name in ['AIInternational','AdvertisingDomains']:
    assert next(i for i,r in enumerate(rules) if r.startswith('RULE-SET,'+name+',')) < rules.index('RULE-SET,ChinaDomains,DIRECT')
for r in rules:
    parts = r.split(',')
    policy = parts[-2] if parts[-1] == 'no-resolve' else parts[-1]
    assert policy in groups or policy in {'DIRECT','REJECT'}, r
    if parts[0] == 'RULE-SET': assert parts[1] in c['rule-providers'], r
for domain in (root / 'ai-extra.txt').read_text().splitlines():
    if domain and not domain.startswith('#'):
        assert f'DOMAIN-SUFFIX,{domain},🤖 AI' in rules, domain
        assert f'DOMAIN-SUFFIX,{domain},🤖 AI' in sr, domain
for domain in ['chatgpt.com','openai.com','oaistatic.com','oaiusercontent.com','claude.ai']:
    assert f'DOMAIN-SUFFIX,{domain},🤖 AI' in rules
assert dns['direct-nameserver'] and dns['proxy-server-nameserver'] and dns['nameserver']
assert all('#🚀 节点选择' in u for u in dns['nameserver'])
assert dns['direct-nameserver-follow-policy'] is False
assert not any(k in c for k in ['proxies','proxy-providers','secret','authentication'])
print(f'Passed: {len(groups)} groups, {len(rules)} rules, {len(c["rule-providers"])} providers.')
if '--online' in sys.argv:
    urls = {v['url'] for v in c['rule-providers'].values()}
    urls |= {l.split(',')[1] for l in sr.splitlines() if l.startswith(('RULE-SET,https://','DOMAIN-SET,https://'))}
    def check(url):
        assert url.startswith('https://raw.githubusercontent.com/') and '?' not in url
        with urllib.request.urlopen(urllib.request.Request(url,method='HEAD'),timeout=25) as response:
            assert response.status == 200, url
        return url
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: results=list(pool.map(check,sorted(urls)))
    print(f'Public sources passed: {len(results)} URLs.')
