# PYthon MAil Sender 

## Description 



## Usage 

### Configure your email 

```bash 
pymas configure --smtp_server "smtp.fake.fr" --smtp_port 587 --smtp_login "your_login"  
```

### Send mail 
```bash 
pymas send --recipients "jean.dupond@fake.fr" --subject "Fake message" --text "Hello Jean" --attachement data.csv 
```

