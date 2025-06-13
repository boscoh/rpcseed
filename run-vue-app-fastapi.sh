# install ttab using `npm i -g ttab`
# on mac, need to change
#   System Prefs -> Security -> Privacy -> Accessibility: add Terminal
ttab "./run-fastapi.sh"
ttab "cd vue-vite-client; npm run client-dev"
sleep 0.5
open http://localhost:5200
