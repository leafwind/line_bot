import random
import json
import logging
import os

from constants import HUGE_GROUP_IDS

tarot_cards = json.load(open('app/tarot.json', encoding='utf8'))


def tarot(source_id):
    random.seed(os.urandom(5))
    card = random.choice(tarot_cards)
    logging.info('%s: %s', card['nameCN'], card['url'])
    replies = []
    if source_id not in HUGE_GROUP_IDS:
        # skip card picture for large groups
        replies.append(('image', card['url']))
    replies.append(('text', f'{card["nameCN"]}: {card["conclusion"]}'))
    return replies


def coc_7e_basic(msg):
    random.seed(os.urandom(5))
    d100 = random.randint(1, 100)  # 1 <= N <= 100
    condition = int(msg.split('<=')[1])
    result = f'克蘇魯的呼喚七版：(1D100<={condition}) 初始結果 → {d100}\n'

    final_dice = d100
    if '(' in msg:
        extra = int(msg.split(')')[0].split('(')[1])
        if -2 <= extra <= 2 and extra != 0:
            tens_digit = d100 // 10
            abs_extra = abs(extra)
            extra_dices = [random.randint(1, 10) for _ in range(abs_extra)]
            if extra < 0:
                extra_dice_desc = '懲罰骰取高'
                tens_digit = max(tens_digit, max(extra_dices))
            else:
                extra_dice_desc = '獎勵骰取低'
                tens_digit = min(tens_digit, min(extra_dices))
            final_dice = tens_digit * 10 + d100 % 10
            result += f'→ 十位數加骰為{"、".join([str(d*10) for d in extra_dices])}，{extra_dice_desc} → 最終值({str(final_dice)})'

    if final_dice == 1:
        final_stat = ' → ＼大★成★功／'
    elif final_dice == 100:
        final_stat = ' → 大失敗，すばらしく運がないな、君は。'
    elif final_dice <= condition // 5:
        final_stat = ' → 極限成功'
    elif final_dice <= condition // 2:
        final_stat = ' → 困難成功'
    elif final_dice <= condition:
        final_stat = ' → 一般成功'
    elif final_dice > condition:
        final_stat = ' → 失敗'
    else:
        raise ValueError(f'invalid final_dice range: {final_dice}')
    result += final_stat
    return result


def nca():
    random.seed(os.urandom(5))
    d10 = random.randint(1, 10)  # 1 <= N <= 10
    desc_str_map = {
        1: '大失敗\n命中包含自己的友方，由被攻擊方選擇被命中的部位。',
        2: '失敗\n未命中',
        3: '失敗\n未命中',
        4: '失敗\n未命中',
        5: '失敗\n未命中',
        6: '成功\n由被攻擊方選擇被命中的部位。',
        7: '成功\n命中腳部。\n如果該部位全部件損壞，由攻擊者選擇其他任意部位。',
        8: '成功\n命中胴部。\n如果該部位全部件損壞，由攻擊者選擇其他任意部位。',
        9: '成功\n命中腕部。\n如果該部位全部件損壞，由攻擊者選擇其他任意部位。',
        10: '成功\n命中頭部。\n如果該部位全部件損壞，由攻擊者選擇其他任意部位。',
    }
    return f'死靈年代記之永遠的後日談：[{d10}]  → {desc_str_map[d10]}'


def choice(matched_msg):
    random.seed(os.urandom(5))
    options_str = matched_msg.split('[')[1][:-1]
    options = options_str.split(',')
    result = f'自訂選項：[{",".join(options)}] → {random.choice(options)}'
    return result


def fortune():
    random.seed(os.urandom(5))
    dice = random.randint(1, 1000)  # 1 <= N <= 1000
    ans = [
        '大吉だよ！\nやったね⭐︎',
        '大吉……騙你的，差一點呢！\n只是吉而已呦(`・ω・´)',
        '吉。🎉\n很棒呢！',
        '中吉。\n還不錯吧。(ゝ∀･)',
        '小吉。\n就是小吉，平淡過日子，願世界和平。☮',
        '半吉。\n㊗️pyon醬祝福你！(^y^)',
        '末吉。\n嗯～勉勉強強吧！(,,・ω・,,)。',
        '末小吉。\n至少不壞呢！(*´∀`)',
        '凶。\nσ ﾟ∀ ﾟ) ﾟ∀ﾟ)σ至少還有很多更糟的！',
        '小凶。\n(́◉◞౪◟◉‵)運氣不是很好呢，怎麼辦？',
        '半凶。\n有點糟糕～(◔౪◔)',
        '末凶。\nすばらしく運がないな、君は。😊',
        '大凶……⁉️\n欸這機率是千分之一喔？\n比大吉的百分之二還慘喔！？\n沒問題嗎？(((ﾟДﾟ;)))'
    ]
    if dice <= 20:
        return ans[0]
    elif dice <= 90:
        return ans[1]
    elif dice <= 160:
        return ans[2]
    elif dice <= 250:
        return ans[3]
    elif dice <= 363:
        return ans[4]
    elif dice <= 444:
        return ans[5]
    elif dice <= 525:
        return ans[6]
    elif dice <= 600:
        return ans[7]
    elif dice <= 720:
        return ans[8]
    elif dice <= 825:
        return ans[9]
    elif dice <= 929:
        return ans[10]
    elif dice <= 999:
        return ans[11]
    elif dice <= 1000:
        return ans[12]
    else:
        raise ValueError
