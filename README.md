# PYthon MAil Sender 

## Description 

Pymas is a command line utility to send mails with attachments simply. 

The idea behind it comes from the fact that in my job I spend a lot of time debugging bits of code that people send me or doing simple examples and I got tired of having to go through my mail client and navigate through the file system via the interface to send an attachment that I had on hand in my terminal. 

## Installation

Clone this repository and run the command : 

```bash 
pip install . 
```

## Usage 

### Configure your email 

Before starting to use pymas you need to configure your mail server information. 

The information to provide is the following: 

- Address of the smtp server 
- Server port 
- Your login 
- Your email address 

The password is not to be filled in at the configuration, it will be asked to you at each mail sending.

For example : 

```bash 
pymas configure --smtp_server "smtp.fake.fr" --smtp_port 587 --smtp_login "your_login"  
```

### Send mail 

To send an email you need to fill in the following information: 

- Recipients
- The subject 
- Body of the text
- Optional attachments 

If the path provided for the attachment is a file a zip archive is automatically made and it is this one that is sent by email. 

Par exemple : 

```bash 
pymas send --recipients "jean.dupond@fake.fr" --subject "Fake message" --text "Hello Jean" --attachement data.csv 
```

