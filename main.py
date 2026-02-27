import httpx
import re
import time
from astrbot.api.event import filter
from astrbot.api.star import Context, Star, register
from astrbot.core.platform import AstrMessageEvent

@register("dnf_gold_monitor", "qingcai", "DNF跨5全平台金价实时看板", "1.0.0")
class DnfGoldPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }

    @filter.command("查金价")
    async def check_gold(self, event: AstrMessageEvent):
        sender_name = event.get_sender_name()
        yield event.plain_result(f"🔍 正在根据 [{sender_name}] 的指示，扫描跨5最新行情...")
        
        report = ["💰 DNF 跨5 实时看板 (买家视角)"]
        report.append(f"📅 统计时间: {time.strftime('%H:%M:%S')}\n")

        targets = [
            {"name": "UU898", "url": "https://www.uu898.com/newTrade-95-c-3-2325-s25022/"},
            {"name": "DD373", "url": "https://www.dd373.com/s-rbg22w-c-42hcun-8tjvpa-55as0c-0-0-0.html"}
        ]

        async with httpx.AsyncClient(headers=self.headers, timeout=15, follow_redirects=True) as client:
            for target in targets:
                try:
                    r = await client.get(target['url'])
                    if r.status_code == 200:
                        # 磨平 HTML 标签
                        plain = re.sub(r'<[^>]+>', ' ', r.text)
                        
                        # 只匹配 "1元=" 后面跟着的两位数比例
                        match = re.findall(r'1\s*元\s*[=等于]\s*(\d{2}\.?\d*)', plain)
                        # 逻辑过滤：只有 40-90 之间的数字才视为金价比例
                        ratios = [float(v) for v in match if 40 < float(v) < 90]
                        
                        if ratios:
                            unique_p = sorted(list(set(ratios)), reverse=True)[:3]
                            report.append(f"【{target['name']}】")
                            for i, v in enumerate(unique_p):
                                report.append(f" {i+1}. 比例 1:{v} (1亿≈{10000/v:.1f}元)")
                            report.append(f" 🔗 直达: {target['url']}\n")
                except:
                    report.append(f"【{target['name']}】查询超时\n")

        yield event.plain_result("\n".join(report))