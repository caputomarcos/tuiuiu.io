#!/usr/bin/env node
var cli = require('yargs');

cli
  .usage('Usage: $0 <command> [options]')
  .help('help');

cli
  .command(
    'component <name>',
    'scaffold out a tuiuiu component',
    require('./component'));

cli
  .argv;
