#!/usr/bin/env node

/**
 * HoloCore Integration Test
 * Tests all Vue frontend + backend API integration
 */

import axios from 'axios';

const API_BASE = 'http://localhost:8000';
const FRONTEND_URL = 'http://localhost:3000';

const testCases = [
  {
    name: 'Backend Health Check',
    test: async () => {
      const response = await axios.get(`${API_BASE}/health`);
      return response.status === 200;
    }
  },
  {
    name: 'James Task Evaluation',
    test: async () => {
      const taskData = {
        task_id: 'test/holocore-integration',
        task_description: 'Test HoloCore integration with Vue frontend'
      };
      const response = await axios.post(`${API_BASE}/api/james/evaluate`, taskData);
      return response.data && response.data.detected_category;
    }
  },
  {
    name: 'Whis Queue Status',
    test: async () => {
      const response = await axios.get(`${API_BASE}/api/whis/queue`);
      return response.data && typeof response.data.pending === 'number';
    }
  },
  {
    name: 'Whis Approvals',
    test: async () => {
      const response = await axios.get(`${API_BASE}/api/whis/approvals`);
      return Array.isArray(response.data);
    }
  },
  {
    name: 'Whis Digest',
    test: async () => {
      const response = await axios.get(`${API_BASE}/api/whis/digest`);
      return response.data && response.data.runes_created !== undefined;
    }
  },
  {
    name: 'Night Training',
    test: async () => {
      const response = await axios.post(`${API_BASE}/api/whis/train-nightly`);
      return response.data && response.data.tasks_processed !== undefined;
    }
  }
];

async function runTests() {
  // Development log removed
  console.log('=' .repeat(50));
  // Development log removed
  // Development log removed
  // Development log removed

  let passed = 0;
  let failed = 0;

  for (const testCase of testCases) {
    try {
      // Development log removed
      const result = await testCase.test();
      
      if (result) {
        // Development log removed
        passed++;
      } else {
        // Development log removed
        failed++;
      }
    } catch (error) {
      // Development log removed
      failed++;
    }
    // Development log removed
  }

  console.log('=' .repeat(50));
  // Development log removed
  
  if (failed === 0) {
    // Development log removed
    // Development log removed
    // Development log removed
    // Development log removed
    // Development log removed
    // Development log removed
  } else {
    // Development log removed
  }
}

// Check if backend is running
async function checkBackend() {
  try {
    await axios.get(`${API_BASE}/health`);
    return true;
  } catch (error) {
    // Development log removed
    return false;
  }
}

async function main() {
  const backendRunning = await checkBackend();
  if (backendRunning) {
    await runTests();
  }
}

main().catch(console.error); 