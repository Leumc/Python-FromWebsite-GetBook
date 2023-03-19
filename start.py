import requests

def pre_(url_f):
	#预处理网页，储存
	r=requests.get(url_f)
	global r_t
	r_t=apart(r.text.lstrip().replace('\n','█'),'█',1,-1)
	
def getContent(line,front,behind,plus):
	#从网页储存文件里获取信息
	ss=r_t[line]
	if front!='None_':
		m_=ss.index(front)+plus[0]
	else:
		m_=0
	if behind!='None_':
		n_=ss.index(behind)+plus[1]
	else:
		n_=-1
	return ss[m_:n_].replace('&nbsp;','')
	
def getLine(key,ori,max_):
	#根据关键词获取行号(列表)
	result_=[]
	num_=0
	for u_ in range(len(r_t)):
		if num_<max_:
			try:
				r_t[u_].index(key)
				result_.append(u_)
				num_+=1
			except:pass
		else:
			break
	if result_==[]:
		if isinstance(ori,int):
			for o_ in range(max_):
				result_.append(o_)
		elif isinstance(ori,tuple):
			result_=ori
	return result_
		
	
def apart(content__,apart_key,plus_1,plus_2):
	#按提供的关键字分割字符串，返回列表
	num_=0
	result_=[]
	n_b=0
	for T in content__:
		if T==apart_key:
			R=content__[n_b+plus_1:num_+plus_2]
			result_.append(R)
			n_b=num_
		num_+=1
	return result_


def getAvailablePage(url_f):
	#从目录网页中获取可用的章节网址(初步处理)
	pre_(url_f)
	line_s=getLine('</a></li><li><a href="',(176,183),3)
	try:
		return getContent(line_s[1],'None_','None_',0)
	except:
		return getContent(line_s[0],'None_','None_',0)

def CombineUrl(basic_url,task_url):
	#结合Url
	return basic_url+task_url

def getCatalogue(url_f):
	#从目录网页中获取可用的章节网址(再处理)，返回可用网址列表
	result_=[]
	for i in apart(getAvailablePage(url_f).lstrip().replace('</a></li><li><a href="','█').replace('<li><a href="','█')+'█','█',0,0):
		try:
			#print(i)
			m_=i.index('█')
			#print(m_)
			n_=i.index('">')
			#print(n_)
			r_=i[m_+2:n_-5]
			C_=CombineUrl('http://www.tstdoors.com/',r_)
			result_.append(C_)
		except:pass
	return result_

def getMemu(url_f):
	#从目录网页中获取可用的目录网址，返回可用网址列表
	result_=[]
	pre_(url_f)
	a_=apart(getContent(getLine('<option value="',193,3)[0],'None_','None_',(0,0)).replace('<option value="','█')+'█','█',1,-1)
	del a_[0]
	for i_ in a_:
		m_=i_.index('.html')
		result_.append(CombineUrl('http://www.tstdoors.com/',i_[0:m_+5]))
	return result_
	
def Final_deal(url_f):
	#最终处理，获取所有可用章节网址
	result_=[]
	for i_ in getMemu(url_f):
		print('\033[32m载入目录>>\033[36m'+i_+'\033[0m')
		url_s=getCatalogue(i_)
		for m_ in url_s:
			print('\033[33m获取到章节>>\033[0m\033[34m'+m_+'.html\033[0m')
			result_.append(m_)
		print('\033[35m共获取到'+str(len(url_s))+'个可用网址\033[0m')
	return result_
	
def createSonUrl(basic_url,i_f):
	#生成网址中部分数值变化的新网址
	return basic_url+'_'+str(i_f)+'.html'
	
def urlTest(url_f):
	#测试网页是否可用(好像没什么用)
	try:
		requests.get(url_f)
		return True
	except:
		return False
		
def pageTest(url_f):
	#检索内容行中是否有'<br />'，即检测是否章节错误(错误章节内容行没有'<br />')
	pre_(url_f)
	try:
		line_=getLine('<div class="amiddle">',(),3)[0]
		con_=getContent(line_,'None_','None_',(0,0))
		if con_.find('<br />')==-1:
			return False
		else:
			return True
	except:
		return True
	
def sonPageJudge(basic_url):
	#判断章节分值是否可用(一段文字会被分成好几个分页，数量不均)
	print('\033[33m进行章节分支判断。\033[0m')
	i_=1
	print('\033[33m载入源页面：\033[0m'+'\033[34m'+basic_url+'.html\033[m')
	result=[]
	while True:
		url=createSonUrl(basic_url,i_)
		if pageTest(url)==False:
			print('\033[31m不可用>>>\033[0m'+'\033[34m'+url+'\033[0m')
			break
		else:
			print('\033[32m可用>>>\033[0m'+'\033[34m'+url+'\033[0m')
			result.append(url)
			i_+=1
	print('\033[33m共'+str(len(result))+'个页面通过测试。\033[0m')
	return result

