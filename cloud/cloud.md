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


# Connect to the instance
You can connect to an EC2 instance in various ways. Applications can interact with services running on the instance over the network.

Users or administrators can connect using SSH for Linux instances or Remote Desktop Protocol (RDP) for Windows instances. Alternatively, AWS services like AWS Systems Manager offer a secure and simplified method for accessing instances.

# Use the instance
After you are connected to the instance, you can begin using it to run commands, install software, add storage, organize files, and perform other tasks.

Amazon EC2 offers a broad range of instance types, each tailored to meet specific use case requirements. These instances come with varying combinations of CPU, memory, storage, and networking capabilities, so you can choose the right mix of resources to optimize performance for your applications.

Different types of instances solve different purposes
Instance types are grouped by instance families which offer varying combinaitons of CPU , storage, and network capacity

- General Purpose

balanced cmopute, meeory and network resources
ideal fro webservers and ocde repositories

- Compute Optimized
Gaming servers , High performance computing, ML tasks

- Memory Optimized 
Fast perofrmance for workload that process large data sets in memory

- Accelerated Computing
Accelerated computing instances use hardware accelerators, like graphics processing units (GPUs), to efficiently handle tasks, such as floating-point calculations, graphics processing, and machine learning.

- Storage Optimized
Storage optimized instances are designed for workloads that require high performance for locally stored data, such as large databases, data warehousing, and I/O-intensive applications.


# How to Provision AWS Resources

All interactions with services are powered by APIs. You can access these APIs through three primary methods: the AWS Management Console, the AWS CLI, or the AWS SDK. Let's review these methods.

- The AWS Management Console is a web interface for managing AWS services, offering quick access to services, search functionality, and simplified workflows. With the mobile app, you monitor resources, view alarms, and check billing, supporting multiple logged-in identities at once.


Good for: Users who prefer a visual, easy-to-use interface for managing and configuring AWS services

# AWS CLI
With the AWS CLI, you manage multiple AWS services directly from the command line across Windows, macOS, and Linux. You can automate tasks through scripts, such as launching EC2 instances.

Good for: Advanced users and developers who need to automate tasks, script actions, and manage AWS resources efficiently from the command line
# AWS SDK
The AWS SDK simplifies integrating AWS services into your applications by providing APIs for various programming languages. AWS offers documentation and sample code for languages like C++, Java, and .NET to help you get started.



Good for: Developers looking to integrate AWS services into their applications using language-specific APIs


# Compute and shared responsibility

An unmanaged service like Amazon EC2 requires you to perform all of the necessary security configuration and management tasks. When you deploy an EC2 instance, you are responsible for configuring security, managing the guest operating system (OS), applying updates, and setting up firewalls (security groups). 

The customer is responsible for configuring, securing, and managing the operating system, networking, and applications on their EC2 instances.

To launch an EC2 instance for a web server, configure the AMI to define the operating system and software; select the instance type to allocate CPU, memory, and storage; and set up storage options, including the type and size of the volume.Load balancing, permissions, and instance termination behavior are not required when launching a basic Amazon EC2 web server.

An AMI is a pre-configured virtual machine image that contains the operating system, application server, and applications. This helps to launch EC2 instances quickly with the desired software and settings.


# AWS Pricing Options
On-Demand Instances:

Pay only for the compute capacity you consume with no upfront payments or long-term commitments required.

# Savings Plans:

Save up to 72 percent across a variety of instance types and services by committing to a consistent usage level for 1 or 3 years.

# Reserved Instances:

Get a savings of up to 75 percent by committing to a 1-year or 3-year term for predictable workloads using specific instance families and AWS Regions.

# Dedicated Hosts:

Reserve an entire physical server for your exclusive use. This option offers full control and is ideal for workloads with strict security or licensing needs.

# Spot Instances:

Bid on spare compute capacity at up to 90 percent off the On-Demand price, with the flexibility to be interrupted when AWS reclaims the instance.

# Dedicated Instances:

Pay for instances running on hardware dedicated solely to your account. This option provides isolation from other AWS customers.

Dedicated Hosts provide exclusive use of physical servers, offering full control over instance placement and resource allocation. This makes them ideal for security- or compliance-driven workloads. 









# Scaling Amazon EC2
- Scalability
Scalability refers to the ability of a system to handle an increased load by adding resources. You can scale up by adding more power to existing machines, or you can scale out by adding more machines. Scalability focuses on long-term capacity planning to make sure that the system can grow and accommodate more users or workloads as needed.

