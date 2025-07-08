<template>
  <div class="runes-container">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="futuristic-title text-4xl mb-2">🧪 Runes Library</h1>
      <p class="text-gray-300">Automation scripts and executable solutions from the Whis AI</p>
    </div>

    <!-- Search and Filters -->
    <div class="glass-panel p-6 mb-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">Search Runes</label>
          <input
            v-model="searchQuery"
            type="text"
            class="w-full glass-panel p-3 rounded-lg border border-gray-600 bg-transparent text-white placeholder-gray-400 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
            placeholder="Search by title, language, or function..."
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">Language</label>
          <select
            v-model="selectedLanguage"
            class="w-full glass-panel p-3 rounded-lg border border-gray-600 bg-transparent text-white focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
          >
            <option value="">All Languages</option>
            <option value="bash">Bash</option>
            <option value="python">Python</option>
            <option value="go">Go</option>
            <option value="yaml">YAML</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">Effectiveness</label>
          <select
            v-model="selectedEffectiveness"
            class="w-full glass-panel p-3 rounded-lg border border-gray-600 bg-transparent text-white focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
          >
            <option value="">Any Effectiveness</option>
            <option value="90">Excellent (90+)</option>
            <option value="80">Good (80+)</option>
            <option value="70">Fair (70+)</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">Category</label>
          <select
            v-model="selectedCategory"
            class="w-full glass-panel p-3 rounded-lg border border-gray-600 bg-transparent text-white focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
          >
            <option value="">All Categories</option>
            <option value="deployment">Deployment</option>
            <option value="monitoring">Monitoring</option>
            <option value="security">Security</option>
            <option value="automation">Automation</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Stats Overview -->
    <div class="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">
      <div class="glass-panel p-6 text-center">
        <div class="text-3xl font-bold text-purple-400 mb-2">{{ stats.total }}</div>
        <div class="text-sm text-gray-300">Total Runes</div>
      </div>
      <div class="glass-panel p-6 text-center">
        <div class="text-3xl font-bold text-green-400 mb-2">{{ stats.executed }}</div>
        <div class="text-sm text-gray-300">Successfully Executed</div>
      </div>
      <div class="glass-panel p-6 text-center">
        <div class="text-3xl font-bold text-blue-400 mb-2">{{ stats.avgEffectiveness }}%</div>
        <div class="text-sm text-gray-300">Avg Effectiveness</div>
      </div>
      <div class="glass-panel p-6 text-center">
        <div class="text-3xl font-bold text-yellow-400 mb-2">{{ stats.automationTime }}</div>
        <div class="text-sm text-gray-300">Time Saved</div>
      </div>
      <div class="glass-panel p-6 text-center">
        <div class="text-3xl font-bold text-indigo-400 mb-2">{{ stats.languages }}</div>
        <div class="text-sm text-gray-300">Languages</div>
      </div>
    </div>

    <!-- Runes Grid -->
    <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
      <div
        v-for="rune in filteredRunes"
        :key="rune.id"
        class="glass-panel p-6 rounded-lg hover:neon-border transition-all duration-300"
        :class="`rune-${rune.language}`"
      >
        <!-- Rune Header -->
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-3">
            <span class="text-2xl">{{ getLanguageIcon(rune.language) }}</span>
            <div>
              <h3 class="futuristic-subtitle text-lg">{{ rune.title }}</h3>
              <div class="flex items-center space-x-2 text-xs text-gray-400">
                <span>{{ rune.language.toUpperCase() }}</span>
                <span>•</span>
                <span>{{ rune.category }}</span>
                <span>•</span>
                <span>{{ rune.timestamp }}</span>
              </div>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <div class="effectiveness-score" :class="getEffectivenessClass(rune.effectiveness)">
              {{ rune.effectiveness }}%
            </div>
            <div class="status-badge" :class="rune.status">
              {{ rune.status }}
            </div>
          </div>
        </div>

        <!-- Rune Description -->
        <div class="mb-4">
          <p class="text-sm text-gray-300">{{ rune.description }}</p>
        </div>

        <!-- Code Preview -->
        <div class="mb-4">
          <div class="code-preview glass-panel p-4 rounded-lg bg-gray-900">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-medium text-gray-400">{{ rune.language.toUpperCase() }} SCRIPT</span>
              <button
                @click="copyCode(rune.script)"
                class="text-xs text-gray-400 hover:text-white transition-colors"
              >
                📋 Copy
              </button>
            </div>
            <pre class="text-xs text-gray-300 overflow-x-auto"><code>{{ rune.script.slice(0, 200) }}{{ rune.script.length > 200 ? '...' : '' }}</code></pre>
          </div>
        </div>

        <!-- Execution Steps -->
        <div class="mb-4">
          <h4 class="text-sm font-medium text-gray-200 mb-2">Execution Steps:</h4>
          <ol class="text-xs text-gray-400 space-y-1">
            <li v-for="(step, index) in rune.steps.slice(0, 3)" :key="index" class="flex items-start space-x-2">
              <span class="text-indigo-400">{{ index + 1 }}.</span>
              <span>{{ step }}</span>
            </li>
            <li v-if="rune.steps.length > 3" class="text-gray-500 ml-4">
              ... and {{ rune.steps.length - 3 }} more steps
            </li>
          </ol>
        </div>

        <!-- Tags and Metrics -->
        <div class="mb-4">
          <div class="flex flex-wrap gap-2 mb-2">
            <span
              v-for="tag in rune.tags.slice(0, 4)"
              :key="tag"
              class="px-2 py-1 text-xs glass-panel rounded"
            >
              {{ tag }}
            </span>
          </div>
          <div class="grid grid-cols-3 gap-4 text-xs text-gray-400">
            <div class="text-center">
              <div class="font-medium text-white">{{ rune.executions }}</div>
              <div>Executions</div>
            </div>
            <div class="text-center">
              <div class="font-medium text-white">{{ rune.successRate }}%</div>
              <div>Success Rate</div>
            </div>
            <div class="text-center">
              <div class="font-medium text-white">{{ rune.avgTime }}</div>
              <div>Avg Time</div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center justify-between">
          <div class="flex space-x-2">
            <button
              @click="viewRune(rune)"
              class="px-3 py-1 text-xs glass-panel rounded hover:neon-border transition-all duration-300"
            >
              View Full Script
            </button>
            <button
              @click="executeRune(rune)"
              class="px-3 py-1 text-xs glass-panel rounded hover:neon-border transition-all duration-300 text-green-400"
              :disabled="rune.status === 'pending'"
            >
              🚀 Execute
            </button>
            <button
              v-if="rune.status === 'pending'"
              @click="approveRune(rune)"
              class="px-3 py-1 text-xs glass-panel rounded hover:neon-border transition-all duration-300 text-blue-400"
            >
              ✓ Approve
            </button>
          </div>
          <div class="text-xs text-gray-400">
            Related Orb: #{{ rune.relatedOrb }}
          </div>
        </div>
      </div>
    </div>

    <!-- Load More -->
    <div v-if="hasMore" class="text-center mt-8">
      <button
        @click="loadMore"
        class="glass-panel px-6 py-3 rounded-lg futuristic-subtitle hover:neon-border transition-all duration-300"
      >
        Load More Runes
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'Runes',
  setup() {
    const searchQuery = ref('')
    const selectedLanguage = ref('')
    const selectedEffectiveness = ref('')
    const selectedCategory = ref('')
    const hasMore = ref(true)

    const stats = ref({
      total: 23,
      executed: 156,
      avgEffectiveness: 87,
      automationTime: '4.2h',
      languages: 4
    })

    const runes = ref([
      {
        id: 1,
        title: 'Kubernetes Deployment Automation',
        language: 'bash',
        category: 'deployment',
        description: 'Automated script for deploying applications to Kubernetes with health checks and rollback capabilities.',
        effectiveness: 94,
        status: 'approved',
        timestamp: '3 hours ago',
        executions: 28,
        successRate: 96,
        avgTime: '2.3m',
        relatedOrb: 1,
        tags: ['k8s', 'deployment', 'automation', 'rollback'],
        steps: [
          'Validate YAML configuration',
          'Apply deployment to cluster',
          'Wait for rollout completion',
          'Verify deployment status',
          'Check pod health',
          'Run smoke tests'
        ],
        script: `#!/bin/bash
set -e

# Kubernetes Deployment Automation Script
NAMESPACE=${1:-default}
DEPLOYMENT_FILE=${2:-deployment.yaml}

echo "🚀 Starting deployment to namespace: $NAMESPACE"

# Validate configuration
kubectl apply --dry-run=client -f $DEPLOYMENT_FILE

# Apply deployment
kubectl apply -f $DEPLOYMENT_FILE -n $NAMESPACE

# Wait for rollout
kubectl rollout status deployment/$DEPLOYMENT_NAME -n $NAMESPACE --timeout=300s

echo "✅ Deployment completed successfully"`
      },
      {
        id: 2,
        title: 'Docker Image Security Scanner',
        language: 'python',
        category: 'security',
        description: 'Python script to scan Docker images for vulnerabilities using multiple security tools.',
        effectiveness: 89,
        status: 'approved',
        timestamp: '5 hours ago',
        executions: 15,
        successRate: 93,
        avgTime: '45s',
        relatedOrb: 5,
        tags: ['docker', 'security', 'scanning', 'vulnerabilities'],
        steps: [
          'Pull Docker image',
          'Run Trivy vulnerability scan',
          'Check for malware',
          'Generate security report',
          'Export results to JSON'
        ],
        script: `#!/usr/bin/env python3
import subprocess
import json
import sys

def scan_image(image_name):
    """Scan Docker image for vulnerabilities"""
    print(f"🔍 Scanning image: {image_name}")
    
    # Run Trivy scan
    result = subprocess.run([
        'trivy', 'image', '--format', 'json', image_name
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Scan failed: {result.stderr}")
        return False
    
    scan_data = json.loads(result.stdout)
    print(f"✅ Scan completed. Found {len(scan_data)} issues")
    return scan_data

if __name__ == "__main__":
    image = sys.argv[1] if len(sys.argv) > 1 else "nginx:latest"
    scan_image(image)`
      },
      {
        id: 3,
        title: 'Infrastructure Health Monitor',
        language: 'go',
        category: 'monitoring',
        description: 'Go-based monitoring tool that checks the health of various infrastructure components.',
        effectiveness: 91,
        status: 'pending',
        timestamp: '1 day ago',
        executions: 8,
        successRate: 100,
        avgTime: '1.2s',
        relatedOrb: 4,
        tags: ['monitoring', 'health-check', 'infrastructure', 'alerts'],
        steps: [
          'Initialize health checkers',
          'Check database connectivity',
          'Verify API endpoints',
          'Monitor resource usage',
          'Send alerts if needed'
        ],
        script: `package main

import (
    "fmt"
    "net/http"
    "time"
)

type HealthChecker struct {
    Name string
    URL  string
}

func (hc *HealthChecker) Check() error {
    client := &http.Client{Timeout: 5 * time.Second}
    resp, err := client.Get(hc.URL)
    if err != nil {
        return fmt.Errorf("health check failed: %v", err)
    }
    defer resp.Body.Close()
    
    if resp.StatusCode != http.StatusOK {
        return fmt.Errorf("unexpected status: %d", resp.StatusCode)
    }
    return nil
}

func main() {
    checkers := []HealthChecker{
        {"API", "http://localhost:8000/health"},
        {"Database", "http://localhost:5432/health"},
    }
    
    for _, checker := range checkers {
        if err := checker.Check(); err != nil {
            fmt.Printf("❌ %s: %v\\n", checker.Name, err)
        } else {
            fmt.Printf("✅ %s: healthy\\n", checker.Name)
        }
    }
}`
      }
    ])

    const filteredRunes = computed(() => {
      return runes.value.filter(rune => {
        const matchesSearch = searchQuery.value === '' || 
          rune.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          rune.description.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          rune.tags.some(tag => tag.toLowerCase().includes(searchQuery.value.toLowerCase()))
        
        const matchesLanguage = selectedLanguage.value === '' || rune.language === selectedLanguage.value
        const matchesEffectiveness = selectedEffectiveness.value === '' || rune.effectiveness >= parseInt(selectedEffectiveness.value)
        const matchesCategory = selectedCategory.value === '' || rune.category === selectedCategory.value
        
        return matchesSearch && matchesLanguage && matchesEffectiveness && matchesCategory
      })
    })

    const getLanguageIcon = (language) => {
      const icons = {
        bash: '💻',
        python: '🐍',
        go: '🐹',
        yaml: '📄'
      }
      return icons[language] || '🧪'
    }

    const getEffectivenessClass = (score) => {
      if (score >= 90) return 'effectiveness-excellent'
      if (score >= 80) return 'effectiveness-good'
      if (score >= 70) return 'effectiveness-fair'
      return 'effectiveness-poor'
    }

    const copyCode = (code) => {
      navigator.clipboard.writeText(code)
      console.log('Code copied to clipboard')
    }

    const viewRune = (rune) => {
      console.log('Viewing rune:', rune.title)
      // Navigate to detailed rune view
    }

    const executeRune = (rune) => {
      console.log('Executing rune:', rune.title)
      // Execute the rune script
    }

    const approveRune = (rune) => {
      rune.status = 'approved'
      console.log('Approved rune:', rune.title)
    }

    const loadMore = () => {
      console.log('Loading more runes...')
      hasMore.value = false
    }

    return {
      searchQuery,
      selectedLanguage,
      selectedEffectiveness,
      selectedCategory,
      stats,
      runes,
      filteredRunes,
      hasMore,
      getLanguageIcon,
      getEffectivenessClass,
      copyCode,
      viewRune,
      executeRune,
      approveRune,
      loadMore
    }
  }
}
</script>

<style scoped>
@import '../assets/futuristic.css';

.code-preview {
  font-family: 'Courier New', monospace;
}

.effectiveness-score {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: bold;
}

.effectiveness-excellent { background-color: rgba(34, 197, 94, 0.2); color: #22c55e; }
.effectiveness-good { background-color: rgba(59, 130, 246, 0.2); color: #3b82f6; }
.effectiveness-fair { background-color: rgba(245, 158, 11, 0.2); color: #f59e0b; }
.effectiveness-poor { background-color: rgba(239, 68, 68, 0.2); color: #ef4444; }

.status-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: bold;
}

.status-badge.approved { background-color: rgba(34, 197, 94, 0.2); color: #22c55e; }
.status-badge.pending { background-color: rgba(245, 158, 11, 0.2); color: #f59e0b; }

.rune-bash { border-left: 3px solid #4ade80; }
.rune-python { border-left: 3px solid #3b82f6; }
.rune-go { border-left: 3px solid #06b6d4; }
.rune-yaml { border-left: 3px solid #8b5cf6; }
</style> 