def cut(data): # 分离字符串与代码
    strType = ''  # 读取到字符串就是字符串引号的类型（',",''',"""），
                  # 没有读取到字符串就是空的
    fxg = False   # 是否读取到字符串中的反斜杠
    zs = False    # 是否是注释
    ans = ['']    # 最终的结果
    i = 0         # 读取到的位置

    while i < len(data):
        if data[i] == '\r':
            continue
        if strType != '':  # 在字符串中
            if fxg:
                if data[i] == '\n':
                    ans[-1] = ans[-1][:(len(ans[-1]) - 1)]
                else:
                    ans[-1] += data[i]
                fxg = False
            elif data[i] == '\\':
                ans[-1] += '\\'
                fxg = True
            elif len(strType) == 1 and i < len(data) - 1 and data[i] == strType:
                ans[-1] += data[i]
                ans.append('')
                strType = ''
            elif len(strType) == 3 and i < len(data) - 3 and data[i:(i + 3)] == strType:
                ans[-1] += strType
                ans.append('')
                strType = ''
                i += 3
                continue
            else:
                ans[-1] += data[i]
        else:
            if zs:
                if data[i] == '\n':
                    zs = False
                    if len(ans[-1]) > 0 and ans[-1][-1] != '\n':
                        ans.append('\n')
                    i += 1
                    continue
                ans[-1] += data[i]
            # 这两个 elif 是匹配字符串
            elif i < len(data) - 3 and (data[i:(i + 3)] == '\'\'\'' or data[i:(i + 3)] == '"""'):
                strType = data[i:(i + 3)]
                ans.append(strType)
                i += 3
                continue
            elif data[i] == '\'' or data[i] == '"':
                strType = data[i]
                ans.append(strType)
            elif data[i] == '#':
                ans.append('#')
                zs = True
            elif data[i] == '\n':
                if len(ans[-1]) == 0 or ans[-1][-1] != '\n':
                    ans[-1] += '\n'
            else:
                ans[-1] += data[i]
        i += 1
    return ans

def charType(x):  # 把字符分类
    # 这样分类是因为，在 Python 中好像可以把中文当作
    # 变量名，所以这样应该没问题
    operators = ['~','`','!','@','#','$','%','^','&','*','(',')','-','+','=','{','}','[',']','|','\\',':',';','<','>',',','?','/','\'','"']
    if x == ' ' or x == '	':
        return 's'  # 空格或 Tab
    if x in operators:
        return 'o'  # 符号
    if x == '.':
        return 'n'  # 照顾小数点，返回数字，合并时特殊处理
    try:
        int(x)
        return 'n'  # 数字
    except:
        return 'l'  # 字母（指可以当变量名）

