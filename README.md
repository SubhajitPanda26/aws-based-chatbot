# Facebook Integrated Chatbot Using AWS Lex With Lambda Validation

Welcome to the Facebook Integrated Chatbot Using AWS Lex With Lambda Validation project! 🚀

In this project, we will guide you through setting up a highly available and reliable chatbot on Facebook Messenger using Amazon Web Services (AWS). Below, you will find detailed instructions for each part of the project.

## **Project Members**
  - [Avidhan Purkait](https://github.com/AvidhanPurkait)
  - [Subhajit Panda](https://github.com/SubhajitPanda26)

## Table of Contents

 - [System Architecture](#System-Architecture)

 - [Introduction](#Introduction)

 - [Lambda Function Creation](#Lambda-Function-Creation)

 - [Amazon Lex Bot Creation](#Amazon-Lex-Bot-Creation)

 - [Facebook Integration](#Facebook-Integration)

 - [Snapshots](#Snapshots)

## System Architecture

![Alt text](Screenshots/Architecture.jpg)

## Introduction

A chatbot is defined as a conversational application that aids in customer service, engagement, and support by replacing or augmenting human support agents with artificial intelligence (AI) and other automation technologies that can communicate with end-users via chat.

This project aims to deploy a Chatbot on Facebook Messenger using AWS from scratch, leveraging various AWS services, and ensuring high availability, security, and scalability.

## Lambda Function Creation

AWS Lambda is a compute service that lets you run code without provisioning or managing servers. With Lambda, you can run code for virtually any type of application or backend service.

### Steps:

⏩ Open Amazon Lambda Console and create a function by selecting Author from Scratch option and Python 3.9 in Runtime and providing Function Name.

![Alt text](Screenshots/LAMBDA/1.jpg)

⏩ Enter the code in the Function Code Section.

![Alt text](Screenshots/LAMBDA/2.jpg)

⏩ Configure the Test Event by providing Event Name and JSON Event.

![Alt text](Screenshots/LAMBDA/3.1.jpg)
![Alt text](Screenshots/LAMBDA/3.2.jpg)

⏩ Test the Code Hook and check the output in the Execution Result tab to verify that the function ran successfully.

![Alt text](Screenshots/LAMBDA/4.jpg)

## Amazon Lex Bot Creation

### Steps:

⏩ Open Amazon Lex console and click on create.

![Alt text](Screenshots/LEX/1.jpg)

⏩ Create a custom bot by providing Bot Name, Output Voice, Session Timeout and selecting COPPA as No.

![Alt text](Screenshots/LEX/2.jpg)

⏩ Create an Intent for the bot.

![Alt text](Screenshots/LEX/3.jpg)

⏩ Create the custom Slot Types and add them to the Intent.

![Alt text](Screenshots/LEX/4.jpg)

⏩ Provide the Sample Utterances.

![Alt text](Screenshots/LEX/5.jpg)

⏩ Customize the Slots.

![Alt text](Screenshots/LEX/6.jpg)

⏩ Edit the Slots by setting Buttons on Prompt Response Card.

![Alt text](Screenshots/LEX/7.jpg)
![Alt text](Screenshots/LEX/8.jpg)
![Alt text](Screenshots/LEX/9.jpg)

⏩ Configure the Confirmation Prompt.

![Alt text](Screenshots/LEX/10.jpg)

⏩ Add the Lambda function as an Initialization and Validation Code Hook.

![Alt text](Screenshots/LEX/11.jpg)

⏩ Add the Lambda function as the Fulfilment Code Hook.

![Alt text](Screenshots/LEX/12.jpg)

⏩ Build and Test the Bot.

![Alt text](Screenshots/LEX/13.jpg)

⏩ Publish the latest version of the bot by creating an alias that points to the latest version.

![Alt text](Screenshots/LEX/14.jpg)

⏩ Open Facebook under Channels and enter Channel Name, Description, KMS Key, Alias, Verify Token and provide Page Access Token and App Secret Key obtained from Facebook.

![Alt text](Screenshots/LEX/15.jpg)

⏩ Activate the Channel and copy the Callback URL.

![Alt text](Screenshots/LEX/16.jpg)

## Facebook Integration

### Steps:

⏩ Log in to the Meta (formerly Facebook) developer portal.

![Alt text](Screenshots/META/1.jpg)

⏩ Create an App by selecting Business as App Type and provide App Name and Email.

![Alt text](Screenshots/META/2.jpg)
![Alt text](Screenshots/META/3.jpg)

⏩ Choose the Messenger product and choose Setup webhooks in the Webhooks section of the page.

![Alt text](Screenshots/META/4.jpg)

⏩ Open Basic Settings and copy App Secret Key and paste it in the Lex Channel.

![Alt text](Screenshots/META/5.jpg)

⏩ Add the Facebook Page to generate Access Token.

![Alt text](Screenshots/META/6.jpg)

⏩ Generate Page Access Token.

![Alt text](Screenshots/META/7.jpg)

⏩ Enter the Callback URL and Verify Token provided in the Amazon Lex console earlier.

![Alt text](Screenshots/META/8.jpg)

⏩ Choose Subscription Fields (messages, messaging_postbacks, and messaging_optins) and save.

![Alt text](Screenshots/META/9.jpg)

## Snapshots

![Alt text](Screenshots/Messenger/1.jpg)
![Alt text](Screenshots/Messenger/2.jpg)
![Alt text](Screenshots/Messenger/3.jpg)
![Alt text](Screenshots/Messenger/4.jpg)
