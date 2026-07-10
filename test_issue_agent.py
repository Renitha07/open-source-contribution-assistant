import os
os.chdir(r'C:\Users\V M Renitha\OneDrive\Desktop\open-source-contribution-assistant')
import sys
sys.path.insert(0, '.')

from graph.builder import graph

initial_state = {
    'repository_url': 'https://github.com/scikit-learn/scikit-learn',
    'repository': {},
    'repository_understanding': {},
    'architecture': {},
    'issue_intelligence': {},
    'execution': {
        'current_stage': 'start',
        'status': 'running',
    },
}

print('Testing full workflow...')
result = graph.invoke(initial_state)

print()
print('=' * 60)
print('ISSUE INTELLIGENCE')
print('=' * 60)
ii = result['issue_intelligence']
print('Total Fetched:', ii['total_fetched'])
print('Filtered:', ii['filtered_count'])
top = ii['top_recommendation']
print('Top Recommendation: #' + str(top['issue']['number']) + ' - ' + top['issue']['title'])
print('Score:', top['score'])
print('Difficulty:', top['difficulty'])
print('Estimated Hours:', top['estimated_hours'])
print('Reasoning:', top['reasoning'][:200])
print('Approach:', top['suggested_approach'][:200])
print()
print('All Ranked Issues:')
for r in ii['ranked_issues'][:5]:
    print('  #' + str(r['issue']['number']) + ' (' + str(r['score']) + ') - ' + r['issue']['title'][:60])
print()
print('Final Stage:', result['execution']['current_stage'])