# Auto stopping of Instances over weekend:

Event bridge rule: https://eu-west-1.console.aws.amazon.com/events/home?region=eu-west-1#/eventbus/default/rules/stopInstancesWeekend
Lambda function: https://eu-west-1.console.aws.amazon.com/lambda/home?region=eu-west-1#/functions/stopInstancesWeekend


- Once Instance id list is updated in Spreadsheet, list of instance ids to be updated in instances.txt present in current folder folder
 ```
i-00e661ddf9010ab9f:icapdemo
i-07d1cbb592c26b8b7:filedropdemo 
i-07098cdaf17dda77b:sharepointproxy
i-04820952d73b4e222:glasswallproxy
i-09a02b16dd9e20952:GWEngProxy
i-014cd65aec4e3ed48:OwaspProxy
i-0badf3228c7723217:govUKProxy
i-0d72ceba0317145d7:gmhscProxy
i-04ac04d00e7327538:ICAP-Test-DP
i-0e0971ea7232b3ebc:sharepointplugin
i-07a4d95cac15e0a87:PatrickMinio
i-0c069423444c85fdc:alertbot
  ```
- Current cron configured in Event brdige rule to auto trigger lambda function at 8 PM UK every day
```
0 20 ? * * *
```
The same has to be updated incase of any changes in schedule 