- Elasticity
Elasticity is the ability to automatically scale resources up or down in response to real-time demand. A system can then rapidly adjust its resources, scaling out during periods of high demand and scaling in when the demand decreases. Elasticity provides cost efficiency and optimal resource usage at any given moment.


# Scale Out - Horizontal Scaling
Adding more resources to the pool so you can get more work done in parallel

# Scale Up - Veritical Scaling
Adding more power to the machine that are running
-> more power per instance

# coffe shop example

Too many customers come in

-> Increasing the size of an order taking instance will not take the toal orders any faster
-> having more order taking instances will speed up the order taking process

-> since we have too many orders coming in we need to increase the number of order making instances as well

# Why are there more order taking than order making instances? 
Amount of work getting done is more than the orders instances can send back of the house. there are no delays in the orders  so no reason to add more instances.

When there are less customers we cna turn off the instances we dont need

# EC2 Auto Scaling


Amazon EC2 Auto Scaling automatically adjusts the number of EC2 instances based on changes in application demand, providing better availability. It offers two approaches. Dynamic scaling adjusts in real time to fluctuations in demand. Predictive scaling preemptively schedules the right number of instances based on anticipated demand.

other aws services used to make this happen:
-> need data about the performance of instances, potentially data of latency and other applicaiton metrics
you can use cloud  watch ti get these metrics 
This data can be used to determine when scaling needs to happen .

An Auto Scaling group is configured with the following three key settings:
# Minimum Capacity
The minimum capacity defines the least number of EC2 instances required to keep the application running. This makes sure that the system never scales below this threshold. It's the number of EC2 instances that launch immediately after you have created the Auto Scaling group. 

# Desired capacity 
The desired capacity is the ideal number of instances needed to handle the current workload, which Auto Scaling aims to maintain. If you do not specify the desired number of EC2 instances in an Auto Scaling group, the desired capacity defaults to your minimum capacity.

# Maximum Capacity
The maximum capacity sets an upper limit on the number of instances that can be launched, preventing over-scaling and controlling costs. For example, you might configure the Auto Scaling group to scale out in response to increased demand.

In this example, a maximum of 12 EC2 instances can be launched. Amazon EC2 Auto Scaling will scale between the minimum and maximum number of instances.

# Directing Traffic with Elastic Load Balancing

Spreading workloads improves the performance of your applications by preventing any single resource from having to handle the full workload on its own. 

To balance traffic across a bunch of EC2 instances , we dont want idle instances we make use of a Load balancer
A load balancer takes in requests and routes them to instances

# Elastic Load Balancing

Elastic Load Balancing (ELB) automatically distributes incoming application traffic across multiple resources, such as EC2 instances, to optimize performance and reliability. A load balancer serves as the single point of contact for all incoming web traffic to an Auto Scaling group. As the number of EC2 instances fluctuates in response to traffic demands, incoming requests are first directed to the load balancer. From there, the traffic is distributed evenly across the available instances.

# Benefits of ELB
1. Efficient traffic distribution:

ELB evenly distributes traffic across EC2 instances, preventing overload on any single instance and optimizing resource utilization.

2. Automatic scaling:

ELB scales with traffic and automatically adjusts to changes in demand for a seamless operation as backend instances are added or removed.

3. Simplified management:

ELB decouples front-end and backend tiers and reduces manual synchronization. It also handles maintenance, updates, and failover to ease operational overhead.

# Routing methods
To optimize traffic distribution, ELB uses several routing methods: Round Robin, Least Connections, IP Hash, and Least Response Time. These routing strategies work together for efficient traffic management and optimal application performance.

Round Robin - Distributes traffic evenly across all available servers in a cyclic manner.
Least Connections - Routes traffic to the server with the fewest active connections, maintaining a balanced load.
IP Hash - Uses the client’s IP address to consistently route traffic to the same server.
Least Response Time - Directs traffic to the server with the fastest response time, minimizing latency.

Load balancing in AWS distributes incoming network traffic across multiple targets (like EC2 instances), while Auto Scaling dynamically adjusts the number of running instances based on demand and policies

# example

Low-demand period: At the beginning of the day, only a few patients are accessing the system to book appointments or view medical records. The existing web servers are sufficient to handle the low traffic. This matches the demand, with no need for additional resources at this point.

