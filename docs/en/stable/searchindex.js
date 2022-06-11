Search.setIndex({docnames:["api/api","api/io","api/parse_functions","api/parsers","api/tests","api/transformers","changelog","contributing","getting-started","index","license"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":4,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,"sphinx.ext.intersphinx":1,sphinx:56},filenames:["api/api.rst","api/io.rst","api/parse_functions.rst","api/parsers.rst","api/tests.rst","api/transformers.rst","changelog.rst","contributing.rst","getting-started.rst","index.rst","license.rst"],objects:{"bite.io":[[1,1,1,"","BytesBuffer"],[1,1,1,"","ParserBuffer"],[1,1,1,"","StreamReaderBuffer"]],"bite.io.BytesBuffer":[[1,2,1,"","at_eof"],[1,2,1,"","get"]],"bite.io.ParserBuffer":[[1,2,1,"","at_eof"],[1,2,1,"","get"]],"bite.io.StreamReaderBuffer":[[1,2,1,"","at_eof"],[1,2,1,"","drop_prefix"],[1,2,1,"","get"]],"bite.parse_functions":[[2,3,1,"","parse_bytes"],[2,3,1,"","parse_incremental"]],"bite.parsers":[[3,1,1,"","And"],[3,1,1,"","CaselessLiteral"],[3,1,1,"","CharacterSet"],[3,1,1,"","Combine"],[3,1,1,"","Counted"],[3,1,1,"","CountedParseTree"],[3,1,1,"","FixedByteCount"],[3,1,1,"","Forward"],[3,1,1,"","Literal"],[3,1,1,"","MatchFirst"],[3,1,1,"","Not"],[3,1,1,"","OneOrMore"],[3,1,1,"","Opt"],[3,1,1,"","ParseError"],[3,1,1,"","ParsedBaseNode"],[3,1,1,"","ParsedCounted"],[3,1,1,"","ParsedLeaf"],[3,1,1,"","ParsedList"],[3,1,1,"","ParsedMatchFirst"],[3,1,1,"","ParsedNil"],[3,1,1,"","ParsedNode"],[3,4,1,"","ParsedOneOrMore"],[3,4,1,"","ParsedOpt"],[3,4,1,"","ParsedRepeat"],[3,4,1,"","ParsedZeroOrMore"],[3,1,1,"","Parser"],[3,1,1,"","Repeat"],[3,1,1,"","TrailingBytesError"],[3,1,1,"","UnmetExpectationError"],[3,1,1,"","ZeroOrMore"]],"bite.parsers.And":[[3,2,1,"","parse"]],"bite.parsers.CaselessLiteral":[[3,2,1,"","parse"]],"bite.parsers.CharacterSet":[[3,2,1,"","parse"]],"bite.parsers.Combine":[[3,2,1,"","parse"]],"bite.parsers.Counted":[[3,2,1,"","parse"]],"bite.parsers.CountedParseTree":[[3,4,1,"","count_expr"],[3,4,1,"","counted_expr"],[3,5,1,"","end_loc"],[3,5,1,"","start_loc"]],"bite.parsers.FixedByteCount":[[3,2,1,"","parse"]],"bite.parsers.Forward":[[3,2,1,"","assign"],[3,2,1,"","parse"],[3,4,1,"","parser"]],"bite.parsers.Literal":[[3,2,1,"","parse"]],"bite.parsers.MatchFirst":[[3,2,1,"","parse"]],"bite.parsers.Not":[[3,2,1,"","parse"]],"bite.parsers.OneOrMore":[[3,2,1,"","parse"]],"bite.parsers.Opt":[[3,2,1,"","parse"]],"bite.parsers.ParsedBaseNode":[[3,4,1,"","name"],[3,4,1,"","parse_tree"]],"bite.parsers.ParsedCounted":[[3,5,1,"","end_loc"],[3,4,1,"","name"],[3,4,1,"","parse_tree"],[3,5,1,"","start_loc"],[3,5,1,"","values"]],"bite.parsers.ParsedLeaf":[[3,4,1,"","end_loc"],[3,4,1,"","name"],[3,4,1,"","parse_tree"],[3,4,1,"","start_loc"],[3,5,1,"","values"]],"bite.parsers.ParsedList":[[3,5,1,"","end_loc"],[3,4,1,"","loc"],[3,4,1,"","name"],[3,4,1,"","parse_tree"],[3,5,1,"","start_loc"],[3,5,1,"","values"]],"bite.parsers.ParsedMatchFirst":[[3,4,1,"","choice_index"],[3,5,1,"","end_loc"],[3,4,1,"","name"],[3,4,1,"","parse_tree"],[3,5,1,"","start_loc"],[3,5,1,"","values"]],"bite.parsers.ParsedNil":[[3,5,1,"","end_loc"],[3,4,1,"","loc"],[3,4,1,"","name"],[3,5,1,"","parse_tree"],[3,5,1,"","start_loc"],[3,5,1,"","values"]],"bite.parsers.ParsedNode":[[3,5,1,"","end_loc"],[3,5,1,"","name"],[3,5,1,"","parse_tree"],[3,5,1,"","start_loc"],[3,5,1,"","values"]],"bite.parsers.Parser":[[3,2,1,"","parse"]],"bite.parsers.Repeat":[[3,2,1,"","parse"]],"bite.parsers.ZeroOrMore":[[3,2,1,"","parse"]],"bite.tests":[[4,1,1,"","MockReader"]],"bite.tests.MockReader":[[4,2,1,"","at_eof"],[4,2,1,"","read"],[4,2,1,"","readexactly"],[4,2,1,"","readline"],[4,2,1,"","readuntil"]],"bite.transformers":[[5,1,1,"","Group"],[5,1,1,"","ParsedTransform"],[5,1,1,"","Suppress"],[5,1,1,"","Transform"],[5,1,1,"","TransformValues"]],"bite.transformers.Group":[[5,2,1,"","parse"]],"bite.transformers.ParsedTransform":[[5,5,1,"","end_loc"],[5,4,1,"","name"],[5,4,1,"","parse_tree"],[5,5,1,"","start_loc"],[5,4,1,"","transform"],[5,5,1,"","values"]],"bite.transformers.Suppress":[[5,2,1,"","parse"]],"bite.transformers.Transform":[[5,2,1,"","parse"]],"bite.transformers.TransformValues":[[5,2,1,"","parse"]],bite:[[1,0,0,"-","io"],[2,0,0,"-","parse_functions"],[3,0,0,"-","parsers"],[5,0,0,"-","transformers"]]},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","function","Python function"],"4":["py","attribute","Python attribute"],"5":["py","property","Python property"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:function","4":"py:attribute","5":"py:property"},terms:{"0":[3,5,8,9],"01":9,"012":3,"0123456789":[2,3,5,8],"01234567890":3,"012345689":3,"02":9,"06":9,"0x7f":3,"0x9f":3,"1":[1,2,3,4,5,8,9],"10":6,"11":9,"123":8,"1234":2,"12345":3,"13":9,"2":[2,3,5,8,9],"2021":10,"2022":9,"21":8,"23":[2,5],"29":9,"3":[3,5,8,9],"30":9,"3abcd":3,"4":[3,8],"4000":8,"42":[2,5],"4321":2,"45":8,"5":[3,8],"6":8,"63":8,"65":5,"67":8,"7143":8,"89":8,"abstract":3,"byte":[1,2,3,4,6,8,9],"case":[3,9],"class":[0,1,3,4,5,8],"default":[3,8],"do":[3,8,10],"export":9,"final":8,"function":[5,8,9],"import":[0,2,3,5,6,8],"int":[1,3,5,8],"new":1,"return":[0,1,2,3,5,6,8],"static":[1,4],"true":[1,2,3,5],"try":[3,5,8],"while":[8,9],A:[1,2,3,5,8,9,10],AND:10,AS:10,And:[0,3],BE:10,BUT:10,Be:8,By:[3,8],FOR:10,For:[2,7,8],IN:10,IS:10,If:[1,2,3,5],In:[8,9],It:[3,8,9],NO:10,NOT:10,Not:[0,3,4,6],OF:10,OR:10,On:8,Such:3,THE:10,TO:10,The:[0,1,2,3,4,6,8,9,10],There:[7,8],These:0,WITH:10,Will:3,_:2,__main__:8,__name__:8,aa:3,aaa:3,ab:[2,3],abc:3,abilitii:9,abl:3,abov:10,acc:8,accept:8,access:[3,5],accord:8,action:10,actual:3,ad:1,add:8,addit:[8,9],addr:8,adher:6,after:8,ahead:[0,3,6],alia:3,all:[0,1,2,3,5,6,8,9,10],allow:[0,2,3,5,6,7,8,9],alreadi:1,also:[0,3,8,9],altern:8,alwai:[1,3],an:[1,2,3,6,7,8,9,10],ani:[3,10],api:9,appli:[0,3],applic:3,approach:9,ar:[0,1,2,3,6,7,8,9],area:[7,9],arg:[1,3,5],aris:10,arrai:8,ascii:8,assign:[3,5,8],associ:10,assum:2,async:[1,2,3,4,5,8],asyncgener:2,asynchron:[2,9],asyncio:[1,2,3,4,5,6,8,9],at_eof:[1,4],at_loc:3,attribut:8,author:10,auto:8,avail:1,await:[2,8],b:[2,3,4,5,8],base:[3,6],basic:[8,9],bb:3,becaus:[1,3,5,8],becom:1,been:1,befor:7,behavior:6,below:6,besid:[0,3,8],best:7,better:9,bite:[0,6,7,8],block:[1,9],bool:[1,2,3,4],both:3,bracket:[0,8],buf:[3,5],buffer:[1,3,5],build:9,bytesbuff:[1,6],c:10,call:[2,3,8],callabl:[3,5],can:[0,2,3,8,9],cancon:3,canon:3,care:8,caselessliter:3,caus:3,chain:8,chang:7,changelog:9,characterset:[2,3,5,8],charg:10,charset:3,check:8,child:[3,5,8],children:[3,5,8],choic:3,choice_index:[3,8],claim:10,close:[6,8],combin:[2,3,5,8,9],come:8,command:8,common:[3,6],complet:[1,2,5,7,8],concret:[3,8],condit:10,connect:10,consist:8,constitut:8,construct:[1,8,9],constructor:3,consum:[2,3,5],contain:[1,8],contract:10,contrast:1,contribut:9,conveni:9,convert:3,copi:10,copyright:10,core:6,correspond:8,could:[6,9],count:3,count_expr:3,count_pars:3,counted_expr:3,counted_parser_factori:3,countedparsetre:3,creat:[0,3],cumbersom:8,current:[7,9],custom:[6,8],damag:10,dar202:[1,3,5],data:[1,2,4],deal:10,debug:9,declar:[0,3,6,8],def:[2,5,8],defin:[0,2,3,8],definit:[3,8],delimited_list:5,denot:8,descent:9,desir:0,detect:6,determin:8,develop:7,differ:5,digit:[3,8],directli:0,discuss:[7,8],distribut:10,dmarc:9,document:[6,8,10],doe:[3,5],done:8,drain:8,drop:1,drop_prefix:1,e:[1,3,8],each:[2,3,8],easier:6,effort:7,either:[0,3],element:[3,8],elif:8,ellipsi:[0,3],els:8,emit:8,empti:3,encod:8,end:[1,3,5],end_loc:[3,5,8],entri:0,eof:6,equal:3,equival:[3,6,8],error:[3,6,9],eval_product:8,eval_sum:8,evalu:8,even:1,event:10,exact:3,exactli:8,exampl:[2,3,5,8],except:[2,3],exclus:[3,5,8],exhibit:9,exist:8,expect:[3,5,6],explicit:6,explicitli:3,exponenti:9,expr:[3,6,8],express:[3,8,9,10],extens:7,extent:8,f:8,fact:9,fail:[2,3],fals:[2,3],far:8,field:3,file:[1,6,10],find:8,first:[0,1,3,9],fit:10,fix:3,fixedbytecount:3,flat:[5,8],flatten:[3,6],focu:7,follow:[0,3,8,10],form:[3,7],format:6,forward:[3,6,8],found:[1,3],four:8,free:10,from:[0,1,2,3,5,6,8,9,10],fundament:[0,7,9],furnish:10,further:8,g:[1,3],gener:[0,3,8,9],get:[1,3,6,9],getsocknam:8,github:[7,9],give:8,given:[0,2,3,5,8],go:1,gosmann:10,grammar:[0,2,8,9],grant:10,group:[5,6,8],ha:[1,6,8],hand:8,handi:8,handle_connect:8,happen:8,have:[1,8,9],help:3,here:[0,8],herebi:10,higher:9,holder:10,how:[1,3],howev:[1,3,8,9],i:[1,3,7,8,9],ideal:7,imap:9,implemen:0,implement:[1,3,4,6,9],implementor:3,impli:10,improv:[7,9],includ:10,incom:[2,8],increment:[2,9],index:[0,1,3,5,9],indic:2,individu:[3,8],infinit:8,infinitli:3,inform:8,initi:6,input:[0,2,3,4,5,8,9],input_buf:4,insensit:3,insert:8,instal:[6,9],instanc:0,instead:5,integ:[0,1,3],integer_token:[2,5],intend:0,interchang:8,interfac:4,introduc:[5,6,9],invert:[3,5],io:[0,3,5],issu:7,item:[5,9],iter:[3,5,6,8],its:8,itself:[3,8],jan:10,join:8,just:[5,6],keep:6,kei:1,kind:10,known:9,kwarg:[1,3],kwd:[3,5],lambda:[3,5,8],larger:7,last:[2,3],later:6,lead:6,leaf:[3,8],least:3,leav:3,left:[3,8],len:8,length:3,let:8,level:9,liabil:10,liabl:10,librari:9,licens:9,like:[3,9],limit:10,line:[2,8],list:[0,3,7],liter:[2,3,5,8],loc:[3,5],localhost:8,locat:[2,3,5],longer:6,look:[0,3,6,7,8],lot:7,magic:8,mai:1,main:[0,2,7,8],make:[3,9],mani:[0,3,8,9],match:[2,3,5,6,8],matchfirst:[0,3],mathemat:8,matter:8,max_repeat:3,maximum:[3,8],me:7,memori:2,merchant:10,merg:[6,10],messag:9,method:[1,3,8],metric:9,might:[7,8],min_repeat:3,minimum:8,minimun:3,miport:6,mit:10,mock:4,mockread:[4,6],modifi:10,modul:9,more:[3,6,7,8],most:[2,3,8,9],much:1,multipl:[3,8],must:[0,1,2,3],my:[7,9],n1234:2,n23:2,n:[1,2,4,8],name:[3,5,8],nc:8,necessarili:7,need:[3,5,7,8,9],neg:[0,3,6],netcat:8,network:9,never:[1,6],next:8,node:[3,5,6,8,9],non:[0,3],none:[2,3,5,8],noninfring:10,noqa:[1,3,5],notabl:6,notat:[0,8],note:[2,8],notic:10,now:6,number:[3,8],object:[1,2,3,4],obtain:[3,10],off:6,often:8,one:[3,6,8],oneormor:3,onli:[3,5,8,9],onlyvalu:6,open_connect:2,open_read:2,oper:[0,3,8,9],opt:[3,6,8],option:[3,5],order:[3,8],other:[3,8,9,10],otherwis:[2,3,5,6,10],out:[8,9,10],overflow:3,overrid:3,overridden:3,packag:0,packrat:9,page:9,paramet:[1,2,3,4,5],pars:[2,3,5,6,9],parse_al:2,parse_byt:[2,3,5,6,8],parse_funct:0,parse_increment:[2,6,8],parse_tre:[3,5,8],parsed_lin:2,parsedbasenod:3,parsedcount:3,parsedleaf:[3,8],parsedlist:3,parsedmatchfirst:[3,8],parsednil:3,parsednod:[0,2,3,5],parsednot:5,parsedoneormor:3,parsedopt:3,parsedrepeat:3,parsedtransform:5,parsedzeroormor:3,parseerror:[2,3],parsenod:6,parser:[1,2,5,6,7],parserbuff:[1,3,5],part:7,particular:10,pass:[3,5],past:1,peg:9,perform:9,permiss:10,permit:10,person:10,pip:8,pleas:7,point:0,portion:10,posit:[0,3],possibl:[1,3,8],preced:8,prevent:6,previou:8,print:[2,3,5,8],produc:[3,5,6],product:8,project:6,properti:[3,5,6],protocol:[0,1,9],provid:[1,2,3,4,5,10],publish:10,pull:7,pure:9,purpos:10,put:[7,8],pypars:9,python:[6,9],queri:8,r:[2,8],rais:[2,3,5,6,8],rang:[1,3,8],react:7,read:[1,2,3,4],reader:[1,2,6,8],readexactli:4,readlin:4,readuntil:4,recent:[2,3],recogniz:9,recurs:[3,6,8,9],refer:[8,9],rel:2,releas:6,relev:8,remov:8,renam:6,repeat:[3,8],repeatedli:3,repetit:3,repositori:9,repres:[3,5],represent:8,request:[1,7,8],requir:3,restrict:10,result:[2,3,5,9],retain:8,right:[8,10],rule:[3,6,8],run:[2,3,5,8],s:3,search:9,section:8,see:6,segmend:[3,5],segment:[2,3],sell:10,semant:6,sent:6,separ:4,sequenc:[0,3,8],serv:8,serve_forev:8,server:8,set:[2,3,8,9],shall:10,should:[1,9],side:8,similar:9,simpl:[8,9],singl:[1,3,8],slice:1,smaller:1,so:[8,10],sock:8,socket:8,softwar:10,some:[7,8],someth:[0,3],sometim:8,somewhat:8,sourc:[1,2,3,4,5],special:0,specifi:8,stack:3,stall:6,start:[2,3,5,9],start_loc:[3,5,8],start_serv:8,still:[7,9],store:8,str:[3,5,8],stream:[1,2,6,9],streamread:[1,2,4,6],streamreaderbuff:1,string:[3,9],structur:[0,5,9],sub:[6,8],subject:10,sublicens:10,subsequ:3,substanti:10,succe:[0,3],success:[3,5,8],sum:[5,8],sum_valu:5,support:9,suppos:3,suppress:[2,5,8],syntax:3,t:[2,3,5],take:[5,8,9],test:[0,8],than:[1,8],thei:8,them:7,thi:[1,3,5,6,8,9,10],though:8,time:[1,3,7],togeth:8,token:8,tort:10,traceback:[2,3],trail:[2,3],trailingbyteserror:[2,3],transform:[6,8],transformvalu:[5,6,8],transfrom:5,treat:[1,3],tree:[2,3,5,8,9],tupl:[3,5,8],type:[3,9],typic:9,u:8,unabl:1,unexpect:6,union:1,unlimit:[0,3],unmetexpectationerror:[3,5],unpars:2,unsuccess:[3,5],until:[3,8],unwieldi:8,us:[1,3,9,10],usag:6,v:[2,3,5,8],valu:[2,3,5,6,8],valueerror:8,variant:3,variou:7,version:6,via:4,vin:5,vout:5,wa:[1,2,3,5],wai:8,wait:6,want:8,warranti:10,we:8,welcom:7,what:[3,5,8],when:[3,8],where:[3,5,7,8],whether:[1,10],which:[3,5,6,8,9],whole:[3,8],whom:10,without:[6,8,10],work:[1,8],worst:9,would:[1,9],write:8,write_eof:8,writer:8,wrote:9,x:[0,3],y:[0,3],yet:[1,9],yield:2,you:[3,8],your:9,zero:[3,8],zeroormor:3},titles:["API reference","bite.io module","bite.parse_functions module","bite.parsers module","bite.tests module","bite.transformers module","Changelog","Contributing","Getting started","Welcome to bite-parser","License"],titleterms:{"0":6,"01":6,"02":6,"06":6,"1":6,"11":6,"13":6,"2":6,"2022":6,"29":6,"3":6,"30":6,"byte":0,"function":0,"import":9,ad:6,api:0,asynchron:8,bite:[1,2,3,4,5,9],chang:6,changelog:6,combin:0,concret:0,content:9,contribut:7,document:9,first:8,fix:6,get:8,implement:8,indic:9,instal:8,introduc:8,io:1,licens:10,link:9,modul:[0,1,2,3,4,5],node:0,pars:[0,8],parse_funct:2,parser:[0,3,8,9],refer:0,remov:6,repetit:0,result:8,start:8,stream:8,structur:8,tabl:9,test:4,transform:[0,5],tree:0,us:8,valu:0,welcom:9,your:8}})