def fg(data, recm):  # 分割代码，变成以语句为单位的列表
    # ans 格式：列表套列表，一个子列表代表一条语句
    # 一个子列表：[0, 'a', '=', '123', '+', '234']
    # 第一项是这条语句的缩进空格个数（Tab 算 4 个空格），
    # 第二项开始是这条语句的真正内容，每个元素放一起，里面没有空格
    ans = [[]] # 最终的结果
    spcnt = 0  # 行首空格的数量，-1 代表不是行首
    kh = 0     # 括号个数，用来判断是否在同一条语句内
    i = 0      # 读取到 data 的第几项
    j = 0      # 读取到 data 那一项的第几个字符
    curi = 0   # ans 到第几项
    curj = 0   # ans 那一项的第几个字符


    while i < len(data):
        if j == 0:
            # 跳到了一个新的项，判断一下是不是注释或者字符串
            if data[i] == '':
                i += 1
                continue
            if data[i][j] == '#':
                if not recm:
                    if spcnt != -1:
                        # 特别处理一下
                        curj = 1
                        ans[curi].append(spcnt)
                        ans[curi].append('')
                        spcnt = -1
                    if ans[curi][curj] != '':
                        curj += 1
                        ans[curi].append('')
                    ans[curi][curj] += data[i]
                    curj += 1
                    ans[curi].append('')
                i += 1
                continue
            elif data[i][j] == '"' or data[i][j] == '\'':
                # spcnt == -1: 这个字符串不在行首，所以不是注释
                if (spcnt == -1) or (not recm):
                    if spcnt != -1:
                        # 特别处理一下
                        curj = 1
                        ans[curi].append(spcnt)
                        ans[curi].append('')
                        spcnt = -1
                    if ans[curi][curj] != '':
                        curj += 1
                        ans[curi].append('')
                    ans[curi][curj] += data[i]
                    curj += 1
                    ans[curi].append('')
                i += 1
                continue

        # 下面是正式处理代码的部分
        if data[i][j] == ' ' or data[i][j] == '	':  # 一个是空格，一个是 Tab
            if spcnt != -1:  # 在行首
                if data[i][j] == ' ':
                    spcnt += 1
                else:
                    spcnt += 4
            else:
                if ans[curi][curj] != '':
                    curj += 1
                    ans[curi].append('')
        else:
            if spcnt != -1:
                # 生成 ans 的第一项和第二项
                curj = 1
                ans[curi].append(spcnt)
                ans[curi].append('')
                spcnt = -1

            if data[i][j] == '\r':
                pass
            elif data[i][j] == '\n':
                if kh == 0 and spcnt == -1:
                    # 切换到下一条语句
                    curi += 1
                    curj = 0
                    ans.append([])
                    spcnt = 0
            elif data[i][j] == '\\':
                # 把后面的空格和换行都吞掉
                j += 1
                while (data[i][j] == '\r' or data[i][j] == '\n' or data[i][j] == ' ' or data[i][j] == '	') and j < len(data[i]):
                    j += 1
                j -= 1
                if ans[curi][curj] != '':  # 人为分割元素
                    curj += 1
                    ans[curi].append('')
            elif data[i][j] == '(' or data[i][j] == '[' or data[i][j] == '{':
                # 处理括号，括号肯定是语句里单独的元素
                kh += 1
                if ans[curi][curj] != '':
                    curj += 1
                    ans[curi].append('')
                ans[curi][curj] += data[i][j]
                curj += 1
                ans[curi].append('')
            elif data[i][j] == ')' or data[i][j] == ']' or data[i][j] == '}':
                kh -= 1
                if ans[curi][curj] != '':
                    curj += 1
                    ans[curi].append('')
                ans[curi][curj] += data[i][j]
                curj += 1
                ans[curi].append('')
            else:  # 普通的内容
                if j == len(data[i]):
                    pass
                elif ans[curi][curj] == '':
                    ans[curi][curj] += data[i][j]
                else:
                    a = charType(ans[curi][curj][-1])
                    b = charType(data[i][j])
                    if ((a == 'n' and b == 'l') or (a == 'l' and b == 'n')) and (ans[curi][curj][-1] != '.' and data[i][j] != '.'):
                        # 数字和字母放在一起，有可能是作函数名称
                        pass
                    elif a != b:
                        curj += 1
                        ans[curi].append('')
                    ans[curi][curj] += data[i][j]

        j += 1
        if j == len(data[i]):
            i += 1
            j = 0

    return fixfg(ans)

def fixfg(data):  # 修复格式问题
    flag = True
    i = 0
    while i < len(data):
        if len(data[i]) < 2:
            del data[i]
            continue

        j = 1
        while j < len(data[i]):
            if data[i][j] == '':
                del data[i][j]
                continue
            j += 1

        if len(data[i]) < 2:
            del data[i]
            continue
        if (data[i][0] % 4 != 0) and (data[i][1][0] != '#'):
            # 这样处理是因为单独一个空格也可以作为缩进
            # 如果这行只是注释，则忽略缩进问题
            flag = False
        i += 1

    if flag:
        for i in range(len(data)):
            data[i][0] //= 4
    return data

def merge(data):  # 合并分割的数组
    ans = ''
    for i in range(len(data)):
        ans += '	' * data[i][0]
        ans += data[i][1]
        for j in range(2, len(data[i])):
            # 判断是否需要加空格
            a = charType(data[i][j - 1][-1])
            b = charType(data[i][j][0])
            if (data[i][j - 1] != '.' and data[i][j] != '.') and (a != 's' and b != 's' and a != 'o' and b != 'o'):
                ans += ' '
            ans += data[i][j]

        ans += '\n'
    return ans

def main(data, remove_comments=True):
    data = cut(data)
    data = fg(data, recm=remove_comments)
    data = merge(data)
    return data
