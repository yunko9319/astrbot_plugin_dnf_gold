# DNF 跨 5 全平台金价实时看板 (AstrBot 插件)

针对 AstrBot v4 框架开发。本插件旨在为 DNF 玩家提供最真实的 [跨 5 区] 金价行情对比，支持 UU898 和 DD373 两大主流平台。采用物理路标切割与正则提取技术，精准过滤侧边栏干扰，买家必看。

## ✨ 功能特性
- **实时播报**: 使用 `/查金价` 指令，秒速获取全平台最新高比例挂单。
- **动态署名**: 自动识别触发指令的用户，播报 “根据 [用户] 的指示”。
- **买家优化**: 自动提取列表前三名最高比例（金币最多），助你精准捡漏。
- **物理隔离**: 自动屏蔽侧边栏“低比例收货价”干扰，只展示真实主列表“出货单”。

## 🛠️ 安装方法

### 方式 A：通过 WebUI 仪表盘安装 (推荐)
1. 进入 AstrBot 仪表盘 -> **插件管理** -> **从 GitHub 安装**。
2. 粘贴本仓库链接：`https://github.com/yunko9319/astrbot_plugin_dnf_gold`
3. 点击安装并等待重启完成。

### 方式 B：手动在服务器安装 (极客模式)
1. **进入插件目录**:
   ```bash
   cd ~/AstrBot/data/plugins/
   ```
2. **克隆仓库**:
   ```bash
   git clone https://github.com/yunko9319/astrbot_plugin_dnf_gold.git
   ```
3. **安装环境依赖**:
   ```bash
   cd ~/AstrBot && source venv/bin/activate
   pip install httpx
   ```
4. **重启服务**:
   ```bash
   sudo systemctl restart astrbot
   ```

## 📜 声明
- 本插件仅用于学习交流，数据采集自平台公开页面，请以官方实际下单价格为准。
- 技术支持：**qingcai**

## ⚖️ 协议[MIT License](LICENSE)
