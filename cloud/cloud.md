# Cloud Computing

On demand delivery of IT resources over the internet with pay-as-you-go pricing

# Cloud


In a cloud-based deployment model, you have the flexibility to migrate your existing resources to the cloud, design and build new applications within the cloud environment, or use a combination of both.



For instance, a company might migrate data resources to the cloud, then develop an application comprised of virtual servers, databases, and networking components entirely hosted in the cloud.

## On-premises


Deploying resources on premises using virtualization and resource management tools does not provide many of the benefits of cloud computing. However, it is sometimes sought for its ability to provide dedicated resources and low latency.



In most cases this deployment model is the same as legacy IT infrastructure while using application management and virtualization technologies to try increasing resource utilization.

## Hybrid


In a hybrid deployment, cloud-based resources and on-premises infrastructure work together. This approach is ideal for situations where legacy applications must remain on premises due to maintenance preferences or regulatory requirements.



For instance, a company might choose to retain certain regulated legacy applications on-premises while using cloud services for advanced data processing and analytics.



Multi-cloud deployments can also be considered hybrid deployments.

## Key benefits of the AWS Cloud
The six key benefits of the AWS Cloud are as follows.

1. By using the AWS Cloud, businesses can transition from fixed investments to variable costs. With variable costs, customer expenses are better aligned with actual usage, thus creating more financial flexibility.
2. Like buying a product in bulk can result in lower prices per unit, the vast global infrastructure of AWS can result in lower costs for customers. This means that AWS can be used by many organizations, from small startups to major corporations. Businesses big and small can access advanced technologies that were previously only accessible to large enterprises.
3. Customers can dynamically scale AWS Cloud resources up or down based on real-time demand. This means businesses can achieve optimal performance without provisioning more or less infrastructure than they need.
4. With the cloud, businesses can rapidly deploy applications and services, accelerating time to market and facilitating quicker responses to changing business needs and market conditions.
5. The AWS Cloud eliminates the need for businesses to invest in physical data centers. This means customers aren't required to spend time and money on utilities and ongoing maintenance. With AWS taking care of the physical infrastructure of the cloud, customer resources can be reallocated to more strategic initiatives.
6. Businesses don't need to set up their own infrastructure to expand internationally. AWS provides a robust global infrastructure that customers can use to deploy applications and services across multiple areas in minutes.

## AWS Regions and Availability Zones
AWS Global Infrastructure consists of physical locations around the world that contain groups of data centers. To learn more about the design of AWS Regions and Availability Zones, choose each of the following two numbered markers.

1. AWS Regions

AWS Regions are physical locations around the world that contain groups of data centers. These groups of data centers are called Availability Zones. Each AWS Region consists of a minimum of three physically separate Availability Zones within a geographic area.

2. Availability Zones

An Availability Zone consists of one or more data centers with redundant power, networking, and connectivity. Regions and Availability Zones are designed to provide low-latency, fault-tolerant access to services for users within a given area.

High Availability - Applications stay running and accesiblw with minimum downtime
Fault Tolerance - Designign a system to continue to operate even if multiple components fail

Building resilience in every layer so no one layer will bring down the whole system

# The AWS Shared Responsibility Model

The AWS Shared Responsibility Model is a concept designed to help AWS and customers work together to create a secure, functional cloud environment. In this lesson, you learn about the components of the AWS Shared Responsibility Model. With a clear understanding of cloud computing responsibilities, organizations can better navigate the complexities of cloud security.


AWS is responsible for the security of the cloud 
Customer - responsible for security in the cloud 

Customer Responsibilty
- Customer Data & Client side data encryption

Customer or AWS Responsibilty
- Server side Encryption 
- Network Traffic Protection
- Platform / Application Management
- OS, network , firewall config

AWS Responsibility
- S/w for compute, storage, databse and networking
- H/w AWS global infra

Cloud computing can be defined as the on-demand delivery of IT resources over the internet with pay-as-you-go pricing. This answer accurately defines cloud computing and directly addresses the finance manager’s concern about fixed costs.

A Region is a physical location around the world that contains multiple, isolated data centers. An Availability Zone consists of one or more discrete data centers, each with independent power, networking, and connectivity.

# Introduction to Amazon EC2

Compute refers to the processing power needed to run applications, manage data, and perform calculations. In the cloud, this power is available on-demand. You can access it remotely without owning or maintaining physical hardware. Essentially, compute in the cloud means creating virtual machines with a cloud provider to run applications and tasks over the internet.

Raw compute capcity to host applications and provide power that business needs

EC2
- cost effectivve 
- flexible
- quick


# Challenges of on-premises resources
- Imagine that you're responsible for designing your company's infrastructure to support new websites. With traditional on-premises resources, you must purchase hardware upfront, wait for delivery, and handle installation and configuration. This process is time-consuming, costly, and inflexible because you're locked into a specific capacity that might not align with changing demands.

# Benefits of using Cloud Resources
In contrast, with Amazon EC2, you can quickly launch, scale, and stop instances based on your needs without the delays and upfront costs associated with traditional on-premises resources.

In Ec2 you only pay for running instances not stopped instances

EC2 instances are virtual machines that share an underlying physical host machine with mulitple other instances

Multi Tenancy - Sharing underlying hardware between virtual machines

In a multi tenant environment you need to ensure that each VM is isolated from each other but is still able to share resources provided by the host

Job or resource sharing and isolation is being done by a <hypervisor> which is running on the host machine

EC2 - AWS manages the underlying host, hyper visor and isolation from instance to instance

A hypervisor is software, firmware, or hardware that creates and runs virtual machines (VMs) on a single physical host machine. It divides physical resources—such as CPU, memory, storage, and networking—and allocates them to isolated guest operating systems.

Ec2 instances are resizable  can start with a small instance and then proceed to bigger ones
- You also decide what type of request can be made to your server and if they are publically or privately accesible

Vertical Scaling -> giving the existing machine more CPU and power 

# Launching a EC2 Instance

- Start by selecting an AMI(Amazon Machine Image) which defines the OS and can include additional s/w.  You can also choose instance type which determines underlying h/w resources.
-   
