module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore', 'perf'],
    ],
    'scope-enum': [
      2,
      'always',
      ['mini', 'h5', 'admin', 'server', 'config', 'ci', 'deps'],
    ],
    'subject-min-length': [2, 'always', 5],
    'subject-max-length': [2, 'always', 100],
  },
};
