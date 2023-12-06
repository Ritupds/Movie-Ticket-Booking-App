module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: ['eslint:recommended', 'plugin:vue/essential'],
  // parserOptions: {
  //   parser: 'babel-eslint',
  //   sourceType: 'module',
  // },
  parserOptions: {
    parser: '@typescript-eslint/parser',
    sourceType: 'module',
  },
  rules: {},
};
