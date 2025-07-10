<template>
  ;
  <div class="login-page">
    ;
    <div class="login-container">
      ;
      <!-- Logo and Title -->;
      <div class="login-header">
        ;
        <div class="logo-container">
          ;
          <h1 class="logo-text">
            LinkOps
          </h1>;
          <div class="logo-glow" />;
        </div>;
        <h2 class="login-title">
          MLOps Command Center
        </h2>;
        <p class="login-subtitle">
          Choose your access level
        </p>;
      </div>;

      <!-- Login Options -->;
      <div class="login-options">
        ;
        <div
          class="option-card demo"
          @click="loginAs('demo')"
        >
          ;
          <div class="option-icon">
            👤
          </div>;
          <h3 class="option-title">
            Demo Mode
          </h3>;
          <p class="option-description">
            ;
            Explore the platform with simulated data and limited functionality;
          </p>;
          <div class="option-features">
            ;
            <span class="feature">• View-only dashboard</span>;
            <span class="feature">• Simulated pipelines</span>;
            <span class="feature">• Mock audit results</span>;
          </div>;
          <button class="login-btn demo-btn">
            ;
            <span class="btn-icon">🚀</span>;
            Enter Demo Mode;
          </button>;
        </div>;

        <div
          class="option-card admin"
          @click="loginAs('admin')"
        >
          ;
          <div class="option-icon">
            ⚡
          </div>;
          <h3 class="option-title">
            Admin Access
          </h3>;
          <p class="option-description">
            ;
            Full platform access with real data and administrative controls;
          </p>;
          <div class="option-features">
            ;
            <span class="feature">• Full dashboard access</span>;
            <span class="feature">• Real pipeline management</span>;
            <span class="feature">• Live audit capabilities</span>;
          </div>;
          <button class="login-btn admin-btn">
            ;
            <span class="btn-icon">🔐</span>;
            Admin Login;
          </button>;
        </div>;
      </div>;

      <!-- Demo Notice -->;
      <div class="demo-notice">
        ;
        <div class="notice-icon">
          💡
        </div>;
        <p class="notice-text">
          ;
          <strong>Demo Mode:</strong> Perfect for exploring features without affecting production data.;
          All actions are simulated and no real changes are made.;
        </p>;
      </div>;

      <!-- Background Effects -->;
      <div class="background-effects">
        ;
        <div class="floating-orb orb-1" />;
        <div class="floating-orb orb-2" />;
        <div class="floating-orb orb-3" />;
      </div>;
    </div>;
  </div>;
</template>;
<script>
import { useMainStore } from '../store/index.js'

export default {
  name: 'Login',
  data() {
    return {
      isLoading: false
    }
  },
  methods: {
    async loginAs(role) {
      this.isLoading = true
      
      try {
        // Simulate login process
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        const store = useMainStore()
        
        // Set authentication role
        store.setAuthRole(role)
        
        // Add notification
        store.addNotification({
          type: 'success',
          message: `Welcome! You're now logged in as ${role === 'demo' ? 'Demo User' : 'Administrator'}`,
          duration: 3000
        })
        
        // Redirect to dashboard
        this.$router.push('/')
        
      } catch (_error) {
        const store = useMainStore()
        store.addNotification({
          type: 'error',
          message: 'Login failed. Please try again.',
          duration: 5000
        })
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>;
<style scoped>;
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
  position: relative;
  overflow: hidden;
}

.login-container {
  max-width: 900px;
  width: 100%;
  padding: 2rem;
  z-index: 10;
  position: relative;
}

.login-header {
  text-align: center;
  margin-bottom: 3rem;
}

.logo-container {
  position: relative;
  display: inline-block;
  margin-bottom: 1rem;
}

.logo-text {
  font-size: 4rem;
  font-weight: 900;
  background: linear-gradient(45deg, #00d4ff, #ff00ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
  position: relative;
  z-index: 2;
}

.logo-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120%;
  height: 120%;
  background: radial-gradient(circle, rgba(0, 212, 255, 0.3) 0%, transparent 70%);
  animation: pulse 3s ease-in-out infinite;
  z-index: 1;
}

.login-title {
  font-size: 2rem;
  color: #e0e0e0;
  margin: 0 0 0.5rem 0;
  font-weight: bold;
}

.login-subtitle {
  color: #888;
  font-size: 1.1rem;
  margin: 0;
}

.login-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.option-card {
  background: rgba(0, 0, 0, 0.6);
  border: 2px solid transparent;
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
}

.option-card::before {
  content: '$2';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #00d4ff, #ff00ff);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.option-card:hover::before {
  transform: scaleX(1);
}

.option-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 212, 255, 0.3);
}

.option-card.demo {
  border-color: rgba(0, 212, 255, 0.3);
}

.option-card.admin {
  border-color: rgba(255, 0, 255, 0.3);
}

.option-card.demo:hover {
  border-color: #00d4ff;
  box-shadow: 0 20px 40px rgba(0, 212, 255, 0.4);
}

.option-card.admin:hover {
  border-color: #ff00ff;
  box-shadow: 0 20px 40px rgba(255, 0, 255, 0.4);
}

.option-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  filter: drop-shadow(0 0 10px rgba(0, 212, 255, 0.5));
}

.option-card.admin .option-icon {
  filter: drop-shadow(0 0 10px rgba(255, 0, 255, 0.5));
}

.option-title {
  font-size: 1.5rem;
  color: #00d4ff;
  margin: 0 0 1rem 0;
  font-weight: bold;
}

.option-card.admin .option-title {
  color: #ff00ff;
}

.option-description {
  color: #e0e0e0;
  margin: 0 0 1.5rem 0;
  line-height: 1.5;
}

.option-features {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.feature {
  color: #888;
  font-size: 0.9rem;
}

.login-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.login-btn::before {
  content: '$2';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.login-btn:hover::before {
  left: 100%;
}

.demo-btn {
  background: linear-gradient(45deg, #00d4ff, #0099cc);
  color: white;
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
}

.demo-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 212, 255, 0.4);
}

.admin-btn {
  background: linear-gradient(45deg, #ff00ff, #cc00cc);
  color: white;
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.3);
}

.admin-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(255, 0, 255, 0.4);
}

.btn-icon {
  font-size: 1.2rem;
}

.demo-notice {
  background: rgba(0, 212, 255, 0.1);
  border: 1px solid rgba(0, 212, 255, 0.3);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  max-width: 600px;
  margin: 0 auto;
}

.notice-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.notice-text {
  color: #e0e0e0;
  margin: 0;
  line-height: 1.5;
}

.background-effects {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 1;
}

.floating-orb {
  position: absolute;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0, 212, 255, 0.2) 0%, transparent 70%);
  animation: float 6s ease-in-out infinite;
}

.orb-1 {
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.orb-2 {
  top: 60%;
  right: 15%;
  animation-delay: 2s;
  background: radial-gradient(circle, rgba(255, 0, 255, 0.2) 0%, transparent 70%);
}

.orb-3 {
  bottom: 20%;
  left: 20%;
  animation-delay: 4s;
  background: radial-gradient(circle, rgba(0, 255, 136, 0.2) 0%, transparent 70%);
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.5;
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1.1);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .login-container {
    padding: 1rem;
  }
  
  .logo-text {
    font-size: 3rem;
  }
  
  .login-title {
    font-size: 1.5rem;
  }
  
  .login-options {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .option-card {
    padding: 1.5rem;
  }
  
  .demo-notice {
    flex-direction: column;
    text-align: center;
  }
}
</style>;
