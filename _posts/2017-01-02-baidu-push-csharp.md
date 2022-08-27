---
title: baidu push c# 구현
categories: dev
tags: [baidu, push, c#]
---
# reference
- [http://push.baidu.com/doc/restapi/restapi](http://push.baidu.com/doc/restapi/sdk_developer)
- [http://push.baidu.com/doc/restapi/sdk_developer](http://push.baidu.com/doc/restapi/sdk_developer)

# 유의할 점
- baidu 의 push server 가 php 로 구현되어있는지 php 의 urlencode 를 구현해야 한다. php 의 urlencode 는 공백(%20)을 '+' 로 대체한다. 

```c#
TimeSpan t = DateTime.Now - new DateTime(1970, 1, 1);
int totalSeconds = (int)t.TotalSeconds;
string timestamp = totalSeconds.ToString();                

SortedDictionary<string, string> param = new SortedDictionary<string, string>();
param["apikey"] = _setting.ApiKey;
param["timestamp"] = timestamp;
param["channel_id"] = baiduNotification.ChannelId;
param["msg"] = baiduNotification.Msg;

if (baiduNotification.MsgType.HasValue)
{
	param["msg_type"] = baiduNotification.MsgType.Value.ToString();
}

if (baiduNotification.DeployStatus.HasValue)
{
	param["deploy_status"] = baiduNotification.DeployStatus.Value.ToString();
}                

string parameterString = "";

foreach (KeyValuePair<string, string> pair in param)
{
	parameterString += pair.Key + "=" + pair.Value;
}

string baseString = _setting.Method + _setting.Url + parameterString + _setting.SecretKey;

string escapedDataString = Uri.EscapeDataString(baseString);
string urlencodedString = escapedDataString.Replace("%20", "+");

string hashedString = "";
using (MD5 md5 = MD5.Create())
{
	byte[] data = md5.ComputeHash(Encoding.UTF8.GetBytes(urlencodedString));

	StringBuilder builder = new StringBuilder();

	for (int i = 0; i < data.Length; ++i)
	{
		builder.Append(data[i].ToString("x2"));
	}

	hashedString = builder.ToString();
}

param["sign"] = hashedString;

string content = "";                
foreach (KeyValuePair<string, string> pair in param)
{
	if (0 < content.Length)
		content += "&";

	content += pair.Key + "=" + pair.Value;
}

HttpClient client = new HttpClient();                    
client.DefaultRequestHeaders.UserAgent.TryParseAdd("BCCS_SDK/3.0 (Darwin; Darwin Kernel Version 14.0.0: Fri Sep 19 00:26:44 PDT 2014; root:xnu-2782.1.97~2/RELEASE_X86_64; x86_64) PHP/5.6.3 (Baidu Push Server SDK V3.0.0 and so on..) cli/Unknown ZEND/2.6.0");

StringContent stringContent = new StringContent(content, Encoding.UTF8, "application/x-www-form-urlencoded");
HttpResponseMessage response = client.PostAsync(_setting.Url, stringContent).Result;
```
