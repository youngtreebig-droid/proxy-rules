# proxy-rules（分流规则，不含节点）

只放规则，不放节点、不放任何订阅地址。用法和 Loyalsoldier、blackmatrix7 的规则一样：**先订阅你自己的节点，再把规则套上去**，规则只按分组名/节点名引用，不需要改任何 URL。

## 文件

| 文件 | 客户端 | 用法 |
|---|---|---|
| `clash-rules.yaml` | Clash Verge / mihomo / Nikki | 这是**覆写文件**，不是独立订阅：先在客户端导入你自己的节点订阅，再把本文件内容粘贴到「全局扩展配置」（Clash Verge）或 mixin（Nikki）里。分组用 `include-all-proxies` 自动纳入当前订阅的全部节点 |
| `shadowrocket-rules.conf` | Shadowrocket | 在「配置」里导入并启用；前提是 SR 里已添加你的节点订阅。本文件用 `policy-regex-filter` 按节点名特征（如「上海电信」「南京移动」「法兰克福」）自动匹配订阅里的节点 |

唯一的例外：`clash-rules.yaml` 的 🤖 AI 组为了保证默认走德国，按名字列了 5 个节点；换节点时改那几行名字即可，其余分组全部自动纳入、不用动。

## 分组

- 🚀 节点选择：默认自动测速，可手动选任意节点
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
