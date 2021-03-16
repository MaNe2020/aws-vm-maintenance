# Dashboard documentation / AWS Compliance
 
- [Dashboard documentation / AWS Compliance](#dashboard-documentation--aws-compliance)
  - [Details of mandatory tags to be added to Instance](#details-of-mandatory-tags-to-be-added-to-instance)
  - [Dashboards for AWS Monitoring](#dashboards-for-aws-monitoring)


## Details of mandatory tags to be added to Instance

All instances should be tagged with following mandatory tags:

    - Name : *Name of Instance*
  
    - Owner : *Owner of Instance*

    - Team  : *K8/GW/Sales* Team for which instance is created

    - Scope :  Purpose of creation of instance. In case Instances is marked as No, a valid justification to keep instance running

    - Delete: *Yes/No* (Any other values are treated as non-compliant)

* Any instance without any above mandatory tags is treated as non-compliant and will be stopped automatically. Be noted that Tag Keys and Values are case sensitive
* All Instances that are not approved for running daily will be stopped automatically. To request an instance not to be stopped, reach out to #aws-vm-maintenance over slack
* If an instance is Non-compliant it gets stopped automatically. Any instance which remains non-compliant for more than 4 days will be terminated



## Dashboards for AWS Monitoring

* Administrators will be provided with access to Kibana dashboards which will provide information on realtime metrics related to various scenarios. Few examples includes: 
    - No of instances running per region
    - No of instances created on given day per region
    - No of instances marked as Delete:No per region

![image (2)](https://user-images.githubusercontent.com/76431508/108069641-45842880-706c-11eb-9b19-c048ef57bd2f.png)
 
