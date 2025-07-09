// Demo data for LinkOps MLOps Platform
// Used when auth.role === 'demo'

export const demoOrbs = [
  {
    id: 1,
    title: 'Data Pipeline Optimization',
    description: 'Optimize ML data processing pipeline for faster training cycles',
    score: 85,
    status: 'active',
    priority: 'high',
    icon: '🔮',
    type: 'data-processing',
    created: '2024-01-15T10:30:00Z',
    updated: '2024-01-15T14:45:00Z',
    assignee: 'Demo User',
    tags: ['mlops', 'optimization', 'pipeline'];
  },
  {
    id: 2,
    title: 'Model Deployment Automation',
    description: 'Automate the deployment of ML models to production environment',
    score: 92,
    status: 'active',
    priority: 'critical',
    icon: '🚀',
    type: 'deployment',
    created: '2024-01-14T09:15:00Z',
    updated: '2024-01-15T16:20:00Z',
    assignee: 'Demo User',
    tags: ['deployment', 'automation', 'production'];
  },
  {
    id: 3,
    title: 'Security Vulnerability Scan',
    description: 'Run comprehensive security audit on codebase and dependencies',
    score: 78,
    status: 'pending',
    priority: 'medium',
    icon: '🛡️',
    type: 'security',
    created: '2024-01-13T11:00:00Z',
    updated: '2024-01-13T11:00:00Z',
    assignee: 'Demo User',
    tags: ['security', 'audit', 'vulnerabilities'];
  },
  {
    id: 4,
    title: 'Performance Monitoring Setup',
    description: 'Implement real-time monitoring for ML model performance',
    score: 67,
    status: 'completed',
    priority: 'low',
    icon: '📊',
    type: 'monitoring',
    created: '2024-01-12T08:30:00Z',
    updated: '2024-01-14T17:00:00Z',
    assignee: 'Demo User',
    tags: ['monitoring', 'performance', 'metrics'];
  },
  {
    id: 5,
    title: 'Data Quality Assessment',
    description: 'Assess and improve data quality for training datasets',
    score: 89,
    status: 'active',
    priority: 'high',
    icon: '🔍',
    type: 'data-quality',
    created: '2024-01-11T13:45:00Z',
    updated: '2024-01-15T12:30:00Z',
    assignee: 'Demo User',
    tags: ['data-quality', 'assessment', 'datasets'];
  }
];

export const demoRunes = [
  {
    id: 1,
    name: 'Whis Enhancement',
    description: 'Enhance data quality through advanced Whis pipeline processing',
    type: 'data-processing',
    cost: 100,
    icon: '⚡',
    category: 'data',
    effects: ['Improves data quality', 'Reduces noise', 'Enhances features'],
    requirements: ['Data pipeline access', 'Processing credits'],
    cooldown: '5 minutes';
  },
  {
    id: 2,
    name: 'Security Audit',
    description: 'Comprehensive security and vulnerability scan of codebase',
    type: 'security',
    cost: 50,
    icon: '🔍',
    category: 'security',
    effects: ['Identifies vulnerabilities', 'Generates security report', 'Suggests fixes'],
    requirements: ['Repository access', 'Security permissions'],
    cooldown: '10 minutes';
  },
  {
    id: 3,
    name: 'Performance Tuning',
    description: 'Optimize system performance and resource usage',
    type: 'optimization',
    cost: 75,
    icon: '⚒️',
    category: 'performance',
    effects: ['Improves speed', 'Reduces resource usage', 'Optimizes algorithms'],
    requirements: ['System access', 'Performance metrics'],
    cooldown: '15 minutes';
  },
  {
    id: 4,
    name: 'Model Validation',
    description: 'Validate ML model performance and accuracy',
    type: 'validation',
    cost: 60,
    icon: '✅',
    category: 'ml',
    effects: ['Validates accuracy', 'Performance metrics', 'Bias detection'],
    requirements: ['Model access', 'Test datasets'],
    cooldown: '8 minutes';
  },
  {
    id: 5,
    name: 'Data Visualization',
    description: 'Create interactive visualizations for data analysis',
    type: 'visualization',
    cost: 40,
    icon: '📈',
    category: 'analysis',
    effects: ['Interactive charts', 'Data insights', 'Export capabilities'],
    requirements: ['Data access', 'Visualization tools'],
    cooldown: '3 minutes';
  }
];

