#!/usr/bin/php
<?php
include '/Users/yangbingxi/www/code.php';
$opts = array(
	'http'=>array(
		'method'=>"GET",
		'header'=> "Host:	www.520tingshu.com\r\n".
				"User-Agent:	Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:31.0) Gecko/20100101 Firefox/31.0\r\n".
				"Accept:	text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n".
				"Accept-Language:	zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3\r\n".
				"Accept-Encoding:	gzip, deflate\r\n".
				"Referer:	http://www.520tingshu.com/down/?11502-0-0.html\r\n".
				'Cookie:	MAX_HISTORY={video:[{"name":"\u4E8E\u516C\u6848","link":"http://www.520tingshu.com/book/book11502.html","pic":"/pic/uploadimg/2014-9/20149197104725122.jpg"},{"name":"\u9EC4\u6CB3\u53E4\u4E8B","link":"http://www.520tingshu.com/book/book11751.html","pic":"/pic/uploadimg/2014-10/20141031812543930.jpg"}]}; bdshare_firstime=1426436559317; Hm_lvt_8d4e1ce243d40f33c6ca050451a189f2=1426436562,1426786484; CNZZDATA3830836=cnzz_eid%3D1926779155-1426432488-%26ntime%3D1426783939; ASPSESSIONIDSSQTDCQD=EANNDKHBBFGBIGOPGGGJEEHP; Hm_lpvt_8d4e1ce243d40f33c6ca050451a189f2=1426786484; hm_t_vis_54806=0\r\n'.
				"Connection:	keep-alive\r\n",
		'follow_location' => false
	)
);

$context = stream_context_create($opts);
$file = file_get_contents('http://www.520tingshu.com/down1/tudou.asp?id=207080894', false, $context);

file_put_contents('tmp.txt', $file);
$xmldoc = new DOMDocument();
$xmldoc->loadHTMLFile('tmp.txt');
$xpathvar = new Domxpath($xmldoc);
$queryResult = $xpathvar->query('//a/@href');
foreach($queryResult as $result){
	$url = $result->textContent;
}

$data = file_get_contents($url);
file_put_contents('1.f4v', $data);