High-demand period: As the day progresses, especially during peak hours, such as early mornings or just before the weekend, more patients access the portal to book appointments, view test results, or contact medical professionals. To handle this surge in demand, the healthcare system automatically scales up the number of servers to help ensure that the system remains responsive and available for all users.

A load balancer directs the incoming traffic to different web servers based on their current load. For instance, if one server starts receiving too many requests, the load balancer will route new requests to a less busy server. This makes sure that no single server becomes overwhelmed. The traffic is evenly distributed across available EC2 instances.

# Messaging and Queuing

Example scenariio:
Cashier hands order to barista -> barista preapres coffee

When Barista is busy with other orders or on break , cashier will just take the order and find the barista or else just drop the order so that he can serve the next customer

This results in slow downs or missing orders

Instead of directly handing orders to a barista we place them in a order board (buffer) and then the barista can pick up the orders from there.

This is called messaging and queing 

If the cashier and barista communicate directly thats -> tightly coupled

If a single component fails or changes it causes issues for the other components or even the whole system

App A <=> App B

This is tightly coupled and this if app b fails , app a can also fail and vice versa

# Loosely Coupled
App A <=> Queue <=> App B 

Even if App B fails . App A can continue functioning normally and keep sending messages to the queue and remain there until they are processed by application B

# Amazon Simple Queue Serve (SQS) 

- send , store and recieve messages between separate components at any volume

Data within a message is called payload

SQS queses are where they are placed till they are processed
 scale automatically, relaible and simple to configure

 (Order Board)

# Amazon Simple Notification Service (SNS)

Similar as it send messages to services. SNS messages arent held for pickup until the processing service can get them
They need a response immeadittely

(Cashier shouting orders that are ready)

can be used to fan out notifications to end users 

# Monolithic applications
Applications consist of multiple components that work together to transmit data, fulfill requests, and keep the application running smoothly. In a traditional approach to application architecture, the components—such as database logic, web application servers, user interfaces, and business logic—are tightly coupled. This means that if one component fails, it can cause the failure of other components, potentially bringing down the entire application.

# Microservices architecture
To improve application availability and resilience, you can adopt a microservices architecture. In this approach, application components are loosely coupled, meaning that if one component fails, the others continue to function normally. The communication between components remains intact, and the failure of a single component does not impact the entire system. This design promotes greater flexibility and reliability in the application.

# EventBridge 
is a serverless service that helps connect different parts of an application using events, helping to build scalable, event-driven systems. With EventBridge, you route events from sources like custom apps, AWS services, and third-party software to other applications. EventBridge simplifies the process of receiving, filtering, transforming, and delivering events, so you can quickly build reliable applications.

# Example - Restaurant Scenario

1. Payment processing - The payment service must verify and process the customer's payment.
2. Restaurant notification- The restaurant receives a notification to start preparing the meal.
3. Inventory management - The inventory system checks if the ingredients for the order are available.
4. Delivery dispatch - A delivery driver is notified to pick up and deliver the meal.

EventBridge can route events, like order placed or payment completed, to the relevant services (payment, restaurant, inventory, and delivery). It can handle high volumes of events during peak times, making sure each service works independently. Even if one service fails, EventBridge will store the event and process it as soon as the service is available again. EventBridge helps provide a smooth and reliable operation across the entire system.

# Amazon SQS
A customer support team consists of a support agent and a technical specialist. The support agent is responsible for receiving customer issues, and the technical specialist works on resolving them. This process works well as long as both the agent and specialist are available and coordinated.

Customer submits an issue -> Support agent assigns ticket to specialist -> Specialist works on issue and informs support agent

However, what happens if the support agent creates a ticket but the technical specialist is busy working on another issue or unavailable? The agent would have to wait until the specialist is free to accept the new ticket, causing delays in resolving customer issues and extending wait times for customers. 

As the volume of customer issues increases, this process becomes inefficient.

Customer submits an issue -> Support agent assigns ticket to specialist -> Specialist works on issue and informs support agent (<X>)

To improve efficiency, they implement a queue system using Amazon SQS. 
The support agent adds customer issues to the queue, creating a backlog. Even if the specialist is busy, the agent can continue adding new issues. 
The specialist checks the queue, resolves issues, and updates the agent. This system provides a smooth workflow and helps handle higher volumes without delays or bottlenecks.


Customer submits an issue -> Support agent assigns ticket to specialist <-> ASQS <-> Specialist works on issue and informs support 