def getSearchR(keyword):
	pre_('http://www.tstdoors.com/ar.php?keyWord='+keyword)
	for l_ in range(len(r_t)):
		try:
			r_t[l_]=r_t[l_].replace('<span class="s3"><a href="','')
		except:pass
	url_s=[]
	for t_ in getLine('<a href="/ldks/',0,10):
		url_s.append(r_t[t_].lstrip().replace('<a href="',''))
	#print(url_s)
	url_r=[]
	Titles_=[]
	try:
		for o_ in url_s:
			m_=o_.index('">')
			n_=o_.index('</a>')
			url_r.append(o_[0:m_])
			Titles_.append(o_[m_+2:n_].replace(':',''))
	except:pass
	#print(url_r)
#	print(Titles_)
	url_R=[]
	for o_ in url_r:
		url_R.append(CombineUrl('http://www.tstdoors.com',o_))
	#print(url_R)
	return url_R,Titles_
	
def searchR_display(keyword):
	con_=getSearchR(keyword)
	global research_
	if con_[0]==[]:
		print('\033[31m无检索结果！请重新检索！\033[0m')
		return False
	else:
		print('\033[35m检索到'+str(len(con_[0]))+'个电子书页面(最大检索数上限为10)\033[0m')
		#print(list(range(len(con_[0])))[3])
		for i_ in range(len(con_[0])):
			print('\033[33m'+str(i_)+'\033[36m.'+con_[1][i_]+'\033[0m')
		while True:
			try:
				input_=input('\033[32m>>输入编号("/rs"重新检索)：\033[33m')
				if int(input_) in range(0,len(con_[0])):
					research_=False
					return con_[0][int(input_)],con_[1][int(input_)]
				else:print('\033[31m>>超出范围！请重新输入！\033[0m')
			except:
				if input_=='/rs':
					research_=True
					break
				else:
					print('\033[31m错误！请重新输入')
		#print(input_)
		
	
#print(searchR_display('血'))

def Get(url_f,file):
	#主程序，获取标题与正文并写入指定文件中
	sss=open(file,'w+')
	print('\033[31m读取章节列表')
	url_s=Final_deal(url_f)
	print('\033[32m共获取到'+str(len(url_s))+'个章节页面')
	print('\033[31m开始获取内容')
	times_=1
	error_times=0
	for url_ in url_s:
		pre_(url_+'.html')
		m_=getLine('<meta name="keywords"',9,3)[0]
		#print(m_)
		content=getContent(m_,'content="','" />',(9,0))
		print('\033[32m成功获取到章节:\033[36m'+content+'\033[0m')
		content_a=''
		son_num=0
		sonUrlTable=sonPageJudge(url_)
		for m in sonUrlTable:
			son_num+=1
			pre_(m)
			content_d=str('    '+getContent(getLine('<br />',203,3)[0],'None_','None_',(0,0)).lstrip().replace('<div class="amiddle" >安卓、IOS版本请访问官网https://www.biqugeapp.co下载最新版本。如浏览器禁止访问，请换其他浏览器试试；如有异常请邮件反馈。</div>','').replace('<br />','\n').replace('<br /','\n'))
			#print(content_d)
			pre_view=content_d.lstrip()[0:10]+'...'
			print('\033[32m成功获取正文片段:\033[0m'+pre_view+'  \033[33m进度：'+str(son_num)+'/'+str(len(sonUrlTable))+'\033[0m')
			content_a=content_a+content_d
		content_f=content+'\n'+content_a+'\n'
		try:
			sss.writelines(content_f+'\n')
			print('\033[35m保存成功   \033[36m总进度：'+str(times_)+'/'+str(len(url_s))+'\033[31m(Error:'+str(error_times)+')\033[0m')
		except:
			print('\033[31m发生意外，保存失败\033[0m')
			error_times+=1
		times_+=1
		
	sss.close()
	

#print('\033[33m\n————————————\n爬虫程序结束\n————————————\n\033[0m')

Judgement=True
print('\033[36m进行执行方式选择：\n\033[33m输入"s"进行书籍检索\n输入"d"直接使用网址')
while Judgement:
	input__=input('\033[35m输入编号：\033[36m')
	if input__=='s':
		Judgement=False
		Judgement0=True
		while Judgement0:
			url__=searchR_display(input('\033[33m输入关键字：\033[34m'))
			if url__!=False and research_==False:
				Judgement0=False
				Judgement1=True
				while Judgement1:
					file__=input('\033[33m保存的文件(默认文件名为:'+url__[1]+'.txt)：\033[34m')
					if file__=='':
						Get(url__[0],url__[1]+'.txt')
					else:
						Get(url__[0],file__)
	elif input__=='d':
		Judgement=False
		Get(input('\033[33m最初的网址：\033[34m'),	input('\033[33m保存的文件：\033[34m'))