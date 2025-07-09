<template>;
  <div class="not-found">;
    <div class="error-container">;
      <div class="error-code">404</div>;
      <h1 class="error-title">Page Not Found</h1>;
      <p class="error-message">;
        The page you're looking for doesn't exist in this dimension.;
      </p>;
      <div class="error-actions">;
        <router-link to="/" class="btn primary">;
          <span class="btn-icon">🏠</span>;
          Return to Dashboard;
        </router-link>;
        <button class="btn secondary" @click="goBack">;
          <span class="btn-icon">⬅️</span>;
          Go Back;
        </button>;
      </div>;
    </div>;
    
    <div class="error-graphic">;
      <div class="holo-cube">;
        <div class="cube-face front"></div>;
        <div class="cube-face back"></div>;
        <div class="cube-face right"></div>;
        <div class="cube-face left"></div>;
        <div class="cube-face top"></div>;
        <div class="cube-face bottom"></div>;
      </div>;
    </div>;
  </div>;
</template>;

<script>;
export default {
  name: 'NotFound',
  methods: {
    goBack() {
      this.$router.go(-1);
    }
  }
}
</script>;

<style scoped>;
.not-found {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
  position: relative;
}

.error-container {
  z-index: 2;
}

.error-code {
  font-size: 8rem;
  font-weight: bold;
  background: linear-gradient(45deg, #00d4ff, #ff00ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 1rem;
  text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
}

.error-title {
  font-size: 2.5rem;
  color: #e0e0e0;
  margin-bottom: 1rem;
}

.error-message {
  font-size: 1.2rem;
  color: #888;
  margin-bottom: 2rem;
  max-width: 500px;
}

.error-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn.primary {
  background: linear-gradient(45deg, #00d4ff, #0099cc);
  color: white;
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
}

.btn.secondary {
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid #00d4ff;
  color: #00d4ff;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 212, 255, 0.4);
}

.btn-icon {
  font-size: 1.2rem;
}

.error-graphic {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1;
  opacity: 0.1;
}

.holo-cube {
  width: 200px;
  height: 200px;
  position: relative;
  transform-style: preserve-3d;
  animation: rotate 10s infinite linear;
}

.cube-face {
  position: absolute;
  width: 200px;
  height: 200px;
  background: rgba(0, 212, 255, 0.1);
  border: 2px solid #00d4ff;
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
}

.cube-face.front {
  transform: translateZ(100px);
}

.cube-face.back {
  transform: translateZ(-100px);
}

.cube-face.right {
  transform: rotateY(90deg) translateZ(100px);
}

.cube-face.left {
  transform: rotateY(-90deg) translateZ(100px);
}

.cube-face.top {
  transform: rotateX(90deg) translateZ(100px);
}

.cube-face.bottom {
  transform: rotateX(-90deg) translateZ(100px);
}

@keyframes rotate {
  from {
    transform: rotateX(0deg) rotateY(0deg);
  }
  to {
    transform: rotateX(360deg) rotateY(360deg);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .error-code {
    font-size: 6rem;
  }
  
  .error-title {
    font-size: 2rem;
  }
  
  .error-message {
    font-size: 1rem;
  }
  
  .error-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .btn {
    width: 200px;
    justify-content: center;
  }
  
  .holo-cube {
    width: 150px;
    height: 150px;
  }
  
  .cube-face {
    width: 150px;
    height: 150px;
  }
  
  .cube-face.front,
  .cube-face.back {
    transform: translateZ(75px);
  }
  
  .cube-face.right,
  .cube-face.left {
    transform: rotateY(90deg) translateZ(75px);
  }
  
  .cube-face.top,
  .cube-face.bottom {
    transform: rotateX(90deg) translateZ(75px);
  }
}
</style>;