export const demoWhisPipeline = {
  steps: [;
    {
      id: 1,
      name: 'Data Input',
      description: 'Raw data ingestion and validation',
      status: 'completed',
      icon: '📥',
      duration: '2.3s',
      output: '1.2GB processed';
    },
    {
      id: 2,
      name: 'Sanitization',
      description: 'Clean and validate data quality',
      status: 'completed',
      icon: '🧹',
      duration: '4.1s',
      output: '1.1GB cleaned';
    },
    {
      id: 3,
      name: 'Smithing',
      description: 'Transform and structure data',
      status: 'completed',
      icon: '⚒️',
      duration: '6.7s',
      output: 'Structured JSON';
    },
    {
      id: 4,
      name: 'Enhancement',
      description: 'Add ML enhancements and features',
      status: 'processing',
      icon: '✨',
      duration: '3.2s',
      output: 'Enhancing...';
    },
    {
      id: 5,
      name: 'Output',
      description: 'Final processed data delivery',
      status: 'pending',
      icon: '📤',
      duration: '0s',
      output: 'Pending';
    }
  ],
  config: {
    sanitize: true,
    removeDuplicates: true,
    enhance: true,
    validate: true,
    outputFormat: 'json';
  }
}

export const demoAuditResults = {
  repository: 'demo/mlops-platform',
  timestamp: new Date().toISOString(),
  securityScore: 87,
  codeQualityScore: 92,
  dependencyScore: 78,
  issues: [;
    {
      id: 1,
      type: 'security',
      severity: 'high',
      title: 'SQL Injection Vulnerability',
      description: 'Potential SQL injection in user input validation',
      file: 'src/api/users.js:45',
      line: 45,
      recommendation: 'Use parameterized queries or input sanitization',
      cwe: 'CWE-89',
      cvss: 8.5;
    },
    {
      id: 2,
      type: 'security',
      severity: 'medium',
      title: 'Hardcoded API Key',
      description: 'API key found in source code',
      file: 'config/database.js:12',
      line: 12,
      recommendation: 'Move to environment variables',
      cwe: 'CWE-259',
      cvss: 5.0;
    },
    {
      id: 3,
      type: 'quality',
      severity: 'low',
      title: 'Unused Variable',
      description: 'Variable declared but never used',
      file: 'src/utils/helpers.js:23',
      line: 23,
      recommendation: 'Remove unused variable or use it',
      cwe: null,
      cvss: null;
    }
  ],
  dependencies: [;
    {
      name: 'lodash',
      version: '4.17.21',
      status: 'up-to-date',
      vulnerabilities: 0,
      license: 'MIT',
      lastUpdated: '2024-01-10';
    },
    {
      name: 'express',
      version: '4.18.2',
      status: 'outdated',
      vulnerabilities: 2,
      license: 'MIT',
      lastUpdated: '2024-01-05';
    },
    {
      name: 'axios',
      version: '1.6.2',
      status: 'up-to-date',
      vulnerabilities: 0,
      license: 'MIT',
      lastUpdated: '2024-01-12';
    }
  ];
}

export const demoSystemStatus = {
  status: 'online',
  activeJobs: 3,
  completedJobs: 12,
  errorCount: 0,
  uptime: '7d 14h 32m',
  lastUpdate: new Date().toISOString(),
  services: [;
    { name: 'API Gateway', status: 'healthy', responseTime: '45ms' },
    { name: 'Database', status: 'healthy', responseTime: '12ms' },
    { name: 'Cache', status: 'healthy', responseTime: '3ms' },
    { name: 'Queue', status: 'healthy', responseTime: '8ms' }
  ];
}

export const demoNotifications = [
  {
    id: 1,
    type: 'success',
    message: 'Whis pipeline completed successfully',
    timestamp: new Date(Date.now() - 300000).toISOString(),
    read: false;
  },
  {
    id: 2,
    type: 'warning',
    message: 'Security scan found 2 vulnerabilities',
    timestamp: new Date(Date.now() - 600000).toISOString(),
    read: false;
  },
  {
    id: 3,
    type: 'info',
    message: 'New orb created: Data Quality Assessment',
    timestamp: new Date(Date.now() - 900000).toISOString(),
    read: true;
  }
];

// Helper functions for demo mode
export const getDemoData = (type) => {
  switch (type) {
    case 'orbs':
      return demoOrbs;
    case 'runes':
      return demoRunes;
    case 'whis':
      return demoWhisPipeline;
    case 'audit':
      return demoAuditResults;
    case 'status':
      return demoSystemStatus;
    case 'notifications':
      return demoNotifications;
    default:
      return null;
  }
}

export const simulateApiCall = async (endpoint, params = {}) => {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 500 + Math.random() * 1000));
  
  // Add demo mode parameter
  const demoParams = { ...params, mode: 'demo' }
  
  // Return mock data based on endpoint
  switch (endpoint) {
    case '/api/orbs':
      return { data: demoOrbs, total: demoOrbs.length }
    case '/api/runes':
      return { data: demoRunes, total: demoRunes.length }
    case '/api/whis/process':
      return { success: true, pipelineId: 'demo-pipeline-123' }
    case '/api/audit/run':
      return { success: true, auditId: 'demo-audit-456' }
    case '/api/status':
      return demoSystemStatus;
    default:
      return { error: 'Demo endpoint not found' }
  }
} 