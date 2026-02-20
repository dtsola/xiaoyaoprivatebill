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
          <h2 class="section-title">扫码联系</h2>
          <div class="qrcode-container">
            <div class="qrcode-item">
              <img
                src="/images/个人二维码.png"
                alt="微信二维码"
                class="qrcode-image clickable"
                @click="openPreview('/images/个人二维码.png', '微信联系')"
              />
              <p class="qrcode-hint">微信联系</p>
            </div>
            <div class="qrcode-divider"></div>
            <div class="qrcode-item">
              <img
                src="/images/开发者交流群.png"
                alt="开发者交流群"
                class="qrcode-image clickable"
                @click="openPreview('/images/开发者交流群.png', '开发者交流群')"
              />
              <p class="qrcode-hint">开发者交流群</p>
            </div>
            <div class="qrcode-divider"></div>
            <div class="qrcode-item">
              <img
                src="/images/用户交流群.png"
                alt="用户交流群"
                class="qrcode-image clickable"
                @click="openPreview('/images/用户交流群.png', '用户交流群')"
              />
              <p class="qrcode-hint">用户交流群</p>
            </div>
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

    <!-- 图片预览模态框 -->
    <Transition name="fade">
      <div v-if="previewVisible" class="preview-modal" @click="closePreview">
        <div class="preview-content" @click.stop>
          <button class="preview-close" @click="closePreview">
            <i class="fas fa-times"></i>
          </button>
          <img :src="previewImage" :alt="previewTitle" class="preview-image" />
          <p class="preview-title">{{ previewTitle }}</p>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 预览状态
const previewVisible = ref(false)
const previewImage = ref('')
const previewTitle = ref('')

// 打开预览
const openPreview = (src, title) => {
  previewImage.value = src
  previewTitle.value = title
  previewVisible.value = true
  document.body.style.overflow = 'hidden'
}

// 关闭预览
const closePreview = () => {
  previewVisible.value = false
  document.body.style.overflow = ''
}
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
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 40px;
  padding: 32px 24px;
  background: var(--bg-color);
  border-radius: var(--radius-md);
}

.qrcode-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  flex: 1;
}

.qrcode-divider {
  width: 1px;
  height: 160px;
  background: var(--border-color);
}

.qrcode-image {
  width: 150px;
  height: auto;
  aspect-ratio: 1;
  object-fit: contain;
  border-radius: var(--radius-md);
  margin-bottom: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.2s ease;
}

.qrcode-image.clickable {
  cursor: pointer;
}

.qrcode-image.clickable:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
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
    width: 160px;
    height: auto;
  }

  .qrcode-container {
    flex-wrap: wrap;
    gap: 16px;
  }

  .qrcode-item {
    flex: 1 1 calc(50% - 8px);
    min-width: 140px;
  }

  .qrcode-image {
    width: 140px;
  }

  .qrcode-divider {
    display: none;
  }


  .project-links {
    flex-direction: column;
  }

  .project-link {
    justify-content: center;
  }

  .preview-content {
    max-width: 90vw;
    max-height: 90vh;
  }

  .preview-image {
    max-width: 90vw;
    max-height: 70vh;
  }
}

/* 图片预览模态框 */
.preview-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
}

.preview-content {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 80vw;
  max-height: 90vh;
}

.preview-close {
  position: absolute;
  top: -50px;
  right: -10px;
  width: 40px;
  height: 40px;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border-radius: 50%;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.preview-close:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.preview-image {
  max-width: 80vw;
  max-height: 80vh;
  object-fit: contain;
  border-radius: var(--radius-md);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
}

.preview-title {
  margin-top: 20px;
  color: white;
  font-size: 16px;
  font-weight: 500;
}

/* 淡入淡出动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
