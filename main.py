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
        yield event.plain_result(f"🔍 正在根据 [{sender_name}] 的指示，扫描 UU 和 DD 的跨5主列表行情...")
        
        report = ["💰 DNF 跨5 实时看板 (买家视角)"]
        report.append(f"📅 统计时间: {time.strftime('%H:%M:%S')}\n")

        async with httpx.AsyncClient(headers=self.headers, timeout=15, follow_redirects=True) as client:
            # --- 1. UU898 提取 ---
            try:
                uu_url = "https://www.uu898.com/newTrade-95-c-3-2325-s25022/"
                r = await client.get(uu_url)
                if r.status_code == 200:
                    plain = re.sub(r'<[^>]+>', ' ', r.text)
                    report.append("【UU898 (江苏1区)】")
                    p_chunks = plain.split("免费兑换此商品")
                    p_ratios = []
                    for chunk in p_chunks[1:7]:
                        # 精准正则：只找 "1元=" 后面跟着的数字
                        match = re.findall(r'1\s*元\s*[=等于]\s*(\d{2}\.?\d*)', chunk)
                        if match:
                            v = float(match[0])
                            if 40 < v < 90: p_ratios.append(v)
                    
                    if p_ratios:
                        unique_p = sorted(list(set(p_ratios)), reverse=True)[:3]
                        for v in unique_p:
                            report.append(f"   - 1:{v} (1亿≈{10000/v:.1f}元)")
                    report.append(f" 🔗 直达: {uu_url}\n")
            except: report.append("【UU898】查询超时\n")

            # --- 2. DD373 提取 ---
            try:
                dd_url = "https://www.dd373.com/s-rbg22w-c-42hcun-8tjvpa-55as0c-0-0-0.html"
                r = await client.get(dd_url)
                if r.status_code == 200:
                    plain = re.sub(r'<[^>]+>', ' ', r.text)
                    report.append("【DD373 (跨5区)】")
                    l_start = plain.find("比例最佳")
                    if l_start != -1:
                        l_chunk = plain[l_start:l_start+8000]
                        l_ratios = re.findall(r'1\s*元\s*[=等于]\s*(\d{2}\.?\d*)', l_chunk)
                        valid_l = [float(x) for x in l_ratios if 40 < float(x) < 90]
                        if valid_l:
                            unique_l = sorted(list(set(valid_l)), reverse=True)[:3]
                            for v in unique_l:
                                report.append(f"   - 1:{v} (1亿≈{10000/v:.1f}元)")
                    report.append(f" 🔗 直达: {dd_url}\n")
            except: report.append("【DD373】查询超时\n")

        yield event.plain_result("\n".join(report))
