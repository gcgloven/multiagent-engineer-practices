"""Single registry for generated roles, skill bindings and squad membership."""

SPECS = {
    'lead': ('Lead', ['frame-problem'], 'Coordinates specialist work and human decisions'),
    'scout': ('Scout', ['investigate-question', 'frame-problem'], 'Explores questions and evidence'),
    'paper-reviewer': ('Paper Reviewer', ['review-paper', 'extract-paper-pdf', 'investigate-question'], 'Reviews papers and literature'),
    'analyst': ('Analyst', ['analyze-data', 'run-experiment', 'frame-problem', 'ub-coding'], 'Owns analysis and measurement contracts'),
    'systems-engineer': ('Systems Engineer', ['design-solution', 'frame-problem', 'ub-design'], 'Owns domain models, architecture and system contracts'),
    'software-engineer': ('Software Engineer', ['deliver-slice', 'run-experiment', 'ub-coding'], 'Implements authorized software and developer tests'),
    'test-code-review-engineer': ('Test & Code Review Engineer', ['deliver-slice', 'ub-review'], 'Independently reviews software and test effectiveness'),
    'verifier': ('Verifier', ['run-experiment', 'design-solution'], 'Independently assesses scientific, measurement and design evidence'),
    'product-manager': ('Product Manager', ['frame-problem', 'explain-work'], 'Clarifies stakeholder needs, requirements and success measures'),
}
ROLES = tuple(SPECS)
SQUADS = {
    'research-engineering': {
        'name': 'Engineering Practice Squad',
        'members': tuple(role for role in ROLES if role != 'lead'),
        'optional_members': tuple(role for role in ROLES if role != 'lead'),
    },
    'open-research': {
        'name': 'Open Research Squad',
        'members': ('scout', 'paper-reviewer', 'analyst', 'verifier'),
    },
    'analytics-engineering': {
        'name': 'Analytics Engineering Squad',
        'members': ('analyst', 'software-engineer', 'test-code-review-engineer', 'verifier', 'systems-engineer'),
        'optional_members': ('systems-engineer',),
    },
    'software-delivery': {
        'name': 'Software Delivery Squad',
        'members': ('software-engineer', 'test-code-review-engineer', 'systems-engineer', 'product-manager', 'verifier'),
        'optional_members': ('systems-engineer', 'product-manager', 'verifier'),
    },
    'engineering-design': {
        'name': 'Engineering Design Squad',
        'members': ('systems-engineer', 'product-manager', 'verifier', 'software-engineer', 'test-code-review-engineer'),
        'optional_members': ('product-manager', 'software-engineer', 'test-code-review-engineer'),
    },
}
SKILLS = ('frame-problem', 'investigate-question', 'review-paper', 'extract-paper-pdf', 'analyze-data',
          'run-experiment', 'deliver-slice', 'explain-work', 'design-solution',
          'ub-coding', 'ub-review', 'ub-design')
