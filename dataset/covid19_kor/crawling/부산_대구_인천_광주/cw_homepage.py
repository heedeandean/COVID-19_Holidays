## 테스트 용입니당 ... 아직 정상 실행 안됐어요 ..ㅜㅜ


from bs4 import BeautifulSoup
import requests
import numpy as np

req = requests.get("http://www.busan.go.kr/covid19/Corona19/travelhist.do")
html = req.text




soup = BeautifulSoup(html, "html.parser")



list = soup.find("div", {'class' : "list_body"})

a = []

list2 = soup.select('#contents > div > div.corona_list > div.list_body > ul:nth-child(48)')







########################### test zone #################################################

# test = list2[0].find("table", {'class' : "tableCol __se_tbl"}).tbody.tr.find_all('td')

# for i in range(len(test)):
#    a.append(test[i].text)
#
# print(a)
#
# list3 = soup.select('#contents > div > div.corona_list > div.list_body')
#
# print(list3[0].select('ul:nth-child(2)'))
# for i in list3[0].ul:
#     print(i)
#

############################################################################

arr = np.empty((0,12) , dtype=str)
print(arr)
list_res = []

list_res_table = []

# 230
for i in range(21,25) :
    for j in range(1,7) :

        list2 = soup.select(
            '#contents > div > div.corona_list > div.list_body > ul:nth-child({}) > li:nth-child({})'.format(i,j))

        print('tagname :: {}  count :: {} ,, {} '.format(list2[0].name,i,j))

        print(list2[0].text)
        list_res.append(list2[0].text)

        if j == 6:
            for tag in list2[0].children :
                print("eee!!",tag.p)
                if tag.name == 'table':
                    print('!!!')
                    #list_res_table.append()
                    for tag_tag in tag.tbody.tr.children:
                        if tag_tag.name == 'td':
                            list_res_table.append(tag_tag.text)

            continue




print(list_res)
np_busan = np.array(list_res).reshape(-1,5)

print('------------')
print(np_busan)

# np.savetxt('save.csv', np_busan, fmt='%s', delimiter=",", encoding='UTF-8')














'''








for t in table.children:
	if t.name == 'thead':
		print(t.get_text(), end=' ')


	if t.name == 'tbody' :
		print(t.get_text(), end=' ')




tr = table.tbody.tr
for t in tr.children:
	print(t.name,'11')
	if t.name == 'td':
		print(t)
		if t["class"] == "N N N N":
			print(t.get_text())




tr = tr.next_sibling.next_sibling


print('@시각')
for t in tr.children:
	if t.name == 'td':
		for i in t.contents:
			if i.name =='p':
				print(i.get_text(), end=' ')
print('\n')



tr = tr.next_sibling.next_sibling



print('@날씨')
for w in tr.children:
	if w.name == 'td' and len(w.contents) > 0:
		print(w['title'], end= ' ')
print('\n')



tr = tr.next_sibling.next_sibling



print('@강수 확률')
for w in tr.children:
	if w.name == 'td' and len(w.contents) > 0:
		print(w.contents[0], end=' ')
print('\n')



tr = tr.next_sibling.next_sibling



print('@강수량')
for w in tr.children:
	if w.name == 'td' and len(w.contents) > 0:
		num = int(w['colspan'])

		for i in range(num):
			print(w.contents[0].strip(), end=' ')
print('\n')



tr = tr.next_sibling.next_sibling


print('@최저/최고 기온')
for w in tr.children:
	if w.name == 'td' and len(w.contents) > 0:
		num = int(w['colspan'])

		for i in range(num):
			print(w.contents[0].get_text(), end='/')
			print(w.contents[2].get_text(), end=' ')
print('\n')



tr = tr.next_sibling.next_sibling



print('@기온(℃)')
for w in tr.children:
	if w.name == 'td' and len(w.contents) > 0:
		print(w.contents[0].get_text(), end=' ')
print('\n')



tr = tr.next_sibling.next_sibling



print('@풍향/풍속(m/s)')
for w in tr.children:
	if w.name == 'td' and len(w.contents) > 0:
		print(w['title'], end= ' ')
print('\n')



tr = tr.next_sibling.next_sibling


print('@습도(%)')
for w in tr.children:
	if w.name == 'td' and len(w.contents) > 0:
		print(w.contents[0].get_text(), end=' ')
print('\n')

'''