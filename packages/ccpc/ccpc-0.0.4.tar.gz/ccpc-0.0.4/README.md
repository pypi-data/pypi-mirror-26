![CCPC logo](resources/images/ccpc_logo.jpg)

***

# CCPC
Chaotic Cable Pulling Chimp

## Installation

`pip install ccpc`

## Example usage

`ccpc --no-verify-ssl -b <url_with_scheme_and_port> -p <project> -t  <token>`

## Create a service account
`oc create serviceaccount <account>`

## Get service account's token
`oc serviceaccounts get-token <account>`

## Give read/write access to a service account to a project
`oc policy add-role-to-user view system:serviceaccount:<project>:<account>`

`oc policy add-role-to-user edit system:serviceaccount:<project>:<account>`

## Build docker image
```sh
git clone https://github.com/panagiks/CCPC
cd CCPC/image
docker build --build-arg VERIFY_SSL=false --build-arg PROJECT=<project> --build-arg BASE_URL=<url_with_scheme_and_port> --build-arg TOKEN=<token> .
```

## Todo

- [ ] Replace prints with standard logging
- [ ] Add some handling if OC responds with error (if it's actually needed)
