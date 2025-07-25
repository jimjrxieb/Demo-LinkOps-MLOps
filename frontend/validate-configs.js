#!/usr/bin/env node

/**
 * Config Validation Script
 * Tests all configuration files for syntax errors before building
 */

const fs = require('fs');
const path = require('path');

console.log('🔍 Validating configuration files...\n');

const configs = [
  { name: 'postcss.config.js', path: './postcss.config.js' },
  { name: 'tailwind.config.js', path: './tailwind.config.js' },
  { name: 'vite.config.js', path: './vite.config.js' },
  { name: 'package.json', path: './package.json' },
];

let allValid = true;

configs.forEach((config) => {
  try {
    console.log(`📋 Testing ${config.name}...`);

    // Test if file exists
    if (!fs.existsSync(config.path)) {
      throw new Error(`File not found: ${config.path}`);
    }

    // Test if file can be parsed
    const content = fs.readFileSync(config.path, 'utf8');

    if (config.name === 'package.json') {
      JSON.parse(content);
    } else {
      // For JS files, try to require them
      require(path.resolve(config.path));
    }

    console.log(`✅ ${config.name} - Valid`);
  } catch (error) {
    console.error(`❌ ${config.name} - Error: ${error.message}`);
    allValid = false;
  }
});

console.log('\n' + '='.repeat(50));

if (allValid) {
  console.log('🎉 All configuration files are valid!');
  console.log('🚀 Ready to build...');
  process.exit(0);
} else {
  console.log('💥 Configuration validation failed!');
  console.log('🔧 Please fix the errors above before building.');
  process.exit(1);
}
