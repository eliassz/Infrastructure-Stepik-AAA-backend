#!/bin/bash

commands=(
    # get_one_plate
    "curl 'http://localhost:8080/get_one_plate?im_id=10022'"
    "curl 'http://localhost:8080/get_one_plate?im_id=baz'"
    "curl 'http://localhost:8080/get_one_plate?im_id=10021'"
    "curl 'http://localhost:8080/get_one_plate?im_id=-10022'"
    "curl 'http://localhost:8080/get_one_plate?im_ids=10022'"
    "curl 'http://localhost:8080/get_one_plate?im_id=1002'"
    # get_multiple_plates
    "curl 'http://localhost:8080/get_multiple_plates?im_id=10022,9965'"
    "curl 'http://localhost:8080/get_multiple_plates?im_id=10022,10021'"
    "curl 'http://localhost:8080/get_multiple_plates?im_id=10021,10022'"
    "curl 'http://localhost:8080/get_multiple_plates?im_id=baz,10022'"
    "curl 'http://localhost:8080/get_multiple_plates?im_id=-10022,10022'"
    "curl 'http://localhost:8080/get_multiple_plates?im_id=str,10022'"
    "curl 'http://localhost:8080/get_multiple_plates?im_ids=str,10022'"
)

printf "%s\n" "${commands[@]}" | xargs -P 10 -I {} sh -c "{}"