English | [简体中文](README.md)

### NotebookQwen 

#### Project Overview
This project is inspired by NotebookLlama and aims to extract text from a given URL, generate podcast scripts, and convert them into video files. 

The project workflow is divided into the following steps:
1. Extract webpage content and save it as a text file.
2. Use LLM (Large Language Model) to generate podcast scripts.
3. Convert the generated podcast script into audio files.
4. Convert the podcast script into image files.
5. Combine the generated audio and image files into video files.

#### Demo

[9.1 Rating! A Must-Watch Chinese Film, *Good Stuff*](https://mp.weixin.qq.com/s/sGEcVIxH6TkIjeWew-LSJg)

[![9.1 Rating! A Must-Watch Chinese Film, *Good Stuff*](https://img.youtube.com/vi/rv-vXynEj6M/0.jpg)](https://www.youtube.com/watch?v=rv-vXynEj6M)

```json
{
    "description": "揭秘高分国产电影《好东西》的魅力。",
    "dialogues": [
        {
            "speaker": "发言者1",
            "contents": [
                "大家好，欢迎收听我们的节目。",
                "今天我们要聊聊一部神作——《好东西》。",
                "这部电影不仅豆瓣评分高达9.1，还收获了无数好评。"
            ]
        },
        {
            "speaker": "发言者2",
            "contents": [
                "哇，9.1分，这确实很高！",
                "这部电影到底有什么特别之处呢？",
                "你能先给我们介绍一下它的基本情况吗？"
            ]
        },
        {
            "speaker": "发言者1",
            "contents": [
                "当然可以。《好东西》是导演邵艺辉的新作。",
                "她之前的《爱情神话》也大获成功。",
                "这次，她讲述的是三个女性在上海的生活故事。"
            ]
        },
        {
            "speaker": "发言者2",
            "contents": [
                "三个女性？听起来很有趣。",
                "她们分别是谁呢？",
                "她们之间有什么特别的互动吗？"
            ]
        },
        {
            "speaker": "发言者1",
            "contents": [
                "这三位女性分别是单亲妈妈王铁梅，乐队主唱小叶，",
                "还有王铁梅的女儿王茉莉。",
                "她们各自有着不同的背景和性格。"
            ]
        },
        {
            "speaker": "发言者2",
            "contents": [
                "嗯，这些角色听起来都很有特点。",
                "你能具体说说她们的性格吗？",
                "比如王铁梅是个怎样的人？"
            ]
        },
        {
            "speaker": "发言者1",
            "contents": [
                "王铁梅非常独立，事业有成，还独自抚养女儿。",
                "小叶则是一个典型的‘恋爱脑’，渴望爱情，",
                "但同时保持自尊。"
            ]
        },
        {
            "speaker": "发言者2",
            "contents": [
                "哇，这两个角色已经很吸引人了。",
                "那王茉莉呢？她是个怎样的孩子？",
                "9岁的孩子能有多深刻？"
            ]
        },
        {
            "speaker": "发言者1",
            "contents": [
                "王茉莉虽然只有9岁，但非常成熟和智慧。",
                "她对世界的看法常常让人眼前一亮。",
                "她的存在为故事增添了独特的视角。"
            ]
        },
        {
            "speaker": "发言者2",
            "contents": [
                "这真是三个非常有魅力的角色。",
                "她们之间的互动是怎么样的呢？",
                "有没有什么特别的情节？"
            ]
        },
        {
            "speaker": "发言者1",
            "contents": [
                "她们之间的互动非常紧密。",
                "王铁梅像母亲一样照顾小叶和王茉莉。",
                "小叶则在情感上支持王铁梅。"
            ]
        },
        {
            "speaker": "发言者2",
            "contents": [
                "嗯，这种互助和支持真的很温暖。",
                "电影中有没有一些特别打动人的场景？",
                "比如某个温馨的日常片段？"
            ]
        },
        {
            "speaker": "发言者1",
            "contents": [
                "有一场戏是小叶主动帮王铁梅照顾王茉莉。",
                "这场戏展现了小叶的善良和体贴。",
                "还有她们一起做饭、聊天的场景，非常真实温暖。"
            ]
        },
        {
            "speaker": "发言者2",
            "contents": [
                "这些场景确实很能打动人心。",
                "电影中还有一些关于女性主义的元素，",
                "比如上野千鹤子的书和金斯伯格的T恤。"
            ]
        },
        {
            "speaker": "发言者1",
            "contents": [
                "是的，这些细节反映了角色的内心世界。",
                "王铁梅经常提到上野千鹤子的书，",
                "小叶则引用金斯伯格的话来鼓励自己。"
            ]
        },
        {
            "speaker": "发言者2",
            "contents": [
                "这些细节确实让角色更加立体。",
                "不过，电影中的男性角色好像被边缘化了。",
                "这是导演有意为之吗？"
            ]
        },
        {
            "speaker": "发言者1",
            "contents": [
                "是的，导演邵艺辉希望更多聚焦于女性的生活和情感。",
                "男性角色虽然存在，但更多的是作为背景。",
                "这种处理方式让主题更加鲜明。"
            ]
        },
        {
            "speaker": "发言者2",
            "contents": [
                "这种处理方式确实很独特。",
                "电影在情感上有哪些特别打动人的地方？",
                "有没有让你印象深刻的场景？"
            ]
        },
        {
            "speaker": "发言者1",
            "contents": [
                "电影的情感处理非常细腻。",
                "比如小叶在铁梅忙时主动帮忙照顾王茉莉。",
                "这些场景让人感受到女性之间的深厚友谊。"
            ]
        },
        {
            "speaker": "发言者2",
            "contents": [
                "嗯，这些场景确实很温暖。",
                "对了，电影中有个关于家务的蒙太奇，",
                "那个场景真的很有创意。"
            ]
        },
        {
            "speaker": "发言者1",
            "contents": [
                "是的，那个蒙太奇非常有创意。",
                "导演通过自然声效来表现家务活，",
                "比如晾衣服像打雷，煎鸡蛋像下暴雨。"
            ]
        },
        {
            "speaker": "发言者2",
            "contents": [
                "哈哈，这个比喻真的太妙了。",
                "我从来没有想过家务活还能这么有趣。",
                "这部电影真的让人感到开心和平静。"
            ]
        },
        {
            "speaker": "发言者1",
            "contents": [
                "是的，这部电影传递了积极向上的生活态度。",
                "在这个充满压力的时代，",
                "看到这样一部温暖幽默的电影是一种享受。"
            ]
        },
        {
            "speaker": "发言者2",
            "contents": [
                "谢谢你的详细介绍。",
                "我已经迫不及待想去电影院看这部电影了。",
                "大家如果感兴趣，也一定要去看看。"
            ]
        },
        {
            "speaker": "发言者1",
            "contents": [
                "没错，希望大家能在《好东西》中找到温暖和感动。",
                "好了，今天的节目就到这里。",
                "感谢大家的收听，我们下次再见！"
            ]
        },
        {
            "speaker": "发言者2",
            "contents": [
                "再见，大家！"
            ]
        }
    ]
}
```

#### Directory Structure
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

#### Installation
Ensure the following dependencies are installed:
```sh
pip install -r requirements.txt
```

#### Configuration
The project requires a `config.toml` file. Here’s how to set it up:

1. Copy the template file:
   ```sh
   cp config-template.toml config.toml
   ```

2. Edit `config.toml`:
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

#### Running the Project
1. Ensure `config.toml` is properly configured.
2. Run the main script with the URL to process:

```sh
python main.py https://mp.weixin.qq.com/s/sGEcVIxH6TkIjeWew-LSJg
```

#### Acknowledgments
- [NotebookLlama](https://github.com/meta-llama/llama-recipes/tree/main/recipes/quickstart/NotebookLlama)

We hope this README is helpful! Feel free to reach out with any questions or suggestions.