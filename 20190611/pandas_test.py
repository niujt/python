import pandas as pd

_list = [value ** 3 for value in range(1, 11)]
_list = pd.DataFrame(_list)
_list = _list.rename(columns={0: 'one'})
_list = _list.add_prefix('number_')
_list['result_check'] = _list['number_one'].apply(lambda x: '大于100' if x > 100 else '小于100')
max = {'number_one': _list.apply(lambda x: x.max())['number_one'], 'result': '大于100'}
_list = _list.append(max, ignore_index=True)
ls = list(str(value) + '的立方' for value in range(1, 11))
ls.append('最大值')
_list.index = ls
_list = _list.fillna('-')
print(_list)
