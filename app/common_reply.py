import re

from linebot.models import (
    TextSendMessage, ImageSendMessage, AudioSendMessage
)

from app.dice import fortune, tarot_line_reply, nca, choice, coc_7e_basic, draw_card, pan_pan, draw_cat, find_schumi, \
    touch_schumi_line_reply, draw_sinoalice
from app.direct_reply import gurulingpo, poor_chinese, qq, mahoshoujo, why, \
    bot_help, tzguguaning, daughter_red, girlfriend, pier_girl, sinoalice_raid_boss
from app.finance import exchange_rate
from app.google_utils.custom_search import google_search_image
from app.weather_status import weather_now, rainfall_now, radar_now, aqi_now, aqi_predict, aqi_status, reservoir_now

# equivalent to:
# fortune_pattern = re.compile(ur'\u904b\u52e2', re.UNICODE)
fortune_pattern = re.compile(r'運勢')
tarot_pattern = re.compile(r'塔羅')
draw_cat_pattern = re.compile(r'抽貓')
coc_7e_basic_pattern = re.compile(
    r"""^cc            # start with cc
        (\(-?[12]\))?  # optional (n), -2 <= n <= 2
        <=\d+
    """, re.VERBOSE | re.IGNORECASE)
coc_7e_skill_pattern = re.compile(
    r"""^cc>\d+\s?
    """, re.VERBOSE | re.IGNORECASE)
gurulingpo_pattern = re.compile(r'咕嚕靈波')
mahoshoujo_pattern = re.compile(r'魔法少女')
tzguguaning_pattern = re.compile(r'慈孤觀音')
daughter_red_pattern = re.compile(r'女兒紅')
girlfriend_pattern = re.compile(r'求女(朋)?友')
why_pattern = re.compile(r'請問為什麼')
google_custom_search_pattern = re.compile(r'^找圖\s+.+')
help_pattern = re.compile(r'/help', re.IGNORECASE)
poor_chinese_pattern = re.compile(r'爛中文')
panpan_pattern = re.compile(r'^撩妹')
qq_pattern = re.compile(r'幫qq', re.IGNORECASE)
nca_pattern = re.compile(r'^nca', re.IGNORECASE)
aqi_predict_pattern = re.compile(r'^空品預測\s+.+')
aqi_status_pattern = re.compile(r'^空品現況\s+.+')
choice_pattern = re.compile(
    r"""choice\s?  # choice + 0~1 space
    \[             # [
    [^,\[\]]+      # not start with , [, ] (at least once)
    (,[^,\[\]]+)+  # plus dot (at least once)
    ]              # ]
    """, re.VERBOSE | re.IGNORECASE)


