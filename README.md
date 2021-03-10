# Auto stopping of Instances over weekend:

Event bridge rule: https://eu-west-1.console.aws.amazon.com/events/home?region=eu-west-1#/eventbus/default/rules/stopInstancesWeekend
Lambda function: https://eu-west-1.console.aws.amazon.com/lambda/home?region=eu-west-1#/functions/stopInstancesWeekend

Source list for instances: https://docs.google.com/spreadsheets/d/1b_HWkmbrnsjtzehzzuK7Wdx0gF0h6RMt-hwJ36MTRfc/edit?usp=sharing

- Once Instance id list is updated in Spreadsheet, list of instance ids to be updated in Lambda function source code. Once lambda function code is updated, `Deploy` button to be clicked. `Test` button should NOT be clicked as it invokes lambda function and will stop instances.
 ```
    prodInstancesList = ['i-00e661ddf9010ab9f', 'i-07d1cbb592c26b8b7', 'i-07098cdaf17dda77b',
    'i-04820952d73b4e222','i-09a02b16dd9e20952','i-014cd65aec4e3ed48','i-0badf3228c7723217',
    'i-0d72ceba0317145d7']
  ```
- Current cron configured in Event brdige rule to auto trigger lambda function at 7 PM UK every Friday
```
0 19 ? * FRI *
```
The same has to be updated incase of any changes in schedule 