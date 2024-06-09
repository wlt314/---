import collections
import string
from collections import Counter
import re

order='etaoinshrdlcumwfgypbvkjxqz'
# 单表代换加密
def encrypt(plaintext, key):
    key_map = {char: key[i] for i, char in enumerate(string.ascii_lowercase)}
    ciphertext = ''
    for char in plaintext.lower():
        if char in key_map:
            ciphertext += key_map[char]
        else:
            ciphertext += char
    return ciphertext

# 单表代换解密
def decrypt(ciphertext, key):
    key_map = {key[i]: char for i, char in enumerate(string.ascii_lowercase)}
    plaintext = ''
    for char in ciphertext.lower():
        if char in key_map:
            plaintext += key_map[char]
        else:
            plaintext += char
    return plaintext

# 频率分析
def frequency_analysis(ciphertext):
    frequency = {chr(i): 0 for i in range(97, 123)}
    for char in ciphertext:
        if char in string.ascii_lowercase:
            frequency[char] += 1;
    return frequency
def decryption_suggestions(ciphertext, common_letters):
    frequency = frequency_analysis(ciphertext)
    #print(frequency)
    temp = [key for key, value in sorted(frequency.items(), key=lambda item: item[1], reverse=True)]
    suggestions = {}
    for i in range(26):
        suggestions[temp[i]] = common_letters[i]
    return suggestions

def decryption_frequencies(ciphertext, suggestions):
    plaintext = ''
    for char in ciphertext:
        if char in suggestions:
            plaintext += suggestions[char];
        else:
            plaintext += char;
    return plaintext;

#基于双字母频率的修改建议
def advice(ciphertext):
    # 清理密文并提取所有双字母组合
    cleaned_text = re.sub(r'[^A-Za-z]', '', ciphertext)  # 仅保留英文字母
    pairs = [cleaned_text[i:i+2] for i in range(len(cleaned_text)-1)]
    # 统计双字母出现的频率
    frequency = Counter(pairs)
    # 计算总双字母组合数量
    total_pairs = sum(frequency.values())
    # 计算每个双字母组合的频率并排序
    sorted_frequency = {pair: count / total_pairs for pair, count in frequency.items()}
    sorted_frequency = dict(sorted(sorted_frequency.items(), key=lambda item: item[1], reverse=True))
    # 英文双字母频率分布
    english_frequency = {
        'th': 1.52,
        'he': 1.28,
        'in': 0.94,
        'an': 0.82,
        're': 0.68,
        'nd': 0.63,
        'at': 0.59,
        'on': 0.57
    }
    # 输出密文中双字母的频率顺序
    #print("密文中双字母的频率顺序:")
    #for pair, freq in sorted_frequency.items():
    #    print(f"{pair}: {freq*100:.2f}%")
    #    输出英文双字母的频率分布
    #print("\n英文双字母的频率分布:")
    #for pair, freq in english_frequency.items():
    #    print(f"{pair}: {freq}%")
    # 比较密文双字母频率与英文双字母频率
    #print("\n比较结果:")
    i=0
    for pair in sorted_frequency:
        i+=1
        if pair not in english_frequency:
            for word in english_frequency:
                i-=1;
                if i== 0:
                    break;
            print("密文中的",pair,"建议改为",word)
            break

# 示例使用
key = 'zyxwvutsrqponmlkjihgfedcba'  # 这是一个示例密钥
#plaintext = 'h e'
#plaintext = input('请输入明文')
plaintext = 'the quick brown fox jumps over the lazy dog near the bank of the river. as the sun sets, the calm water reflects the vibrant hues of twilight. amidst the rustling leaves, a gentle breeze whispers through the valley, carrying with it the sweet scent of blooming flowers.'

ciphertext = encrypt(plaintext, key)
decrypted_text = decrypt(ciphertext, key)
suggestions = decryption_suggestions(ciphertext, order)  # 假设这是英文中字母的常见频率顺序
decry = decryption_frequencies(ciphertext,suggestions)

#print(frequency_analysis(plaintext))
print('原文:', plaintext)
print('加密后:',ciphertext)
#print('解密后: ',{decrypted_text})
print('替代表:', suggestions)
#print(suggestions['o'])
print('攻击后:',decry)
#print(suggestions)

flag =0
while flag !='1':
    print("这是建议:")
    advice(decry)
    x=input("您对替换表的修改，交换原替代表中的字母x（密文中的字母）:")
    y=input("和字母y：")
    temp = suggestions[x]
    suggestions[x] = suggestions[y]
    suggestions[y] = temp
    print('现在的替换表：',suggestions)
    decry = decryption_frequencies(ciphertext, suggestions)
    print("解密得到的明文：",decry)
    flag = input("解密完成了吗，完成输入1，否则输入0:")
