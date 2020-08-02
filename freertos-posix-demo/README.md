1. Create a new Amazon Linux Cloud9 environment - t3.small (2 GiB RAM + 2 vCPU)

2. Open a new terminal in Cloud9 and install 'scons' and pcap development libraries

sudo pip install scons
sudo yum install libpcap-devel

3. Clone the FreeRTOS repository

git clone --recursive https://github.com/FreeRTOS/FreeRTOS

4. Compile and run the project

cd ~/environment/FreeRTOS/FreeRTOS/Demo/Posix_GCC/ && scons && sudo ./build/posix_demo 

5. (Optional) Switch to the "Blinky" demo by changing the flag 'mainCREATE_SIMPLE_BLINKY_DEMO_ONLY' to 1 and 'mainCREATE_TCP_ECHO_TASKS_SINGLE' to 0