Log Parser utility tool
======================

It displays the below details for every log file 

- A count of unique IP addresses
- A map of IP address to number of requests (how many requests did each IP make?)
- The distribution of HTTP status codes returned
- The top 5 referrers for GET requests

Dynamic updates of the log file is taken care. However you need to refresh the browser when you update the log file on your system to reflect new values.



Installation and Usage:
----------------------
 
Place the log file you want to parse in the /tmp/log folder and run the below docker command.

docker run -ti -p 8080:8080 -v /tmp/log:/mnt/ saggi432/logparser:latest

Open the browser on the url http://localhost:8080/stats



