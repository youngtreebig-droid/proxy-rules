# proxy-rules

只放分流配置，不含节点、密码、控制面板密钥和节点订阅地址。先在客户端添加节点订阅，再应用本仓库配置。

## 当前策略

| 流量 | 策略 |
|---|---|
| 内网、群晖、QuickConnect | DIRECT |
| 国际 AI 网站、API、资源域名 | 🤖 AI → 🇩🇪 德国节点 |
| Netflix、Disney、YouTube 等 | 🎬 流媒体，默认香港上海电信 |
| 广告名单 | REJECT |
| 国内域名及中国 IP | DIRECT |
| 其余未匹配流量 | 🚀 节点选择 → 🇭🇰 上海电信 |

AI 和默认出口分别只引用德国组、香港上海电信组，避免之前保存的墨西哥等选择继续生效。香港上海电信组仅在匹配的上海电信香港节点之间测速；自动测速组保留作排障用途，不参与默认出口选择。

节点名至少各有一个能匹配 `德国|法兰克福|Germany|Frankfurt` 和 `(香港|Hong Kong|HK).*上海电信`。更换机场或节点名后必须检查匹配结果。需要更换 AI 地区时明确修改 AI 组。

## 文件

- `clash-rules.yaml`：支持 MRS 的 mihomo/Nikki 覆写文件，不是独立订阅，不适用于旧版 Clash 内核。
- `nikki-dns.yaml`：与上述配置合并使用。国外 DNS 经默认代理，节点和直连连接使用国内 DoH；包含域名嗅探。
- `shadowrocket-rules.conf`：Shadowrocket 配置。国际 AI 分类为 2026-11-03 快照，随本配置更新；广告及国内域名列表由客户端远程刷新。
- `ai-extra.txt`：人工补充域名；修改后同步到两个客户端配置。
- `validate_rules.py`：检查出口约束、规则引用、补充域名同步和公共来源可访问性。

## Nikki 部署

1. 备份 `/etc/config/nikki`、mixin 和运行配置；备份留在路由器，不能上传仓库。
2. 合并 `clash-rules.yaml`、`nikki-dns.yaml` 至 mixin，保留本机 Tailscale 等专用规则和监听器。
3. LuCI 启用 DNS 上游覆写及域名嗅探。局域网访问控制中的 DNS 必须开启；顶层 DNS 劫持开关不能覆盖一条显式 DNS 绕过规则。
4. LuCI 设置优先于 mixin，检查最终生成配置。节点和直连解析使用国内 DoH；普通国外查询使用经过 `🚀 节点选择` 的 DoH。删除旧的国外直连 DNS 策略。
5. 运行 `mihomo -t` 校验后启动。订阅优先本地缓存，避免每次启动先停代理、再联网下载订阅。订阅更新可在代理正常运行时执行。
6. 从普通 LAN DNS 查询、连接日志核对 AI 实际走德国、默认实际走香港上海电信，不能只看分组名称。

**设备自身开启 Shadowrocket、Clash、VPN 或浏览器代理时，先由设备选择出口。路由器不能从加密的客户端代理连接中重新识别 ChatGPT。** 测试路由器分流应使用不经过客户端代理的连接。

## 规则来源与边界

- 国际 AI、国内域名、内网域名和国内 IP：[MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat)，mihomo 每日刷新 MRS。
- 广告：[Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules)；Shadowrocket 使用对应的 [surge-rules](https://github.com/Loyalsoldier/surge-rules)。
- 流媒体：[blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)。

AI、流媒体优先于广告和国内名单，保护登录及资源请求。域名拦截不能保证过滤与正常内容共用域名的视频广告。规则命中不代表地区解锁或账号一定可用。不要将整个共享 CDN 或公共云 IP 段强制归入 AI。

安装 PyYAML 后运行 `python3 validate_rules.py --online`。更新后同时核对来源、节点匹配和实际连接出口。
