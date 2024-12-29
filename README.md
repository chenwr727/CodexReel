# NotebookQwen

本项目参考NotebookLlama，是一个自动化生成视频的项目，通过从指定的URL获取内容，生成播客脚本，合成语音，生成图片，并最终生成视频。
#### Demo

[华为 Mate 品牌盛典一文汇总：Mate 70、Mate X6、纯血鸿蒙、尊界 S800...](https://www.ithome.com/0/813/427.htm)

https://github.com/user-attachments/assets/b9ce609d-5171-4c20-b281-d7a740e99c70

```json
{
    "description": "华为盛典",
    "dialogues": [
        {
            "speaker": "小简",
            "contents": [
                "各位，今天我们来聊聊华为的新鲜玩意儿，",
                "Mate 70系列可谓是“史上最强大”的手机！",
                "这名字可不是白叫的。"
            ]
        },
        {
            "speaker": "老陈",
            "contents": [
                "史上最强大？",
                "这名字听着可真有气势，",
                "感觉就像是手机中的超人啊！",
                "这手机要是跟我一起出门，",
                "我得给它个超人披风！"
            ]
        },
        {
            "speaker": "小简",
            "contents": [
                "你觉得这手机需要披风吗？",
                "它已经有“金丝锦纤”和“东方锦色”这些高大上的名字了，",
                "跟你一起跟风出门，",
                "直接改成“锦衣卫”了！"
            ]
        },
        {
            "speaker": "老陈",
            "contents": [
                "哈哈，我还想说，屏幕才真牛，",
                "居然支持1-120Hz动态刷新率！",
                "你说如果我老陈用上这个手机，",
                "能不能比我老婆的语速还快？"
            ]
        },
        {
            "speaker": "小简",
            "contents": [
                "这可难说，",
                "她要是用心说话，120Hz也追不上，",
                "更何况你右手太慢啊！",
                "不过Mate 70的摄像头倒是真的不错，",
                "5000万像素的变焦，",
                "拍个远处的风景简直是“跨世代的远近”。"
            ]
        },
        {
            "speaker": "老陈",
            "contents": [
                "我听说Mate 70还可以卫星寻呼？",
                "那得多牛啊，",
                "跟外星人聊天也不成问题了！",
                "我觉得我可以问问外星人，",
                "‘你们的手机是哪个品牌？’"
            ]
        },
        {
            "speaker": "小简",
            "contents": [
                "哈哈，外星人肯定会告诉你，",
                "他们那叫“银河手机”，",
                "支持宇宙网络，",
                "信号比你的流量卡强多了！"
            ]
        },
        {
            "speaker": "老陈",
            "contents": [
                "说到流量卡，让我想到了“尊界 S800”！",
                "这车启动得快得过飞机，",
                "零百加速3.3秒，",
                "难不成我坐上去能飞到北京喝咖啡？"
            ]
        },
        {
            "speaker": "小简",
            "contents": [
                "当然能飞！",
                "要是新保姆没跟上，坐在车里说：",
                "‘我看了一下，今儿个下雪了，’",
                "你直接跟她说，",
                "‘没关系，我是高速通行证！’"
            ]
        },
        {
            "speaker": "老陈",
            "contents": [
                "高速通行证！哈哈，",
                "进到车顶上直接一键开启“智驾模式”，",
                "那才是灵魂出窍的感觉。"
            ]
        },
        {
            "speaker": "小简",
            "contents": [
                "没错！不过你知道吗，",
                "这次发布会上还有一款腕表，",
                "价格23999元，连黄金都镶嵌了。",
                "要是我戴上这块表，",
                "能不能让人以为我是在带财神？"
            ]
        },
        {
            "speaker": "老陈",
            "contents": [
                "财神到！",
                "难不成我也得给自己配一款手表，",
                "看看哪个小区的老太太能先发现我。",
                "我是“高贵大爷”？"
            ]
        },
        {
            "speaker": "小简",
            "contents": [
                "哈哈，希望那时候你别把自己的老花镜丢了，",
                "别到时候给新手表盖了膜，",
                "结果只能当一块砖头，",
                "用来阻挡阳光！"
            ]
        },
        {
            "speaker": "老陈",
            "contents": [
                "说得好！",
                "这华为盛典就像换头大戏，",
                "都是高科技和奢华的再组合，",
                "但归根结底，",
                "我们还是要用心生活，",
                "才能把生活过得金光闪闪！"
            ]
        },
        {
            "speaker": "小简",
            "contents": [
                "没错！",
                "不管技术多么牛，",
                "最后生活中的快乐，",
                "都是自主创造的！",
                "希望每位朋友都能像华为的新品一样，",
                "绽放出最精彩的光彩！",
                "谢谢大家！"
            ]
        }
    ]
}
```

## 目录

- [项目结构](#项目结构)
- [安装](#安装)
- [配置](#配置)
- [运行](#运行)
- [项目功能](#项目功能)
- [目录说明](#目录说明)
- [示例](#示例)
- [贡献](#贡献)
- [许可证](#许可证)

## 项目结构

```
.
├── app.py
├── config-template.toml
├── config.toml
├── main.py
├── requirements.txt
├── run.sh
├── utils/
│   ├── __init__.py
│   ├── config.py
│   ├── image.py
│   ├── llm.py
│   ├── log.py
│   ├── processing.py
│   ├── tts.py
│   └── video.py
└── web/
    ├── __init__.py
    ├── config.py
    ├── crud.py
    ├── database.py
    ├── models.py
    ├── schemas.py
    ├── service.py
    └── web.py
```

## 安装

1. 克隆仓库到本地：

   ```sh
   git clone https://github.com/chenwr727/NotebookQwen.git
   cd NotebookQwen
   ```

2. 创建并激活虚拟环境：

   ```sh
   python -m venv venv
   source venv/bin/activate  # 对于Windows系统，使用 `venv\Scripts\activate`
   ```

3. 安装依赖：

   ```sh
   pip install -r requirements.txt
   ```

## 配置

1. 复制 `config-template.toml` 并重命名为 `config.toml`：

   ```sh
   cp config-template.toml config.toml
   ```

2. 编辑 `config.toml` 文件，填写相应的API密钥和配置。

## 运行

### 启动服务

1. 启动FastAPI应用：

   ```sh
   python app.py
   ```

2. 启动Streamlit应用：

   ```sh
   streamlit run web.py --server.port 8000
   ```

### 使用脚本

1. 运行 `main.py` 脚本处理指定URL：

   ```sh
   python main.py <url>
   ```

### 使用Shell脚本

1. 使用 `run.sh` 脚本管理服务：

   ```sh
   # 启动服务
   ./run.sh start

   # 停止服务
   ./run.sh stop

   # 重启服务
   ./run.sh restart
   ```

## 项目功能

- 从指定URL获取内容并解析。
- 使用LLM生成播客脚本。
- 合成语音并生成音频文件。
- 生成图片。
- 合成视频并生成最终视频文件。
- 提供基于FastAPI的API接口和基于Streamlit的Web界面。

## 目录说明

- `app.py`：FastAPI应用入口。
- `main.py`：主脚本，处理URL并生成视频。
- `utils/`：工具模块，包括配置加载、日志记录、图像生成、LLM处理、语音合成、视频处理等。
- `web/`：Web相关模块，包括数据库、模型、CRUD操作、服务等。
- `web.py`：Streamlit应用入口。
- `run.sh`：管理服务的Shell脚本。
- `config-template.toml`：配置模板文件。
- `requirements.txt`：项目依赖列表。

## 示例

以下是一个示例命令，用于处理指定的URL并生成视频：

```sh
python main.py https://example.com/article
```

## 贡献

欢迎贡献代码！请提交Pull Request或报告问题。具体步骤如下：

1. Fork 本仓库。
2. 创建新分支 (`git checkout -b feature/new-feature`)。
3. 提交更改 (`git commit -am 'Add some feature'`)。
4. 推送到新分支 (`git push origin feature/new-feature`)。
5. 提交Pull Request。

## 许可证

此项目使用MIT许可证。详情参见 [LICENSE](LICENSE) 文件。