pattern_mapping_common = [
    {
        'cmd': fortune_pattern,
        'type': 'search',
        'function': fortune,
    },
    {
        'cmd': nca_pattern,
        'type': 'search',
        'function': nca,
    },
    {
        'cmd': tarot_pattern,
        'type': 'search',
        'function': tarot_line_reply,
        'multi_type_output': True
    },
    {
        'cmd': google_custom_search_pattern,
        'type': 'search',
        'function': google_search_image,
        'multi_type_output': True,
        'matched_as_arg': True
    },
    {
        'cmd': draw_cat_pattern,
        'type': 'search',
        'function': draw_cat,
        'multi_type_output': True
    },
    {
        'cmd': '找朽咪',
        'type': 'equal',
        'function': find_schumi,
        'multi_type_output': True
    },
    {
        'cmd': '摸朽咪',
        'type': 'equal',
        'function': touch_schumi_line_reply,
        'multi_type_output': True
    },
    {
        'cmd': choice_pattern,
        'type': 'search',
        'function': choice,
        'matched_as_arg': True
    },
    {
        'cmd': coc_7e_basic_pattern,
        'type': 'search',
        'function': coc_7e_basic,
        'matched_as_arg': True
    },
    {
        'cmd': '天氣',
        'type': 'equal',
        'function': weather_now
    },
    {
        'cmd': '即時雨量',
        'type': 'equal',
        'function': rainfall_now
    },
    {
        'cmd': '雷達',
        'type': 'equal',
        'function': radar_now
    },
    {
        'cmd': '空品',
        'type': 'equal',
        'function': aqi_now
    },
    {
        'cmd': '碼頭姑娘',
        'type': 'equal',
        'function': pier_girl
    },
    {
        'cmd': '水庫',
        'type': 'equal',
        'function': reservoir_now,
        'multi_type_output': True
    },
    {
        'cmd': aqi_predict_pattern,
        'type': 'search',
        'function': aqi_predict,
        'matched_as_arg': True
    },
    {
        'cmd': aqi_status_pattern,
        'type': 'search',
        'function': aqi_status,
        'matched_as_arg': True,
        'multi_type_output': True
    },
    {
        'cmd': '匯率',
        'type': 'equal',
        'function': exchange_rate
    },
    {
        'cmd': '抽死愛',
        'type': 'equal',
        'function': draw_sinoalice,
        'multi_type_output': True
    },
    {
        'cmd': '何老師抽卡',
        'type': 'equal',
        'function': draw_card
    },
    {
        'cmd': poor_chinese_pattern,
        'type': 'search',
        'function': poor_chinese
    },
    {
        'cmd': panpan_pattern,
        'type': 'search',
        'function': pan_pan
    },
    {
        'cmd': qq_pattern,
        'type': 'search',
        'function': qq
    },
    {
        'cmd': mahoshoujo_pattern,
        'type': 'search',
        'function': mahoshoujo
    },
    {
        'cmd': gurulingpo_pattern,
        'type': 'search',
        'function': gurulingpo
    },
    {
        'cmd': why_pattern,
        'type': 'search',
        'function': why
    },
    {
        'cmd': tzguguaning_pattern,
        'type': 'search',
        'function': tzguguaning
    },
    {
        'cmd': '討伐時間',
        'type': 'equal',
        'function': sinoalice_raid_boss
    },
    {
        'cmd': daughter_red_pattern,
        'type': 'search',
        'function': daughter_red,
        'multi_type_output': True
    },
    {
        'cmd': girlfriend_pattern,
        'type': 'search',
        'function': girlfriend,
        'multi_type_output': True
    },
    {
        'cmd': help_pattern,
        'type': 'search',
        'function': bot_help
    },
]

last_msg = {}
replied_time = {}


def build_complex_msg(result):
    complex_msg = []
    for msg_type, msg in result:
        if msg_type == 'text':
            complex_msg.append(TextSendMessage(text=msg))
        elif msg_type == 'image':
            complex_msg.append(ImageSendMessage(
                original_content_url=msg,
                preview_image_url=msg,
            ))
        elif msg_type == 'audio':
            complex_msg.append(AudioSendMessage(
                original_content_url=msg,
                duration=10 * 1000
            ))
        elif msg_type == 'flex':
            complex_msg.append(msg)
        else:
            raise ValueError(f" unknown msg_type: {msg_type}")
    return complex_msg


def get_reply_from_mapping_function(msg_info, robot_settings, pattern_mapping):
    for p in pattern_mapping:
        if p['type'] == 'equal':
            if msg_info.msg == p['cmd']:
                result = p['function'](msg_info, robot_settings)
                if p.get('multi_type_output', False):
                    return build_complex_msg(result)
                else:
                    return [TextSendMessage(text=result)]

        elif p['type'] == 'search':
            match = p['cmd'].search(msg_info.msg)
            if match:
                if p.get('matched_as_arg', False):
                    result = p['function'](match.group(0), msg_info, robot_settings)
                else:
                    result = p['function'](msg_info, robot_settings)
                if p.get('multi_type_output', False):
                    return build_complex_msg(result)
                else:
                    return [TextSendMessage(text=result)]
        else:
            raise ValueError(f" unknown pattern type: {p['type']}")
    return None


def common_reply(msg_info, robot_settings):
    reply = get_reply_from_mapping_function(msg_info, robot_settings, pattern_mapping_common)
    if reply:
        return reply
    # import logging
    # logger = logging.getLogger(__name__)
    # if msg == last_msg.get(source_id, None):
    #     now = int(time.time())
    #     logger.info('偵測到重複，準備推齊')
    #     repeated_diff_ts = now - replied_time.get((source_id, msg), 0)
    #     if repeated_diff_ts > 600:
    #         logger.info(f'{msg} 上次重複已經超過 {repeated_diff_ts} 秒，執行推齊！')
    #         replied_time[(source_id, msg)] = now
    #         return [TextSendMessage(text=msg)]
    #     else:
    #         logger.info(f'{msg} 上次重複在 {repeated_diff_ts} 秒內，不推齊')
    last_msg[msg_info.source_id] = msg_info.msg
    return []