Amazon SNS is a publish-subscribe service that publishers use to send messages to subscribers through SNS topics. 

# Example: Amazon SNS

A company that sells a variety of products is currently sending a single email to all customers with updates on various topics, such as new products, special offers, and upcoming events. Although this method worked initially, customers want to receive only the updates they’re interested in. The current email update is causing customer dissatisfaction and lower engagement.

1. Segment the communication

The company decides to divide the communication into three separate topics, including one for new products, one for special offers, and one for events. Each topic will focus on a specific area of interest.

2. Let customers choose topics

Customers can subscribe to the topics they care about, such as the following:

A customer might subscribe only to new product updates.
Another customer might opt only for event notifications.
A third customer might choose to subscribe to new product updates and special offers.

3. Send tailored notifications

With Amazon SNS, the company can send personalized notifications to subscribers based on their specific interests. Amazon SNS makes sure that these notifications are promptly delivered to the right audience, improving the efficiency and relevance of the communication.

# Introduction to Serverless Computing

# Key takeaways: Unmanaged and managed services
AWS offers both unmanaged and managed services to suit different levels of control and responsibility. By understanding this model, you will know which tasks AWS manages and which you are responsible for, helping you secure and manage your cloud resources effectively.

# Unmanaged and managed services
With unmanaged compute services like Amazon EC2, AWS takes care of the underlying physical infrastructure, but you're responsible for setting up, securing, and maintaining the operating system, network configurations, and applications on your instances. Managed services, on the other hand, reduce the amount of infrastructure you need to manage. While AWS handles much of the operational overhead, you might still need to perform some provisioning or configuration depending on the service.

# When to use what?
With unmanaged services like Amazon EC2, you set up and manage everything: the operating system, security updates, and network settings. AWS only takes care of the physical hardware. 

Managed services handle most of the infrastructure for you, but you still need to set up things like deployment options, scaling, and environment settings. 

With fully managed services like AWS Lambda, you don’t manage any servers at all. You upload your code, and AWS takes care of the rest, including infrastructure, scaling, and availability.

# AWS Lambda

Lambda is a serverless compute service that runs code in response to events without the need to provision or manage servers. It automatically manages the underlying infrastructure, scaling resources based on the volume of requests. You are charged only for the compute time consumed, down to the millisecond. Lambda handles execution, scaling, and resource allocation. You can optimize performance by configuring the appropriate memory size for your function.

# How Lambda works

1. Upload code to Lambda

First, upload the code to Lambda, which uploads as a Lambda function.

2. Set code to trigger from an event source

Next, configure your code to be triggered by events, like AWS services, mobile apps, or HTTP requests.

3. Run code when triggered

Your code runs only when an event occurs, like a file upload or user action. Lambda automatically handles all the server management, scaling, and infrastructure. The Lambda runtime executes your function code using the event data passed to it. This way, your code runs reliably, securely, and efficiently—without you managing the servers or environment it runs in.

4. Pay only for the compute time used

You are charged only for the compute time consumed, down to the millisecond. The price depends on the amount of memory that you allocate to your function.

# Lambda use cases

1. Real-time image processing for a social media application
A social media company uses Lambda to process images uploaded by users. When a photo is uploaded, Lambda is triggered to resize the image, apply filters, and save it in an optimized format to storage. This event-driven, serverless approach makes sure that the application can handle high volumes of uploads without needing to manage infrastructure.

# Why Lambda: It automatically scales based on uploads and charges only for the time spent processing each image.

2. Personalized content delivery for a news aggregator

A news aggregator uses Lambda to fetch and process news articles from multiple sources, then it tailors recommendations based on user preferences. When a user opens the application or performs a search, Lambda functions are triggered to retrieve data, run personalization logic, and return relevant content.

# Why Lambda: It automatically scales with user traffic and reduces costs by running code only when users interact.

3. Real-time event handling for an online game
A gaming company uses Lambda to handle in-game events like player actions, game state changes, and real-time leader board updates. Each event (like scoring a point or unlocking an achievement) triggers a Lambda function that updates player data and game status.


# Why Lambda: It handles thousands of events, in real-time, with no need to manage servers. Costs scale with usage, which is ideal for peak gaming times.


# Example


User -> upload -> ASQS -> Process(Lambda) ->CloudWatch Logs

# Containers and Orchestration on AWS

