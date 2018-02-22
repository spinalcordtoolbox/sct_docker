# run SCT on windows
An SCT  with ssh Dockerfile  
To build the container: 
docker build --tag neuropoly/sct .

To run the sct:
docker run -p 2222:22 --rm -it --name sct_ssh  neuropoly/sct 

Then ssh to the contaner with X tunelling enable  option and the port to 2222 on the local host , you should then be 
able to access all sct features on a windows machine. The username and password are respectively `sct` ... and  `sct`!
