# 🔧 Quick Fix: Docker Registry Authentication

## ✅ **Step 1: Set GitHub Secrets**

**Go to:** `LinkOps-MLOps → Settings → Secrets and variables → Actions → New repository secret`

**Set these secrets:**

| Secret Name | Value |
|-------------|-------|
| `DOCKER_USER` | Your Docker Hub username (e.g., `jimjrxieb`) |
| `DOCKER_CRED` | A Docker Hub access token (NOT password!) |

**🔐 Generate Docker token:** https://hub.docker.com/settings/security

---

## 📦 **Step 2: Fix Namespace Permissions**

**Current workflow uses:**
```yaml
image_name="linkops/$name:latest"
```

This pushes to: `docker.io/linkops/<service>:latest`

### ✔️ **Option A: Use Organization Namespace**
- Ensure your `DOCKER_USER` has push permission to `linkops` namespace
- Organization owner must add you as collaborator with **Write** permissions

### 🛠️ **Option B: Use Personal Namespace (Recommended for Testing)**

**Change this line in `.github/workflows/main.yml`:**
```yaml
# Comment out organization namespace:
# image_name="linkops/$name:latest"

# Uncomment personal namespace:
image_name="${{ secrets.DOCKER_USER }}/$name:latest"
```

**Result:** Images push to `docker.io/jimjrxieb/<service>:latest` (your own space)

---

## 🚀 **Step 3: Test the Fix**

1. **Set GitHub secrets** (Step 1)
2. **Choose namespace option** (Step 2) 
3. **Push to main branch:**
   ```bash
   git add .
   git commit -m "Fix Docker registry authentication"
   git push origin main
   ```
4. **Monitor workflow:** https://github.com/jimjrxieb/LinkOps-MLOps/actions

---

## 🎯 **Expected Results**

✅ **Workflow will now:**
- Validate Docker credentials before building
- Login successfully to Docker Hub
- Build all 17 microservices 
- Push images without "access denied" errors
- Report detailed success/failure status

✅ **Your Docker images will be available at:**
- Organization: `hub.docker.com/r/linkops/service-name`
- Personal: `hub.docker.com/r/jimjrxieb/service-name`

---

## 🆘 **Still Having Issues?**

**Run local test:**
```bash
chmod +x test_docker_registry.sh
./test_docker_registry.sh
```

**Common fixes:**
- Verify `DOCKER_CRED` is an **access token**, not password
- Check `DOCKER_USER` matches your Docker Hub username exactly
- Ensure you have push permissions to the target namespace
- Try personal namespace if organization access is uncertain 