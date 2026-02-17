<template>
  <div class="about-author-page">
    <!-- 页面内容 -->
    <div class="content-container">
      <div class="author-card">
        <!-- 头部信息 -->
        <div class="author-header">
          <div class="author-avatar">
            <img src="/images/author-avatar.jpg" alt="dtsola" />
          </div>
          <h1 class="author-name">dtsola</h1>
          <p class="author-title">IT解决方案架构师 | 一人公司实践者</p>
        </div>

        <!-- 联系方式 -->
        <div class="contact-section">
          <h2 class="section-title">联系方式</h2>

          <div class="contact-list">
            <a href="https://www.dtsola.com" target="_blank" rel="noopener noreferrer" class="contact-item">
              <div class="contact-icon website">
                <i class="fas fa-globe"></i>
              </div>
              <div class="contact-info">
                <div class="contact-label">个人网站</div>
                <div class="contact-value">www.dtsola.com</div>
              </div>
              <i class="fas fa-external-link-alt contact-arrow"></i>
            </a>

            <a href="https://space.bilibili.com/736015" target="_blank" rel="noopener noreferrer" class="contact-item">
              <div class="contact-icon bilibili">
                <i class="fab fa-bilibili"></i>
              </div>
              <div class="contact-info">
                <div class="contact-label">B站</div>
                <div class="contact-value">space.bilibili.com/736015</div>
              </div>
              <i class="fas fa-external-link-alt contact-arrow"></i>
            </a>

            <div class="contact-item">
              <div class="contact-icon wechat">
                <i class="fab fa-weixin"></i>
              </div>
              <div class="contact-info">
                <div class="contact-label">微信</div>
                <div class="contact-value">dtsola</div>
              </div>
              <div class="contact-note">（与我建联，备注：github）</div>
            </div>
          </div>
        </div>

        <!-- 二维码展示 -->
        <div class="qrcode-section">
          <h2 class="section-title">微信二维码</h2>
          <div class="qrcode-container">
            <img src="/images/个人二维码.png" alt="微信二维码" class="qrcode-image" />
            <p class="qrcode-hint">扫描二维码添加微信</p>
          </div>
        </div>

        <!-- 项目信息 -->
        <div class="project-section">
          <h2 class="section-title">关于本项目</h2>
          <p class="project-description">
            小遥账单助手是一个<strong>隐私优先</strong>的个人账单分析工具，
            数据完全本地处理，不上传任何服务器。支持支付宝和微信账单的自动解析和多维度数据可视化分析。
          </p>
          <div class="project-links">
            <a href="https://github.com/dtsola/xiaoyaoprivatebill" target="_blank" rel="noopener noreferrer" class="project-link">
              <i class="fab fa-github"></i>
              <span>GitHub 仓库</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 关于作者页面 - 静态内容，无需额外逻辑
</script>

<style scoped>
.about-author-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

/* 内容容器 */
.content-container {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: 40px;
  box-shadow: var(--shadow-card);
}

/* 作者卡片 */
.author-card {
  max-width: 600px;
  margin: 0 auto;
}

/* 作者头部 */
.author-header {
  text-align: center;
  margin-bottom: 40px;
  padding-bottom: 32px;
  border-bottom: 1px solid var(--border-color);
}

.author-avatar {
  width: 120px;
  height: 120px;
  margin: 0 auto 20px;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  background: #f5f5f7;
}

.author-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.author-name {
  font-size: 32px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0 0 8px 0;
}

.author-title {
  font-size: 16px;
  color: var(--secondary-text);
  margin: 0;
}

/* 联系方式区域 */
.contact-section {
  margin-bottom: 40px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0 0 20px 0;
}

.contact-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: var(--bg-color);
  border-radius: var(--radius-md);
  text-decoration: none;
  transition: all 0.2s ease;
}

.contact-item:hover {
  background: var(--hover-bg);
  transform: translateX(4px);
}

.contact-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.contact-icon.website {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.contact-icon.bilibili {
  background: linear-gradient(135deg, #00A1D6 0%, #00B5E5 100%);
  color: white;
}

.contact-icon.wechat {
  background: linear-gradient(135deg, #07C160 0%, #06AE56 100%);
  color: white;
}

.contact-info {
  flex: 1;
}

.contact-label {
  font-size: 12px;
  color: var(--secondary-text);
  margin-bottom: 2px;
}

.contact-value {
  font-size: 15px;
  color: var(--text-color);
  font-weight: 500;
}

.contact-arrow {
  color: var(--secondary-text);
  font-size: 12px;
}

.contact-note {
  font-size: 13px;
  color: var(--secondary-text);
}

/* 二维码区域 */
.qrcode-section {
  margin-bottom: 40px;
}

.qrcode-container {
  text-align: center;
  padding: 24px;
  background: var(--bg-color);
  border-radius: var(--radius-md);
}

.qrcode-image {
  width: 200px;
  height: 200px;
  border-radius: var(--radius-md);
  margin-bottom: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.qrcode-hint {
  font-size: 14px;
  color: var(--secondary-text);
  margin: 0;
}

/* 项目信息区域 */
.project-section {
  padding-top: 32px;
  border-top: 1px solid var(--border-color);
}

.project-description {
  font-size: 15px;
  line-height: 1.8;
  color: var(--text-color);
  margin: 0 0 20px 0;
}

.project-description strong {
  color: var(--primary-color);
  font-weight: 600;
}

.project-links {
  display: flex;
  gap: 12px;
}

.project-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: var(--primary-color);
  color: white;
  text-decoration: none;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.project-link:hover {
  background: #0066E6;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .about-author-page {
    padding: 16px;
  }

  .content-container {
    padding: 24px;
  }

  .author-avatar {
    width: 100px;
    height: 100px;
  }

  .author-name {
    font-size: 24px;
  }

  .author-title {
    font-size: 14px;
  }

  .contact-item {
    padding: 12px;
  }

  .contact-icon {
    width: 40px;
    height: 40px;
    font-size: 18px;
  }

  .qrcode-image {
    width: 180px;
    height: 180px;
  }

  .project-links {
    flex-direction: column;
  }

  .project-link {
    justify-content: center;
  }
}
</style>
