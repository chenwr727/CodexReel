简体中文 | [English](README_EN.md)

# NotebookQwen

#### 项目概述
本项目参考NotebookLlama，旨在从输入的网址中提取文本，生成播客文本，并将其转换为视频文件。

项目主要分为以下几个步骤：
1. 获取网页内容并保存为文本文件。
2. 使用LLM（大型语言模型）生成播客文本。
3. 将生成的播客文本转换为语音文件。
4. 将生成的播客文本转换为图片文件。
5. 将生成的语音和图片文件转换为视频文件。

#### Demo

[华为 Mate 品牌盛典一文汇总：Mate 70、Mate X6、纯血鸿蒙、尊界 S800...](https://www.ithome.com/0/813/427.htm)

https://github.com/user-attachments/assets/e1a7100e-a30b-4b6d-8a65-824f338acada

```json
{
    "description": "华为 Mate 品牌盛典：科技与创新的盛宴",
    "dialogues": [
        {
            "speaker": "小简",
            "contents": [
                "欢迎来到本期的科技探索播客！",
                "我是小简，今天我们要聊一场科技盛宴。",
                "那就是刚刚结束的华为 Mate 品牌盛典。"
            ]
        },
        {
            "speaker": "老陈",
            "contents": [
                "嗨，小简，很高兴又和你一起探讨科技话题。",
                "这次的华为 Mate 品牌盛典听起来真的很精彩。",
                "你对这次发布会有什么初步印象吗？"
            ]
        },
        {
            "speaker": "小简",
            "contents": [
                "确实非常精彩，尤其是 Mate 70 系列和 Mate X6 折叠屏手机的发布。",
                "这两款产品不仅设计精美，技术上也有很多突破。",
                "还有纯血鸿蒙系统和一系列全场景产品，真是让人目不暇接。"
            ]
        },
        {
            "speaker": "老陈",
            "contents": [
                "哇，听起来真的很厉害！",
                "特别是这个‘纯血鸿蒙系统’，我一直很好奇。",
                "它到底是什么意思呢？"
            ]
        },
        {
            "speaker": "小简",
            "contents": [
                "‘纯血鸿蒙’是指华为完全自主开发的操作系统，不再依赖第三方组件。",
                "这意味着鸿蒙系统将更加安全、稳定，用户体验也会更流畅。",
                "这是国产操作系统的一个重要里程碑。"
            ]
        },
        {
            "speaker": "老陈",
            "contents": [
                "嗯，这确实是一个巨大的进步。",
                "操作系统是整个生态的核心，完全自主开发能提升安全性和用户体验。",
                "对了，小简，你提到的 Mate 70 系列，它的设计和性能有哪些特别之处呢？"
            ]
        },
        {
            "speaker": "小简",
            "contents": [
                "Mate 70 系列的设计非常经典，采用中轴对称设计，后置镜头模组点缀着‘星光饰钉’。",
                "材质方面，主打‘金丝锦纤’和‘东方锦色’，给人以高级感。",
                "屏幕方面，标准版是 6.7 英寸直屏，Pro 和 Pro+ 是 6.9 英寸等深四曲屏。"
            ]
        },
        {
            "speaker": "老陈",
            "contents": [
                "哇，2500nit 的亮度，这简直是在黑暗中也能看得清清楚楚啊！",
                "对了，小简，你在发布会上有没有注意到 Mate 70 的摄像头有什么特别之处？"
            ]
        },
        {
            "speaker": "小简",
            "contents": [
                "Mate 70 的摄像头确实非常值得关注。",
                "它首发搭载了红枫原色影像系统，配备 150 万多光谱通道的红枫原色摄像头。",
                "色彩还原准确度提升了 120%，还支持 AI 电影质感引擎。"
            ]
        },
        {
            "speaker": "老陈",
            "contents": [
                "听起来真的很吸引人！",
                "我平时喜欢拍照，特别是旅行的时候。",
                "如果有一台这样的手机，肯定能拍出很多漂亮的照片。"
            ]
        },
        {
            "speaker": "小简",
            "contents": [
                "没错，Mate X6 折叠屏手机的三网卫星通信功能也非常前沿。",
                "它支持北斗卫星消息、天通卫星通信以及低轨卫星互联网。",
                "这意味着即使在没有地面网络覆盖的情况下，用户也可以通过卫星发送和接收信息。"
            ]
        },
        {
            "speaker": "老陈",
            "contents": [
                "哇，这真的太棒了！",
                "想象一下，如果你在偏远地区迷路了，还能通过卫星发送求救信号。",
                "这简直是救命稻草啊！"
            ]
        },
        {
            "speaker": "小简",
            "contents": [
                "这次发布会还有很多其他值得关注的产品。",
                "比如 WATCH D2，它是华为首款动态血压监测智能手表。",
                "可以实现 24 小时的血压监测，并生成专业的动态血压报告。"
            ]
        },
        {
            "speaker": "老陈",
            "contents": [
                "听你这么一说，我都有点心动了。",
                "特别是 WATCH D2，对于像我这样经常出差的人来说，随时监测血压真的很有用。"
            ]
        },
        {
            "speaker": "小简",
            "contents": [
                "还有 FreeBuds Pro 4 耳机，这是华为首款搭载纯血鸿蒙系统的 TWS 耳机。",
                "支持 48kHz/24bit 无损传输，音质非常出色。"
            ]
        },
        {
            "speaker": "老陈",
            "contents": [
                "听你这么一说，我都有点迫不及待想试试这些新产品了。",
                "小简，你对这次发布会的整体感受如何？"
            ]
        },
        {
            "speaker": "小简",
            "contents": [
                "总的来说，我觉得这次发布会非常成功。",
                "华为不仅展示了强大的技术创新能力，还展现了对用户体验的极致追求。",
                "每一款产品都充满了惊喜，相信会在市场中引起不小的轰动。"
            ]
        },
        {
            "speaker": "老陈",
            "contents": [
                "嗯，我也非常期待这些产品的上市。",
                "希望它们能给我们的生活带来更多的便利和乐趣。",
                "好了，今天的节目就到这里，感谢大家的收听，我们下期再见！"
            ]
        },
        {
            "speaker": "小简",
            "contents": [
                "谢谢大家，我们下次节目再见！"
            ]
        }
    ]
}
```

#### 目录结构
```
project/
├── main.py
├── utils/
│   ├── config.py
│   ├── image.py
│   ├── llm.py
│   ├── log.py
│   ├── processing.py
│   ├── tts.py
│   └── video.py
├── config-template.toml
└── config.toml
```

#### 安装依赖
确保安装了以下依赖库：
```sh
pip install -r requirements.txt
```

#### 配置文件
项目需要一个配置文件 `config.toml`，示例如下：

1. 复制模板文件：
   ```sh
   cp config-template.toml config.toml
   ```

2. 修改 `config.toml` 文件内容：
   ```toml
   [llm]
   api_key = "YOUR_LLM_API_KEY"
   base_url = "https://api.example.com"
   model = "your_model_name"
   prompt_writer = "Your initial prompt for generating the podcast"
   prompt_rewriter = "Your rewriter prompt for refining the podcast"

   [tts]
   api_key = "YOUR_TTS_API_KEY"
   model = "your_tts_model_name"
   voices = ["voice1", "voice2"]
   ```

#### 运行项目
1. 确保配置文件 `config.toml` 已正确配置。
2. 运行主脚本 `main.py` 并传入URL作为参数。

```sh
python main.py https://mp.weixin.qq.com/s/sGEcVIxH6TkIjeWew-LSJg
```

#### 致谢
- [NotebookLlama](https://github.com/meta-llama/llama-recipes/tree/main/recipes/quickstart/NotebookLlama)

希望这个README对你有帮助！如果有任何问题或建议，请随时联系。
