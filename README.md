# proxy-rules（分流规则，不含节点）

只放规则，不放节点。节点来自你自己的节点订阅（单独维护），本仓库的规则文件通过名称/特征引用节点，两边互不掺杂。

## 文件

| 文件 | 客户端 | 用法 |
|---|---|---|
| `clash-rules.yaml` | Clash Verge / mihomo / Nikki | 作为订阅导入；导入后把文件里 `proxy-providers.youngtree.url` 换成你自己的节点订阅地址（.txt 订阅即可），节点会自动拉取 |
| `shadowrocket-rules.conf` | Shadowrocket | 在「配置」里导入并启用；前提是 SR 里已添加你的节点订阅。本文件用 `policy-regex-filter` 按节点名特征（如「上海电信」「南京移动」「法兰克福」）自动匹配订阅里的节点，不绑定具体订阅名 |

## 分组

- 🚀 节点选择：手动选节点（默认第一个香港节点）
- ♻️ 自动测速：全部节点按延迟自动选
- 🤖 AI：默认德国，可单选（德国/巴西/墨西哥/香港）
- 🎬 流媒体：默认自动测速，可单选

## 规则

- AI（OpenAI/Claude/Gemini/Copilot 等，含 Grok、Perplexity、Mistral、Cursor 等补充域名）→ 🤖 AI
- 流媒体（Netflix/Disney/YouTube/Spotify/HBO/PrimeVideo/Hulu/AppleTV/TikTok）→ 🎬 流媒体
- 广告名单 → REJECT
- 国内名单 + 中国 IP → 直连
- 其余 → 🚀 节点选择

规则名单来自 blackmatrix7/ios_rule_script，客户端远程引用、自动更新。
