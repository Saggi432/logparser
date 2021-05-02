Log Parser utility tool
======================

It displays the below details for every log file 

- A count of unique IP addresses
- A map of IP address to number of requests (how many requests did each IP make?)
- The distribution of HTTP status codes returned
- The top 5 referrers for GET requests



Installation and Usage:
----------------------
 
Place the log file you want to parse in the /tmp/log folder and run the below docker command.

docker run -ti -p 8080:8080 -v /tmp/log:/mnt/ sample

Open the browser on the url http://localhost:8080/stats



