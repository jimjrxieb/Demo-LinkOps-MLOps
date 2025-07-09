#!/usr/bin/env node

/**
 * HoloCore Simple Integration Test
 * Tests backend API endpoints using fetch
 */

const API_BASE = 'http://localhost:8000';

const testCases = [
  {
    name: 'Backend Health Check',
    test: async () => {
      const response = await fetch(`${API_BASE}/health`);
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
      const response = await fetch(`${API_BASE}/api/james/evaluate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData)
      });
      const data = await response.json();
      return data && data.detected_category;
    }
  },
  {
    name: 'Whis Queue Status',
    test: async () => {
      const response = await fetch(`${API_BASE}/api/whis/queue`);
      const data = await response.json();
      return data && typeof data.pending === 'number';
    }
  },
  {
    name: 'Whis Approvals',
    test: async () => {
      const response = await fetch(`${API_BASE}/api/whis/approvals`);
      const data = await response.json();
      return Array.isArray(data);
    }
  },
  {
    name: 'Whis Digest',
    test: async () => {
      const response = await fetch(`${API_BASE}/api/whis/digest`);
      const data = await response.json();
      return data && data.runes_created !== undefined;
    }
  }
];

async function runTests() {
  // Development log removed
  console.log('=' .repeat(50));
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
    const response = await fetch(`${API_BASE}/health`);
    return response.status === 200;
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