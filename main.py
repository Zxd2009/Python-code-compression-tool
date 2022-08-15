def cut(data): # 分离字符串与代码
    strType = ''  # 读取到字符串就是字符串引号的类型（',",''',"""），
                  # 没有读取到字符串就是空的
    fxg = False   # 是否读取到字符串中的反斜杠
    zs = False    # 是否是注释
    ans = ['']    # 最终的结果
    i = 0         # 读取到的位置

    while i < len(data):
        if strType != '':  # 在字符串中
            if fxg:
                ans[len(ans) - 1] += data[i]
                fxg = False
            elif data[i] == '\\':
                ans[len(ans) - 1] += '\\'
                fxg = True
            elif len(strType) == 1 and i < len(data) - 1 and data[i] == strType:
                ans[len(ans) - 1] += data[i]
                ans.append('')
                strType = ''
            elif len(strType) == 3 and i < len(data) - 3 and data[i:(i + 2)] == strType:
                ans[len(ans) - 1] += strType
                ans.append('')
                i += 3
                continue
            else:
                ans[len(ans) - 1] += data[i]
        else:
            if zs:
                if data[i] == '\r':
                    continue
                elif data[i] == '\n':
                    zs = False
                    cur = len(ans) - 1
                    if len(ans[cur]) > 0 and ans[cur][len(ans[cur]) - 1] != '\n':
                        ans[len(ans) - 1] += '\n'
                    i += 1
                    continue
                ans[len(ans) - 1] += data[i]
            # 这两个 elif 是匹配字符串
            elif data[i] == '\'' or data[i] == '"':
                strType = data[i]
                ans.append(strType)
            elif i < len(data) - 3 and (data[i:(i + 2)] == '\'\'\'' or data[i:(i + 2)] == '"""'):
                strType = data[i:(i + 3)]
                ans.append(strType)
                i += 3
                continue
            elif data[i] == '#':
                ans[len(ans) - 1] += '#'
                zs = True
            elif data[i] == '\r':
                pass
            elif data[i] == '\n':
                cur = len(ans) - 1
                if len(ans[cur]) == 0 or ans[cur][len(ans[cur]) - 1] != '\n':
                    ans[len(ans) - 1] += '\n'
            else:
                ans[len(ans) - 1] += data[i]
        i += 1
    return ans

def canint(x):
    try:
        int(x)
    except:
        return False
    return True

def ys(data):  # 压缩掉代码多余的空格和注释
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                   'U', 'V', 'W', 'X', 'Y', 'Z', '_',  # 因为 '_' 可以作为变量名，所以放到这里
               'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z']

    zs = False
    spcnt = -1  # 行首空格的数量，-1 代表不是行首
    ans = ''    # 最终的结果
    i = 0
    while i < len(data):
        if zs:
            if data[i] == '\n':
                zs = False
                spcnt = 0
                if len(ans) == 0 or ans[len(ans) - 1] != '\n':
                    ans += '\n'
        elif data[i] == '#':  # 读取到注释
            ans += '	' * (spcnt // 4)
            spcnt = -1
            zs = True
        elif data[i] == ' ' or data[i] == '	':  # 一个是空格，一个是 Tab
            if spcnt != -1:
                if data[i] == ' ':
                    spcnt += 1
                else:
                    spcnt += 4
            else:
                if i == len(data) - 1:
                    pass
                elif len(ans) == 0:
                    ans += ' '
                elif ans[len(ans) - 1] in letters and i < len(data) - 1 and data[i + 1] in letters:
                    ans += ' '
                elif canint(ans[len(ans) - 1]) and i < len(data) - 1 and data[i + 1] in letters:
                    ans += ' '
                elif ans[len(ans) - 1] and i < len(data) - 1 and canint(data[i + 1]):
                    ans += ' '
        elif data[i] == '\r':
            ans += '	' * (spcnt // 4)
            spcnt = -1
        elif data[i] == '\n':
            spcnt = 0
            if len(ans) == 0 or ans[len(ans) - 1] != '\n':
                ans += '\n'
        else:
            ans += '	' * (spcnt // 4)
            spcnt = -1
            ans += data[i]
        i += 1
    return ans

def main(data):
    data = cut(data)
    lans = ''

    for i in range(len(data)):
        if len(data[i]) == 0:
            continue
        if data[i][0] == '\'' or data[i][0] == '"':  # 这一项是字符串
            lans += data[i]
            continue
        lans += ys(data[i])
    return lans
