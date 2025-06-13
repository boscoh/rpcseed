# install ttab using `npm i -g ttab`
# on mac, need to change
#   System Prefs -> Security -> Privacy -> Accessibility: add Terminal
ttab "cd py-fastapi; ./run.sh"
ttab "cd vue-app-client; npm install; npm run client-dev"
./open-url.sh "http://localhost:5200" &
