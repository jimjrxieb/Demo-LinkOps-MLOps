#!/usr/bin/env node

/**
 * Frontend-Backend Integration Test
 * Tests all API endpoints to ensure frontend can connect to backend services
 */

const axios = require('axios');

// Configuration
const SERVICES = {
  mlopsPlatform: 'http://localhost:8000',
  auditAssess: 'http://localhost:8003',
  whisDataInput: 'http://localhost:8004',
  whisEnhance: 'http://localhost:8006'
};

// Colors for console output
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

async function testHealthEndpoint(serviceName, url) {
  try {
    const response = await axios.get(`${url}/health`, { timeout: 5000 });
    log(`✅ ${serviceName}: Healthy`, 'green');
    return { service: serviceName, status: 'healthy', data: response.data };
  } catch (error) {
    log(`❌ ${serviceName}: Unhealthy - ${error.message}`, 'red');
    return { service: serviceName, status: 'unhealthy', error: error.message };
  }
}

async function testMLOpsPlatform() {
  log('\n🔧 Testing MLOps Platform API...', 'blue');
  
  const tests = [
    { name: 'Health Check', endpoint: '/health', method: 'GET' },
    { name: 'Get Tasks', endpoint: '/tasks/', method: 'GET' },
    { name: 'Get Scripts', endpoint: '/scripts/', method: 'GET' },
    { name: 'Get Orbs', endpoint: '/orbs/', method: 'GET' },
    { name: 'Get Runes', endpoint: '/runes/', method: 'GET' },
    { name: 'Get Digest', endpoint: '/digest/', method: 'GET' }
  ];

  for (const test of tests) {
    try {
      const response = await axios({
        method: test.method,
        url: `${SERVICES.mlopsPlatform}${test.endpoint}`,
        timeout: 5000
      });
      log(`  ✅ ${test.name}: ${response.status}`, 'green');
    } catch (error) {
      log(`  ❌ ${test.name}: ${error.response?.status || error.message}`, 'red');
    }
  }
}

async function testAuditAssess() {
  log('\n🔍 Testing Audit Assess API...', 'blue');
  
  const tests = [
    { name: 'Health Check', endpoint: '/health', method: 'GET' },
    { name: 'Get Suggestions', endpoint: '/scan/suggestions/', method: 'GET' },
    { name: 'Get Scaffold Plan', endpoint: '/scan/scaffold-plan/', method: 'GET' }
  ];

  for (const test of tests) {
    try {
      const response = await axios({
        method: test.method,
        url: `${SERVICES.auditAssess}${test.endpoint}`,
        timeout: 5000
      });
      log(`  ✅ ${test.name}: ${response.status}`, 'green');
    } catch (error) {
      log(`  ❌ ${test.name}: ${error.response?.status || error.message}`, 'red');
    }
  }

  // Test audit endpoint with sample data
  try {
    const auditData = {
      repo_url: 'https://github.com/test/test-repo',
      branch: 'main'
    };
    
    log('  🔄 Testing repository audit (this may take a while)...', 'yellow');
    const response = await axios({
      method: 'POST',
      url: `${SERVICES.auditAssess}/scan/audit`,
      data: auditData,
      timeout: 30000
    });
    log(`  ✅ Repository Audit: ${response.status}`, 'green');
  } catch (error) {
    log(`  ❌ Repository Audit: ${error.response?.status || error.message}`, 'red');
  }
}

async function testWhisDataInput() {
  log('\n📥 Testing Whis Data Input API...', 'blue');
  
  const tests = [
    { name: 'Health Check', endpoint: '/health', method: 'GET' }
  ];

  for (const test of tests) {
    try {
      const response = await axios({
        method: test.method,
        url: `${SERVICES.whisDataInput}${test.endpoint}`,
        timeout: 5000
      });
      log(`  ✅ ${test.name}: ${response.status}`, 'green');
    } catch (error) {
      log(`  ❌ ${test.name}: ${error.response?.status || error.message}`, 'red');
    }
  }
}

async function testWhisEnhance() {
  log('\n🚀 Testing Whis Enhance API...', 'blue');
  
  const tests = [
    { name: 'Health Check', endpoint: '/health', method: 'GET' },
    { name: 'Get Loopback Stats', endpoint: '/loopback/stats', method: 'GET' }
  ];

  for (const test of tests) {
    try {
      const response = await axios({
        method: test.method,
        url: `${SERVICES.whisEnhance}${test.endpoint}`,
        timeout: 5000
      });
      log(`  ✅ ${test.name}: ${response.status}`, 'green');
    } catch (error) {
      log(`  ❌ ${test.name}: ${error.response?.status || error.message}`, 'red');
    }
  }
}

async function testFrontendProxy() {
  log('\n🌐 Testing Frontend Proxy Configuration...', 'blue');
  
  const proxyTests = [
    { name: 'MLOps Platform Proxy', url: 'http://localhost:3000/api/tasks/' },
    { name: 'Audit Assess Proxy', url: 'http://localhost:3000/audit/health' },
    { name: 'Whis Data Input Proxy', url: 'http://localhost:3000/whis-data/health' },
    { name: 'Whis Enhance Proxy', url: 'http://localhost:3000/whis-enhance/health' }
  ];

  for (const test of proxyTests) {
    try {
      const response = await axios.get(test.url, { timeout: 5000 });
      log(`  ✅ ${test.name}: ${response.status}`, 'green');
    } catch (error) {
      log(`  ❌ ${test.name}: ${error.response?.status || error.message}`, 'red');
    }
  }
}

async function runAllTests() {
  log('🚀 Starting Frontend-Backend Integration Tests', 'blue');
  log('==============================================', 'blue');

  // Test health endpoints
  log('\n🏥 Testing Service Health...', 'blue');
  const healthResults = await Promise.all([
    testHealthEndpoint('MLOps Platform', SERVICES.mlopsPlatform),
    testHealthEndpoint('Audit Assess', SERVICES.auditAssess),
    testHealthEndpoint('Whis Data Input', SERVICES.whisDataInput),
    testHealthEndpoint('Whis Enhance', SERVICES.whisEnhance)
  ]);

  // Test individual service APIs
  await testMLOpsPlatform();
  await testAuditAssess();
  await testWhisDataInput();
  await testWhisEnhance();

  // Test frontend proxy (if frontend is running)
  await testFrontendProxy();

  // Summary
  log('\n📊 Test Summary', 'blue');
  log('===============', 'blue');
  
  const healthyServices = healthResults.filter(r => r.status === 'healthy').length;
  const totalServices = healthResults.length;
  
  log(`Services Healthy: ${healthyServices}/${totalServices}`, healthyServices === totalServices ? 'green' : 'yellow');
  
  if (healthyServices === totalServices) {
    log('\n🎉 All services are healthy! Frontend should be able to connect successfully.', 'green');
  } else {
    log('\n⚠️  Some services are unhealthy. Please check the service status before testing frontend.', 'yellow');
  }

  log('\n💡 Next Steps:', 'blue');
  log('1. Start the frontend: cd frontend && npm run dev', 'reset');
  log('2. Open http://localhost:3000 in your browser', 'reset');
  log('3. Test the audit form and dashboard functionality', 'reset');
}

// Run tests if this script is executed directly
if (require.main === module) {
  runAllTests().catch(error => {
    log(`\n💥 Test execution failed: ${error.message}`, 'red');
    process.exit(1);
  });
}

module.exports = {
  testHealthEndpoint,
  testMLOpsPlatform,
  testAuditAssess,
  testWhisDataInput,
  testWhisEnhance,
  testFrontendProxy,
  runAllTests
}; 