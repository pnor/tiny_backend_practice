#!/usr/bin/env sh

CMD="$1"
server_url="http://127.0.0.1:8000"
shift

case "$CMD" in
    "customers")
        echo "getting customers"
        curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET "$server_url/customers"
        ;;
    "goods")
        echo "getting goods"
        curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET "$server_url/goods"
        ;;
esac
