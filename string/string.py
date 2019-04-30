message = 'dasdhasd@dasd@dasdas@sadsa@112121'
# @分割
texts = message.split('@')
for text in texts:
    print(text)
print('*'*50)
# 全部的
b = message[:]
print(b)
print('*'*50)
# 去掉最后两位
b = message[:-2]
print(b)
print('*'*50)
# 前两位
b = message[:2]
print(b)
print('*'*50)
# if判断
if '@' in message:
    print('yes')
# else if判断
elif '#' in message:
    print('wow')
# else 
else:
    print('shit!!!')
print('*'*50)
# 更新字符串   第四位开始换成!
print(message[:3] + '!')
print('*'*50)



