import { createRouter, createWebHistory } from 'vue-router';

// Import views
import Demo from '../views/Demo.vue';
import DemoDashboard from '../views/DemoDashboard.vue';
import WhisPipeline from '../views/WhisPipeline.vue';
import OrbLibrary from '../views/OrbLibrary.vue';
import AddKeys from '../views/AddKeys.vue';
import AboutDemo from '../views/AboutDemo.vue';

// Import new demo views
import MLCreator from '../views/MLCreator.vue';
import MLBuilder from '../views/MLBuilder.vue';
import AgentBuilder from '../views/AgentBuilder.vue';
import AgentCreator from '../views/AgentCreator.vue';
import HTC from '../views/HTC.vue';
import HTCFeedback from '../views/HTCFeedback.vue';
import HTCPromptEditor from '../views/HTCPromptEditor.vue';
import Reports from '../views/Reports.vue';
import RAGSearch from '../views/RAGSearch.vue';
import SearchMemory from '../views/SearchMemory.vue';
import SyncDashboard from '../views/SyncDashboard.vue';
import ModelCreator from '../views/ModelCreator.vue';
import MCPToolCreator from '../views/MCPToolCreator.vue';
import ToolExecutor from '../views/ToolExecutor.vue';
import AutoRunner from '../views/AutoRunner.vue';
import MCPExecution from '../views/MCPExecution.vue';
import MCPLogs from '../views/MCPLogs.vue';
import LLMChat from '../views/LLMChat.vue';

// Import demo components
import DemoRAG from '../components/DemoRAG.vue';
import DemoPipeline from '../components/DemoPipeline.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: DemoDashboard,
  },
  {
    path: '/demo',
    name: 'Demo',
    component: Demo,
  },
  {
    path: '/pipeline',
    name: 'WhisPipeline',
    component: WhisPipeline,
  },
  {
    path: '/orbs',
    name: 'OrbLibrary',
    component: OrbLibrary,
  },
  {
    path: '/keys',
    name: 'AddKeys',
    component: AddKeys,
  },
  {
    path: '/about',
    name: 'AboutDemo',
    component: AboutDemo,
  },
  // New demo routes with unified API
  {
    path: '/ml',
    name: 'MLCreator',
    component: MLCreator,
  },
  {
    path: '/ml-builder',
    name: 'MLBuilder',
    component: MLBuilder,
  },
  {
    path: '/model-creator',
    name: 'ModelCreator',
    component: ModelCreator,
  },
  {
    path: '/mcp-tool-creator',
    name: 'MCPToolCreator',
    component: MCPToolCreator,
  },
  {
    path: '/execute-tool',
    name: 'ToolExecutor',
    component: ToolExecutor,
  },
  {
    path: '/auto-runner',
    name: 'AutoRunner',
    component: AutoRunner,
  },
  {
    path: '/mcp-execution',
    name: 'MCPExecution',
    component: MCPExecution,
  },
  {
    path: '/mcp-logs',
    name: 'MCPLogs',
    component: MCPLogs,
  },
  {
    path: '/ai-chat',
    name: 'LLMChat',
    component: LLMChat,
  },
  {
    path: '/agent-builder',
    name: 'AgentBuilder',
    component: AgentBuilder,
  },
  {
    path: '/agents',
    name: 'AgentCreator',
    component: AgentCreator,
  },
  {
    path: '/htc',
    name: 'HTC',
    component: HTC,
  },
  {
    path: '/htc-feedback',
    name: 'HTCFeedback',
    component: HTCFeedback,
  },
  {
    path: '/htc-prompt-editor',
    name: 'HTCPromptEditor',
    component: HTCPromptEditor,
  },
  {
    path: '/reports',
    name: 'Reports',
    component: Reports,
  },
  {
    path: '/rag-search',
    name: 'RAGSearch',
    component: RAGSearch,
  },
  {
    path: '/search-memory',
    name: 'SearchMemory',
    component: SearchMemory,
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: SyncDashboard,
  },
  {
    path: '/tool-executor',
    name: 'ToolExecutor',
    component: ToolExecutor,
  },
  // Legacy demo routes (for backward compatibility)
  {
    path: '/demo/rag',
    name: 'DemoRAG',
    component: DemoRAG,
  },
  {
    path: '/demo/pipeline',
    name: 'DemoPipeline',
    component: DemoPipeline,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
