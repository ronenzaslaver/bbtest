#!/bin/sh
echo '#!/bin/sh' > ./bbtest.installer.example.sh 
echo "curl --data 'Hello Sara!' $1" >> ./bbtest.installer.example.sh 
chmod +x ./bbtest.installer.example.sh
