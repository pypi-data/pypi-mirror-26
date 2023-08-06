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
