# URL2VideoStudio 🎬

> 一键将文章转换为引人入胜的视频内容！

## 📖 项目介绍

URL2VideoStudio 是一个创新的自动化视频生成工具，能够将任意文章智能转化为生动有趣的对话视频。本项目参考 NotebookLlama，通过先进的 AI 技术，实现从文本到视频的全流程自动化制作。

### ✨ 特色功能

- 🤖 **智能内容理解** - 自动提取文章精华，深度理解文章主旨
- 🎭 **多角色对话** - AI 驱动的对话生成，让内容更生动有趣
- 🔍 **智能素材匹配** - 基于语义的视频素材智能匹配
- 🗣️ **AI 语音合成** - 自然流畅的多角色配音系统
- 🎥 **专业视频制作** - 自动剪辑与合成，打造精致视频内容

### 🎯 应用场景

- 📰 新闻资讯视频化 - 快速将热点新闻转化为短视频
- 📚 文章内容可视化 - 让文章内容更具表现力
- 🎤 播客内容制作 - 自动生成对话式播客
- 📱 短视频内容生产 - 批量生产优质短视频
- 🎮 游戏资讯转视频 - 游戏攻略、新闻的视频化呈现

## 🛠️ 技术栈

- **后端框架**: FastAPI
- **前端界面**: Streamlit
- **AI 服务**: OpenAI GPT API
- **语音合成**: Tongyi TTS
- **视频处理**: FFmpeg
- **数据存储**: SQLite

## 🚀 快速开始

### 环境要求

- Python 3.10+
- FFmpeg
- ImageMagick

### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/chenwr727/URL2VideoStudio.git
cd URL2VideoStudio
```

2. 创建并激活 conda 环境：
```bash
conda create -n url2video python=3.10
conda activate url2video
```

3. 安装依赖：
```bash
pip install -r requirements.txt
conda install -c conda-forge ffmpeg
```

### 配置

1. 复制配置模板：
```bash
copy config-template.toml config.toml
```

2. 编辑 `config.toml`，配置以下必要参数：
- OpenAI API 密钥
- Tongyi TTS 服务密钥
- Pexels API 密钥
- 其他可选配置

## 📂 项目结构

```
URL2VideoStudio/
├── api/                    # API接口模块
│   ├── crud.py            # 数据库操作
│   ├── database.py        # 数据库配置
│   ├── models.py          # 数据模型
│   ├── router.py          # 路由定义
│   └── service.py         # 业务逻辑
├── schemas/               # 数据模型定义
│   ├── config.py         # 配置模型
│   ├── task.py           # 任务模型
│   └── video.py          # 视频模型
├── services/             # 外部服务集成
│   ├── llm.py           # LLM服务
│   ├── pexels.py        # 视频素材服务
│   ├── tts.py           # 语音合成服务
│   └── video.py         # 视频处理服务
├── utils/                # 工具模块
│   ├── config.py        # 配置管理
│   ├── log.py           # 日志工具
│   ├── subtitle.py      # 字幕处理
│   ├── text.py          # 文本处理
│   └── video.py         # 视频工具
└── web.py               # Web界面入口
```

## 🖥️ 使用方法

### Web界面

1. 启动服务：
```bash
python app.py
```

2. 启动Web界面：
```bash
streamlit run web.py --server.port 8000
```

### 命令行使用

处理单个URL：
```bash
python main.py https://example.com/article
```

## 📝 示例

> 注意：以下示例视频经过剪辑压缩，仅展示部分效果。完整视频可通过点击标题查看原文后自行生成。

<table>
    <thead>
        <tr>
            <th align="center"><g-emoji class="g-emoji" alias="arrow_forward">▶️</g-emoji> <a href="https://mp.weixin.qq.com/s/31AxWlPevYdI_CLErHReEQ">《欧洲：被分到小孩那桌的尴尬》</a></th>
            <th align="center"><g-emoji class="g-emoji" alias="arrow_forward">▶️</g-emoji> <a href="https://mp.weixin.qq.com/s/tQMKS6HBH5bFVwa7otJaww">《哪吒带飞的东北富豪，如何保持IP热度？》</a></th>
            <th align="center"><g-emoji class="g-emoji" alias="arrow_forward">▶️</g-emoji> <a href="https://m.ithome.com/html/831514.htm">《无创血糖检测仪：科技让生活更轻松》</a></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="center"><video src="https://github.com/user-attachments/assets/452561f5-acb5-4225-9e8b-eb080f8b0a7d"></video></td>
            <td align="center"><video src="https://github.com/user-attachments/assets/a28b6e03-3685-4014-a856-6a57adb86be1"></video></td>
            <td align="center"><video src="https://github.com/user-attachments/assets/e5dab72d-041c-436e-aa51-de9edfe1ba6d"></video></td>
        </tr>
    </tbody>
</table>

## 🤝 贡献指南

欢迎贡献代码！请参考以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 提交 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [NotebookLlama](https://github.com/NotebookLlama) - 项目灵感来源
- 所有贡献者和用户